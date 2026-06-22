---
name: activity-score-robustness-assessment
description: Use when after computing PLAGE-derived activity scores for pathways or metabolite sets (Molecular Families, Mass2Motifs) from log2-standardized metabolomics intensity data.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3520
  tools:
  - PALS (Pathway Activity Level Scoring)
  - GNPS
  - MS2LDA
  - PALS Viewer
  - Reactome
derived_from:
- doi: 10.3390/metabo11020103
  title: pals
- doi: 10.1186/1471-2105-6-225
  title: ''
evidence_spans:
- we introduce **PALS (Pathway Activity Level Scoring)**, a complete tool that performs database queries of pathways, decomposes activity levels in pathways
- we introduce PALS (Pathway Activity Level Scoring), a complete tool that performs database queries of pathways, decomposes activity levels in pathways
- Molecular Families from GNPS
- Mass2Motifs from MS2LDA
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pals
    doi: 10.3390/metabo11020103
    title: pals
  dedup_kept_from: coll_pals
schema_version: 0.2.0
---

# activity-score-robustness-assessment

## Summary

Evaluate the robustness of pathway or metabolite-set activity scores computed via PLAGE decomposition against noise and missing peaks in metabolomics intensity data. This skill assesses whether activity scores remain stable and interpretable across perturbations of the input peak intensity matrix, a critical validation step for metabolomics pathway analysis where noise and missing data are prevalent.

## When to use

After computing PLAGE-derived activity scores for pathways or metabolite sets (Molecular Families, Mass2Motifs) from log2-standardized metabolomics intensity data. Use this skill to validate that the activity scores are not artifacts of noise or data imputation, especially when peak intensity matrices have high sparsity or uncertain annotations. Compare PLAGE results to alternative methods (ORA, GSEA) to confirm the method's advantage in handling incomplete peak data.

## When NOT to use

- Input intensity matrix is already preprocessed as a normalized feature table (e.g., already log-transformed and standardized by another tool); robustness assessment assumes you control preprocessing and noise injection.
- Metabolite set definitions are sparse or very small (< 3 members per set), as SVD-based decomposition and statistical significance testing require sufficient set size.
- Data does not come from metabolomics peak detection workflows; PLAGE robustness advantage is specific to peak-based mass spectrometry data with characteristic sparsity and noise patterns.

## Inputs

- intensity_csv: peak intensity matrix (rows = peak IDs, columns = sample intensities, optional second row with group labels)
- annotation_csv: two-column matrix mapping peak IDs to KEGG or ChEBI compound identifiers
- metabolite_set_definitions: pathway or non-pathway groupings (e.g., Molecular Families from GNPS, Mass2Motifs from MS2LDA, or user-defined lists)
- experimental_design: dictionary or metadata specifying group memberships and case/control comparisons
- noise_perturbation_parameters: min_replace threshold (default 5000), noise magnitude or missing-data fraction for robustness testing

## Outputs

- activity_scores_baseline: PLAGE-derived numerical scores (rows = metabolite sets, columns = samples or comparisons) with p-values and coverage statistics
- activity_scores_perturbed: activity scores recomputed under noise or missing-peak conditions
- robustness_comparison_table: side-by-side p-value, ranking, and score magnitude comparisons between baseline and perturbed runs
- robustness_summary_figure: visual comparison of activity score distributions, scatter plots (baseline vs. perturbed), or ranking preservation curves
- method_comparison_report: quantitative comparison of robustness metrics (e.g., Spearman correlation of rankings, MSE of scores) for PLAGE vs. ORA vs. GSEA under same perturbations

## How to apply

Load the intensity CSV matrix (rows = peak features, columns = samples with optional group annotations) and annotation CSV (peak ID mapped to KEGG or ChEBI compound IDs). Perform standard preprocessing: data imputation (replace zero-only factors with min_replace threshold, e.g., 5000; replace partial zeros with factor mean), log2 transformation, and standardization to zero mean and unit variance. Apply PLAGE decomposition to compute activity scores for each metabolite set across samples. To assess robustness, introduce controlled noise or simulate missing peaks (removing peaks below intensity thresholds or randomly masking a fraction of non-zero entries) and recompute activity scores. Qualitatively and quantitatively compare activity score distributions, rankings, and p-values before and after perturbation. If PLAGE-derived scores remain consistent in ordering and significance while alternative methods (ORA, GSEA) show greater sensitivity to perturbation, this confirms superior robustness. Document the magnitude of noise tolerance (e.g., percentage of peaks removed or noise standard deviation) that activity scores can withstand while preserving pathway/set ranking integrity.

## Related tools

- **PALS (Pathway Activity Level Scoring)** (Performs PLAGE decomposition to compute activity scores for metabolite sets; enables robustness testing via programmatic API and command-line batch processing with configurable min_replace and noise parameters) — https://github.com/glasgowcompbio/PALS
- **PALS Viewer** (Web interface (Streamlit-based) for visual inspection of activity score rankings, filtering by p-value and coverage, and side-by-side comparison of PLAGE, ORA, and GSEA results) — https://pals.glasgowcompbio.org/app/
- **GNPS** (Source of Molecular Families metabolite groupings for non-pathway robustness testing) — http://gnps.ucsd.edu/
- **MS2LDA** (Source of Mass2Motifs metabolite groupings for non-pathway robustness testing) — http://ms2lda.org/
- **Reactome** (Pathway database queried by PALS for compound and protein annotations; supports COMPOUND, ChEBI, UniProt, and ENSEMBL modes for metabolomics and proteomics robustness studies)

## Examples

```
python pals/run.py PLAGE notebooks/test_data/HAT/int_df.csv notebooks/test_data/HAT/annotation_df.csv test_output.csv --db PiMP_KEGG --comparisons Stage_1/Control Stage_2/Control --min_replace 5000
```

## Evaluation signals

- Activity score rankings (sorted by p-value) remain consistent (high Spearman rank correlation, ρ > 0.8) when baseline intensity data is perturbed by noise or missing peaks within realistic tolerances (e.g., ≤20% random peak removal or signal-to-noise ratio degradation).
- P-value distributions for significantly active metabolite sets (p < 0.05) show smaller relative shifts under perturbation for PLAGE than for ORA or GSEA, quantified by coefficient of variation or mean absolute percent change in p-values.
- Coverage metrics (unq_pw_F, tot_ds_F, F_coverage) and sample-wise activity scores remain interpretable and do not become degenerate (e.g., all NaN, uniform, or zero-variance) after noise injection.
- Qualitative visual inspection of pre- and post-perturbation scatter plots shows tight clustering around the diagonal (for score correlations) or low spread in ranking positions, confirming minimal reordering of sets.
- Method comparison shows PLAGE has lower root-mean-square error (RMSE) or smaller mean absolute deviation (MAD) in activity scores under perturbation relative to ORA and GSEA, supporting the claim of superior robustness to noise and missing peaks.

## Limitations

- Robustness assessment depends critically on the choice of noise model and perturbation magnitude; the paper and README do not prescribe specific thresholds for 'acceptable' noise tolerance, leaving judgment to the analyst.
- Data imputation strategy (zero replacement by min_replace or factor mean) directly affects activity scores; robustness may reflect imputation method choice rather than inherent PLAGE stability. Sensitivity analysis across imputation strategies is not automated in PALS.
- PLAGE uses singular value decomposition (SVD) on potentially high-dimensional matrices; numerical stability and rank-deficiency issues can arise if metabolite sets are very large or if the intensity matrix has extreme condition number, but these edge cases are not explicitly discussed.
- Robustness testing requires manual re-runs with perturbed data; PALS does not include built-in functions for automated noise injection and comparative recomputation, so reproducibility and batch evaluation require custom scripting.
- Comparison to ORA and GSEA assumes those methods are correctly implemented in PALS; discrepancies in robustness may reflect implementation differences rather than fundamental algorithmic advantages.

## Evidence

- [readme] The results are found to be more robust to noise and missing peaks compared to the alternatives (ORA, GSEA). This is particularly important for metabolomics peak data, where noise and missing peaks: "The results are found to be more robust to noise and missing peaks compared to the alternatives (ORA, GSEA). This is particularly important for metabolomics peak data, where noise and missing peaks"
- [other] Evaluate robustness of PLAGE-derived activity scores against noise and missing peaks, comparing qualitatively to pathway-based results.: "Evaluate robustness of PLAGE-derived activity scores against noise and missing peaks, comparing qualitatively to pathway-based results."
- [intro] PALS results are more robust to noise and missing peaks compared to ORA and GSEA alternatives: "PALS results are more robust to noise and missing peaks compared to ORA and GSEA alternatives"
- [readme] the decomposition approach in PALS is amenable to the analysis of any group of metabolite sets, not just pathways: "the decomposition approach in PALS is amenable to the analysis of any group of metabolite sets, not just pathways"
- [readme] Data imputation is performed to the intensity matrix when it is loaded: if all of the samples in a single experimental factor have intensities of zero these are replaced by the minimum intensity value (which can be set by the user); and if only some of the sample values in a factor are zero then these are replaced by the mean value of the non-zero samples in that factor. The data is subsequently transformed to log-2 base and standardised using the preprocessing module in Scipy such that the intensity matrix has a zero mean and unit variance across the samples.: "Data imputation is performed to the intensity matrix when it is loaded: if all of the samples in a single experimental factor have intensities of zero these are replaced by the minimum intensity"
