"""Signals the identity rule reads from a record, and the registry readers it relies on."""
import gzip
import pathlib
import struct
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from scripts import tool_identity as ti
from scripts.resolve_tool_licenses import load_common_words
from scripts.tool_registry_sources import read_rds_matrix


@pytest.mark.parametrize("url,key", [
    ("https://github.com/Open2C/cooler.git", "github.com/open2c/cooler"),
    ("https://github.com/sneumann/CAMERA/issues/new", "github.com/sneumann/camera"),
    ("git+https://gitlab.com/a/b", "gitlab.com/a/b"),
    ("https://github.com/biocore", None),
    ("https://www.bioconductor.org/", None),
    ("https://bioconductor.org/packages/limma", None),
    ("http://www.smallrnagroup.uni-mainz.de/software.html",
     "smallrnagroup.uni-mainz.de/software.html"),
    ('"https://github.com/Mercedeh66/mbQTL"', "github.com/mercedeh66/mbqtl"),
    ("https://github.com/computational-metabolomics/structToolbox,",
     "github.com/computational-metabolomics/structtoolbox"),
    ("https://github.com/computational-metabolomics/structToolbox, https://example.org/x",
     "github.com/computational-metabolomics/structtoolbox"),
])
def test_repo_key(url, key):
    assert ti.repo_key(url) == key


def context(text):
    return ti.RecordContext(collection="genomics", life_science=True, names=["igraph"],
                            local_text=text, skill_text="")


@pytest.mark.parametrize("text,ecosystem", [
    ("library(igraph)", "r"),
    ("suppressPackageStartupMessages(library(igraph))", "r"),
    ('BiocManager::install(c("limma", "igraph"))', "r"),
    ("igraph::cluster_louvain(g)", "r"),
    ("we used the R package igraph", "r"),
    ("import igraph as ig", "python"),
    ("from igraph import Graph", "python"),
    ("pip install --upgrade igraph", "python"),
    ("the Python library igraph", "python"),
    ("conda install -c conda-forge igraph", "conda"),
])
def test_code_evidence_binds_the_name_to_an_ecosystem(text, ecosystem):
    assert ecosystem in context(text).code_evidence()


@pytest.mark.parametrize("text", [
    "igraph was used for network analysis",
    "library(igraphx)",
    "import igraphs",
    "we import data into igraph",
])
def test_a_mention_is_not_code_evidence(text):
    assert context(text).code_evidence() == {}


def test_the_common_words_list_ships_and_holds_the_known_traps():
    words = load_common_words()
    for w in ("cooler", "gambit", "meteor", "singularity", "salmon"):
        assert w in words
    assert ti.name_is_weak("UMAP", words) and ti.name_is_weak("STAR", words)
    assert not ti.name_is_weak("Trimmomatic", words)


def _rds(columns, rows):
    """A gzip XDR serialisation of an R character matrix with column names."""
    def i(v):
        return struct.pack(">i", v)

    def chars(s):
        b = s.encode()
        return i(9 | (1 << 15)) + i(len(b)) + b  # CHARSXP

    nrow, ncol = len(rows), len(columns)
    values = [rows[r][c] for c in range(ncol) for r in range(nrow)]
    body = i(16 | (1 << 9)) + i(len(values)) + b"".join(chars(v) for v in values)
    # attributes: pairlist(dim = c(nrow, ncol), dimnames = list(NULL, columns))
    body += i(2 | (1 << 10)) + i(1) + chars("dim") + i(13) + i(2) + i(nrow) + i(ncol)
    body += i(2 | (1 << 10)) + i(1) + chars("dimnames") + i(19) + i(2) + i(254)
    body += i(16) + i(ncol) + b"".join(chars(c) for c in columns)
    body += i(254)
    return gzip.compress(b"X\n" + i(3) + i(0x040400) + i(0x030500) + i(5) + b"UTF-8" + body)


def test_the_rds_reader_reads_a_character_matrix():
    data = _rds(["Package", "License"], [["igraph", "GPL (>= 2)"], ["shiny", "MIT + file LICENSE"]])
    assert read_rds_matrix(data) == [{"Package": "igraph", "License": "GPL (>= 2)"},
                                     {"Package": "shiny", "License": "MIT + file LICENSE"}]


def test_a_perl_module_path_is_not_r_code():
    ctx = ti.RecordContext(collection="genomics", life_science=True, names=["Getopt::Long"],
                           local_text="use Getopt::Long; GetOptions(...)", skill_text="")
    assert ctx.code_evidence(["GetoptLong"]) == {}


def test_a_requirements_install_does_not_name_pip_as_a_package():
    ctx = ti.RecordContext(collection="astronomy", life_science=False, names=["pip"],
                           local_text="pip install -e . pip install -r requirements.txt",
                           skill_text="")
    assert ctx.code_evidence() == {}


def test_r_code_must_spell_the_package_with_its_case():
    ctx = ti.RecordContext(collection="metabolomics", life_science=True, names=["MeTEor"],
                           local_text="library(MeTEor)", skill_text="")
    assert ctx.code_evidence(only="meteor") == {}
    assert "r" in ctx.code_evidence(only="MeTEor")


def test_a_package_name_with_its_own_capitals_must_appear_as_written():
    ctx = ti.RecordContext(collection="genomics", life_science=True, names=["acorn"],
                           local_text="you can install the R package acorn", skill_text="")
    assert ctx.code_evidence(only="acoRn") == {}
    lower = ti.RecordContext(collection="genomics", life_science=True, names=["Splatter"],
                             local_text="generated with the R package Splatter", skill_text="")
    assert "r" in lower.code_evidence(only="splatter")


class _Reg:
    id, scope, ecosystem = "bioconductor", "life_science", "r"

    def __init__(self, repo):
        self.repo = repo

    def repo_values(self, record):
        return [self.repo] if self.repo else []

    def dois(self, record):
        return set()

    def is_data_package(self, record):
        return False

    def restricts_use(self, record):
        return False

    def text(self, record):
        return "Universal enrichment tool for interpreting omics data"

    def word_share(self, tokenize):
        return {}


def _subject_ctx():
    own = {"github.com/guangchuangyu/clusterprofiler"}
    return ti.RecordContext(collection="metagenomics", life_science=True, names=["clusterProfiler"],
                            local_text="library(clusterProfiler)", skill_text="", repos=own,
                            subject_repos=own)


def test_a_bioconductor_package_that_moved_account_is_still_the_tool():
    moved = ti.judge(_Reg("https://github.com/YuLab-SMU/clusterProfiler"), "clusterProfiler", {},
                     _subject_ctx(), frozenset())
    assert moved.accept
    other = ti.judge(_Reg("https://github.com/someone/otherpkg"), "clusterProfiler", {},
                     _subject_ctx(), frozenset())
    assert not other.accept and other.contradiction[0]["kind"] == "subject-repository"
