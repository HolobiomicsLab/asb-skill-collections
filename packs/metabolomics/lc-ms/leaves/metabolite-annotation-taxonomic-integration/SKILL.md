---
name: metabolite-annotation-taxonomic-integration
description: Use when you have paired metabolomics data (MS/MS spectra and feature quantification) linked to organismal or tissue taxonomy, and you want to reduce false positive annotations and improve annotation rank by filtering candidate metabolites to those chemically plausible within the given taxon.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3860
  edam_topics:
  - http://edamontology.org/topic_0639
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0154
  tools:
  - R
  - tima (R package)
  - LOTUS
  - SIRIUS v5/v6
  - GNPS
  - Spectra (R package)
  techniques:
  - LC-MS
derived_from:
- doi: 10.3389/fpls.2019.01329
  title: tima
evidence_spans:
- The initial work is available at <https://doi.org/10.3389/fpls.2019.01329>
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_tima
    doi: 10.3389/fpls.2019.01329
    title: tima
  dedup_kept_from: coll_tima
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3389/fpls.2019.01329
  all_source_dois:
  - 10.3389/fpls.2019.01329
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-annotation-taxonomic-integration

## Summary

Integrate taxonomic metadata with mass spectrometry spectral data to improve metabolite annotation confidence by constraining candidate compound lists to those known to occur in the sampled organism or tissue. This skill leverages structure-organism pairing libraries (e.g. LOTUS) and spectral databases to perform taxonomically informed metabolite identification.

## When to use

Apply this skill when you have paired metabolomics data (MS/MS spectra and feature quantification) linked to organismal or tissue taxonomy, and you want to reduce false positive annotations and improve annotation rank by filtering candidate metabolites to those chemically plausible within the given taxon. Use it after spectral preprocessing and before or during spectral library matching.

## When NOT to use

- Input is already a fully annotated feature table with high-confidence compound identifications — re-running annotation is redundant.
- Sample metadata lacks organism or tissue taxonomy information — taxonomic filtering cannot be applied and the skill offers no advantage over non-taxonomic annotation.
- Only raw mass spectrometry data (mzML/mzXML) is available without prior feature extraction and quantification.

## Inputs

- Feature quantification table (CSV/TSV format with columns: feature ID, retention time, m/z, sample intensities)
- MS/MS spectra file (MGF format) — fragment spectra for features
- Sample metadata table (CSV/TSV) — maps samples to organism taxa
- Optional: SIRIUS v5/v6 output files (.zip) for structure prediction
- Optional: GNPS-FBMN results for spectral networking

## Outputs

- Annotated feature table with compound IDs, names, and confidence scores
- Intermediate spectral matching results (cosine similarity scores)
- Taxonomically filtered candidate compound lists per feature
- Annotation report with method and citation guidance

## How to apply

Obtain or prepare three core inputs: (1) a feature quantification table (CSV/TSV with feature ID, retention time, m/z, and sample intensities), (2) MS/MS spectra in MGF format for each or a subset of features, and (3) sample metadata linking samples to organism taxa (CSV/TSV). Install the tima R package and validate input file structure using tima::validate_inputs(), confirming required columns are present and metadata taxa are consistent. Execute the canonical tima workflow via tima::run_app() or command-line interface, which integrates the provided spectral data, chemical properties, and structure-organism knowledge (defaulting to the LOTUS library with >650k organism-metabolite pairs). The workflow scores and ranks candidate annotations by matching observed spectra against spectral libraries and chemical databases while filtering candidates by organism/tissue taxonomy. Validate completion by confirming all expected output files are generated with appropriate content structure and annotation confidence metrics.

## Related tools

- **tima (R package)** (Core workflow engine: orchestrates feature validation, spectral matching, taxonomic filtering, and annotation ranking using integrated knowledge bases) — https://github.com/taxonomicallyinformedannotation/tima
- **LOTUS** (Default structure-organism pairing library (>650k pairs) used to filter candidate metabolites by taxon) — https://lotusnprod.github.io/lotus-manuscript/
- **SIRIUS v5/v6** (Optional external tool for in silico structure prediction and molecular formula scoring to improve candidate ranking)
- **GNPS** (Optional external spectral networking and annotation source to augment spectral matching results)
- **Spectra (R package)** (Backend library for reading and processing MS/MS spectra (MGF format))

## Examples

```
tima::validate_inputs(features='data/example_features.csv', spectra='data/example_spectra.mgf', metadata='data/example_metadata.tsv', feature_col='row ID', filename_col='filename', organism_col='ATTRIBUTE_species'); tima::run_app()
```

## Evaluation signals

- All intermediate annotation outputs are generated (spectral match scores, candidate lists, taxon-filtered subsets) with expected file structure and column counts
- Feature-to-compound mappings are created for all features with available spectra; unmatched features are reported separately
- Annotation confidence metrics (e.g. cosine similarity scores, rank position within taxon-filtered candidates) fall within expected ranges (typically 0–1 for normalized scores)
- Taxonomy-filtered candidate lists contain no compounds documented in sources (e.g. LOTUS, HMDB) outside the given organism's clade, clade, or tissue distribution
- Comparison of annotation results before and after taxonomic filtering shows improved top-candidate plausibility relative to organism biology (fewer off-taxon false positives in top ranks)

## Limitations

- Annotation quality depends on coverage of the sampled organism/tissue in structure-organism databases; rare or poorly-studied taxa may have sparse pairing libraries, reducing filtering effectiveness.
- MS/MS spectral data for only a subset of features limits the scope of annotation to those features with available fragmentation spectra; features without spectra cannot be annotated using this workflow.
- Workflow is marked as 'experimental' and relies on external database versions (LOTUS, HMDB, etc.); database updates or deprecated versions may affect reproducibility and require citation of specific versions.
- No changelog is available, making it difficult to track which improvements or bug fixes have been applied since the original 2019 publication.

## Evidence

- [readme] The workflow integrates spectral, chemical, and taxonomic knowledge to perform annotation.: "performs taxonomically informed metabolite annotation by integrating spectral, chemical, and taxonomic knowledge"
- [readme] Core inputs required are feature table, MS/MS spectra, and sample metadata linked to taxonomy.: "Feature quantification table (.csv/.tsv) - Peak areas/heights across samples, MS/MS spectra file (.mgf) - Fragment spectra for each or some features, Sample metadata (.csv/.tsv) - Links samples to"
- [readme] LOTUS is the default organism-metabolite pairing library with >650k pairs.: "We provide LOTUS (>650k pairs) as default"
- [readme] Validation step checks input files and metadata consistency before processing.: "Start by validating your input files to catch issues early and save debugging time"
- [readme] Workflow execution uses a Shiny GUI with customizable parameters and file paths.: "you can open a small GUI to adapt your parameters and launch your job"
- [readme] Workflow origins trace to a 2019 publication with improvements made since.: "The initial work is available at https://doi.org/10.3389/fpls.2019.01329, with many improvements made since then"
