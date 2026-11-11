"""A repository's own licence file, read conservatively, and compared with a registry."""
import pathlib
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from scripts import repository_licence as rl

FILES = pathlib.Path(__file__).parent / "fixtures" / "tool_licences" / "licence_files"


def text(name):
    return (FILES / name).read_text(encoding="utf-8")


@pytest.mark.parametrize("name,licence,tier", [
    ("mit.txt", "MIT", "open"),
    ("bsd3.txt", "BSD-3-Clause", "open"),
    ("bsd2.txt", "BSD-2-Clause", "open"),
    ("gpl3.txt", "GPL-3.0", "open"),
    ("gpl3_notice_or_later.txt", "GPL-3.0-or-later", "open"),
    ("lgpl21.txt", "LGPL-2.1", "open"),
    ("apache2.txt", "Apache-2.0", "open"),
    ("cc_by_nc_sa.txt", "CC-BY-NC-SA-4.0", "noncommercial"),
    ("academic_only.txt", rl.NONCOMMERCIAL_FILE, "noncommercial"),
    # Jellyfish states its choice with an SPDX line.
    ("jellyfish_dual.txt", "BSD-3-Clause OR GPL-3.0-only", "open"),
])
def test_a_licence_file_is_read_from_its_title_or_grant(name, licence, tier):
    reading = rl.classify_file(text(name))
    assert (reading["license"], reading["tier"]) == (licence, tier)


def test_the_gpl_appendix_template_is_not_an_or_later_notice():
    """The GPL prints "or (at your option) any later version" in its How to Apply section."""
    assert rl.classify_file(text("gpl3.txt"))["license"] == "GPL-3.0"


def test_a_gnu_licence_is_read_from_its_heading_not_its_body():
    """The LGPL-2.1 body speaks of "the ordinary GNU General Public License, version 2"."""
    body = text("lgpl21.txt") + "\nyou may apply the ordinary GNU General Public License, version 2\n"
    assert rl.classify_file(body)["license"] == "LGPL-2.1"


@pytest.mark.parametrize("name,reason", [
    ("mit_with_bundled_apache.txt", "several-licences"),
    ("r_mit_template.txt", "unrecognised"),
    ("bsd4.txt", "bsd-advertising-clause"),
])
def test_what_the_file_cannot_settle_is_unread(name, reason):
    reading = rl.classify_file(text(name))
    assert reading["tier"] is None and reading["reason"] == reason


def test_a_description_licence_field_is_read_with_the_r_grammar():
    reading = rl.classify_description(text("DESCRIPTION"))
    assert (reading["license"], reading["tier"]) == ("GPL-2.0-or-later", "open")


@pytest.mark.parametrize("registry,file,agree", [
    ("GPL-3.0-or-later", "GPL-3.0", True),
    ("GPL-3.0-only", "GPL-3.0-or-later", True),
    ("GPL", "GPL-2.0", True),
    ("BSD", "BSD-3-Clause", True),
    ("GPL-2.0-only OR GPL-3.0-only", "GPL-3.0", True),
    ("GPL-3.0-or-later", "MIT", False),           # STAR, Kraken2 on Bioconda
    ("GPL-3.0-only", "BSD-3-Clause", False),      # MUON on bio.tools
    ("GPL-2.0-only", "GPL-3.0", False),
    ("LGPL-3.0-only", "LGPL-2.1", False),         # MetFrag
    ("MIT", "MIT", True),
    ("GNU General Public License (GPL)", "GPL-3.0", True),   # seqmagick on Bioconda
    ("GPL-3.0-only", "GPL", True),                          # a DESCRIPTION that says GPL
])
def test_agreement_is_by_family_and_version(registry, file, agree):
    assert rl.agrees(registry, file) is agree


def test_raw_urls_are_raw_content_never_an_api():
    urls = [u for _, u in rl.raw_urls("https://github.com/scverse/muon")]
    assert urls[0] == "https://raw.githubusercontent.com/scverse/muon/HEAD/LICENSE"
    assert urls[-1].endswith("/DESCRIPTION")
    assert all("api.github.com" not in u for u in urls)
    assert rl.raw_urls("https://gitlab.com/a/b")[0][1] == "https://gitlab.com/a/b/-/raw/HEAD/LICENSE"
    assert rl.raw_urls("https://bitbucket.org/a/b") == []
    assert rl.raw_urls("http://www.smallrnagroup.uni-mainz.de/software.html") == []


# --------------------------------------------------------------------------- #
# The confirmation step, by who wrote the registry entry                      #
# --------------------------------------------------------------------------- #

import re  # noqa: E402

from scripts import resolve_tool_licenses as r  # noqa: E402
from scripts.tool_registry_sources import Fetcher  # noqa: E402


def _cache(tmp_path, repo, files):
    """A Fetcher over recorded repository files; anything not recorded is absent."""
    for name, fixture in files.items():
        url = f"raw.githubusercontent.com/{repo}/HEAD/{name}"
        key = "repofile-" + re.sub(r"[^A-Za-z0-9.]+", "_", url)
        (tmp_path / key).write_text(text(fixture) if fixture in [p.name for p in FILES.iterdir()]
                                    else fixture, encoding="utf-8")
    return Fetcher(tmp_path, offline=True)


def ev(route, licence, tier, repo):
    return {"route": f"registry:{route}", "license": licence, "license_tier": tier,
            "license_raw": licence, "license_detection": f"{route}-package",
            "license_evidence": f"https://example.org/{route}", "repo_url": f"https://github.com/{repo}",
            "matched": repo.split("/")[-1]}


def test_star_bioconda_gpl_is_replaced_by_the_repositorys_mit(tmp_path):
    f = _cache(tmp_path, "alexdobin/STAR", {"LICENSE": "mit.txt"})
    out, outcome = r.confirm(ev("bioconda", "GPL-3.0-or-later", "open", "alexdobin/STAR"), f)
    assert outcome == "replaced"
    assert (out["license"], out["license_detection"]) == ("MIT", "repository-licence-file")
    assert out["license_evidence"].endswith("/alexdobin/STAR/HEAD/LICENSE")
    assert out["confirmation"]["registry_license"] == "GPL-3.0-or-later"


def test_muon_bio_tools_gpl_is_replaced_by_the_repositorys_bsd(tmp_path):
    f = _cache(tmp_path, "scverse/muon", {"LICENSE": "bsd3.txt"})
    out, outcome = r.confirm(ev("biotools", "GPL-3.0-only", "open", "scverse/muon"), f)
    assert (outcome, out["license"]) == ("replaced", "BSD-3-Clause")


def test_a_third_party_licence_without_a_repository_statement_is_withheld(tmp_path):
    out, outcome = r.confirm(ev("bioconda", "MIT", "open", "o/none"), Fetcher(tmp_path, offline=True))
    assert out is None and outcome == "withheld-unconfirmed:no-licence-file"
    unread = _cache(tmp_path, "o/tmpl", {"LICENSE": "r_mit_template.txt"})
    out, outcome = r.confirm(ev("biotools", "MIT", "open", "o/tmpl"), unread)
    assert out is None and outcome.startswith("withheld-unconfirmed")


def test_a_third_party_open_licence_becomes_noncommercial_when_the_repository_says_so(tmp_path):
    f = _cache(tmp_path, "o/acad", {"LICENSE": "academic_only.txt"})
    out, outcome = r.confirm(ev("bioconda", "MIT", "open", "o/acad"), f)
    assert (outcome, out["license_tier"]) == ("replaced", "noncommercial")


def test_a_confirmed_licence_keeps_the_registry_reading(tmp_path):
    f = _cache(tmp_path, "o/g", {"LICENSE": "gpl3.txt"})
    out, outcome = r.confirm(ev("bioconda", "GPL-3.0-or-later", "open", "o/g"), f)
    assert (outcome, out["license"]) == ("confirmed", "GPL-3.0-or-later")
    assert out["license_detection"] == "bioconda-package"


def test_pypi_and_its_repository_in_different_tiers_leave_the_record_unknown(tmp_path):
    """MassCube: PyPI says CC BY-NC 4.0, the repository Apache-2.0."""
    f = _cache(tmp_path, "o/masscube", {"LICENSE": "apache2.txt"})
    out, outcome = r.confirm(ev("pypi", "CC-BY-NC-4.0", "noncommercial", "o/masscube"), f)
    assert out is None
    assert outcome == "withheld-contradiction:pypi=CC-BY-NC-4.0|repository=Apache-2.0"


def test_pypi_and_its_repository_in_one_tier_take_the_repository_licence(tmp_path):
    """snfpy: classifier LGPLv3, repository file GPL version 3."""
    f = _cache(tmp_path, "o/snfpy", {"LICENSE": "gpl3.txt"})
    out, outcome = r.confirm(ev("pypi", "LGPL-3.0-only", "open", "o/snfpy"), f)
    assert (outcome, out["license"]) == ("replaced", "GPL-3.0")


def test_pypi_without_a_repository_statement_is_kept(tmp_path):
    out, outcome = r.confirm(ev("pypi", "MIT", "open", "o/none"), Fetcher(tmp_path, offline=True))
    assert (outcome, out["license"]) == ("kept-unconfirmed", "MIT")


def test_bioconductor_reads_only_description_and_a_licence_file_never_overrides(tmp_path):
    """xcms: DESCRIPTION says GPL (>= 2); the LICENSE file carries a bundled component's terms."""
    f = _cache(tmp_path, "sneumann/xcms", {"LICENSE": "lgpl21.txt", "DESCRIPTION": "DESCRIPTION"})
    out, outcome = r.confirm(ev("bioconductor", "GPL-2.0-or-later", "open", "sneumann/xcms"), f)
    assert (outcome, out["license"]) == ("confirmed", "GPL-2.0-or-later")
    (tmp_path / "x").mkdir()
    only_licence = _cache(tmp_path / "x", "o/r", {"LICENSE": "lgpl21.txt"})
    out, outcome = r.confirm(ev("cran", "GPL-2.0-or-later", "open", "o/r"), only_licence)
    assert (outcome, out["license"]) == ("kept-unconfirmed", "GPL-2.0-or-later")


def test_bioconductor_withholds_only_on_a_tier_contradiction_with_description(tmp_path):
    f = _cache(tmp_path, "o/r", {"DESCRIPTION": "Package: r\nLicense: CC BY-NC 4.0\n"})
    out, outcome = r.confirm(ev("bioconductor", "MIT", "open", "o/r"), f)
    assert out is None and outcome.startswith("withheld-contradiction:bioconductor=MIT")
    (tmp_path / "y").mkdir()
    g = _cache(tmp_path / "y", "o/s", {"DESCRIPTION": "Package: s\nLicense: GPL-3\n"})
    out, outcome = r.confirm(ev("cran", "MIT", "open", "o/s"), g)
    assert (outcome, out["license"]) == ("kept-registry-declares", "MIT")


# --------------------------------------------------------------------------- #
# Added terms, the README, and the guards on a replacement                    #
# --------------------------------------------------------------------------- #

def test_a_permissive_file_with_added_terms_is_not_that_licence():
    """bmxp: "MIT License (Dual License)", a separate commercial licence for redistribution."""
    assert rl.classify_file(text("mit_dual_added_terms.txt"))["tier"] == "noncommercial"
    contact = rl.classify_file(text("mit_added_contact.txt"))
    assert (contact["tier"], contact["reason"]) == (None, "permissive-with-added-terms")


def test_added_terms_are_looked_for_outside_the_canonical_wording_only():
    # The Unlicense itself says "commercial or non-commercial".
    assert rl.classify_file(text("unlicense.txt"))["license"] == "Unlicense"
    # A copyright holder's name is not a term.
    holder = text("mit.txt").replace("[Example Author]", "Academic Medical Center")
    assert rl.classify_file(holder)["license"] == "MIT"
    # The GNU and Apache texts use these words in their own bodies.
    assert rl.classify_file(text("apache2.txt"))["license"] == "Apache-2.0"
    assert rl.classify_file(text("gpl3.txt"))["license"] == "GPL-3.0"


def test_added_terms_withhold_an_author_written_licence(tmp_path):
    f = _cache(tmp_path, "o/bmxp", {"LICENSE": "mit_dual_added_terms.txt"})
    out, outcome = r.confirm(ev("pypi", "MIT", "open", "o/bmxp"), f)
    assert out is None and outcome.startswith("withheld-added-terms:pypi=MIT")
    (tmp_path / "b").mkdir()
    g = _cache(tmp_path / "b", "o/bmxp", {"LICENSE": "mit_dual_added_terms.txt"})
    out, outcome = r.confirm(ev("bioconda", "MIT", "open", "o/bmxp"), g)
    assert (outcome, out["license_tier"]) == ("replaced", "noncommercial")
    (tmp_path / "c").mkdir()
    h = _cache(tmp_path / "c", "o/tool", {"LICENSE": "mit_added_contact.txt"})
    out, outcome = r.confirm(ev("bioconda", "MIT", "open", "o/tool"), h)
    assert out is None and outcome == "withheld-added-terms:bioconda=MIT|repository=unread"


def test_a_readme_that_restricts_use_withholds_an_open_record(tmp_path):
    """USAT: an LGPL-2.1 file, and a README "Free for all academic and educational purposes"."""
    f = _cache(tmp_path, "o/USAT", {"LICENSE": "lgpl21.txt", "README.md": "README_restricted.md"})
    out, outcome = r.confirm(ev("biotools", "LGPL-2.1-only", "open", "o/USAT"), f)
    assert out is None
    assert outcome == "withheld-readme-restriction:Free for all academic and educational purposes."


def test_a_readme_about_a_dependencys_licence_does_not_withhold(tmp_path):
    f = _cache(tmp_path, "o/tool", {"LICENSE": "mit.txt", "README.md": "README_dependency.md"})
    out, outcome = r.confirm(ev("bioconda", "MIT", "open", "o/tool"), f)
    assert outcome == "confirmed"
    assert out["confirmation"]["readme"].endswith("/o/tool/HEAD/README.md")


def test_a_readme_research_use_only_disclaimer_is_not_a_licence_term():
    assert rl.readme_restriction("For research use only. Not for use in diagnostic procedures.") is None
    assert rl.readme_restriction("This software is for academic use only.") is not None


def test_a_replacement_reads_only_a_repository_named_like_the_tool(tmp_path):
    """bootRanges: the bio.tools repository holds the paper's scripts, not the tool."""
    f = _cache(tmp_path, "o/bootRangespaper", {"LICENSE": "mit.txt"})
    record = dict(ev("biotools", "GPL-3.0-only", "open", "o/bootRangespaper"), matched="bootranges")
    out, outcome = r.confirm(record, f, tool_name="bootRanges")
    assert out is None and outcome == "withheld-repository-name:bootRangespaper"
    (tmp_path / "m").mkdir()
    g = _cache(tmp_path / "m", "o/EpiNano", {"LICENSE": "mit.txt"})
    moved = dict(ev("biotools", "GPL-2.0-only", "open", "o/EpiNano"), matched="epinano")
    out, outcome = r.confirm(moved, g, tool_name="EpiNano")
    assert (outcome, out["license"]) == ("replaced", "MIT")  # a moved repository is not seen


def test_gnu_statements_differing_only_in_version_give_the_family(tmp_path):
    """FastTree: Bioconda GPL-2.0-or-later, a GPL version 3 text in the repository."""
    f = _cache(tmp_path, "o/FastTree", {"LICENSE": "gpl3.txt"})
    out, outcome = r.confirm(ev("bioconda", "GPL-2.0-or-later", "open", "o/FastTree"), f)
    assert (outcome, out["license"], out["license_tier"]) == ("family-fallback", "GPL", "open")
    assert (out["confirmation"]["registry_license"], out["confirmation"]["file_license"]) == (
        "GPL-2.0-or-later", "GPL-3.0")
    assert rl.gnu_family("LGPL-3.0-only", "GPL-3.0") is None


def test_a_third_party_version_the_repository_does_not_state_gives_the_family(tmp_path):
    """rMSIKeyIon: bio.tools GPL-3.0, the repository's DESCRIPTION says `License: GPL`."""
    f = _cache(tmp_path, "o/rMSIKeyIon", {"DESCRIPTION": "Package: rMSIKeyIon\nLicense: GPL\n"})
    out, outcome = r.confirm(ev("biotools", "GPL-3.0-only", "open", "o/rMSIKeyIon"), f)
    assert (outcome, out["license"], out["license_tier"]) == ("family-fallback", "GPL", "open")
    assert out["confirmation"]["registry_license"] == "GPL-3.0-only"
    assert out["license_detection"] == "repository-licence-file"

    (tmp_path / "v").mkdir()
    g = _cache(tmp_path / "v", "o/versioned", {"LICENSE": "gpl3.txt"})
    out, outcome = r.confirm(ev("biotools", "GPL-3.0-only", "open", "o/versioned"), g)
    assert (outcome, out["license"]) == ("confirmed", "GPL-3.0-only")



# --------------------------------------------------------------------------- #
# Fifth pass                                                                  #
# --------------------------------------------------------------------------- #

def test_a_readme_saying_the_binary_is_closed_withholds_even_through_a_dependency(tmp_path):
    """MZA: the binary is closed-source and its libraries add restrictions on its use."""
    sentence = rl.readme_restriction(text("README_mza.md"))
    assert sentence and "closed-source code" in sentence
    f = _cache(tmp_path, "o/mza", {"LICENSE": "bsd2.txt", "README.md": "README_mza.md"})
    out, outcome = r.confirm(ev("biotools", "BSD-2-Clause", "open", "o/mza"), f)
    assert out is None and outcome.startswith("withheld-readme-restriction:")


def test_an_optional_or_third_party_dependency_with_its_own_terms_does_not_withhold():
    """A tool's tier is its own code's licence: PredPSI-SVR needs ANNOVAR, SMETANA a solver."""
    assert rl.readme_restriction(text("README_optional_solver.md")) is None
    assert rl.readme_restriction("An open alternative to closed-source software.") is None


@pytest.mark.parametrize("sentence", [
    "All software provided by the group is intended exclusively for academic research and training purposes.",
    "This software is intended only for academic use.",
    "Use is restricted to academic institutions.",
    "Free, for academic research only.",
])
def test_readme_wordings_that_restrict_use(sentence):
    assert rl.readme_restriction(sentence) == sentence


@pytest.mark.parametrize("sentence", [
    "pytorch-ranger (only for training)",
    "Widely used in academic research and industry.",
    "Supports research and teaching in many labs.",
])
def test_readme_wordings_that_do_not(sentence):
    assert rl.readme_restriction(sentence) is None


def test_calibracurve_terms_of_use_withhold():
    assert "exclusively for academic research" in rl.readme_restriction(text("README_calibracurve.md"))


def test_a_field_of_use_term_in_an_r_licence_file_withholds(tmp_path):
    """dsb: `CC0 | file LICENSE`, and the file says the software shall not be used in diagnosis."""
    f = _cache(tmp_path, "o/dsb", {"LICENSE": "dsb_license.txt"})
    record = dict(ev("cran", "CC0-1.0", "open", "o/dsb"), license_raw="CC0 | file LICENSE")
    out, outcome = r.confirm(record, f)
    assert out is None and outcome.startswith("withheld-field-of-use:")


def test_a_bundled_component_licence_file_is_not_a_field_of_use_term(tmp_path):
    """xcms: `GPL (>= 2) + file LICENSE`; the file carries a component's LGPL text."""
    f = _cache(tmp_path, "sneumann/xcms", {"LICENSE": "lgpl21.txt", "DESCRIPTION": "DESCRIPTION"})
    record = dict(ev("bioconductor", "GPL-2.0-or-later", "open", "sneumann/xcms"),
                  license_raw="GPL (>= 2) + file LICENSE")
    out, outcome = r.confirm(record, f)
    assert (outcome, out["license"]) == ("confirmed", "GPL-2.0-or-later")


class _Bioc:
    id = "bioconductor"

    def __init__(self, fetcher):
        self.fetcher = fetcher

    def repo_values(self, record):
        return []

    def dois(self, record):
        return set()


def _verdict():
    from scripts.tool_identity import Verdict
    return Verdict(True, "skill-domain-corroborated", [], [])


def _metnet_ctx():
    from scripts.tool_identity import RecordContext
    own = {"github.com/simeoni-biolab/metnet"}
    return RecordContext(collection="metabolomics", life_science=True, names=["MetNet"],
                         local_text="", skill_text="", repos=own, subject_repos=own)


def test_the_bioconductor_exception_needs_the_papers_repository_to_be_that_r_package(tmp_path):
    """MetNet: the paper's repository is a Java tool; Bioconductor's MetNet is another tool."""
    java = _cache(tmp_path, "simeoni-biolab/metnet", {"README.md": "# MetNet\nA Java tool."})
    verdict = _verdict()
    r.check_subject_exception(_Bioc(java), "MetNet", {}, _metnet_ctx(), verdict)
    assert not verdict.accept and verdict.contradiction[-1]["kind"] == "subject-repository"
    (tmp_path / "r").mkdir()
    rpkg = _cache(tmp_path / "r", "simeoni-biolab/metnet", {"DESCRIPTION": "Package: MetNet\nLicense: GPL-3\n"})
    verdict = _verdict()
    r.check_subject_exception(_Bioc(rpkg), "MetNet", {}, _metnet_ctx(), verdict)
    assert verdict.accept


def test_a_gnu_text_is_not_a_field_of_use_term():
    """IPO: `GPL (>= 2) + file LICENSE`; GPL-2.0 section 3c speaks of noncommercial distribution."""
    gpl2 = ("GNU GENERAL PUBLIC LICENSE\nVersion 2, June 1991\n\nc) Accompany it with the information "
            "you received as to the offer to distribute corresponding source code. (This alternative "
            "is allowed only for noncommercial distribution and only if you received the program in "
            "object code or executable form with such an offer, in accord with Subsection b above.)\n")
    assert rl.field_of_use(gpl2) is None
    assert rl.field_of_use(text("dsb_license.txt")).startswith("THE SOFTWARE SHALL NOT BE USED")
