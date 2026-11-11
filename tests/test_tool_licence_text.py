"""Registry licence strings read into SPDX and a tier, without inventing a version."""
import pathlib
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from scripts.license_tier import load_map
from scripts.tool_licence_text import UNVERSIONED_FAMILIES, read_licence


def read(raw, fmt="spdx_or_text"):
    out = read_licence(raw, fmt)
    return out["license"], out["tier"]


# Strings the earlier classifier mapped to the wrong version or licence.
@pytest.mark.parametrize("raw,expected", [
    ("GNU General Public License v2 (GPLv2)", "GPL-2.0-only"),
    ("GPLv2+", "GPL-2.0-or-later"),
    ("GNU General Public License v2 or later (GPLv2+)", "GPL-2.0-or-later"),
    ("LGPL 2.1 or later", "LGPL-2.1-or-later"),
    ("GNU Lesser General Public License v3 (LGPLv3)", "LGPL-3.0-only"),
    ("GPL-2.0+", "GPL-2.0-or-later"),
    ("GPL-3.0", "GPL-3.0-only"),
    ("GPLv3", "GPL-3.0-only"),
    ("GPL >=3", "GPL-3.0-or-later"),
    ("GNU General Public License v3.0", "GPL-3.0-only"),
])
def test_a_gnu_version_is_read_never_invented(raw, expected):
    assert read(raw) == (expected, "open")


@pytest.mark.parametrize("raw", ["GPL", "LGPL", "AGPL", "BSD", "BSD License",
                                 "GNU General Public License (GPL)",
                                 "GNU Library or Lesser General Public License (LGPL)"])
def test_an_unversioned_family_gets_a_tier_but_keeps_the_sources_words(raw):
    licence, tier = read(raw)
    assert tier == "open"
    assert licence == raw  # no guessed SPDX id, no invented version


def test_every_member_of_an_unversioned_family_is_open_in_the_tier_map():
    """The family rule holds only while the map lists every member as open."""
    spdx = {k.lower(): v for k, v in load_map()["spdx"].items()}
    members = {"GPL": ["gpl-2.0-only", "gpl-3.0-only", "gpl-3.0-or-later"],
               "LGPL": ["lgpl-2.0-only", "lgpl-2.1-only", "lgpl-3.0-only"],
               "AGPL": ["agpl-3.0-only", "agpl-3.0-or-later"],
               "BSD": ["bsd-2-clause", "bsd-3-clause", "bsd"]}
    assert set(members) == set(UNVERSIONED_FAMILIES.values())
    for family, ids in members.items():
        assert all(spdx[i] == "open" for i in ids), family


@pytest.mark.parametrize("raw,expected,tier", [
    ("Creative Commons Attribution Non-Commercial License V2.0", "CC-BY-NC-2.0", "noncommercial"),
    ("CC BY-NC-SA 4.0", "CC-BY-NC-SA-4.0", "noncommercial"),
    ("CC BY-NC-ND 4.0", "CC-BY-NC-ND-4.0", "noncommercial"),
    ("CC-BY-ND-4.0", "CC-BY-ND-4.0", "restricted"),
])
def test_non_commercial_and_no_derivatives_never_land_in_open(raw, expected, tier):
    assert read(raw) == (expected, tier)


@pytest.mark.parametrize("raw", ["Free for non-commercial use, see LICENSE file",
                                 "Academic and Non-Commercial Research Use",
                                 "ANNEVO Non-Commercial License",
                                 "Restricted. Free for non-commercial users."])
def test_unrecognised_non_commercial_prose_is_unread_not_open(raw):
    assert read(raw)[1] is None


# Strings that previously went unread.
@pytest.mark.parametrize("raw,fmt,expected", [
    ("BSD-3", "spdx_or_text", "BSD-3-Clause"),
    ("Apache 2.0", "spdx_or_text", "Apache-2.0"),
    ("Apache License V2.0", "spdx_or_text", "Apache-2.0"),
    ("LGPL-2", "r_description_field", "LGPL-2.0-only"),
    ("GPL-2 | GPL-3", "r_description_field", "GPL-2.0-only OR GPL-3.0-only"),
    ("Artistic-2.0-only", "spdx_or_text", "Artistic-2.0"),
    ("NCBI-PD", "spdx_or_text", "NCBI-PD"),
    ("GPL-3.0-or-later OR BSD-2-Clause", "spdx_or_text", "GPL-3.0-or-later OR BSD-2-Clause"),
    ("GPL (>= 2)", "r_description_field", "GPL-2.0-or-later"),
    ("GPL(>=2)", "r_description_field", "GPL-2.0-or-later"),
    ("LGPL (>= 2.1)", "r_description_field", "LGPL-2.1-or-later"),
    ("MIT + file LICENSE", "r_description_field", "MIT"),
    ("BSD_3_clause + file LICENSE", "r_description_field", "BSD-3-Clause"),
    ("GPL (>= 2) + file LICENSE", "r_description_field", "GPL-2.0-or-later"),
    ("GPL-3 | file LICENSE", "r_description_field", "GPL-3.0-only OR LicenseRef-file-LICENSE"),
    ("perl_5", "spdx_or_text", "Artistic-1.0-Perl OR GPL-1.0-or-later"),
    ("(MIT OR Apache-2.0)", "spdx_or_text", "MIT OR Apache-2.0"),
    ("Mozilla Public License 2.0 (MPL 2.0)", "spdx_or_text", "MPL-2.0"),
    ("GPL-3.0-or-later AND LGPL-3.0-or-later", "spdx_or_text",
     "GPL-3.0-or-later AND LGPL-3.0-or-later"),
])
def test_licence_grammar(raw, fmt, expected):
    assert read(raw, fmt) == (expected, "open")


@pytest.mark.parametrize("raw,fmt", [
    ("file LICENSE", "r_description_field"),
    ("Artistic-2.0 + file LICENSE", "r_description_field"),  # the file may restrict
    ("Varies; see https://genome.ucsc.edu/license", "spdx_or_text"),
    ("Apache Software License", "spdx_or_text"),  # Apache 1.x is not in the tier map
    ("GPL (> 2)", "r_description_field"),
    ("Custom", "spdx_or_text"),
    ("Other", "spdx_or_text"),
    ("GNU", "spdx_or_text"),
    ("", "spdx_or_text"),
    (None, "spdx_or_text"),
    ("MIT AND see the enclosed terms", "spdx_or_text"),
])
def test_what_cannot_be_read_stays_unread(raw, fmt):
    assert read(raw, fmt)[1] is None


def test_an_or_takes_the_most_permissive_read_choice():
    assert read("CC BY-NC 4.0 | GPL-3", "r_description_field")[1] == "open"
    assert read("CC BY-NC 4.0 | file LICENSE", "r_description_field")[1] is None


def test_an_and_takes_the_most_restrictive_part():
    assert read("MIT AND CC-BY-NC-4.0")[1] == "noncommercial"


def test_the_raw_string_is_kept():
    assert read_licence("GPLv2+")["raw"] == "GPLv2+"
