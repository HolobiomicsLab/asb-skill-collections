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
