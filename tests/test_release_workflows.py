"""Release-side workflows: which jobs and steps run for which event.

* publish-pypi.yml: a GitHub Release fires `release: published` whatever its
  tag, so a release of a collection tag (`<slug>-vN`, e.g.
  `metabolomics-v0.2.0`) used to build and publish the Python package to PyPI.
  The build and publish jobs now run only on a manual dispatch or on a release
  whose tag starts with `v` and contains no `-v`.
* release.yml: a collection tag made a production Zenodo draft whenever the
  ZENODO_TOKEN secret was set, which collides with the draft of
  scripts/zenodo_deposit.py (Zenodo keeps one unpublished version per record).
  The upload step now runs only when the repository variable ZENODO_UPLOAD is
  `true`.
* pages.yml: deployed only on a push to main touching the site paths, so
  enabling Pages deployed nothing until such a push. It can now be dispatched.

The `if:` conditions are evaluated by `evaluate`, a small reader of the GitHub
Actions expression syntax these workflows use: string literals, context paths,
`==`, `!=`, `!`, `&&`, `||`, parentheses, and the functions `startsWith`,
`contains`, `success` and `always`. String comparison and both string
functions ignore case, as on GitHub, and a missing value reads as null, which
equals the empty string.
"""
import pathlib
import re

import pytest

yaml = pytest.importorskip("yaml")

ROOT = pathlib.Path(__file__).parent.parent
WORKFLOWS = ROOT / ".github" / "workflows"

_TOKEN = re.compile(
    r"\s*(?:(?P<string>'(?:[^']|'')*')"
    r"|(?P<op>==|!=|&&|\|\||!|\(|\)|,)"
    r"|(?P<word>[A-Za-z_][A-Za-z0-9_.]*))"
)


def _tokens(text: str) -> list[tuple[str, str]]:
    found, position = [], 0
    text = text.strip()
    while position < len(text):
        match = _TOKEN.match(text, position)
        if not match or match.end() == position:
            raise ValueError(f"cannot read expression at {text[position:]!r}")
        kind = match.lastgroup
        found.append((kind, match.group(kind)))
        position = match.end()
    return found


def _text(value) -> str:
    return "" if value is None else str(value)


def _lookup(context: dict, path: str):
    value = context
    for part in path.split("."):
        if not isinstance(value, dict):
            return None
        value = value.get(part)
    return value


def _equal(left, right) -> bool:
    if isinstance(left, bool) or isinstance(right, bool):
        return bool(left) == bool(right)
    return _text(left).casefold() == _text(right).casefold()


FUNCTIONS = {
    "startsWith": lambda s, p: _text(s).casefold().startswith(_text(p).casefold()),
    "contains": lambda s, p: _text(p).casefold() in _text(s).casefold(),
    "success": lambda: True,
    "always": lambda: True,
}


class _Reader:
    """Recursive descent over the token list: || < && < comparison < ! < primary."""

    def __init__(self, text: str, context: dict):
        self.tokens = _tokens(text)
        self.at = 0
        self.context = context

    def peek(self):
        return self.tokens[self.at] if self.at < len(self.tokens) else (None, None)

    def take(self, value=None):
        token = self.peek()
        if value is not None and token[1] != value:
            raise ValueError(f"expected {value!r}, found {token[1]!r}")
        self.at += 1
        return token

    def read(self):
        value = self.either()
        if self.at != len(self.tokens):
            raise ValueError(f"unread tokens: {self.tokens[self.at:]}")
        return value

    def either(self):
        value = self.both()
        while self.peek()[1] == "||":
            self.take()
            right = self.both()
            value = value or right
        return value

    def both(self):
        value = self.compare()
        while self.peek()[1] == "&&":
            self.take()
            right = self.compare()
            value = value and right
        return value

    def compare(self):
        value = self.unary()
        if self.peek()[1] in ("==", "!="):
            op = self.take()[1]
            right = self.unary()
            same = _equal(value, right)
            return same if op == "==" else not same
        return value

    def unary(self):
        if self.peek()[1] == "!":
            self.take()
            return not self.unary()
        return self.primary()

    def primary(self):
        kind, value = self.take()
        if value == "(":
            inner = self.either()
            self.take(")")
            return inner
        if kind == "string":
            return value[1:-1].replace("''", "'")
        if kind != "word":
            raise ValueError(f"unexpected token {value!r}")
        if value in ("true", "false"):
            return value == "true"
        if value == "null":
            return None
        if self.peek()[1] == "(":
            self.take("(")
            args = []
            while self.peek()[1] != ")":
                args.append(self.either())
                if self.peek()[1] == ",":
                    self.take(",")
            self.take(")")
            return FUNCTIONS[value](*args)
        return _lookup(self.context, value)


def evaluate(condition, context: dict) -> bool:
    """Evaluate an `if:` condition; an absent condition means success()."""
    if condition is None:
        return True
    text = str(condition).strip()
    if text.startswith("${{") and text.endswith("}}"):
        text = text[3:-2]
    return bool(_Reader(text, context).read())


def _workflow(name: str) -> dict:
    return yaml.safe_load((WORKFLOWS / name).read_text())


def jobs_that_run(name: str, context: dict) -> set[str]:
    """Jobs of the workflow that run for this context: needs all ran and the if holds."""
    jobs = _workflow(name)["jobs"]
    ran: dict[str, bool] = {}

    def runs(job_id: str) -> bool:
        if job_id not in ran:
            job = jobs[job_id]
            needs = job.get("needs") or []
            needs = [needs] if isinstance(needs, str) else needs
            ran[job_id] = all(runs(n) for n in needs) and evaluate(job.get("if"), context)
        return ran[job_id]

    return {job_id for job_id in jobs if runs(job_id)}


class _AnyOutput(dict):
    """Outputs of a step that ran: every output reads as set."""

    def get(self, key, default=None):
        return "set"


def steps_that_run(name: str, job_id: str, context: dict) -> list[dict]:
    """Steps of one job that run for this context, in order; a step that ran sets its outputs."""
    context = {**context, "steps": {}}
    ran = []
    for step in _workflow(name)["jobs"][job_id]["steps"]:
        if evaluate(step.get("if"), context):
            ran.append(step)
            if step.get("id"):
                context["steps"][step["id"]] = {"outputs": _AnyOutput()}
        elif step.get("id"):
            context["steps"][step["id"]] = {"outputs": {}}
    return ran


def tag_push(tag: str, variables: dict | None = None) -> dict:
    return {"github": {"event_name": "push", "ref_name": tag, "ref": f"refs/tags/{tag}"},
            "vars": variables or {}, "inputs": {}}


def release_event(tag: str) -> dict:
    return {"github": {"event_name": "release", "ref_name": tag,
                       "event": {"release": {"tag_name": tag}}}}


def dispatch_event(target: str) -> dict:
    return {"github": {"event_name": "workflow_dispatch", "ref_name": "main", "event": {}},
            "inputs": {"target": target}}


# --- the evaluator itself ------------------------------------------------------


@pytest.mark.parametrize("expression, expected", [
    ("'a' == 'A'", True),
    ("!contains('metabolomics-v0.2.0', '-v')", False),
    ("startsWith('v0.2.0', 'v') && !contains('v0.2.0', '-v')", True),
    ("false || (true && !false)", True),
    ("vars.UNSET == 'true'", False),
    ("steps.zenodo.outputs.doi != ''", False),
    ("${{ github.event_name == 'release' }}", True),
])
def test_evaluator_reads_the_expressions_the_workflows_use(expression, expected):
    assert evaluate(expression, {"github": {"event_name": "release"}}) is expected


# --- GAP-009: publish-pypi.yml runs for package tags only ----------------------


@pytest.mark.parametrize("tag", [
    "metabolomics-v0.2.0", "metabolomics-v0.1.0", "metabolomics-v3", "proteomics-v1",
    "vision-v1", "v0.2.0-v2",
])
def test_a_collection_release_skips_build_and_every_publish_job(tag):
    assert jobs_that_run("publish-pypi.yml", release_event(tag)) == set()


@pytest.mark.parametrize("tag", ["v0.2.0", "v1.0.0rc1", "v0.3.0-rc.1"])
def test_a_package_release_builds_and_publishes_to_pypi(tag):
    assert jobs_that_run("publish-pypi.yml", release_event(tag)) == {"build", "publish-pypi"}


@pytest.mark.parametrize("target, publish_job", [
    ("testpypi", "publish-testpypi"), ("pypi", "publish-pypi"),
])
def test_a_manual_dispatch_still_builds_and_publishes_to_its_target(target, publish_job):
    assert jobs_that_run("publish-pypi.yml", dispatch_event(target)) == {"build", publish_job}


def test_each_publish_job_states_the_package_tag_guard_itself():
    jobs = _workflow("publish-pypi.yml")["jobs"]
    for job_id in ("build", "publish-pypi"):
        condition = jobs[job_id]["if"]
        assert "startsWith(github.event.release.tag_name, 'v')" in condition, job_id
        assert "!contains(github.event.release.tag_name, '-v')" in condition, job_id


def test_releasing_pypi_doc_names_the_tag_guard():
    text = (ROOT / "docs" / "RELEASING_PYPI.md").read_text()
    assert "contains no `-v`" in text
    assert "metabolomics-v0.2.0" in text


# --- GAP-057: release.yml makes no Zenodo draft unless ZENODO_UPLOAD is true --


def _names(steps: list[dict]) -> list[str]:
    return [step.get("name", "") for step in steps]


@pytest.mark.parametrize("variables", [{}, {"ZENODO_UPLOAD": ""}, {"ZENODO_UPLOAD": "false"},
                                       {"ZENODO_UPLOAD": "1"}, {"ZENODO_PUBLISH": "true"}])
def test_a_collection_tag_run_makes_no_zenodo_call_unless_zenodo_upload_is_true(variables):
    ran = steps_that_run("release.yml", "release", tag_push("metabolomics-v0.2.0", variables))
    assert any("Release gate" in name for name in _names(ran))
    for step in ran:
        text = yaml.safe_dump(step)
        assert "zenodo.org" not in text, step.get("name")
        assert "ZENODO_TOKEN" not in text, step.get("name")
    assert not any("CITATION.cff" in name for name in _names(ran))


def test_zenodo_upload_true_turns_the_upload_step_on():
    ran = steps_that_run("release.yml", "release",
                         tag_push("metabolomics-v0.2.0", {"ZENODO_UPLOAD": "true"}))
    assert "zenodo" in [step.get("id") for step in ran]


def test_the_zenodo_step_condition_names_the_variable():
    steps = _workflow("release.yml")["jobs"]["release"]["steps"]
    (zenodo,) = [step for step in steps if step.get("id") == "zenodo"]
    assert zenodo["if"] == "vars.ZENODO_UPLOAD == 'true'"


def test_release_deposit_doc_states_the_order_and_the_variable():
    text = (ROOT / "docs" / "RELEASE_DEPOSIT.md").read_text()
    assert "## Order of a release" in text
    assert "`ZENODO_UPLOAD`" in text
    assert "published by hand" in text


# --- GAP-078: pages.yml can be dispatched --------------------------------------


def _triggers(name: str) -> dict:
    workflow = _workflow(name)
    # YAML 1.1 reads the bare key `on` as the boolean true.
    return workflow.get("on", workflow.get(True)) or {}


def test_pages_can_be_dispatched_and_still_deploys_on_site_pushes():
    triggers = _triggers("pages.yml")
    assert "workflow_dispatch" in triggers
    assert "docs-site/**" in triggers["push"]["paths"]
