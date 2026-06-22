---
name: chemical-ontology-mapping
description: Use when your analysis has produced both in silico structural predictions (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3520
  tools:
  - SIRIUS
  - NPClassifier
  - GNPS
  - CANOPUS
  - ClassyFire
  - ConCISE
  techniques:
  - LC-MS
derived_from:
- doi: 10.3390/metabo12121275
  title: ConCISE
evidence_spans:
- ConCISE utlizes the structural annotations provided by in silico tools such as [SIRIUS]
- use NPClassifier instead of ClassyFire by checking the box in the GUI
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# chemical-ontology-mapping

## Summary

Reconcile structural annotations from in silico tools (SIRIUS, CANOPUS) with library match ontology classifications (ClassyFire or NPClassifier) to assign a single canonical chemical classification per spectral feature. This skill applies a consensus algorithm to resolve conflicting classifications when multiple sources rank the same compound differently.

## When to use

Your analysis has produced both in silico structural predictions (e.g., from SIRIUS output with CANOPUS summary) and spectral library match results (from GNPS or manual ClassyFire batch retrieval) that each carry chemical class annotations, and you need a single authoritative classification per feature for downstream chemical interpretation or reporting.

## When NOT to use

- You have only in silico annotations and no library spectral match data; consensus requires at least two independent classification sources to be meaningful.
- Your spectral library matches lack any ontology enrichment (no ClassyFire or NPClassifier columns) and you cannot retrieve them; ConCISE requires parsed ontology data as input.
- You need to preserve all candidate annotations rather than collapse to a single canonical class per feature; ConCISE is designed to produce a single consensus output, not a ranked list.

## Inputs

- SIRIUS structural annotations file
- CANOPUS summary table (.tsv)
- GNPS library match result file (DBResult) with ontology columns or manually enriched file
- Networking info file (e.g., Node_info.tsv from feature-based molecular networking)
- Optional: GNPS task ID for direct data retrieval

## Outputs

- Consensus classification table mapping each spectral feature to canonical superclass, class, and subclass
- Feature-to-classification mapping suitable for network annotation or chemical reporting

## How to apply

Load the in silico structural annotations (SIRIUS output + CANOPUS summary) and library match ontology data (ClassyFire or NPClassifier classifications from GNPS DBResult or Fiehn Labs batch retrieval). Normalize structural candidate identifiers and their associated chemical classifications across both sources. Apply ConCISE's consensus classification algorithm, which reconciles multiple ontology assignments by voting at superclass, class, and subclass levels using configurable percent-consensus thresholds (default: 50% superclass, 70% class, 70% subclass). Select the highest-confidence chemical classification per feature and output a consensus mapping table. If GNPS ontology data is unavailable, manually retrieve ClassyFire classifications from InChiKeys via the Fiehn Labs batch tool and merge results back into the GNPS DBResult file with correct column names (superclass, class, subclass) before consensus processing.

## Related tools

- **SIRIUS** (Provides in silico structural predictions and candidate annotations for consensus input) — https://bio.informatik.uni-jena.de/software/
- **CANOPUS** (Generates chemical ontology predictions paired with SIRIUS structural candidates)
- **ClassyFire** (Source of chemical class ontologies for both library matches and in silico candidates; can be queried via Fiehn Labs batch tool when GNPS supply is unavailable) — https://cfb.fiehnlab.ucdavis.edu/
- **NPClassifier** (Alternative ontology source to ClassyFire; selected via GUI checkbox or CLI argument)
- **GNPS** (Supplies library spectral matches and their associated ClassyFire ontology annotations; currently deprecated for new ontology data but historical GNPS task IDs can be queried directly) — https://gnps.ucsd.edu/ProteoSAFe/static/gnps-splash.jsp
- **ConCISE** (Core consensus classification reconciliation tool; implements voting algorithm across superclass, class, and subclass levels) — https://github.com/Zquinlan/conCISE

## Examples

```
python3 src/conciseCLI.py 16616afa8edd490ea7e50cc316a20222 exampleFiles/canopus_summary.tsv exampleFiles/Node_info.tsv 50 70 70 False
```

## Evaluation signals

- Every spectral feature (row) in the output consensus table has exactly one superclass, class, and subclass assignment—no null or multi-valued cells.
- Consensus classifications align with the dominant (highest-voted) ontology assignment from input sources when thresholds are met; spot-check 5–10 features by inspecting their source votes.
- If GNPS data was manually enriched via Fiehn Labs batch, verify that the merged DBResult file has correct column names (superclass, class, subclass) matching input ontology structure before consensus processing.
- For features where consensus threshold is not met (e.g., tied vote), ConCISE outputs indicate how many sources agreed at each taxonomic level; review these flags to identify low-confidence features.
- Output classification distribution (superclass proportions, class/subclass entropy) should reflect expected chemical diversity of the sample; extreme skew may indicate parameter mistuning or input data quality issues.

## Limitations

- GNPS has stopped supplying ClassyFire ontology information for spectral library matches; manual retrieval via Fiehn Labs batch is required as a workaround, which is labor-intensive for large libraries.
- Consensus voting depends on configurable percent thresholds (default 50% superclass, 70% class/subclass); no universal threshold recommendation is provided—users must tune per dataset or validate against ground truth.
- ConCISE requires both in silico annotations and library match data; it cannot operate on a single source alone, limiting its use to datasets where both pipelines have been executed.
- Chemical classification conflicts between sources (e.g., ClassyFire vs. NPClassifier assign different superclasses) are resolved by voting, not by comparative evaluation of evidence quality, so systematic bias in one source can propagate to consensus.
- Mac GUI is deprecated; Mac users must use command-line interface or MyBinder virtual environment, reducing accessibility.

## Evidence

- [other] ConCISE operates by taking structural annotations from in silico tools like SIRIUS and integrating them with ontology classification data (from ClassyFire or NPClassifier) supplied via library matches: "ConCISE operates by taking structural annotations from in silico tools like SIRIUS and integrating them with ontology classification data (from ClassyFire or NPClassifier) supplied via library matches"
- [readme] ConCISE works by finding consensus annotations of putative annotations using the ClassyFire ontologies which are supplied by GNPS for library spectral matches and in silico putative annotations.: "ConCISE works by finding consensus annotations of putative annotations using the ClassyFire ontologies which are supplied by GNPS for library spectral matches and in silico putative annotations."
- [other] Apply ConCISE's consensus classification algorithm to reconcile multiple classification sources and select the dominant or highest-confidence chemical class per spectral feature.: "Apply ConCISE's consensus classification algorithm to reconcile multiple classification sources and select the dominant or highest-confidence chemical class per spectral feature."
- [readme] Currently GNPS has stopped supplying classyfire ontology information for spectral library matches. There are two workarounds: 1) use NPClassifier instead of ClassyFire by checking the box in the GUI or 2) Manually pull classyfire data for your library match data.: "Currently GNPS has stopped supplying classyfire ontology information for spectral library matches. There are two workarounds: 1) use NPClassifier instead of ClassyFire by checking the box in the GUI"
- [readme] You can copy the InChiKey's from the GNPS DBResult file into the Fiehn Labs' classyfire Batch identifier. Once these results are merged back into the original GNPS DBResult file with the correct column names (i.e. superclass, class, subclass), you can use this file in place of the libraryID.: "You can copy the InChiKey's from the GNPS DBResult file into the Fiehn Labs' classyfire Batch identifier. Once these results are merged back with correct column names (superclass, class, subclass),"
- [readme] Superclass percent consensus (optional; default = 50), Class percent consensus (optional; default = 70), Subclass percent consensus (optional; default = 70): "Superclass percent consensus (optional; default = 50), Class percent consensus (optional; default = 70), Subclass percent consensus (optional; default = 70)"
