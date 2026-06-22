---
name: corpus-preparation-validation
description: Use when when you have raw LC-MS-MS fragmentation spectra in MGF format and need to convert them into a corpus JSON file before running topic modeling.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - run_gensim.py
  - gensim
derived_from:
- doi: 10.1073/pnas.1608041113
  title: MS2LDA
evidence_spans:
- pipenv --python 2.7
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms2lda_substructure_discovery_mass2motif_cq
    doi: 10.1073/pnas.1608041113
    title: MS2LDA
  dedup_kept_from: coll_ms2lda_substructure_discovery_mass2motif_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1073/pnas.1608041113
  all_source_dois:
  - 10.1073/pnas.1608041113
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# corpus-preparation-validation

## Summary

Prepare and validate a document-term corpus from mass spectrometry fragmentation data (MS2/MGF files) into a structured JSON representation suitable for topic modeling. This skill ensures that preprocessed document-term representations are correctly formatted, complete, and ready for downstream LDA inference.

## When to use

When you have raw LC-MS-MS fragmentation spectra in MGF format and need to convert them into a corpus JSON file before running topic modeling. Apply this skill after spectrum acquisition but before LDA inference, particularly when working with metabolomics data requiring unsupervised characterization of fragment patterns.

## When NOT to use

- Input data is already in corpus JSON format or has been preprocessed into document-term vectors
- MS2 spectra lack sufficient fragmentation data or contain primarily noise, rendering topic inference unreliable
- Raw mass spectrometry data has not been subjected to baseline correction or quality filtering beforehand

## Inputs

- MGF file (MS2 fragmentation spectra in Mascot Generic Format)
- MS2 metabolomics dataset (LC-MS-MS fragmentation data)

## Outputs

- corpus JSON file (preprocessed document-term representation)
- corpus metadata (record count, feature statistics)

## How to apply

Execute the corpus generation step using the run_gensim.py script with the 'corpus' command, specifying the input MGF file format and output corpus JSON path. The script preprocesses raw MS2 fragmentation data into document-term representations where each spectrum becomes a document and fragment mass-to-charge ratios (m/z) with intensities become term weights. Validate the resulting corpus JSON file by confirming it contains properly formatted document-term pairs, that all spectra from the input MGF were successfully converted, and that term weights fall within expected intensity ranges. The corpus JSON output serves as the direct input to the gensim LDA inference step and should be inspected for structural completeness before proceeding.

## Related tools

- **run_gensim.py** (Command-line script that executes the corpus generation preprocessing step on MGF input files) — https://github.com/glasgowcompbio/ms2ldaviz
- **Python** (Runtime environment for executing the corpus preprocessing and validation workflow)
- **gensim** (Underlying library used by run_gensim.py to construct the document-term corpus representation)

## Examples

```
./run_gensim.py corpus -f mgf myexp.mgf myexp.corpus.json
```

## Evaluation signals

- Corpus JSON file is valid JSON with correct schema: array of documents, each containing term-weight pairs
- Document count in output corpus matches or is proportional to spectrum count in input MGF file
- All term weights are non-negative numeric values within expected intensity ranges for MS data
- No missing or malformed document-term entries; corpus file is readable and parseable by downstream LDA tool
- Corpus file size is reasonable relative to input MGF size (no truncation or data loss during conversion)

## Limitations

- Corpus generation quality depends on upstream MS2 data quality; low-quality spectra or artifacts will propagate into the corpus representation
- The script assumes MGF format compliance; non-standard or corrupted MGF files may fail preprocessing
- Document-term representation may lose some instrument-specific metadata (e.g., precursor m/z, retention time) that are not captured in the feature-only corpus format

## Evidence

- [intro] Generate corpus/features from MS2 file: "Performs 3 steps: 1. Generate corpus/features from MS2 file"
- [readme] Run gensim lda workflow includes corpus generation as first step: "./run_gensim.py corpus -f mgf myexp.mgf myexp.corpus.json"
- [readme] Corpus JSON file is input to LDA inference: "Load the corpus JSON file (myexp.corpus.json) containing preprocessed document-term representations"
- [intro] MS2 data used for metabolomics characterization: "topics inferred from Latent Dirichlet Allocation can be used to assist in the unsupervised characterisation of fragmented (LC-MS-MS) metabolomics data"
