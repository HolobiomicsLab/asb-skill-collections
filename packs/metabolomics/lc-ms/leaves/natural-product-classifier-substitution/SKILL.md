---
name: natural-product-classifier-substitution
description: Use when gNPS has ceased supplying ClassyFire ontology information for spectral library matches, causing downstream ConCISE consensus classification to fail or produce incomplete ontology fields.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3674
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - NPClassifier
  - SIRIUS
  - GNPS
  - ClassyFire
  - ConCISE
  techniques:
  - LC-MS
derived_from:
- doi: 10.3390/metabo12121275
  title: ConCISE
evidence_spans:
- use NPClassifier instead of ClassyFire by checking the box in the GUI
- ConCISE utlizes the structural annotations provided by in silico tools such as [SIRIUS]
- Currently GNPS has stopped supplying classyfire ontology information for spectral library matches
- Currently GNPS has stopped supplying classyfire ontology information for spectral library matches.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_concise_cq
    doi: 10.3390/metabo12121275
    title: ConCISE
  dedup_kept_from: coll_concise_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3390/metabo12121275
  all_source_dois:
  - 10.3390/metabo12121275
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# natural-product-classifier-substitution

## Summary

Substitute NPClassifier for ClassyFire ontology assignments in ConCISE when GNPS ClassyFire ontology data is unavailable. This workaround enables consensus classification of natural products using an alternative taxonomic backbone while maintaining compatibility with existing ConCISE workflows.

## When to use

GNPS has ceased supplying ClassyFire ontology information for spectral library matches, causing downstream ConCISE consensus classification to fail or produce incomplete ontology fields. Apply this skill when: (1) your GNPS DBResult file lacks ClassyFire superclass/class/subclass columns, (2) you have in silico structural annotations from SIRIUS or CANOPUS, and (3) you need valid consensus classifications but cannot manually retrieve ClassyFire data from the Fiehn Labs batch tool.

## When NOT to use

- ClassyFire ontology data is already available from GNPS or has been manually retrieved from the Fiehn Labs batch tool and merged into your input file — use standard ClassyFire mode instead.
- Your input annotations lack any structural information (InChIKey, SMILES, or InChI) required by NPClassifier to generate predictions.
- You require exact ClassyFire ontology compliance for downstream standardization or publication — NPClassifier and ClassyFire taxonomies are not bijective and may assign different superclass/class/subclass labels to the same compound.

## Inputs

- GNPS task ID or spectral library match file (CSV/TSV with structural annotations and optional ClassyFire columns)
- Canopus_summary.tsv file from SIRIUS or CANOPUS in silico predictions
- Node_info.tsv file from GNPS feature-based molecular networking

## Outputs

- Consensus classification file with NPClassifier-derived superclass, class, and subclass assignments
- Consensus confidence metrics (percent agreement at each taxonomic level)

## How to apply

Toggle the NPClassifier (NPC) argument from False to True in the ConCISE command-line interface, or check the corresponding NPClassifier box in the graphical user interface. This substitution redirects ConCISE to derive taxonomic ontologies from NPClassifier instead of ClassyFire for both library spectral matches and in silico putative annotations. Run the classification step on structural annotations; ConCISE will generate consensus output using NPClassifier-derived superclass, class, and subclass fields. Verify that ClassyFire is no longer invoked in the logs and that output consensus files contain NPClassifier ontology assignments with no null values in taxonomic columns. Compare consensus confidence or coverage metrics (e.g., number of compounds reaching the specified percent consensus thresholds) against archived ClassyFire-based runs to validate ontology coverage.

## Related tools

- **NPClassifier** (Alternate natural product taxonomy predictor; replaces ClassyFire ontology assignments when GNPS data is unavailable)
- **ClassyFire** (Primary natural product ontology classifier; substituted by NPClassifier when GNPS supply chain fails)
- **SIRIUS** (Generates in silico structural annotations and MS fragmentation interpretation for input to ConCISE) — https://bio.informatik.uni-jena.de/software/
- **GNPS** (Provides spectral library matches and feature-based molecular networking data; source of ClassyFire ontologies (when available)) — https://gnps.ucsd.edu/ProteoSAFe/static/gnps-splash.jsp
- **ConCISE** (Consensus classification engine; implements NPClassifier substitution via NPC toggle argument) — https://github.com/Zquinlan/conCISE

## Examples

```
python3 src/conciseCLI.py 16616afa8edd490ea7e50cc316a20222 exampleFiles/canopus_summary.tsv exampleFiles/Node_info.tsv 50 70 70 True
```

## Evaluation signals

- Output consensus file contains NPClassifier-derived values in superclass, class, and subclass columns with no null entries for successfully classified compounds.
- Comparison of consensus coverage: tally the number of compounds reaching the specified percent consensus thresholds (default: 50% superclass, 70% class, 70% subclass) and verify non-zero consensus counts in at least 80% of input features.
- Log or stdout output confirms 'NPC=True' or 'Using NPClassifier' is active and does not invoke ClassyFire API calls.
- Consensus scores (calculated as the percentage of contributing annotations agreeing on a taxonomic label) are computed and reported for each compound; verify scores are in the range [0, 100] and match the specified thresholds.
- Spot-check 5–10 output compound records against NPClassifier web predictions using their InChIKey or SMILES to confirm ontology assignments are plausible.

## Limitations

- NPClassifier and ClassyFire use distinct ontology hierarchies and may assign different superclass/class/subclass labels to the same compound, limiting direct comparability with archived ClassyFire-based workflows.
- NPClassifier performance depends on the quality and structural completeness of input annotations; compounds with ambiguous or incomplete SMILES/InChIKey records may receive lower confidence or no predictions.
- ConCISE requires both GNPS network topology (Node_info.tsv) and CANOPUS/SIRIUS in silico predictions; if either input is missing or malformed, the substitution does not recover consensus classification for those features.
- No changelog is publicly available; version history and bug fixes for NPClassifier integration may not be fully documented.

## Evidence

- [readme] Currently GNPS has stopped supplying classyfire ontology information for spectral library matches: "Currently GNPS has stopped supplying classyfire ontology information for spectral library matches"
- [readme] use NPClassifier instead of ClassyFire by checking the box in the GUI or changing the NPC argument from False to True: "use NPClassifier instead of ClassyFire by checking the box in the GUI or changing the NPC argument from False to True"
- [readme] Use NPClassifier in place of ClassyFire Ontologies (True or False; e.g., 'True' will utilize NPClassifier ontologies for both library matches and in silico matches): "Use NPClassifier in place of ClassyFire Ontologies (True or False; e.g., 'True' will utilize NPClassifier ontologies for both library matches and in silico matches)"
- [readme] ConCISE works by finding consensus annotations of putative annotations using the ClassyFire ontologies which are supplied by GNPS for library spectral matches and in silico putative annotations: "ConCISE works by finding consensus annotations of putative annotations using the ClassyFire ontologies which are supplied by GNPS for library spectral matches and in silico putative annotations"
- [other] NPClassifier is offered as a validated workaround when ClassyFire ontology information is unavailable, accessible by toggling the NPC argument from False to True or checking the corresponding GUI box: "NPClassifier is offered as a validated workaround when ClassyFire ontology information is unavailable, accessible by toggling the NPC argument from False to True or checking the corresponding GUI box"
