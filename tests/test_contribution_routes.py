"""The four contribution routes are named in the same words wherever a skill is met.

1. this skill is wrong or could be better;
2. a skill is missing: request it, or propose yours;
3. a paper is not referenced: propose it;
4. something technical failed: report it.

Each lands on the issue tracker of the public registry with the collection and
the skill filled in. One vocabulary of kinds and labels runs through the issue
templates, scripts/skill_feedback.py, scripts/make_improvement_report.py, the
site and the report helper a collection can ship in `bin/`. Routers released
before the contribution section existed stay valid; a section that is present
must be current.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

from scripts import intake_issue, router_shape
from scripts import make_improvement_report as mir
from scripts import skill_feedback as sf

REPO = Path(__file__).resolve().parent.parent
TEMPLATES = REPO / ".github" / "ISSUE_TEMPLATE"
SITE = REPO / "docs-site"
FIXTURE = REPO / "tests" / "fixtures" / "router_collection"
NODE = shutil.which("node")

# The labels that exist on the public registry (2026-11-11). A template label
# outside this set is dropped by GitHub without a word.
REPOSITORY_LABELS = {
    "auto-report", "blocked", "bug", "dependencies", "documentation", "duplicate",
    "enhancement", "good first issue", "help wanted", "improvement", "invalid",
    "needs-triage", "paper-intake", "propose", "question", "review-requested",
    "triaged", "usage-feedback", "wontfix",
}
ROUTE_WORDS = list(sf.ROUTES.values())


def _front(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8").split("---\n", 2)[1])


def _js_array(text: str, name: str) -> list[str]:
    match = re.search(rf"const {name} = \[([^\]]*)\]", text)
    assert match, name
    return re.findall(r'"([^"]+)"', match.group(1))


# --------------------------------------------------------------------------- #
# One vocabulary                                                               #
# --------------------------------------------------------------------------- #
def test_kinds_cover_both_earlier_lists_and_faults_are_a_route():
    assert set(sf.KINDS) == {"defect", "drift", "enhancement", "efficiency", "gap", "composition"}
    for old in ("correction", "enhancement", "new-skill", "bug", "tool-update", "other"):
        assert sf.normalise_kind(old) in sf.KINDS
    assert set(sf.ROUTE_KINDS["skill"]) | set(sf.ROUTE_KINDS["missing"]) == set(sf.KINDS)
    assert "fault" in sf.ROUTES and "fault" not in sf.KINDS


def test_labels_are_canonical():
    assert sf.labels_for("defect") == ["usage-feedback", "needs-triage"]
    assert sf.labels_for("gap", drafted=True) == ["usage-feedback", "needs-triage", "propose", "auto-report"]
    assert "propose" in sf.labels_for("composition")
    assert sf.route_labels("fault") == ["bug", "needs-triage", "auto-report"]
    assert sf.route_labels("paper", drafted=False) == ["propose", "paper-intake", "needs-triage"]
    for route in sf.ROUTES:
        assert set(sf.route_labels(route)) <= REPOSITORY_LABELS


def test_improvement_report_uses_the_same_kinds_and_labels():
    assert mir.KINDS == list(sf.KINDS)
    payload = mir.report_payload("some-skill", "new-skill", "body")
    assert payload["title"] == "gap: some-skill"
    assert payload["labels"] == sf.labels_for("gap", drafted=True)
    assert payload["template"] == sf.ROUTE_TEMPLATES["missing"]
    url = mir.issue_url(sf.REGISTRY, "some-skill", "correction", "body")
    assert "labels=usage-feedback%2Cneeds-triage%2Cauto-report" in url
    assert "improvement" not in url


def test_site_form_uses_the_same_kinds_and_labels():
    script = (SITE / "contribute.js").read_text(encoding="utf-8")
    page = (SITE / "contribute.html").read_text(encoding="utf-8")
    assert _js_array(script, "KINDS") == list(sf.KINDS)
    assert _js_array(script, "PROPOSE_KINDS") == sorted(sf.PROPOSE_KINDS, key=list(sf.KINDS).index)
    assert _js_array(script, "BASE_LABELS") == sf.labels_for("defect")
    assert '"auto-report"' in script and "improvement," not in script
    legacy = dict(re.findall(r'"?([\w-]+)"?: "([\w-]+)"', re.search(r"LEGACY_KINDS = \{([^}]*)\}", script).group(1)))
    assert legacy == sf.LEGACY_KINDS
    options = re.findall(r'<option value="([^"]+)">', page.split('id="kind"')[1].split("</select>")[0])
    assert options == list(sf.KINDS)
    for template in sf.ROUTE_TEMPLATES.values():
        if template != sf.ROUTE_TEMPLATES["paper"]:
            assert template in page or template in script


def test_paper_page_flag_is_a_route_one_report():
    script = (SITE / "paper.js").read_text(encoding="utf-8")
    flag = script.split('"btn-flag"')[1]
    labels = re.search(r"labels: \[([^\]]*)\]", flag).group(1)
    assert re.findall(r'"([^"]+)"', labels) == sf.labels_for("defect", drafted=True)
    assert sf.ROUTES["skill"] in flag and sf.ROUTE_TEMPLATES["skill"] in flag


def test_feedback_template_lists_the_route_kinds():
    text = (TEMPLATES / sf.ROUTE_TEMPLATES["skill"]).read_text(encoding="utf-8")
    for kind in sf.ROUTE_KINDS["skill"]:
        assert f"- `{kind}`: {sf.KINDS[kind]}" in text
    for kind in sf.ROUTE_KINDS["missing"]:
        assert f"`{kind}`:" not in text
    assert _front(TEMPLATES / sf.ROUTE_TEMPLATES["skill"])["labels"] == sf.labels_for("defect")
    assert set(_front(TEMPLATES / sf.ROUTE_TEMPLATES["missing"])["labels"]) == set(sf.labels_for("gap"))


# --------------------------------------------------------------------------- #
# Issue chooser                                                                #
# --------------------------------------------------------------------------- #
def test_the_four_routes_come_first_in_the_chooser():
    files = sorted(path.name for path in TEMPLATES.glob("*.md"))
    assert files[:4] == list(sf.ROUTE_TEMPLATES.values())
    for route, name in sf.ROUTE_TEMPLATES.items():
        text = (TEMPLATES / name).read_text(encoding="utf-8")
        assert sf.ROUTES[route] in text, name
        assert set(_front(TEMPLATES / name)["labels"]) == set(sf.route_labels(route, drafted=False)), name


def test_new_route_templates_use_existing_labels_only():
    for route in ("missing", "fault"):
        assert set(_front(TEMPLATES / sf.ROUTE_TEMPLATES[route])["labels"]) <= REPOSITORY_LABELS


def test_fault_template_names_every_component():
    text = (TEMPLATES / sf.ROUTE_TEMPLATES["fault"]).read_text(encoding="utf-8")
    for component, meaning in sf.FAULT_COMPONENTS.items():
        assert f"- `{component}`: {meaning}" in text


def test_chooser_config_keeps_blank_issues_and_links_the_site():
    config = yaml.safe_load((TEMPLATES / "config.yml").read_text(encoding="utf-8"))
    assert config["blank_issues_enabled"] is True
    urls = [link["url"] for link in config["contact_links"]]
    assert "https://holobiomicslab.github.io/asb-skill-collections/contribute.html" in urls
    assert "https://holobiomicslab.github.io/asb-skill-collections/propose.html" in urls
    assert any(url.endswith("/SECURITY.md") for url in urls)
    for link in config["contact_links"]:
        assert set(link) == {"name", "url", "about"}


# --------------------------------------------------------------------------- #
# Route 3: the site form and the helper write what the intake parser reads     #
# --------------------------------------------------------------------------- #
FIELDS = {"what": "Spec2Vec, spectral similarity scoring", "link": "10.1371/journal.pcbi.1008724",
          "type": "paper", "collection": "metabolomics",
          "why": "Learns spectral similarity from fragment co-occurrence.",
          "version": "next", "open_access": "yes", "you": "@someone", "coi": "none disclosed"}


@pytest.mark.skipif(NODE is None, reason="node is not installed")
def test_site_paper_body_is_read_by_the_intake_parser():
    script = (
        "const m = require(process.argv[1]);"
        "process.stdout.write(JSON.stringify(m.buildProposalBody(JSON.parse(process.argv[2]))));"
    )
    result = subprocess.run([NODE, "-e", script, str(SITE / "propose.js"), json.dumps(FIELDS)],
                            capture_output=True, text=True, timeout=60, check=True)
    body = json.loads(result.stdout)
    fields = intake_issue.validate_issue(
        {"number": 7, "body": body, "author": {"login": "someone"}}, "metabolomics", "paper")
    assert fields["What is it?"] == FIELDS["what"]
    assert fields["Link:"] == FIELDS["link"]
    assert fields["Type:"] == "paper"
    assert fields["Target collection:"] == "metabolomics"
    assert fields["Why it matters (one or two sentences):"] == FIELDS["why"]
    assert fields["Conflict of interest?"] == "none disclosed"
    assert body == sf.paper_body(FIELDS)


def test_helper_paper_report_is_read_by_the_intake_parser():
    report = sf.render_paper(FIELDS["what"], FIELDS["link"], "paper", "metabolomics/v3", FIELDS["why"])
    fields = intake_issue.validate_issue(
        {"number": 8, "body": report["body"], "author": {"login": "someone"}}, "metabolomics", "paper")
    assert fields["Target collection:"] == "metabolomics"
    assert report["labels"] == ["propose", "paper-intake", "needs-triage", "auto-report"]
    assert report["title"] == f"Propose: {FIELDS['what']}"


def test_paper_form_offers_only_released_collections_without_a_default():
    page = (SITE / "propose.html").read_text(encoding="utf-8")
    select = page.split('<select name="collection"')[1].split("</select>")[0]
    offered = re.findall(r'<option value="([^"]+)">', select)
    manifest = json.loads((SITE / "search_index" / "manifest.json").read_text(encoding="utf-8"))
    released = sorted(slug for slug, entry in manifest["domains"].items()
                      if any(c["status"] == "released" for c in entry["collections"]))
    assert offered == released
    assert 'value="" selected disabled' in select
    assert 'value="metabolomics" required' not in page
    assert '<script src="propose.js"></script>' in page


# --------------------------------------------------------------------------- #
# Route renderers                                                              #
# --------------------------------------------------------------------------- #
def test_fault_report_is_redacted_and_routed():
    report = sf.render_fault("search", "python3 /Users/me/c/bin/search_skills.py --query x",
                             "Traceback in /home/me/x.py", versions="Python 3.12",
                             collection="metabolomics/v3", release="metabolomics-v3.0.2")
    assert report["route"] == "fault" and report["template"] == "4-technical-fault.md"
    assert "/Users/me" not in report["body"] and "/home/me" not in report["body"]
    assert "**Release:** `metabolomics-v3.0.2`" in report["body"]
    assert report["title"].startswith("fault: search: ")
    with pytest.raises(ValueError, match="unknown component"):
        sf.render_fault("kernel", "x", "y")


def test_missing_skill_report_asks_for_new_work():
    report = sf.render_issue("gap", "batch alignment with internal standards", "searched, nothing")
    assert report["route"] == "missing"
    assert "propose" in report["labels"] and "auto-report" in report["labels"]
    assert "### What was tried" in report["body"]


def test_address_is_bounded_and_falls_back_to_a_short_one():
    short = sf.render_issue("defect", "x", "brief")
    found = sf.issue_address(short)
    assert found["address"].startswith(sf.ISSUES_URL + "/new?template=1-skill-feedback.md")
    assert "body=" in found["address"]
    long = sf.render_issue("defect", "x", "word " * 3000)
    found = sf.issue_address(long)
    assert found["address"] is None
    assert "body=" not in found["short_address"]
    assert len(found["short_address"]) <= sf.MAX_ADDRESS_LENGTH


# --------------------------------------------------------------------------- #
# The vendored report helper                                                   #
# --------------------------------------------------------------------------- #
def test_helper_template_is_generated_from_the_feedback_script():
    template = router_shape.REPORT_HELPER.read_bytes()
    assert router_shape.embed_report_logic(template) == template
    pii, logic = router_shape.report_logic_blocks()
    assert logic in template and pii in template
    assert router_shape.PACKAGE_REPORT_HELPER.read_bytes() == template


def test_helper_is_standard_library_only_and_never_calls_the_network():
    text = router_shape.REPORT_HELPER.read_text(encoding="utf-8")
    imports = set(re.findall(r"^(?:import|from) ([\w.]+)", text, re.M))
    assert imports <= {"__future__", "re", "typing", "hashlib", "urllib.parse",
                       "argparse", "json", "sys", "pathlib"}
    assert "urlopen" not in text and "socket" not in text and "subprocess" not in text


def _helper_unit(tmp_path: Path) -> Path:
    unit = tmp_path / "unit"
    shutil.copytree(FIXTURE / ".claude-plugin", unit / ".claude-plugin")
    assert router_shape.write_report_helper(unit) is True
    assert router_shape.write_report_helper(unit) is False
    return unit


def _run_helper(unit: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, "-I", "-S", str(unit / "bin" / "report_issue.py"), *args],
                          cwd="/", capture_output=True, text=True, timeout=60)


def test_shipped_helper_runs_isolated_and_fills_in_the_collection(tmp_path: Path):
    unit = _helper_unit(tmp_path)
    result = _run_helper(unit, "skill", "--skill", "peak-align", "--symptom",
                         "failed on /Users/me/run.raw", "--json")
    assert result.returncode == 0, result.stderr
    report = json.loads(result.stdout)
    assert "**Collection:** `fixture/v1`" in report["body"]
    assert "**Release:** `fixture-v1.0.0`" in report["body"]
    assert "/Users/me" not in report["body"] and "/Users/me" not in report["address"]
    assert report["labels"] == sf.labels_for("defect", drafted=True)
    assert report["address"].startswith(sf.ISSUES_URL + "/new?")


@pytest.mark.parametrize("args", [
    ("missing", "--task", "align batches", "--tried", "searched twice"),
    ("paper", "--what", "Spec2Vec", "--link", "10.1371/journal.pcbi.1008724", "--why", "useful"),
    ("fault", "--component", "plugin", "--ran", "/plugin install x", "--happened", "not found"),
])
def test_every_route_renders_from_the_helper(tmp_path: Path, args):
    unit = _helper_unit(tmp_path)
    result = _run_helper(unit, *args)
    assert result.returncode == 0, result.stderr
    assert f"Route: {sf.ROUTES[args[0]]}" in result.stdout
    assert "post only on an explicit yes" in result.stdout


def test_a_long_report_prints_the_body_and_a_short_address(tmp_path: Path):
    unit = _helper_unit(tmp_path)
    result = _run_helper(unit, "skill", "--skill", "x", "--symptom", "word " * 3000)
    assert result.returncode == 0
    assert "too long for an address" in result.stdout
    address = [line for line in result.stdout.splitlines() if line.startswith("Address: ")][0]
    assert "body=" not in address


def test_asbb_report_wraps_the_same_helper(capsys):
    from asb_skill_collections.asbb_cli import main
    assert main(["report", "fault", "--component", "cli", "--ran", "asbb fetch x",
                 "--happened", "HTTP 404", "--json"]) == 0
    report = json.loads(capsys.readouterr().out)
    assert report["labels"] == sf.route_labels("fault")
    assert report["template"] == "4-technical-fault.md"
    assert main(["report", "skill", "--skill", "x"]) == 2


# --------------------------------------------------------------------------- #
# Router section                                                               #
# --------------------------------------------------------------------------- #
def _unit(tmp_path: Path) -> Path:
    unit = tmp_path / "installed" / "fixture"
    shutil.copytree(FIXTURE, unit)
    return unit


def _router(unit: Path) -> str:
    return (unit / "skills" / "_router" / "SKILL.md").read_text(encoding="utf-8")


def _section(text: str) -> str:
    return text[text.index(router_shape.CONTRIBUTION_HEADING):]


@pytest.mark.parametrize("helper", [True, False])
def test_generated_routers_carry_the_section(tmp_path: Path, helper: bool):
    unit = _unit(tmp_path)
    if helper:
        router_shape.write_report_helper(unit)
    router_shape.write_routers(unit, rewrite=True)
    workflow = (unit / "workflows" / "_workflow_router" / "SKILL.md").read_text(encoding="utf-8")
    for text in (_router(unit), workflow):
        section = " ".join(_section(text).split())
        for words in ROUTE_WORDS:
            assert words in section
        assert "`fixture/v1` improves from use." in section and "release" not in section
        assert "post only on an explicit yes" in section
        assert "Never paste paths, credentials or sample names." in section
        assert "gh issue create --repo HolobiomicsLab/asb-skill-collections" in section
        assert ("bin/report_issue.py" in section) is helper
        assert "asb-skills-" not in section
        prose = re.sub(r"```bash.*?```", "", _section(text), flags=re.S)
        assert 110 <= len(prose.split()) <= 190
        assert router_shape.contribution_status(text, router_shape.unit_contract(unit)) == "current"
    assert router_shape.router_contribution_findings(unit) == []


def test_the_helper_command_of_the_router_runs(tmp_path: Path):
    unit = _unit(tmp_path)
    router_shape.write_report_helper(unit)
    router_shape.write_routers(unit, rewrite=True)
    [command] = re.findall(r"```bash\n(python3 [^\n]*report_issue\.py[^\n]*)\n```", _router(unit))
    command = command.replace(router_shape.SKILL_DIR, str(unit / "skills" / "_router"))
    argv = [sys.executable if part == "python3" else part
            for part in re.findall(r'"[^"]*"|\S+', command)]
    argv = [part.strip('"') for part in argv]
    argv = [("peak-align" if part == "<slug>" else part) for part in argv]
    result = subprocess.run(argv, cwd=tmp_path, capture_output=True, text=True, timeout=60)
    assert result.returncode == 0, result.stderr
    assert "fixture-v1.0.0" in result.stdout and "Route: " in result.stdout


def test_a_released_router_without_the_section_is_accepted_and_kept(tmp_path: Path):
    unit = _unit(tmp_path)
    router = unit / "skills" / "_router" / "SKILL.md"
    released = router.read_text(encoding="utf-8")
    assert router_shape.CONTRIBUTION_HEADING not in released
    assert router_shape.router_contribution_findings(unit) == []
    router_shape.write_router(unit, 10)
    assert router_shape.CONTRIBUTION_HEADING not in router.read_text(encoding="utf-8")
    assert router_shape.contribution_status(released, router_shape.unit_contract(unit)) == "absent"


def test_a_stale_section_is_found_and_refreshed(tmp_path: Path):
    unit = _unit(tmp_path)
    router_shape.write_routers(unit, rewrite=True)
    router = unit / "skills" / "_router" / "SKILL.md"
    text = router.read_text(encoding="utf-8")
    router.write_text(text.replace("Never paste paths", "Do not paste paths"), encoding="utf-8")
    assert router_shape.router_contribution_findings(unit) == ["skills/_router/SKILL.md"]
    checked = subprocess.run([sys.executable, str(REPO / "scripts" / "check_release_surface.py"), str(unit)],
                             capture_output=True, text=True, timeout=120)
    assert checked.returncode == 1 and "stale-contribution-section" in checked.stdout
    assert router_shape.main(["--check", str(unit)]) == 1
    router_shape.write_router(unit, 10)
    assert router.read_text(encoding="utf-8") == text
    assert router_shape.main(["--check", str(unit)]) == 0


def test_a_version_bump_leaves_the_section_current(tmp_path: Path):
    unit = _unit(tmp_path)
    router_shape.write_routers(unit, rewrite=True)
    rendered = _router(unit)
    plugin = unit / ".claude-plugin" / "plugin.json"
    meta = json.loads(plugin.read_text(encoding="utf-8"))
    plugin.write_text(json.dumps({**meta, "version": "1.0.1"}), encoding="utf-8")
    assert router_shape.router_contribution_findings(unit) == []
    router_shape.write_router(unit, 10)
    assert _section(_router(unit)) == _section(rendered)


def test_the_helper_takes_the_release_a_unit_is_about_to_publish(tmp_path: Path):
    unit = _unit(tmp_path)
    router_shape.write_report_helper(unit)
    (unit / ".zenodo.json").write_text(json.dumps({"version": "v1.1.0"}), encoding="utf-8")
    result = _run_helper(unit, "skill", "--skill", "peak-align", "--symptom", "the flag changed")
    assert result.returncode == 0, result.stderr
    assert "fixture-v1.1.0" in result.stdout and "fixture-v1.0.0" not in result.stdout


def test_scripts_only_ships_the_helper_only_when_asked(tmp_path: Path):
    unit = _unit(tmp_path)
    router_shape.main(["--scripts-only", str(unit)])
    assert not (unit / "bin" / "report_issue.py").exists()
    router_shape.main(["--scripts-only", "--with-report-helper", str(unit)])
    assert (unit / "bin" / "report_issue.py").read_bytes() == router_shape.REPORT_HELPER.read_bytes()


# --------------------------------------------------------------------------- #
# Search output                                                                #
# --------------------------------------------------------------------------- #
def _search(unit: Path) -> str:
    result = subprocess.run([sys.executable, str(unit / "bin" / "search_skills.py"),
                             "--query", "zzqqxx unmatched words"],
                            cwd="/", capture_output=True, text=True, timeout=120)
    assert result.returncode == 0, result.stderr
    return result.stdout


def test_an_empty_search_names_routes_two_and_three(tmp_path: Path):
    unit = _unit(tmp_path)
    out = _search(unit)
    assert sf.ROUTES["missing"] in out and sf.ROUTES["paper"] in out
    assert sf.ISSUES_URL in out
    router_shape.write_report_helper(unit)
    out = _search(unit)
    assert f'python3 "{unit.resolve() / "bin" / "report_issue.py"}" missing --help' in out


# --------------------------------------------------------------------------- #
# Texts                                                                        #
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("name", ["README.md", "AGENTS.md", "CLAUDE.md", ".github/CONTRIBUTING.md",
                                  "docs/CONTRIBUTION_LOOP.md"])
def test_texts_name_the_four_routes(name: str):
    text = " ".join((REPO / name).read_text(encoding="utf-8").split())
    for words in ROUTE_WORDS:
        assert words.lower() in text.lower(), (name, words)


@pytest.mark.parametrize("name", ["README.md", "AGENTS.md", "CLAUDE.md", ".github/CONTRIBUTING.md",
                                  "docs/CONTRIBUTION_LOOP.md", ".github/copilot-instructions.md",
                                  ".github/PULL_REQUEST_TEMPLATE.md", "docs/adding-papers.md"])
def test_no_text_sends_the_public_to_a_private_repository(name: str):
    text = (REPO / name).read_text(encoding="utf-8")
    assert not re.search(r"github\.com/HolobiomicsLab/asb-skills-", text), name
    assert not re.search(r"(open|start|use) a (GitHub )?Discussion", text, re.I), name
