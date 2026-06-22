---
name: method-equivalence-verification-across-api-invocations
description: Use when when a tool like TARDIS extends its API to accept multiple input types (e.g., both file paths and MsExperiment objects), and you need to confirm that screening-mode diagnostic outputs (e.g., EIC plots, peak detection metrics) are identical regardless of which invocation pattern is used.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3801
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - xcms
  - Spectra
  - MsExperiment
  - TARDIS
  - R
  - knitr
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.5c00567
  title: tardis
evidence_spans:
- It makes use of an established retention time correction algorithm from the `xcms` package
- loads MS data as `Spectra` objects so it's easily integrated with other tools
- Alternatively, instead of using file paths as input for TARDIS, the user can also use an `MsExperiment` object
- R package for *TArgeted Raw Data Integration In Spectrometry*
- knitr::include_graphics
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_tardis
    doi: 10.1021/acs.analchem.5c00567
    title: tardis
  dedup_kept_from: coll_tardis
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c00567
  all_source_dois:
  - 10.1021/acs.analchem.5c00567
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# method-equivalence-verification-across-api-invocations

## Summary

Verify that two distinct API invocation patterns (file-path-based vs. object-based) of the same analytical method produce functionally identical outputs on the same input data. This skill is critical when a tool's API is refactored or extended to support alternative input types, and reproducibility must be guaranteed across both calling conventions.

## When to use

When a tool like TARDIS extends its API to accept multiple input types (e.g., both file paths and MsExperiment objects), and you need to confirm that screening-mode diagnostic outputs (e.g., EIC plots, peak detection metrics) are identical regardless of which invocation pattern is used. This is especially important before recommending one API pattern over another to users.

## When NOT to use

- Do not use this skill when the two API patterns are intended to serve fundamentally different use cases (e.g., one is a simplified interface, the other a full pipeline) — method-equivalence verification assumes both should produce identical results.
- Do not apply when input data differ between invocations (different mzML files, different sample metadata) — equivalence testing requires identical inputs.
- Do not use when comparing outputs from different tools or different versions of the same tool; this skill is for verifying two invocation routes within a single tool at a single version.

## Inputs

- mzML files (centroided, polarity-specific)
- MsExperiment object (containing Spectra and annotated sampleData with type column)
- Target list data.frame with columns: compound ID, name, m/z, retention time (minutes), polarity

## Outputs

- EIC PNG diagnostic files (visual chromatograms)
- Data frame with AUC (area under curve) for each target in each run
- Tibble with average QC metrics (Max. Int., SNR, peak_cor, points over peak) per target
- Comparison report documenting file set equivalence, visual EIC equivalence, and numerical metric agreement

## How to apply

Execute tardisPeaks() in screening_mode=TRUE using both the file-path invocation (passing mzML file paths directly) and the object-based invocation (passing an MsExperiment object containing Spectra and annotated sampleData with type labels). Collect all diagnostic output files (EIC PNG files, diagnostic tables) from both runs. Perform a systematic comparison: first, verify that the PNG file sets are identical in number and naming; then, visually inspect the EIC chromatogram content to confirm peaks appear at the same retention times and m/z values with matching intensity profiles. Finally, extract any quantitative metrics (AUC, max intensity, SNR) from both invocations and verify numerical equivalence or acceptable numerical tolerance. Divergence in EIC shape, peak detection, or metrics indicates the API refactoring has introduced a behavioral difference and should trigger investigation of data flow or parameter handling differences between the two code paths.

## Related tools

- **TARDIS** (Primary analysis tool; tardisPeaks() is invoked twice (file-path and object-based modes) to generate diagnostic outputs for comparison) — https://github.com/pablovgd/TARDIS
- **Spectra** (Loads MS data into R objects compatible with MsExperiment; used to prepare input for object-based invocation)
- **MsExperiment** (Container class holding Spectra and sampleData; enables alternative API invocation pattern requiring sampleData$type annotation)
- **xcms** (Underlying retention time correction algorithm used within TARDIS; relevant for understanding peak detection consistency)
- **knitr** (Used to programmatically embed and visually compare EIC PNG outputs in a markdown or HTML comparison report)

## Examples

```
# File-path invocation
results_file <- tardisPeaks(lcmsData = c('run1.mzML', 'run2.mzML'), screening_mode = TRUE, targets = target_df, outputFolder = 'output_file')

# Object-based invocation
results_obj <- tardisPeaks(lcmsData = ms_experiment, screening_mode = TRUE, targets = target_df, outputFolder = 'output_object')

# Verify equivalence: compare EIC PNG file sets and metrics
identical(list.files('output_file', pattern='.png'), list.files('output_object', pattern='.png'))
```

## Evaluation signals

- File set equivalence: both invocations produce identical numbers of EIC PNG files with matching file names and target identifiers.
- Visual EIC equivalence: side-by-side inspection of EIC chromatograms shows peaks at identical m/z and retention time, with visually indistinguishable intensity profiles and baseline characteristics.
- Numerical metric equivalence: AUC, max intensity, SNR, peak_cor, and 'points over peak' values agree to at least 3 significant figures between file-path and object-based runs (or differ by < 1% relative error if using loose tolerance).
- Polarity filtering consistency: both invocations correctly filter and separate positive/negative polarity targets based on the target list and sampleData$type annotations.
- Screening-mode reproducibility: identical targets marked as 'visible' or 'not visible' in m/z/RT windows across both invocations.

## Limitations

- Verification relies on visual inspection of PNG files, which is subjective; systematic pixel-level comparison or automated image diff may be more robust for high-throughput validation.
- No changelog found in TARDIS repository; breaking changes between tool versions may invalidate prior equivalence claims.
- The skill assumes both invocation routes actually invoke the same underlying algorithm; if the codebase has separate peak-detection branches for file-path vs. object-based input, equivalence is not guaranteed without code inspection.
- Equivalence testing is sensitive to floating-point precision differences; numerical agreement should specify acceptable tolerance (e.g., relative error < 0.1%) rather than exact equality.
- MsExperiment object-based invocation requires proper annotation of sampleData$type (QC vs. sample); failure to populate this column will silently produce incorrect results that may appear equivalent in file count but differ in polarity filtering and metric aggregation.

## Evidence

- [other] The tardisPeaks() function accepts both file paths and MsExperiment objects as input when screening_mode=TRUE, with the MsExperiment approach requiring sampleData$type to be populated to distinguish QC from sample runs.: "the tardisPeaks() function accepts both file paths and MsExperiment objects as input when screening_mode=TRUE, with the MsExperiment approach requiring sampleData$type to be populated"
- [other] Verify functional equivalence by comparing EIC outputs and metrics between file-path and object-based invocations.: "Compare the EIC PNG file set and visual content against reference EIC PNGs produced from the equivalent file-path-based tardisPeaks() invocation to verify functional equivalence."
- [intro] Polarity filtering is performed within TARDIS, so no prior subsetting is needed.: "Polarity filtering is done within `TARDIS`, so no polarity subsetting has to be performed"
- [intro] TARDIS outputs include automatically calculated area under the peak, max intensity and various quality metrics.: "automatically calculate area under the peak, max intensity and various quality metrics for targeted chemical compounds in LC-MS data"
- [results] Results include diagnostic tables with AUC, Max. Int., SNR, peak_cor, and points over the peak.: "Other results include tables with the other metrics (Max. Int., SNR, peak_cor and points over the peak)"
- [results] EIC chromatograms are saved in the output folder for inspection.: "The resulting EICs are again saved in the output folder and can be inspected"
- [intro] Alternatively, instead of using file paths as input for TARDIS, the user can also use an MsExperiment object.: "Alternatively, instead of using file paths as input for TARDIS, the user can also use an `MsExperiment` object"
- [other] MsExperiment is constructed from Spectra objects and sampleData with type labels.: "Construct an MsExperiment object combining the Spectra object and sampleData. 4. Prepare a target list data frame containing compound ID, name, theoretical m/z, expected retention time in minutes,"
