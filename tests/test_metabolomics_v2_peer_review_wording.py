"""Generated collection descriptions do not overstate source review status."""

import re

from scripts import collect_metabolomics_collection as collector


PEER_REVIEWED = re.compile(r"\bpeer[-\s]?reviewed\b", re.IGNORECASE)


def test_the_collector_default_description_makes_no_peer_review_claim() -> None:
    assert not PEER_REVIEWED.search(collector.COLLECTION_DESCRIPTION)
