---
name: relative-intensity-threshold-filtering
description: Use when metabolomics LC-MS GC-MS untargeted lipidomics requires filtering MS/MS spectra by applying a minimum intensity threshold for product ions relative to the base peak in each scan to reduce false positives in fragmentation pattern queries.
when_to_use_negative:
- The input spectra are from targeted analysis (e.g., SRM/MRM) where all relevant ions are already separated and abundant—intensity thresholding is redundant.
- The diagnostic ion is known to be very weak or variable in true positives (e.g., rare isotope patterns with <10% base peak intensity); a low threshold may be missed entirely.
- Analysis goal is discovery of new structural variants where minor fragments may carry diagnostic information; strict intensity thresholds may exclude novel chemistry.
edam_operation: http://edamontology.org/operation_3695
edam_topics:
- http://edamontology.org/topic_3520
- http://edamontology.org/topic_0121
tools:
- name: MassQL
  role: Query language and execution engine that parses INTENSITYPERCENT directives and applies relative intensity filtering during MS/MS scan traversal
  repo: https://github.com/mwang87/MassQueryLanguage
- name: lark parser
  role: Parses the MassQL query string into an internal data structure; transforms 'INTENSITYPERCENT=<value>' tokens into filter conditions
  repo: https://github.com/lark-parser/lark
- name: pyteomics
  role: Reads MS data files (mzML, mzXML, MGF) and extracts MS/MS scan spectra with intensity values required for relative intensity calculation
- name: pandas
  role: Performs data frame filtering and manipulation to apply the INTENSITYPERCENT condition across all scans in vectorized form
- name: MZmine
  role: Open-source MS analysis tool with native MassQL support, allowing users to apply relative intensity thresholds in a graphical workflow
  repo: https://github.com/mzmine/mzmine
provenance:
  source_task_ids:
  - task_003
  source_papers:
  - doi: 10.1038/s41592-025-02660-z
    title: A universal language for finding mass spectrometry data patterns
schema_version: 0.2.0
metadata:
  iri: https://w3id.org/holobiomicslab/asb-skill/relative-intensity-threshold-filtering@sha256:777ae9464df62d25dcb11bc128c7fce096d2f497af59bdf38e1d49f950f77405
---

# Relative Intensity Threshold Filtering

## Summary

Filter MS/MS spectra by requiring product ions to meet a minimum intensity threshold relative to the base peak (most intense ion) in each scan. This skill is essential for reducing false positives when querying large repositories for characteristic fragmentation patterns, such as phosphate product ions from organophosphate esters or isotope patterns from metal-binding compounds.

## When to use

Apply this skill when executing broad MS/MS queries across public repositories (e.g., GNPS/MassIVE with >230 million spectra) that would otherwise retrieve thousands of candidate spectra. Use it to prioritize spectra where a diagnostic product ion is prominent relative to other fragments, improving signal-to-noise and reducing the proportion of spurious matches. Critical when the diagnostic ion is a minor fragment in many spectra but highly abundant in true positives.

## When NOT to use

- The input spectra are from targeted analysis (e.g., SRM/MRM) where all relevant ions are already separated and abundant—intensity thresholding is redundant.
- The diagnostic ion is known to be very weak or variable in true positives (e.g., rare isotope patterns with <10% base peak intensity); a low threshold may be missed entirely.
- Analysis goal is discovery of new structural variants where minor fragments may carry diagnostic information; strict intensity thresholds may exclude novel chemistry.

## Inputs

- LC-MS/MS dataset in mzML, mzXML, or MGF format
- MassQL query string with MS2PROD, TOLERANCEPPM, and INTENSITYPERCENT parameters
- Reference MS/MS spectra of known compounds (e.g., from GNPS libraries) to calibrate threshold

## Outputs

- Filtered set of MS/MS spectra meeting both m/z and relative intensity criteria
- Tabular export (CSV/TSV) with scan identifiers, precursor m/z, product ion m/z, intensity values, and metadata
- Metadata including scan number, retention time, and base peak intensity for matched spectra

## How to apply

During MassQL query execution, specify an INTENSITYPERCENT threshold (e.g., 50%) alongside the product ion m/z and mass tolerance (ppm). The query engine filters all MS/MS scans to retain only those where the target product ion intensity is ≥ the specified percentage of the base peak intensity within that scan. For example, a phosphate fragment query 'MS2PROD=98.9847:TOLERANCEPPM=50:INTENSITYPERCENT=50' will only match spectra where the m/z 98.9847 ± 50 ppm peak is at least 50% as intense as the tallest peak in that MS/MS spectrum. Apply this threshold early in the workflow—during parsing by the lark parser and filtering via pandas—to avoid caching and processing spectra that will be discarded. Tune the threshold empirically: start with reference spectra of known compounds (e.g., GNPS spectral libraries) to determine the median base peak percentage of true positives, then set the threshold slightly lower to capture true signal while rejecting background noise.

## Related tools

- **MassQL** (Query language and execution engine that parses INTENSITYPERCENT directives and applies relative intensity filtering during MS/MS scan traversal) — https://github.com/mwang87/MassQueryLanguage
- **lark parser** (Parses the MassQL query string into an internal data structure; transforms 'INTENSITYPERCENT=<value>' tokens into filter conditions) — https://github.com/lark-parser/lark
- **pyteomics** (Reads MS data files (mzML, mzXML, MGF) and extracts MS/MS scan spectra with intensity values required for relative intensity calculation)
- **pandas** (Performs data frame filtering and manipulation to apply the INTENSITYPERCENT condition across all scans in vectorized form)
- **MZmine** (Open-source MS analysis tool with native MassQL support, allowing users to apply relative intensity thresholds in a graphical workflow) — https://github.com/mzmine/mzmine

## Examples

```
from massql.query import QuerySpectra; query = QuerySpectra('MS2PROD=98.9847:TOLERANCEPPM=50:INTENSITYPERCENT=50'); results = query.query_spectra_file('marine_water.mzML')
```

## Evaluation signals

- Verify that all output spectra have product ion intensity ≥ (INTENSITYPERCENT / 100) × base peak intensity; sample-check 10–20 spectra to confirm calculation is correct.
- Compare output counts at different INTENSITYPERCENT thresholds (e.g., 25%, 50%, 75%) against reference MS/MS libraries; confirm that the chosen threshold recovers known compounds at expected frequency (e.g., >90% recall) while reducing false positives.
- Check that the base peak intensity values in output metadata are consistent; base peak should always be ≥ product ion intensity.
- Validate that no spectra are included if the target m/z is absent or falls outside the TOLERANCEPPM window, independent of intensity.
- For large repository queries (>230 million spectra), confirm that the retrieval count is consistent with repository size and typical compound abundance; e.g., a specific phosphate query on >230 million spectra should retrieve hundreds of thousands of candidates, with intensity filtering reducing that by 70–90% depending on threshold.

## Limitations

- Threshold is fixed globally across all scans; cannot adapt to compound-specific fragmentation efficiency or instrument-specific noise profiles.
- Low-intensity diagnostic ions (e.g., rare isotope peaks with natural abundance <5%) may be missed if threshold is set above their expected relative abundance; one reported siderophore was missed because the 54Fe peak intensity fell outside 25% tolerance.
- MassQL has limited capability to leverage consecutive MS spectra from a chromatographic feature; relative intensity filtering is applied per-scan, not across the feature envelope.
- Intensity thresholding does not account for baseline noise; on very noisy spectra, a high intensity threshold may incorrectly flag weak true signal as noise.

## Evidence

- [methods] INTENSITYPERCENT threshold parameter for filtering MS/MS spectra: "MS2PROD=98.9847:TOLERANCEPPM=50:INTENSITYPERCENT=50 product ion m/z, mass tolerance (ppm) and peak intensity ≥ 50% of base peak."
- [full_text] Application of intensity filtering to reduce false positives in large-scale queries: "retaining only those with a product ion at m/z 98.9847 ± 50 ppm and peak intensity ≥ 50% of base peak"
- [full_text] Demonstration that intensity thresholding improves specificity on public repositories: "The MassQL query found 338,439 MS/MS spectra matching organophosphate ester phosphate product ion query across >230 million spectra in GNPS/MassIVE"
- [full_text] Calibration of intensity threshold using reference spectra: "we first used the GNPS spectral libraries (which contained 4,533 reference spectra of bile acids) to design and refine MassQL queries"
- [full_text] Limitation: low-intensity diagnostic ions missed by fixed thresholds: "The unique compound that was found using IIMN but not by the MassQL query was missed because the 54Fe peak intensity fell outside of the expected intensity tolerance of 25%"
- [full_text] Implementation: pandas data frame filtering for intensity conditions: "The query engine itself processes the query over these data frames using the Python pandas library to perform data filtering and manipulations"
