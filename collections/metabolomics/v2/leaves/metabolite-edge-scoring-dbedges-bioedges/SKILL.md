---
name: metabolite-edge-scoring-dbedges-bioedges
description: Use when you have a measured m/z value from spatially-resolved metabolomics
  or mass spectrometry imaging and need to assign a molecular formula with high confidence.
  Use it specifically when you have access to a pre-constructed formula network (KnownSet
  database) linking 2.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3801
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0769
  tools:
  - SMART
  techniques:
  - LC-MS
  - MS-imaging
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.4c06210
  title: SMART
evidence_spans:
- we present SMART, an open-source platform designed for precise formula assignment
  in mass spectrometry imaging
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_smart_cq
    doi: 10.1021/acs.analchem.4c06210
    title: SMART
  dedup_kept_from: coll_smart_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c06210
  all_source_dois:
  - 10.1021/acs.analchem.4c06210
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-edge-scoring-dbedges-bioedges

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Score candidate molecular formulae for a given m/z value by quantifying their connectivity within a formula network using database edges (DBEdges) and biological edges (BioEdges) as strength-of-evidence criteria. This skill ranks formula candidates in spatially-resolved mass spectrometry imaging by combining network topology with mass accuracy, improving annotation precision over LC-MS approaches.

## When to use

Apply this skill when you have a measured m/z value from spatially-resolved metabolomics or mass spectrometry imaging and need to assign a molecular formula with high confidence. Use it specifically when you have access to a pre-constructed formula network (KnownSet database) linking 2.8 million formulae via DBEdges (HMDB, ChEMBL, PubChem) and BioEdges (KEGG), and when formula candidates have been extracted but require ranking by their strength of association rather than mass accuracy alone.

## When NOT to use

- Input is already a validated feature table with confirmed annotations; scoring is redundant.
- No pre-built formula network (KnownSet database) is available or feasible to construct for your molecular domain.
- Formula candidates have not yet been extracted from the database; use extraction/regression step first.

## Inputs

- m/z value (decimal number, e.g. 185.9934)
- ion polarity (+, -, or 0 for neutral)
- KnownSet database file (smart.db) comprising 2.8 million interconnected formulae
- trained multiple linear regression model (e.g. lr_4f.pkl)
- PPM tolerance threshold (default 5)

## Outputs

- ranked table of candidate formulae
- scores for each candidate based on linked formulae count, DBEdges/BioEdges strength, and PPM accuracy
- confidence metrics per candidate
- database source annotations (H=HMDB, E=ChEMBL, P=PubChem)

## How to apply

For a given m/z value, first extract candidate formulae within a specified PPM tolerance (default 5 ppm) using a multiple linear regression model applied to the KnownSet database. Then score each candidate formula using three weighted criteria: (1) the number and strength of linked formulae connections within the formula network, (2) the type and count of DBEdges (chemical relationship evidence from HMDB, ChEMBL, PubChem) and BioEdges (metabolic pathway evidence from KEGG) connecting the candidate to other formulae, and (3) mass accuracy expressed as PPM deviation from the input m/z. Rank candidates by composite regression score and return ranked results with confidence metrics. This approach leverages the rationale that true metabolites are more densely connected in chemical and biological networks than spurious mass matches.

## Related tools

- **SMART** (platform housing the multiple linear regression model, KnownSet database, and scoring algorithm for formula assignment in mass spectrometry imaging) — https://github.com/bioinfo-ibms-pumc/SMART

## Examples

```
python SMART.py -i 185.9934 -d smart.db -l lr_4f.pkl -p 0 -m 5
```

## Evaluation signals

- Verify that all returned candidate formulae fall within the specified PPM tolerance of the input m/z value.
- Confirm that candidates are ranked in descending order of regression score (highest-confidence formulae first).
- Check that each candidate carries at least one valid DBEdge or BioEdge annotation from HMDB, ChEMBL, PubChem, or KEGG; candidates with zero network connections should score lowest.
- Validate that PPM values are calculated correctly: (observed m/z − theoretical m/z) / theoretical m/z × 1,000,000 ≤ threshold.
- Benchmarking on reference datasets should show precision comparable to or better than LC-MS-based annotation approaches (precision metric from article).

## Limitations

- Accuracy depends on the completeness and currency of the KnownSet database (HMDB, ChEMBL, PubChem, KEGG); missing or outdated formulae and edges will reduce sensitivity.
- The raw SMART database exceeds 1 Terabyte; users must either request the full version from authors or use the temporary HMDB-only version, which limits coverage to HMDB-indexed formulae.
- Multiple linear regression model weights (lr_4f.pkl) were trained on specific reference datasets; generalization to novel m/z ranges or tissue types is not characterized.
- Scoring does not account for isotope patterns, adduct formation, or in-source fragmentation; input m/z must already represent intact molecular ions or known adducts.

## Evidence

- [readme] By employing a multiple linear regression model, SMART extracts formula networks associated with the m/z of interest and scores potential candidates based on various criteria, including linked formulae, DBEdges/BioEdges, and PPMs ppms values.: "scores potential candidates based on various criteria, including linked formulae, DBEdges/BioEdges, and PPMs ppms values"
- [readme] SMART constructs a KnownSet database that comprise 2.8 million formulae interconnected by DBEdges sourced from repositories such as HMDB, ChEMBL, PubChem, and BioEdges from KEGG biological reactant pairs.: "2.8 million formulae interconnected by DBEdges sourced from repositories such as HMDB, ChEMBL, PubChem, and BioEdges from KEGG"
- [readme] Spatially-resolved metabolomics plays a critical role in unraveling tissue-specific metabolic complexities. Despite significance, this profound technology generates thousands of features, the accurate annotation of which lags notably behind LC-MS based approaches.: "accurate annotation of which lags notably behind LC-MS based approaches"
- [readme] PPM threshold for formula assignment (Default: 5).: "PPM threshold for formula assignment (Default: 5)"
- [readme] Benchmarking on reference datasets demonstrates SMART is able to predict the formulae with a desirable precision.: "Benchmarking on reference datasets demonstrates SMART is able to predict the formulae with a desirable precision"
