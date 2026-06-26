---
name: diagnostic-quality-assessment-of-chromatographic-peaks
description: Use when after running targeted peak detection in TARDIS (screening_mode
  = FALSE) on centroided .mzML LC–MS files, apply this skill to verify that integrated
  peaks for your target compounds exhibit acceptable quality.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3370
  tools:
  - TARDIS
  - Spectra
  - R
  - xcms
  - MSConvert (ProteoWizard)
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.5c00567
  title: tardis
evidence_spans:
- Targeted peak integration of LC-MS data using TARDIS
- loads MS data as `Spectra` objects so it's easily integrated with other tools
- rmarkdown::html_document
- Quick start for targeted peak integration of LC-MS data using TARDIS
- It makes use of an established retention time correction algorithm from the `xcms`
  package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_tardis_cq
    doi: 10.1021/acs.analchem.5c00567
    title: tardis
  dedup_kept_from: coll_tardis_cq
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

# Diagnostic Quality Assessment of Chromatographic Peaks

## Summary

Use TARDIS to automatically calculate and inspect multiple quality metrics (area under peak, max intensity, signal-to-noise ratio, peak correlation, and points over peak) for targeted compounds in LC–MS data, enabling visual and quantitative confirmation that detected peaks meet analytical standards. This skill is essential when you need to validate whether peak detection and integration have succeeded before proceeding to statistical analysis.

## When to use

After running targeted peak detection in TARDIS (screening_mode = FALSE) on centroided .mzML LC–MS files, apply this skill to verify that integrated peaks for your target compounds exhibit acceptable quality. Use it when you need to judge whether peaks are truly signal versus noise, whether retention time and m/z windows were correctly set, and whether quality varies across runs or compounds. This is a validation gate before generating final quantitative feature tables.

## When NOT to use

- Input is already a curated feature table or significantly pre-filtered data—this skill is for initial peak validation, not secondary QC.
- Raw (non-centroided) .mzML files without preprocessing—TARDIS requires centroided data as input.
- Untargeted discovery mode where compounds and m/z windows are unknown—this skill assumes a predefined target list with theoretical m/z and expected retention times.

## Inputs

- Centroided .mzML LC–MS files
- TARDIS results object (list with data.frame of AUC values and tibble of quality metrics)
- Target compound information table (ID, Name, m/z, RT in minutes, polarity)
- EIC plots saved by TARDIS in screening or full mode

## Outputs

- Validated peak quality metrics table (Max. Int., SNR, peak_cor, points over peak per target and run)
- Visual EIC diagnostic plots with confirmed peak localization
- Pass/fail assessment per target (suitable for downstream feature table generation)

## How to apply

After TARDIS peak integration completes, inspect the results object—a list containing a data.frame with area-under-curve (AUC) for each target in each run, a tibble with average metrics (Max. Int., SNR, peak_cor, points over peak) for QC runs, and saved EIC plots in the output folder. For each target, examine the EIC plots to visually confirm peaks localize within their expected m/z and retention-time windows. Cross-reference plot inspection with the tabulated metrics: targets with low SNR, few points over the peak, or poor peak_cor should trigger re-evaluation of m/z/RT window settings or exclusion from downstream analysis. Document the polarity (positive/negative) filtering applied by TARDIS and any sawtooth profiles in the EICs caused by filtering of empty spectra, which is expected behavior in multiplexed scan acquisition.

## Related tools

- **TARDIS** (Core tool that performs targeted peak detection, integration, and automatic calculation of quality metrics; outputs results object and diagnostic EIC plots) — https://github.com/pablovgd/TARDIS
- **Spectra** (R package for loading and manipulating centroided MS data as Spectra objects; passed to TARDIS for integration)
- **xcms** (Provides retention time correction algorithm used internally by TARDIS for alignment)
- **MSConvert (ProteoWizard)** (Converts vendor-native mass spectrometry formats to .mzML and performs centroiding preprocessing)
- **R** (Programming environment for running TARDIS and interpreting results) — https://cloud.r-project.org/index.html

## Examples

```
library(TARDIS); results <- tardisPeaks(targets_df, mzml_files, screening_mode=FALSE); inspect(results$EICs); summary(results$quality_metrics)
```

## Evaluation signals

- All EIC plots show target peaks visibly localized within their defined m/z ± tolerance and retention-time windows (visual confirmation of correct window selection).
- SNR (signal-to-noise ratio) values are consistently above an acceptable threshold (article does not specify a cutoff; practitioner must define based on analytical context) across QC runs, indicating true signal detection.
- Peak_cor metric values (peak shape correlation) are close to 1.0, indicating well-shaped, non-distorted peaks free from co-elution or instrumental artifacts.
- Points over the peak count is sufficient (article does not specify minimum; depends on chromatographic resolution), ensuring robust peak definition with adequate data density.
- Max. Int. and AUC values are consistent and non-zero across replicate runs for the same target, suggesting reproducible detection; large run-to-run variance may indicate window misalignment or sample variability.

## Limitations

- Sawtooth profiles in EIC data are expected when TARDIS filters empty spectra to avoid overlapping m/z scan windows in multiplexed acquisition; this does not indicate failure but requires awareness during visual inspection.
- TARDIS automatically performs polarity filtering based on the ionization mode column; if the target list or raw data lacks correct polarity annotation, filtering may silently exclude valid peaks.
- Quality metrics (SNR, peak_cor, points over peak) are calculated automatically but lack published cutoff thresholds; practitioners must establish context-specific acceptance criteria.
- No changelog is provided in the GitHub repository, limiting reproducibility tracing across TARDIS versions; update TARDIS carefully in production workflows.

## Evidence

- [intro] TARDIS automatically calculates area under the peak, max intensity and various quality metrics for targeted chemical compounds in LC-MS data: "TARDIS` offers an easy and straightforward way to automatically calculate area under the peak, max intensity and various quality metrics for targeted chemical compounds in LC-MS data"
- [results] Results include specific tables of Max. Int., SNR, peak_cor and points over the peak for each target: "Other results include tables with the other metrics (Max. Int., SNR, peak_cor and points over the peak)"
- [intro] The screening step generates diagnostic EIC plots that can be inspected to verify targets are visible within m/z and RT windows: "First, we perform a screening step to check if our targets are visible within our *m/z* and RT windows"
- [intro] Empty spectra filtering within TARDIS produces expected sawtooth profiles in multiplex acquisition: "you will notice that peaks will have a sawtooth profile, because of the filtering of empty spectra within TARDIS"
- [intro] Polarity filtering is automatic within TARDIS based on ionization mode column: "Polarity filtering is done within `TARDIS`, so no polarity subsetting has to be performed"
- [results] Results object structure includes data.frame with AUC and tibble with averaged QC metrics: "The `results` object is a `list` that contains a `data.frame` with the AUC of each target in each run"
