---
name: spectral-result-visualization-verification
description: Use when after running annotateRC to generate ranked candidate annotations for LC-MS AIF features, when you need to confirm that (1) the top-ranked candidate match is chemically plausible given the observed fragment ions, (2) alternative candidate annotations exist and are correctly ranked, and (3).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3937
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
  tools:
  - MetaboAnnotatoR
  - R
  - xcms
  - RamClustR
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.1c03032
  title: metaboannotator
evidence_spans:
- MetaboAnnotatoR is designed to perform metabolite annotation of features from LC-MS All-ion fragmentation (AIF) datasets
- To install this package, start R (version "4.5.0" or higher)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metaboannotator
    doi: 10.1021/acs.analchem.1c03032
    title: metaboannotator
  dedup_kept_from: coll_metaboannotator
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.1c03032
  all_source_dois:
  - 10.1021/acs.analchem.1c03032
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Spectral Result Visualization and Verification

## Summary

Verify and visually inspect annotated metabolite spectra with matched fragment ions to confirm candidate ranking accuracy and annotation quality. This skill combines human-readable visualization of pseudo-MS/MS spectra against candidate matches with file-based auditing to ensure the annotation pipeline produced complete, valid outputs.

## When to use

After running annotateRC to generate ranked candidate annotations for LC-MS AIF features, when you need to confirm that (1) the top-ranked candidate match is chemically plausible given the observed fragment ions, (2) alternative candidate annotations exist and are correctly ranked, and (3) all expected output file types (global results table, ranked results, ranked spectra PDFs, pseudo-MS/MS MGF file) are present and non-empty in the output directory.

## When NOT to use

- Annotation workflow has not yet been executed or annotateRC output is unavailable.
- Raw LC-MS data has not been processed to pseudo-MS/MS spectra via xcms and RamClustR; MetaboAnnotatoR requires centroid-mode AIF chromatograms and pseudo-MS/MS spectra as input.
- Output directory already contains results from a prior run and you need to distinguish old from new outputs; this skill does not perform incremental or delta verification.

## Inputs

- MetaboAnnotatoR annotations object (output from annotateRC function)
- Temporary or target directory path for output
- Ranked candidate matches per feature with ion match metadata

## Outputs

- Global annotations results file
- Ranked results table (CSV or equivalent)
- Ranked spectra PDF files (one per feature with matched ions plotted)
- Pseudo-MS/MS MGF file (all pseudo-spectra)
- Audit report documenting file names, formats, sizes, and completion status

## How to apply

Invoke saveAnnotations on the annotations object returned by annotateRC, specifying a target output directory and enabling all save flags (global results, ranked results, ranked spectra PDFs, pseudo-MS/MS MGF). Enumerate all generated files and verify that global results file, ranked results file, ranked spectra PDF files (one per feature), and pseudo-MS/MS MGF file are present with file size > 0 bytes. Retrieve the ranked candidate list for each feature using the annotations object, and visually inspect the spectra with matched ions plotted for the top candidate and alternative candidates to assess whether the fragment pattern distribution is consistent with the proposed metabolite structure and ionization mode. Cross-reference ion matches with the feature's pseudo-MS/MS spectrum to confirm that high-confidence matches (high cosine similarity or match count) correspond to biologically plausible fragmentations.

## Related tools

- **MetaboAnnotatoR** (Core annotation and output generation package; executes annotateRC and saveAnnotations functions to produce ranked candidate annotations and visualization artifacts) — https://github.com/gggraca/MetaboAnnotatoR
- **xcms** (Upstream preprocessing: peak-picking and feature detection from centroid-mode LC-MS AIF chromatograms to generate feature table input to annotateRC)
- **RamClustR** (Upstream preprocessing: generates pseudo-MS/MS spectra from AIF data, required as input alongside xcms output and feature table for annotateRC)

## Examples

```
saveAnnotations(annotations_object, output_dir = '/tmp/annotation_results', saveGlobalResults = TRUE, saveRankedResults = TRUE, saveRankedPDFs = TRUE, savePseudoMGF = TRUE)
```

## Evaluation signals

- All expected output files present in target directory: global results file, ranked results CSV, one ranked spectra PDF per feature, pseudo-MS/MS MGF file, with each file size > 0 bytes.
- Ranked spectra PDF plots display observed pseudo-MS/MS peaks alongside matched ions for top-ranked candidate; ion match count and cosine similarity are consistent with visual peak overlap in the plot.
- Global results table contains one row per feature with candidate metabolite name, match score, adduct type, and confidence metrics; ranked results table lists alternative candidates (if any) with their match ranks and scores.
- Pseudo-MS/MS MGF file is valid and can be parsed; each spectrum entry corresponds to a feature in the original feature table and contains m/z and intensity pairs.
- Ion matches in ranked spectra visualizations correspond to fragment ions expected for the proposed metabolite under the stated ionization mode (e.g., [M+H]+ or [M-H]−); no obvious chemical impossibilities (e.g., fragments heavier than precursor).

## Limitations

- Visualization quality and interpretability depend on the quality of upstream pseudo-MS/MS spectra generated by RamClustR; poor spectral resolution or high noise can obscure fragment pattern and lead to ambiguous candidate ranking.
- The saveAnnotations function does not provide granular error messages per file type; if one output format fails (e.g., PDF generation), the overall save operation may not clearly indicate which format was problematic.
- No changelog available in the repository documentation; version compatibility and breaking changes between MetaboAnnotatoR releases are not systematically documented, which may affect reproducibility of results across different installation dates.
- The skill assumes fragment libraries have been correctly specified and loaded; validation of library integrity and spectrum database currency is outside the scope of this skill.

## Evidence

- [intro] It is possible to visualise the spectra containing the matched ions to each candidate: "It is possible to visualise the spectra containing the matched ions to each candidate"
- [intro] It is possible to inspect if there were other candidate annotations for a given feature: "It is also possible to inspect if there were other candidate annotations for a given feature"
- [intro] It is possible to save the annotation results to a user-specified directory: "It is possible to save the annotation results to a user-specified directory"
- [other] Call saveAnnotations with the annotations object and a temporary directory path as output destination. Enumerate all files generated in the temporary directory.: "Call saveAnnotations with the annotations object and a temporary directory path as output destination. 3. Enumerate all files generated in the temporary directory."
- [other] Verify presence of global results file, ranked results file, ranked spectra PDF files (one per feature), and pseudo-MS/MS MGF file. Check that each file is non-empty (file size > 0 bytes).: "Verify presence of global results file, ranked results file, ranked spectra PDF files (one per feature), and pseudo-MS/MS MGF file. 5. Check that each file is non-empty (file size > 0 bytes)."
- [intro] MetaboAnnotatoR is designed to perform metabolite annotation of features from LC-MS All-ion fragmentation (AIF) datasets, using ion fragment databases: "MetaboAnnotatoR is designed to perform metabolite annotation of features from LC-MS All-ion fragmentation (AIF) datasets, using ion fragment databases"
- [readme] It requires raw LC-MS AIF chromatograms acquired/transformed in centroid mode: "It requires raw LC-MS AIF chromatograms acquired/transformed in centroid mode"
