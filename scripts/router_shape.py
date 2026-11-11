#!/usr/bin/env python3
"""Convert a skill unit to the router-shaped layout.

A plugin host advertises every skill under a unit's ``skills/`` directory by
injecting its name and description into the session prompt, so a unit with
hundreds or thousands of leaves costs more context than a session can spare
just by being installed. This moves the leaf corpus to ``leaves/`` — still
shipped, still installed, but read on demand — and leaves behind a single
router skill plus the retrieval script and index it needs.

Idempotent: re-running on an already-shaped unit refreshes the router,
retrieval script and index without moving anything.

    python scripts/router_shape.py packs/metabolomics/lc-ms \\
        --index collections/metabolomics/v2/skills_index.json

Render only the leaf and workflow routers of a shaped unit, whole:

    python scripts/router_shape.py --routers-only --rewrite <unit>
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path

import yaml

# Invoked by path (`python scripts/x.py`), only `scripts/` lands on sys.path, so
# the repo root has to be added before the sibling package can be imported.
if __package__ in (None, ""):
    import os.path as _p
    import sys as _sys

    _sys.path.insert(0, _p.dirname(_p.dirname(_p.abspath(__file__))))

from asb_skill_collections import layout
from scripts.skill_index import parse_frontmatter

REPO = Path(__file__).resolve().parent.parent
SEARCH_SCRIPT = REPO / "scripts" / "templates" / "search_skills.py"
SELECTOR_SOURCE = REPO / "asb_skill_collections" / "asb_skill_index.py"
SELECTOR_BEGIN = b"# BEGIN VENDORED SELECTOR\n"
SELECTOR_END = b"# END VENDORED SELECTOR\n"
# The report helper a unit may ship in bin/: its two vendored blocks are the
# report logic of scripts/skill_feedback.py and the patterns of pii_config.py.
REPORT_HELPER = REPO / "scripts" / "templates" / "report_issue.py"
PACKAGE_REPORT_HELPER = REPO / "asb_skill_collections" / "report_issue.py"
REPORT_HELPER_NAME = "report_issue.py"
FEEDBACK_SOURCE = REPO / "scripts" / "skill_feedback.py"
PII_SOURCE = REPO / "scripts" / "pii_config.py"
PII_BEGIN = b"# BEGIN VENDORED PII CONFIG\n"
PII_END = b"# END VENDORED PII CONFIG\n"
LOGIC_BEGIN = b"# BEGIN VENDORED REPORT LOGIC\n"
LOGIC_END = b"# END VENDORED REPORT LOGIC\n"
SHARED_BEGIN = b"# BEGIN SHARED REPORT LOGIC\n"
SHARED_END = b"# END SHARED REPORT LOGIC\n"
FUTURE_IMPORT = b"from __future__ import annotations\n"
REGISTRY = "HolobiomicsLab/asb-skill-collections"
REGISTRY_ISSUES = f"https://github.com/{REGISTRY}/issues"
CONTRIBUTION_HEADING = "## Report and contribute"
ROUTER_SLUG = "_router"
MAX_CONTRACT_LEAVES = 20
TOOL_FIELDS = ("tools", "metadata.tools")
SOURCE_FIELDS = ("derived_from", "provenance.source_papers")

# The commands are written from the skill's own directory, never from the plugin
# root or the working directory: an agent that `cd`s into the skill directory
# before a root-relative command fails, and so does `python` on a stock macOS.
# Claude Code replaces `${CLAUDE_SKILL_DIR}` in a skill body with that absolute
# directory before the agent reads it, so the command is runnable as printed.
# A host that does not (Codex reads the file as written) leaves the variable;
# LOCATE_ROOT tells the agent to replace it, and never names the variable
# itself, since Claude Code would substitute that mention too.
SKILL_DIR = "${CLAUDE_SKILL_DIR}"
ROOT_FROM_SKILL = f"{SKILL_DIR}/../.."
PYTHON = "python3"
SEARCH_COMMAND = f'{PYTHON} "{ROOT_FROM_SKILL}/bin/search_skills.py"'
BINDER_COMMAND = f'{PYTHON} "{ROOT_FROM_SKILL}/bin/perspicacite_kb_bind.py"'
WORKFLOW_ROUTER_SLUG = "_workflow_router"

LOCATE_ROOT = """Run the commands as written, from any working directory; do not `cd`.
If a command still shows a `${{...}}` variable instead of an absolute path, the
host did not fill it in: replace the variable with the absolute directory of
this file, `<collection root>/{relative}`."""

PYTHON_NOTE = (
    "Python 3.9 or later, standard library only, no network; where `python3` "
    "is missing, use `python` or `py -3`."
)

CITE_IN_ANSWER = (
    "In the answer, name the skill and give its source DOI and its licence tier."
)

APPLY_WITH_EVIDENCE = """## 2. Apply

Read the `read:` path of the chosen hit, `leaves/<slug>/SKILL.md`. Its
frontmatter carries {tool_keys} (what to install or invoke), {source_keys}
(source paper DOIs) and `evidence_spans` (verbatim anchors from the paper or
repo). Follow the body.
{cite}"""

APPLY_WITH_BODY_EVIDENCE = """## 2. Apply

Read the `read:` path of the chosen hit, `leaves/<slug>/SKILL.md`. Its
frontmatter carries {tool_keys} (what to install or invoke) and {source_keys}
(source paper DOIs). Find verbatim evidence lines in the body, then follow the
procedure.
{cite}"""

# Filled with .format(binder=..., root=..., guide=...): the command holds
# `${CLAUDE_SKILL_DIR}`, whose braces must not be parsed as a format field.
GROUND_WITH_BINDER = """## 3. Ground (recommended)

Before trusting a parameter, threshold or default, verify it against the paper
the skill was built from. `kb_bundle.json` maps each skill to its source KBs:

```bash
{binder} query --collection "{root}" \\
  --skill <slug> --question "<what you need to verify>"
```{guide}"""

GROUND_FROM_DOIS = """## 3. Ground (recommended)

Before trusting a parameter, threshold or default, verify it against the
source-paper DOIs of the leaf{source_pointer}.{guide}"""

# One definition of the tiers, taken from governance/LICENSE_TIERS.md and
# scripts/license_tier.py: `restricted` is a verdict (a licence was found and it
# constrains reuse), `unknown` is an open question (no tool licence found).
TIERS_SECTION = """## Licence tiers

Each skill hit prints `tier`, the licence tier of the tool it relies on (the
skill text itself is CC-BY-4.0). Check it before presenting a candidate.
`open`: commercial use allowed. `noncommercial`: academic or non-commercial use
only; get explicit confirmation of a non-commercial purpose before applying it.
`restricted`: a licence was established and it constrains reuse (for example a
vendor licence); say so before commercial use or redistribution. `unknown`: no
licence for the tool was established; say so, and treat the tool as all rights
reserved until the user has checked it."""

# Addressed to the agent: the four routes of scripts/skill_feedback.py ROUTES, in
# the same words, the moments to offer a report and the consent rule. Rendered
# whole from the unit (collection, release, helper shipped or not), so a present
# section is either current or stale; routers released without it stay valid.
CONTRIBUTION_SECTION = """{heading}

`{collection}`{release} improves from use. Offer a report yourself, once per
problem, when a procedure failed or no longer matches the tool, the search
returned nothing usable and the work was done unaided, the user names a
method paper whose DOI the search does not find, the leaves had to be
composed by hand, or a command of this collection failed. Name the route:

1. this skill is wrong or could be better;
2. a skill is missing: request it, or propose yours;
3. a paper is not referenced: propose it;
4. something technical failed: report it.

After a no, do not raise it again. Draft the report, show the user its exact
title, labels and body, and post only on an explicit yes. Never paste paths,
credentials or sample names.
{how}
Reports go to the public registry; a maintainer carries them into the private
domain repository."""

CONTRIBUTION_WITH_HELPER = """
```bash
{helper} skill --skill <slug> --kind defect --symptom "<what happened>"
```

Routes: `skill`, `missing`, `paper`, `fault` (`--help` lists the fields). It
redacts and prints the report and a prefilled address. With `gh` and the
user's yes, run `gh issue create --repo {registry}`; otherwise give the user
the address.
"""

CONTRIBUTION_WITHOUT_HELPER = """
Write the title and body: the route, the skill slug or task, what happened.
With `gh` and the user's yes, run `gh issue create --repo {registry}`;
otherwise give the user the address
`{issues}/new?title=<title>&body=<body>`, URL-encoded.
"""

REPORT_COMMAND = f'{PYTHON} "{ROOT_FROM_SKILL}/bin/{REPORT_HELPER_NAME}"'


def unit_identity(unit: Path) -> dict:
    """Collection and release labels of a unit, so its reports are attributable.

    The collection is `<slug>/v<version>` from `collection.yaml`, else the plugin
    name; the release is `<plugin name>-v<plugin version>`.
    """
    meta = {}
    plugin = unit / ".claude-plugin" / "plugin.json"
    if plugin.is_file():
        meta = json.loads(plugin.read_text(encoding="utf-8"))
    name = str(meta.get("name") or unit.name)
    version = str(meta.get("version") or "")
    collection = name
    manifest = unit / "collection.yaml"
    if manifest.is_file():
        document = yaml.safe_load(manifest.read_text(encoding="utf-8")) or {}
        if document.get("slug") and document.get("version") is not None:
            collection = f"{document['slug']}/v{document['version']}"
    return {"collection": collection, "release": f"{name}-v{version}" if version else ""}


def contribution_section(contract: dict) -> str:
    """Render the report-and-contribute section of a unit's routers."""
    how = (CONTRIBUTION_WITH_HELPER if contract.get("has_report_helper")
           else CONTRIBUTION_WITHOUT_HELPER)
    release = contract.get("release") or ""
    return CONTRIBUTION_SECTION.format(
        heading=CONTRIBUTION_HEADING,
        collection=contract.get("collection") or "this collection",
        release=f" (release `{release}`)" if release else "",
        how=how.format(helper=REPORT_COMMAND, registry=REGISTRY, issues=REGISTRY_ISSUES),
    )


def contribution_status(text: str, contract: dict) -> str:
    """`absent`, `current` or `stale`: the state of a router's contribution section.

    Routers released before the section existed carry none, and that is
    accepted; a section that is present must be the one the unit renders.
    """
    pattern = re.compile(rf"^{re.escape(CONTRIBUTION_HEADING)}[^\n]*\n.*?(?=^## |\Z)", re.M | re.S)
    match = pattern.search(text)
    if not match:
        return "absent"
    expected = contribution_section(contract).strip()
    # The labels are compared apart from the text: a release stage that bumps
    # the plugin version after the routers were rendered must not turn every
    # router stale. The labels are refreshed with the section.
    return "current" if _mask_identity(match.group().strip()) == _mask_identity(expected) else "stale"


IDENTITY_SENTENCE = re.compile(r"^`[^`\n]*`(?: \(release `[^`\n]*`\))? improves from use\.", re.M)


def _mask_identity(section: str) -> str:
    return IDENTITY_SENTENCE.sub("<collection> improves from use.", section, count=1)


def router_contribution_findings(unit: Path) -> list[str]:
    """Routers of a unit whose contribution section is present and stale."""
    contract = None
    findings = []
    for relative in (f"{layout.ADVERTISED_DIRNAME}/{ROUTER_SLUG}/SKILL.md",
                     f"{layout.WORKFLOW_DIRNAME}/{WORKFLOW_ROUTER_SLUG}/SKILL.md"):
        router = unit / relative
        if not router.is_file():
            continue
        text = router.read_text(encoding="utf-8")
        if CONTRIBUTION_HEADING not in text:
            continue
        if contract is None:
            contract = {**unit_identity(unit), "has_report_helper": has_report_helper(unit)}
        if contribution_status(text, contract) == "stale":
            findings.append(relative)
    return findings


def has_report_helper(unit: Path) -> bool:
    return (unit / "bin" / REPORT_HELPER_NAME).is_file()


# The frontmatter is rendered by `router_frontmatter` with yaml.safe_dump, never
# by string formatting: a description holds free text such as "ASB Genomics: 3246
# skills", and an unquoted ": " makes the whole frontmatter unparsable.
ROUTER_TEMPLATE = """---
{frontmatter}---

# {title} router

**{count:,} evidence-grounded skills**, each derived from a
method paper (journal article or preprint) and its code{extras}.
They ship beside this router as data, in `leaves/<slug>/SKILL.md`. **Do not
list `leaves/` and do not read the indexes whole.** Search, then read the one
file you need.

{search_section}

{apply_section}

{grounding_section}

{tiers_section}

{contribution_section}
"""


def search_section(contract: dict) -> str:
    """Render step 1: the cwd-independent search commands for this unit."""
    lines = ["# one atomic skill",
             f'{SEARCH_COMMAND} --query "<the user\'s task>" -k 10']
    if contract.get("workflows_count") and contract.get("search_workflows"):
        lines += ["# an end-to-end workflow for a whole analysis goal",
                  f'{SEARCH_COMMAND} --query "<the user\'s goal>" --target workflows -k 3']
    if contract.get("tools_count") and contract.get("search_tools"):
        lines += ["# a tool record (licence tier, source DOIs)",
                  f'{SEARCH_COMMAND} --query "<a tool name or task>" --target tools -k 5']
    filters = ["`--tool <name>`", "`--edam <iri-substring>`"]
    if contract.get("has_techniques"):
        filters.insert(1, "`--technique <tag>`")
    narrow = "Narrow with " + ", ".join(filters[:-1]) + f" or {filters[-1]}."
    commands = "\n".join(lines)
    return (
        "## 1. Search\n\n"
        + LOCATE_ROOT.format(relative=f"{layout.ADVERTISED_DIRNAME}/{ROUTER_SLUG}")
        + f"\n\n```bash\n{commands}\n```\n\n"
        + "Each hit prints the absolute `read:` path; a skill hit also its licence "
        + "tier and source DOI. "
        + f"{narrow}\n{PYTHON_NOTE}"
    )


def leaf_slugs(unit: Path) -> list[str]:
    """Slugs the unit ships, from whichever layout it currently uses."""
    return sorted(d.name for d in layout.slug_dirs(unit))


def move_leaves(unit: Path, keep: set[str]) -> int:
    """Move every skill except `keep` out of the advertised dir. Returns count."""
    advertised = unit / layout.ADVERTISED_DIRNAME
    target = unit / layout.LEAF_DIRNAME
    if not advertised.is_dir():
        return 0
    target.mkdir(exist_ok=True)
    moved = 0
    for child in sorted(advertised.iterdir()):
        if not child.is_dir() or child.name in keep:
            continue
        shutil.move(str(child), str(target / child.name))
        moved += 1
    return moved


def write_index(unit: Path, source_index: Path, slugs: set[str]) -> int:
    """Write the unit's own skills_index.json as a subset of a parent index."""
    rows = json.loads(source_index.read_text(encoding="utf-8"))
    subset = [r for r in rows if r.get("slug") in slugs]
    (unit / "skills_index.json").write_text(
        json.dumps(subset, indent=1, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return len(subset)


def unit_contract(unit: Path) -> dict:
    """Describe the frontmatter and grounding capabilities a unit ships."""
    leaves = unit / layout.LEAF_DIRNAME
    directories = (
        sorted(path for path in leaves.iterdir() if path.is_dir())
        if leaves.is_dir()
        else layout.slug_dirs(unit)
    )
    skill_files = [
        path / "SKILL.md"
        for path in directories
        if (path / "SKILL.md").is_file()
    ][:MAX_CONTRACT_LEAVES]
    frontmatters = [parse_frontmatter(path) for path in skill_files]
    tool_fields = tuple(
        field for field in TOOL_FIELDS if any(
            (field == "tools" and field in fm)
            or (
                field == "metadata.tools"
                and isinstance(fm.get("metadata"), dict)
                and "tools" in fm["metadata"]
            )
            for fm in frontmatters
        )
    )
    source_fields = tuple(
        field for field in SOURCE_FIELDS if any(
            (field == "derived_from" and field in fm)
            or (
                field == "provenance.source_papers"
                and isinstance(fm.get("provenance"), dict)
                and "source_papers" in fm["provenance"]
            )
            for fm in frontmatters
        )
    )
    tool_keys = " and ".join(f"`{field}`" for field in tool_fields)
    source_keys = " and ".join(f"`{field}`" for field in source_fields)
    has_evidence_spans = any("evidence_spans" in fm for fm in frontmatters)
    has_binder = (unit / "bin" / "perspicacite_kb_bind.py").is_file()
    has_guide = (unit / "GROUNDING.md").is_file()
    apply_template = APPLY_WITH_EVIDENCE if has_evidence_spans else APPLY_WITH_BODY_EVIDENCE
    guide = "\n\nSee `GROUNDING.md` for the backends and tiers." if has_guide else ""
    if has_binder:
        grounding_section = GROUND_WITH_BINDER.format(
            binder=BINDER_COMMAND, root=ROOT_FROM_SKILL, guide=guide
        )
    else:
        pointer = f", listed in its {source_keys} frontmatter" if source_keys else ""
        grounding_section = GROUND_FROM_DOIS.format(
            source_pointer=pointer, guide=guide
        )
    return {
        "tool_fields": tool_fields,
        "source_fields": source_fields,
        "tool_keys": tool_keys,
        "source_keys": source_keys,
        "evidence_location": (
            "`evidence_spans`" if has_evidence_spans
            else "verbatim evidence lines in the body"
        ),
        "has_binder": has_binder,
        "has_guide": has_guide,
        "apply_section": apply_template.format(
            tool_keys=tool_keys, source_keys=source_keys, cite=CITE_IN_ANSWER
        ),
        "grounding_section": grounding_section,
        "has_report_helper": has_report_helper(unit),
        **unit_identity(unit),
        **unit_inventory(unit),
    }


def unit_inventory(unit: Path) -> dict:
    """Counts and filters the router may advertise, read from what the unit ships.

    Counted the way `check_advertised_counts.py` counts them (tool records and
    workflow definitions on disk), so the router never advertises a target or a
    filter the unit cannot serve.
    """
    rows = []
    index = unit / "skills_index.json"
    if index.is_file():
        rows = json.loads(index.read_text(encoding="utf-8"))
    return {
        "has_techniques": any(row.get("techniques") for row in rows),
        "workflows_count": sum(
            1 for _ in unit.glob(f"{layout.WORKFLOW_DIRNAME}/*/workflow.yaml")
        ),
        "tools_count": sum(1 for _ in unit.glob("tools/*.yaml")),
        "search_workflows": any(
            (unit / name).is_file()
            for name in ("workflows/workflows_index.json", "workflows_index.json")
        ),
        "search_tools": (unit / "tools_index.json").is_file(),
        "workflow_names": sorted(
            path.parent.name
            for path in unit.glob(f"{layout.WORKFLOW_DIRNAME}/*/workflow.yaml")
        ),
    }


def _section_is_current(section: str, number: int, contract: dict) -> bool:
    """Return whether one existing router section describes the unit contract."""
    if number == 3:
        has_binder = "perspicacite_kb_bind.py" in section
        has_guide = "GROUNDING.md" in section
        if contract["has_binder"]:
            return (
                has_binder
                and BINDER_COMMAND in section
                and (not has_guide or contract["has_guide"])
            )
        expected = all(
            f"`{field}`" in section for field in contract["source_fields"]
        )
        absent = set(SOURCE_FIELDS) - set(contract["source_fields"])
        has_phantom = any(f"`{field}`" in section for field in absent)
        points_to_dois = "source-paper DOI" in section
        return (
            not has_binder
            and has_guide == contract["has_guide"]
            and expected
            and points_to_dois
            and not has_phantom
        )

    expected_tools = contract["tool_fields"]
    has_tools = all(f"`{field}`" in section for field in expected_tools)
    legacy_alias = (
        expected_tools == ("metadata.tools",)
        and section.splitlines()[0] != "## 2. Apply"
        and "`tools`" in section
    )
    has_tools = has_tools or legacy_alias
    has_sources = all(
        f"`{field}`" in section for field in contract["source_fields"]
    )
    has_evidence_field = "`evidence_spans`" in section
    has_body_evidence = "verbatim evidence lines in the body" in section
    if contract["evidence_location"] == "`evidence_spans`":
        evidence = has_evidence_field and not has_body_evidence
    else:
        evidence = has_body_evidence and not has_evidence_field
    absent_sources = set(SOURCE_FIELDS) - set(contract["source_fields"])
    has_phantom_source = any(
        f"`{field}`" in section for field in absent_sources
    )
    absent_tools = set(TOOL_FIELDS) - set(expected_tools)
    has_phantom_tool = any(f"`{field}`" in section for field in absent_tools)
    if legacy_alias:
        has_phantom_tool = False
    return (
        has_tools
        and has_sources
        and evidence
        and not has_phantom_source
        and not has_phantom_tool
    )


def _section_is_stale_search(section: str, contract: dict) -> bool:
    """Step 1 is generated whole, so anything but the current text is stale."""
    return section.strip() != search_section(contract).strip()


def _refresh_router_sections(body: str, contract: dict) -> str:
    """Replace only stale sections in an existing router.

    Steps 1 to 3, the licence tiers and a contribution section that is
    present are refreshed; the frontmatter, title and introduction of an
    existing router are kept as written, and a router without a contribution
    section does not gain one (only a rewrite renders it).
    """
    rendered = body
    replacements = {
        r"## 1\.": (search_section(contract), _section_is_stale_search),
        r"## 2\.": (
            contract["apply_section"],
            lambda section, c: not _section_is_current(section, 2, c),
        ),
        r"## 3\.": (
            contract["grounding_section"],
            lambda section, c: not _section_is_current(section, 3, c),
        ),
        r"## Licen[cs]e tiers": (
            TIERS_SECTION,
            lambda section, c: section.strip() != TIERS_SECTION.strip(),
        ),
        # Never added to a released router by a refresh: absent stays absent.
        re.escape(CONTRIBUTION_HEADING): (
            contribution_section(contract),
            lambda section, c: section.strip() != contribution_section(c).strip(),
        ),
    }
    for heading, (replacement, is_stale) in replacements.items():
        pattern = re.compile(rf"^{heading}[^\n]*\n.*?(?=^## |\Z)", re.M | re.S)
        match = pattern.search(rendered)
        if match and is_stale(match.group(), contract):
            tail = rendered[match.end():]
            rendered = (
                rendered[:match.start()]
                + replacement
                + ("\n\n" if tail else "\n")
                + tail
            )
    return rendered


def router_frontmatter(
    router_name: str, description: str, count: int, indexes: list[str] | None = None
) -> str:
    """Render the router frontmatter as YAML that parses back to its values."""
    return yaml.safe_dump(
        {
            "name": router_name,
            "description": description,
            "license": "CC-BY-4.0",
            "metadata": {
                "skills_count": count,
                "leaf_dir": layout.LEAF_DIRNAME,
                "retrieval": "bin/search_skills.py",
                "indexes": indexes or ["skills_index.json"],
            },
            "schema_version": "0.2.0",
        },
        sort_keys=False,
        allow_unicode=True,
        width=1000,
    )


def domain_label(name: str, description: str) -> str:
    """The domain as the plugin description names it ("ASB Proteomics: ...").

    Falls back to the plugin name. This is the only per-domain scope text every
    unit ships; nothing else is invented for the router description.
    """
    head = re.split(r"[:.]", description, maxsplit=1)[0].strip()
    head = re.sub(r"^ASB\s+", "", head)
    if not head or len(head.split()) > 4:
        head = name.replace("-", " ").title()
    return head


def _lower_words(label: str) -> str:
    """Lower-case capitalised words for mid-sentence use; keep acronyms (AI)."""
    return " ".join(
        "-".join(
            part.lower() if part[:1].isupper() and part[1:].islower() else part
            for part in word.split("-")
        )
        for word in label.split()
    )


def router_description(domain: str, count: int, contract: dict) -> str:
    """When to use the router first, then what it searches; hosts truncate the rest.

    Codex cut a description near 169 characters and Claude Code shortens
    descriptions when its skill listing exceeds its budget, so the first
    sentence alone has to name the domain and the trigger. The trigger is a
    plain question about how to do a task in the domain: live sessions with a
    description that spoke of "a task that needs a skill" never loaded the
    router for a question that did not mention skills.
    """
    topic = _lower_words(domain)
    served = [f"{count:,} evidence-grounded {topic} skills distilled from method papers "
              "and their code"]
    workflows = contract.get("workflows_count") if contract.get("search_workflows") else 0
    tools = contract.get("tools_count") if contract.get("search_tools") else 0
    if workflows:
        served.append(f"{workflows} end-to-end workflow{'s' if workflows != 1 else ''}")
    if tools:
        served.append(f"{tools:,} tool records")
    listed = (
        ", ".join(served[:-1]) + f" and {served[-1]}" if len(served) > 1 else served[0]
    )
    return (
        f"Use for any {topic} how-to question (which method, tool, parameters or "
        f"pipeline to use), before answering from memory. Searches {listed}, "
        "then reads the one that fits."
    )


def write_router(unit: Path, count: int, rewrite: bool = False) -> None:
    """Write the single advertised entry-point skill.

    An existing router is refreshed section by section unless ``rewrite`` asks
    for the whole file, frontmatter and description included, to be rendered.
    """
    contract = unit_contract(unit)
    out = unit / layout.ADVERTISED_DIRNAME / ROUTER_SLUG / "SKILL.md"
    if out.is_file() and not rewrite:
        existing = out.read_text(encoding="utf-8")
        refreshed = _refresh_router_sections(existing, contract)
        if refreshed != existing:
            out.write_text(refreshed, encoding="utf-8")
        return
    meta = json.loads((unit / ".claude-plugin" / "plugin.json").read_text())
    name, description = meta["name"], meta["description"]
    title = description.split(".")[0].strip() or name
    domain = domain_label(name, description)
    if title.startswith("ASB ") and ":" in title:
        title = f"ASB {domain}"
    indexes = ["skills_index.json"]
    if contract["search_workflows"] and contract["workflows_count"]:
        indexes.append("workflows/workflows_index.json")
    if contract["search_tools"] and contract["tools_count"]:
        indexes.append("tools_index.json")
    frontmatter = router_frontmatter(
        f"{name}-router", router_description(domain, count, contract), count, indexes
    )
    extras = []
    if contract["search_workflows"] and contract["workflows_count"]:
        n = contract["workflows_count"]
        extras.append(f"{n} end-to-end workflow{'s' if n != 1 else ''}")
    if contract["search_tools"] and contract["tools_count"]:
        extras.append(f"{contract['tools_count']:,} tool records")
    body = ROUTER_TEMPLATE.format(
        frontmatter=frontmatter,
        title=title,
        count=count,
        extras=(", with " + " and ".join(extras)) if extras else "",
        search_section=search_section(contract),
        apply_section=contract["apply_section"],
        grounding_section=contract["grounding_section"],
        tiers_section=TIERS_SECTION,
        contribution_section=contribution_section(contract),
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(body, encoding="utf-8")


WORKFLOW_ROUTER_TEMPLATE = """---
{frontmatter}---

# {title} composite workflow router

This is the goal-level entry point of {title}. The leaf router (`{name}-router`)
finds one atomic skill; this router selects an end-to-end workflow with ordered
stages, candidate leaf skills, grounding and a declarative `workflow.yaml`.

## 1. Select

{locate}

```bash
{search} --query "<the user's goal>" --target workflows -k 3
```

{python_note}
For a manual lookup, match the goal against the `description` of each row of
`{skill_dir}/../workflows_index.json`.

Available workflows (published as outlines):

| workflow | what it does |
|---|---|
{rows}

If no workflow fits the goal, fall back to the leaf router (`{name}-router`) and
assemble steps from atomic skills.

## 2. Run

Read the chosen `workflows/<slug>/SKILL.md` (the `read:` path of the hit) and
follow its **Stages** in order. Each stage carries a goal, candidate leaf skills
(primary first), the tools to install or invoke, and its typed inputs and
outputs. The machine-readable `workflows/<slug>/workflow.yaml` is the DAG
(`after`, `inputs_from`). Automatic grading of that DAG (`asb solve-workflow`)
is **not part of this release**: no released ASB version loads these files, so
run the stages yourself. Honor the I/O contract: each stage consumes the prior
stage's declared outputs. Optional stages are marked.

For a stage's leaf skills, read each `{root}/leaves/<leaf-slug>/SKILL.md` for
the procedure, or use the leaf router to pick among the candidates for the
exact data.

## 3. Ground

Before trusting a parameter or default, ground the stage's leaves against the
papers they were distilled from. Each stage's `grounding.kb_slugs` and `dois` in
`workflow.yaml` name the source papers and their `asb-paper-<doi>` knowledge
bases.

> These workflows are published as **outlines**: the stage structure is
> validated, the execution is not. Bindings were chosen by semantic retrieval
> plus deterministic selection. `derived_from_workflows` is a provenance record;
> no ablation experiment consuming it is released.

{contribution_section}
"""


def _workflow_summary(skill: Path) -> str:
    """The one-line `## Summary` of a workflow SKILL.md, else its description."""
    text = skill.read_text(encoding="utf-8")
    match = re.search(r"^## Summary\s*\n+(.+?)\s*$", text, re.M)
    if match:
        return " ".join(match.group(1).split())
    return " ".join(str(parse_frontmatter(skill).get("description") or "").split())


def write_workflow_router(unit: Path, rewrite: bool = False) -> bool:
    """Write `workflows/_workflow_router/SKILL.md` from the shipped workflows.

    The router is not advertised (it lives outside `skills/`); the leaf router
    points to the same `--target workflows` search. Returns whether it wrote.
    An existing workflow router is kept unless ``rewrite`` is set.
    """
    workflows = unit / layout.WORKFLOW_DIRNAME
    index = workflows / "workflows_index.json"
    out = workflows / WORKFLOW_ROUTER_SLUG / "SKILL.md"
    if not index.is_file() or (out.is_file() and not rewrite):
        return False
    rows = json.loads(index.read_text(encoding="utf-8"))
    if not rows:
        return False
    meta = json.loads((unit / ".claude-plugin" / "plugin.json").read_text())
    name = meta["name"]
    domain = domain_label(name, meta["description"])
    collection = {}
    if (unit / "collection.yaml").is_file():
        collection = yaml.safe_load(
            (unit / "collection.yaml").read_text(encoding="utf-8")
        ) or {}
    first = parse_frontmatter(workflows / rows[0]["slug"] / "SKILL.md")
    bound_by = {row.get("bound_by") for row in rows} - {None}
    metadata = {"kind": "workflow-router"}
    if collection.get("iri"):
        metadata["collection"] = collection["iri"]
    metadata["indexes"] = ["workflows_index.json"]
    if len(bound_by) == 1:
        metadata["bound_by"] = bound_by.pop()
    frontmatter = {
        "name": f"{name}-workflow-router",
        "description": (
            f"Use when a user has a whole {_lower_words(domain)} analysis goal "
            "rather than a single atomic step and needs an end-to-end composite "
            "workflow selected and grounded against source papers."
        ),
        "license": collection.get("license") or "CC-BY-4.0",
        "metadata": metadata,
        "schema_version": "0.3.0",
    }
    if isinstance(first.get("attribution"), dict):
        frontmatter["attribution"] = first["attribution"]
    table = "\n".join(
        f"| `{row['slug']}` | "
        f"{_workflow_summary(workflows / row['slug'] / 'SKILL.md').replace('|', '/')} |"
        for row in rows
    )
    body = WORKFLOW_ROUTER_TEMPLATE.format(
        frontmatter=yaml.safe_dump(
            frontmatter, sort_keys=False, allow_unicode=True, width=1000
        ),
        title=f"ASB {domain}",
        name=name,
        locate=LOCATE_ROOT.format(
            relative=f"{layout.WORKFLOW_DIRNAME}/{WORKFLOW_ROUTER_SLUG}"
        ),
        search=SEARCH_COMMAND,
        python_note=PYTHON_NOTE,
        skill_dir=SKILL_DIR,
        root=ROOT_FROM_SKILL,
        rows=table,
        contribution_section=contribution_section(
            {**unit_identity(unit), "has_report_helper": has_report_helper(unit)}
        ),
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(body, encoding="utf-8")
    return True


def embed_selector(script: bytes) -> bytes:
    """Replace a marked vendor block with the canonical module's exact bytes."""
    if script.count(SELECTOR_BEGIN) != 1 or script.count(SELECTOR_END) != 1:
        raise ValueError("retrieval script must contain exactly one selector block")
    before, body = script.split(SELECTOR_BEGIN)
    _, after = body.split(SELECTOR_END)
    return before + SELECTOR_BEGIN + SELECTOR_SOURCE.read_bytes() + SELECTOR_END + after


def selector_block(script: bytes) -> bytes | None:
    """The bytes between the selector markers of a script, or None without one block."""
    if script.count(SELECTOR_BEGIN) != 1 or script.count(SELECTOR_END) != 1:
        return None
    return script.split(SELECTOR_BEGIN)[1].split(SELECTOR_END)[0]


def _between(source: bytes, begin: bytes, end: bytes, label: str) -> bytes:
    if source.count(begin) != 1 or source.count(end) != 1:
        raise ValueError(f"{label} must contain exactly one {begin.decode().strip()} block")
    return source.split(begin)[1].split(end)[0]


def report_logic_blocks() -> tuple[bytes, bytes]:
    """The PII patterns and the shared report logic, as the helper vendors them.

    pii_config.py is taken whole after its future import (a second future
    import mid-file is a syntax error); skill_feedback.py between its SHARED
    REPORT LOGIC markers.
    """
    pii = PII_SOURCE.read_bytes()
    if pii.count(FUTURE_IMPORT) != 1:
        raise ValueError("pii_config.py must hold exactly one future import")
    logic = _between(FEEDBACK_SOURCE.read_bytes(), SHARED_BEGIN, SHARED_END, "skill_feedback.py")
    return pii.split(FUTURE_IMPORT, 1)[1], logic


def embed_report_logic(script: bytes) -> bytes:
    """Replace the two vendored blocks of the report helper with current sources."""
    pii, logic = report_logic_blocks()
    for begin, end, body in ((PII_BEGIN, PII_END, pii), (LOGIC_BEGIN, LOGIC_END, logic)):
        _between(script, begin, end, "report helper")
        before, rest = script.split(begin)
        _, after = rest.split(end)
        script = before + begin + body + end + after
    return script


def sync_report_helper() -> list[str]:
    """Regenerate the helper template and its package copy; return what changed."""
    generated = embed_report_logic(REPORT_HELPER.read_bytes())
    changed = []
    for path in (REPORT_HELPER, PACKAGE_REPORT_HELPER):
        if not path.is_file() or path.read_bytes() != generated:
            path.write_bytes(generated)
            changed.append(str(path))
    return changed


def write_report_helper(unit: Path) -> bool:
    """Ship the report helper in a unit's bin/; return whether it wrote.

    Only the generation of a new unit calls this. Released collections without
    the helper stay valid: their routers carry no contribution section, or one
    rendered without the helper.
    """
    out = unit / "bin" / REPORT_HELPER_NAME
    generated = embed_report_logic(REPORT_HELPER.read_bytes())
    if out.is_file() and out.read_bytes() == generated:
        return False
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(generated)
    return True


def refresh_scripts(unit: Path, keep_selector: bool = False) -> dict:
    """Regenerate standalone selectors without changing indexes or skill files.

    The collection router supplies the wrapper for technique packs. Existing
    semantic wrappers retain their embedding implementation; only their marked
    keyword selector is regenerated, and a wrapper without a marked selector
    (it imports the one of `search_skills.py`) is left as it is.

    With ``keep_selector`` the wrapper of `bin/search_skills.py` is refreshed
    around the selector block the unit already ships. A patch release uses it
    to change what a search prints without changing how a released collection
    ranks; no other script is touched.
    """
    search = unit / "bin" / "search_skills.py"
    template = SEARCH_SCRIPT.read_bytes()
    if keep_selector:
        shipped = selector_block(search.read_bytes()) if search.is_file() else None
        if shipped is None:
            raise ValueError(f"{search}: no shipped selector block to keep")
        before, body = template.split(SELECTOR_BEGIN)
        generated = {search: before + SELECTOR_BEGIN + shipped + SELECTOR_END + body.split(SELECTOR_END)[1]}
    else:
        generated = {search: embed_selector(template)}
        semantic = unit / "bin" / "semantic_search.py"
        if semantic.is_file() and selector_block(semantic.read_bytes()) is not None:
            generated[semantic] = embed_selector(semantic.read_bytes())
    updated = []
    for path, content in generated.items():
        if not path.is_file() or path.read_bytes() != content:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
            updated.append(str(path))
    return {"unit": str(unit), "updated": updated}


def shape(
    unit: Path, source_index: Path, keep: set[str], rewrite: bool = False
) -> dict:
    """Apply the whole conversion to one unit and report what changed."""
    slugs = set(leaf_slugs(unit))
    moved = move_leaves(unit, keep | {ROUTER_SLUG})
    refresh_scripts(unit)
    write_report_helper(unit)
    indexed = write_index(unit, source_index, slugs)
    write_router(unit, indexed or len(slugs), rewrite=rewrite)
    write_workflow_router(unit, rewrite=rewrite)
    return {"unit": str(unit), "moved": moved, "indexed": indexed, "leaves": len(slugs)}


def write_routers(unit: Path, rewrite: bool = False) -> dict:
    """Render the leaf and workflow routers of an already shaped unit."""
    index = unit / "skills_index.json"
    count = len(json.loads(index.read_text(encoding="utf-8"))) if index.is_file() else len(
        leaf_slugs(unit)
    )
    write_router(unit, count, rewrite=rewrite)
    wrote = write_workflow_router(unit, rewrite=rewrite)
    return {"unit": str(unit), "skills": count, "workflow_router": wrote}


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("units", nargs="*", help="unit directories to convert")
    p.add_argument("--index", help="parent skills_index.json to subset (required for conversion)")
    p.add_argument("--keep", default="", help="comma-separated slugs to keep advertised")
    p.add_argument("--scripts-only", action="store_true",
                   help="refresh vendored selectors only; do not move leaves or rewrite indexes")
    p.add_argument("--keep-selector", action="store_true",
                   help="with --scripts-only: refresh the wrapper of bin/search_skills.py around the "
                        "selector block the unit already ships (same ranking, new output)")
    p.add_argument("--routers-only", action="store_true",
                   help="render the routers of a shaped unit only; no leaf, index or script change")
    p.add_argument("--with-report-helper", action="store_true",
                   help="with --scripts-only: also ship bin/report_issue.py (next generation only)")
    p.add_argument("--check", action="store_true",
                   help="read-only: fail when a router carries a stale contribution section "
                        "(a router without one is accepted)")
    p.add_argument("--sync-report-helper", action="store_true",
                   help="regenerate scripts/templates/report_issue.py and its package copy")
    p.add_argument("--rewrite", action="store_true",
                   help="render existing routers whole (frontmatter included) instead of "
                        "refreshing stale sections")
    args = p.parse_args(argv)
    if args.sync_report_helper:
        print({"updated": sync_report_helper()})
        return 0
    if not args.units:
        p.error("at least one unit directory is required")
    if args.check:
        stale = {raw: router_contribution_findings(Path(raw)) for raw in args.units}
        for raw, routers in stale.items():
            for router in routers:
                print(f"{raw}: {router}: stale contribution section; render it with --routers-only --rewrite")
        print(f"router check: {sum(map(len, stale.values()))} stale contribution sections "
              f"in {len(stale)} units")
        return 1 if any(stale.values()) else 0
    if args.with_report_helper and not args.scripts_only:
        p.error("--with-report-helper needs --scripts-only")
    if args.scripts_only and args.routers_only:
        p.error("--scripts-only and --routers-only are exclusive")
    if args.keep_selector and not args.scripts_only:
        p.error("--keep-selector needs --scripts-only")
    if not (args.scripts_only or args.routers_only) and not args.index:
        p.error("--index is required unless --scripts-only or --routers-only is used")
    keep = {s for s in args.keep.split(",") if s}
    for raw in args.units:
        if args.scripts_only:
            print(refresh_scripts(Path(raw), keep_selector=args.keep_selector))
            if args.with_report_helper:
                print({"unit": raw, "report_helper": write_report_helper(Path(raw))})
        elif args.routers_only:
            print(write_routers(Path(raw), rewrite=args.rewrite))
        else:
            print(shape(Path(raw), Path(args.index), keep, rewrite=args.rewrite))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
