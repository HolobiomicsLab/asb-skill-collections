---
name: chemical-classification-scheme-validation
description: Use when you have structural annotations from in silico tools (SIRIUS,
  CANOPUS) and spectral library matches from GNPS, but need to (1) reconcile conflicting
  or incomplete ClassyFire ontology assignments, or (2) substitute NPClassifier taxonomy
  when ClassyFire ontology data is unavailable from GNPS.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3280
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3391
  tools:
  - NPClassifier
  - SIRIUS
  - GNPS
  - ClassyFire
  - ConCISE
  - Fiehn Labs ClassyFire Batch
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.3390/metabo12121275
  title: ConCISE
evidence_spans:
- use NPClassifier instead of ClassyFire by checking the box in the GUI
- ConCISE utlizes the structural annotations provided by in silico tools such as [SIRIUS]
- Currently GNPS has stopped supplying classyfire ontology information for spectral
  library matches
- Currently GNPS has stopped supplying classyfire ontology information for spectral
  library matches.
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

# chemical-classification-scheme-validation

## Summary

Validate and generate consensus chemical classifications from structural annotations by reconciling multiple ontology sources (ClassyFire or NPClassifier) with configurable agreement thresholds. This skill addresses the practical challenge of assigning reliable chemical taxonomy labels when primary ontology data sources (e.g., GNPS ClassyFire) become unavailable.

## When to use

Apply this skill when you have structural annotations from in silico tools (SIRIUS, CANOPUS) and spectral library matches from GNPS, but need to (1) reconcile conflicting or incomplete ClassyFire ontology assignments, or (2) substitute NPClassifier taxonomy when ClassyFire ontology data is unavailable from GNPS. Typical trigger: GNPS has stopped supplying ClassyFire ontology information for your spectral library matches.

## When NOT to use

- Input does not include structural annotations or ontology labels (e.g., raw mass spectra without in silico predictions or library matches).
- You require the original ClassyFire ontology data and have access to the Fiehn Labs batch tool or archived GNPS data—manual curation may be more reliable than substitution.
- Consensus thresholds are not scientifically justified for your analysis; low-confidence multi-source agreement may introduce more noise than value.

## Inputs

- GNPS task ID or spectral library match file with library annotations
- Canopus_summary.tsv file with in silico structural predictions
- Node_info.tsv or equivalent molecular networking metadata
- InChIKey identifiers (for optional manual ClassyFire batch lookup via Fiehn Labs)

## Outputs

- Consensus classification file with superclass, class, and subclass assignments
- Per-compound consensus confidence metrics (percent agreement at each ontology level)
- Classification output indicating which ontology source (ClassyFire or NPClassifier) was used

## How to apply

Load structural annotations (InChIKeys, SMILES, or compound identifiers) from GNPS library matches and in silico predictions into ConCISE. Configure the classification ontology source by toggling the NPC argument (False for ClassyFire, True for NPClassifier) or via the GUI checkbox. Set consensus thresholds for each ontology level (default: 50% for superclass, 70% for class and subclass). Run the classification workflow to compute agreement across all source annotations, generating a consensus classification output where only assignments meeting the specified threshold are retained. Verify that non-consensus or below-threshold assignments are flagged or excluded, allowing downstream prioritization of high-confidence structural assignments.

## Related tools

- **SIRIUS** (Provides structural annotations and in silico predictions used as input to ConCISE classification consensus) — https://bio.informatik.uni-jena.de/software/
- **ClassyFire** (Primary ontology source for chemical taxonomy assignment; substituted by NPClassifier when unavailable)
- **NPClassifier** (Alternative validated ontology source toggled via NPC argument when ClassyFire data is unavailable)
- **GNPS** (Source of spectral library matches and ClassyFire ontology annotations; currently no longer supplies ClassyFire data) — https://gnps.ucsd.edu/ProteoSAFe/static/gnps-splash.jsp
- **ConCISE** (Main workflow tool that reconciles and generates consensus chemical classifications) — https://github.com/Zquinlan/conCISE
- **Fiehn Labs ClassyFire Batch** (Optional manual lookup tool to retrieve ClassyFire taxonomy for InChIKeys when GNPS data is absent) — https://cfb.fiehnlab.ucdavis.edu/

## Examples

```
python3 src/conciseCLI.py 16616afa8edd490ea7e50cc316a20222 exampleFiles/canopus_summary.tsv exampleFiles/Node_info.tsv 50 70 70 True
```

## Evaluation signals

- Consensus output file contains superclass, class, and subclass columns with no null values where threshold was met.
- Percent-agreement metrics at each ontology level are ≥ the configured thresholds (default 50% superclass, 70% class/subclass).
- ClassyFire is no longer invoked in the ConCISE run log when NPC argument is True; NPClassifier ontologies appear in output.
- Comparison of consensus confidence between NPClassifier and archived ClassyFire runs (if available) shows agreement or expected divergence due to ontology differences.
- Below-threshold assignments are either excluded or explicitly flagged in output; no ambiguous or partial consensus labels appear without annotation.

## Limitations

- NPClassifier and ClassyFire use different ontology hierarchies; direct comparison or merging of their classifications may require manual curation or intermediate mapping.
- Consensus accuracy depends on the quality and diversity of input structural annotations; if all sources are derived from the same tool or contain systematic errors, consensus may be false confidence.
- Manual workaround using Fiehn Labs batch lookup is labor-intensive for large datasets and requires reformatting column names (superclass, class, subclass) in the GNPS output file.
- ConCISE GUI for macOS is deprecated; only CLI and MyBinder interfaces are currently functional on Mac, limiting ease of use.

## Evidence

- [readme] Currently GNPS has stopped supplying classyfire ontology information for spectral library matches: "Currently GNPS has stopped supplying classyfire ontology information for spectral library matches"
- [readme] use NPClassifier instead of ClassyFire by checking the box in the GUI or changing the NPC argument from False to True: "use NPClassifier instead of ClassyFire by checking the box in the GUI or changing the NPC argument from False to True"
- [readme] ConCISE works by finding consensus annotations of putative annotations using the ClassyFire ontologies which are supplied by GNPS for library spectral matches and in silico putative annotations: "ConCISE works by finding consensus annotations of putative annotations using the ClassyFire ontologies"
- [readme] Superclass percent consensus (optional; default = 50), Class percent consensus (optional; default = 70), Subclass percent consensus (optional; default = 70): "Superclass percent consensus (optional; default = 50), Class percent consensus (optional; default = 70), Subclass percent consensus (optional; default = 70)"
- [readme] You can copy the InChiKey's from the GNPS DBResult file into the Fiehn Labs' classyfire Batch identifier. Once these results are merged back into the original GNPS DBResult file with the correct column names (i.e. superclass, class, subclass), you can use this file in place of the libraryID: "You can copy the InChiKey's from the GNPS DBResult file into the Fiehn Labs' classyfire Batch identifier"
