---
name: isotopologue-ratio-quality-filtering
description: Use when when extracting isotopologue patterns from centroided mzML files in non-targeted metabolomics workflows, apply this filter after detecting candidate isotopologue peaks but before finalizing the benchmark dataset.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3800
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - mzRAPP
  - enviPat
  - R
  - Skyline
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1093/bioinformatics/btab231/6214530
  title: mzRAPP
evidence_spans:
- 'You can now start mzRAPP using: library(mzRAPP); callmzRAPP()'
- The goal of mzRAPP is to allow reliability assessment of non-targeted data pre-processing (NPP)
- mzRAPP extracts and validates chromatographic peaks for which boundaries are provided for all (enviPat predicted) isotopologues
- library(mzRAPP)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mzrapp_cq
    doi: 10.1093/bioinformatics/btab231/6214530
    title: mzRAPP
  dedup_kept_from: coll_mzrapp_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btab231/6214530
  all_source_dois:
  - 10.1093/bioinformatics/btab231/6214530
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# isotopologue-ratio-quality-filtering

## Summary

Filter out isotopologue peaks whose predicted abundance ratios deviate excessively from observed ratios, or whose peak shape does not correlate well with the most abundant isotopologue. This ensures that only high-confidence isotopologue patterns are retained in benchmark datasets for metabolomics peak detection assessment.

## When to use

When extracting isotopologue patterns from centroided mzML files in non-targeted metabolomics workflows, apply this filter after detecting candidate isotopologue peaks but before finalizing the benchmark dataset. Use it whenever enviPat-predicted isotopologue patterns must be validated against observed LC-HRMS data to remove systematic false positives or noise artifacts that would inflate false-positive rates in downstream peak-detection method evaluation.

## When NOT to use

- Input data are already centroided and peak-picked; use this skill on raw or profile-mode mzML files only.
- No reference target molecules with known composition or retention time are available; this skill requires prior knowledge of which peaks to validate.
- The instrument's mass resolution is <5 ppm at m/z 400, making isotopologue separation ambiguous and the correlation/ratio filters unreliable.

## Inputs

- Centroided mzML files (LC-HRMS data)
- Target molecule list with molecular composition (SumForm_c column)
- Retention time boundaries per molecule (user.rtmin, user.rtmax in seconds)
- Instrument resolution specification (enviPat instrument code or custom resolution CSV)
- Selected adducts for screening (M+H, M+NH4, M+Na, M+K, etc.)
- enviPat-predicted isotopologue patterns and theoretical abundances

## Outputs

- Filtered benchmark dataset (CSV) containing only validated isotopologue peaks
- Per-molecule isotopologue summary: count of isotopologues passing filters, detected adduct forms
- Filtered peak list with: molecule name, adduct, m/z, retention time boundaries, measured peak area/height, Pearson correlation coefficient to most abundant isotopologue

## How to apply

After extracting chromatographic peaks for all predicted isotopologues of target molecules, apply two cascading filters: (1) retain only isotopologues for which at least the theoretically most abundant isotopologue and one additional isotopologue are detected; (2) remove any remaining isotopologue peaks where the measured peak area or height deviates >30% from the enviPat-predicted relative abundance, OR where the Pearson correlation coefficient between the peak shape (intensity profile across scans) and the most abundant isotopologue is <0.85. These thresholds (30% ratio bias, r > 0.85 correlation) act as proxies for peak-picking quality and isotopologue mass resolution at the instrument's actual m/z accuracy. The filtering step is agnostic to absolute peak height and focuses on pattern fidelity, making it robust across different sample concentrations.

## Related tools

- **mzRAPP** (Implements isotopologue extraction, enviPat prediction, and automated filtering pipeline; provides GUI and R API for benchmark generation and filter parameter configuration) — https://github.com/YasinEl/mzRAPP
- **enviPat** (Predicts exact isotopologue masses, theoretical abundances, and resolution-dependent isotope patterns for target molecules)
- **Skyline** (Optional manual peak curation tool to export peak boundaries (user.rtmin/user.rtmax) for input to mzRAPP) — https://skyline.ms/
- **R** (Runtime environment for mzRAPP library and statistical calculations (Pearson correlation, abundance ratio assessment))

## Examples

```
library(mzRAPP); callmzRAPP() # Then navigate to Generate Benchmark tab, select mzML files, sample-group CSV, target-file CSV, set instrument to OrbitrapXL,Velos,VelosPro_R60000@400, adducts M+NH4,M+Na,M+K, set lowest isotopologue 0.05, min scans 6, mz precision 6 ppm, mz accuracy 5 ppm; mzRAPP automatically applies 30% ratio bias and Pearson r>0.85 filters during benchmark generation.
```

## Evaluation signals

- Verify output benchmark CSV has ≥2 isotopologues per molecule (at least theoretically most abundant + one additional), confirming the 'at least two isotopologues' retention rule was enforced.
- Check that all retained isotopologue peak areas/heights fall within ±30% of enviPat-predicted relative abundance for the respective adduct.
- Confirm Pearson correlation coefficient ≥0.85 for all retained isotopologues vs. the most abundant isotopologue within each molecule–adduct group.
- Spot-check a sample of filtered peaks by visual inspection of extracted ion chromatograms in mzRAPP's 'View Benchmark' tab to ensure peaks appear well-shaped and resolve from background noise.
- Cross-validate with downstream peak-detection method performance: if benchmark passes filtering but NPP tools still report high rates of split/missing isotopologues, re-examine filter thresholds or sample quality.

## Limitations

- The 30% ratio-bias and 0.85 correlation thresholds are empirically derived from OrbitrapXL/Velos/VelosPro instruments at R=60,000 (@ m/z 400); applicability to other mass resolving powers or instrument types is not validated in the cited article.
- Filtering assumes accurate enviPat predictions; if the target molecule's molecular composition (SumForm_c) is miscoded (e.g., 'C12H8N0S2' with a leading zero), isotopologue predictions will be wrong and filters will incorrectly reject or accept peaks.
- The filter does not account for adduct-specific ionization efficiency variations; isotopologues of low-abundance adducts (e.g., M+K) may have legitimately lower peak areas and fail the 30% threshold even when correctly detected.
- Pearson correlation is computed across chromatographic scans; if peak width is <6 scans (mzRAPP's default minimum), the correlation coefficient may be unreliable or artificially inflated.
- Filter is inapplicable to unresolved or overlapping isotopologues; if two molecules' isotopologue clusters co-elute, individual isotopologue peak shapes cannot be isolated.

## Evidence

- [methods] removing isotopologues that do not satisfy criteria in peak shape and abundance (Isotopologue ratio bias < 30%): "removing isotopologues that do not satisfy criteria in peak shape and abundance (Isotopologue ratio bias < 30%)"
- [readme] Isotopologue peaks with an area or height which is more than 30% off the predicted value or a Pearson Correlation coef < 0.85 (as compared to the highest isotopologue) are removed.: "Isotopologue peaks with an area or height which is more than 30% off the predicted value or a Pearson Correlation coef < 0.85 (as compared to the highest isotopologue) are removed."
- [readme] Only isotopologues for which the theoretically most abundant and at least one additional isotopologue are found are considered for the final benchmark.: "Only isotopologues for which the theoretically most abundant and at least one additional isotopologue are found are considered for the final benchmark."
- [readme] mzRAPP extracts and validates chromatographic peaks for which boundaries are provided for all (enviPat predicted) isotopologues: "mzRAPP extracts and validates chromatographic peaks for which boundaries are provided for all (enviPat predicted) isotopologues"
- [methods] Sufficient quality of low peaks was ensured by removing isotopologues that do not satisfy criteria in peak shape (peak shape correlation with most abundant isotopologue): "Sufficient quality of low peaks was ensured by removing isotopologues that do not satisfy criteria in peak shape (peak shape correlation with most abundant isotopologue)"
