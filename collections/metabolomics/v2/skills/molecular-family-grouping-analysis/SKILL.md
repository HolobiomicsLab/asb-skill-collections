---
name: molecular-family-grouping-analysis
description: Use when you have untargeted metabolomics peak intensity data and spectral groupings (Molecular Families or Mass2Motifs) but lack confident chemical annotations or want to avoid pathway database dependency.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3501
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - GNPS
  - MS2LDA
  - PALS (Pathway Activity Level Scoring)
  - GNPS (Global Natural Products Social Molecular Networking)
  - MS2LDA (Mass2Motif Latent Dirichlet Allocation)
  - PALS Viewer
derived_from:
- doi: 10.3390/metabo11020103
  title: pals
- doi: 10.1186/1471-2105-6-225
  title: ''
evidence_spans:
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

# molecular-family-grouping-analysis

## Summary

Apply PALS decomposition (PLAGE method) to metabolite groupings from spectral clustering (Molecular Families from GNPS, Mass2Motifs from MS2LDA) to compute activity scores and identify significantly changing metabolite groups across experimental conditions. This extends classical pathway-based analysis to spectral phenotypes, which are often more robust to annotation uncertainty in untargeted metabolomics.

## When to use

You have untargeted metabolomics peak intensity data and spectral groupings (Molecular Families or Mass2Motifs) but lack confident chemical annotations or want to avoid pathway database dependency. Spectral groupings are particularly useful when peaks cannot be reliably assigned to known metabolites, as they group by fragment pattern similarity rather than chemical identity.

## When NOT to use

- Input peaks already have confident chemical structure annotations and a curated pathway database is available—use classical pathway analysis (KEGG, Reactome) instead.
- Spectral groupings were not generated from the same mass spectrometry dataset or instrument—inter-dataset spectral clustering is unreliable.
- Sample size is very small (n < 3 per group)—SVD-based activity scores require sufficient rank.

## Inputs

- Peak intensity matrix (CSV): row_id (peak feature identifier) in column 1, sample columns with log2 intensity values, optional group assignment row
- Annotation table (CSV): two columns mapping peak IDs to Molecular Family or Mass2Motif identifiers
- Experimental design specification: case/control group labels and comparison pairs

## Outputs

- Ranked metabolite group activity table: group ID, activity scores per sample, p-values, detected member count, coverage fraction
- Group activity visualizations: sorted by p-value for prioritization of significant spectral phenotypes

## How to apply

Load your log2-normalized, per-factor imputed peak intensity matrix (rows = peak features with IDs in column 1, columns = samples) and a two-column annotation table mapping peak IDs to Molecular Family or Mass2Motif identifiers (obtained from GNPS or MS2LDA clustering). Apply PALS decomposition using the PLAGE method, which computes a singular value decomposition (SVD) on the intensity submatrix for each metabolite group, deriving a single activity score per group per sample. Specify experimental design as case/control pairs. PLAGE is more robust to noise and missing peaks than ORA or GSEA alternatives—critical for metabolomics where baseline noise is high and peak detection is probabilistic. Evaluate output by checking that activity score p-values and coverage (proportion of group members detected) are reasonable; cross-validate against known treatment effects if available.

## Related tools

- **PALS (Pathway Activity Level Scoring)** (Core decomposition and activity scoring engine; performs PLAGE SVD-based decomposition on any metabolite grouping (not limited to pathways)) — https://github.com/glasgowcompbio/PALS
- **GNPS (Global Natural Products Social Molecular Networking)** (Source of Molecular Family spectral groupings; provides unsupervised clustering of MS/MS spectra by cosine similarity) — http://gnps.ucsd.edu/
- **MS2LDA (Mass2Motif Latent Dirichlet Allocation)** (Source of Mass2Motif spectral motif groupings; decomposes MS/MS spectra into recurring fragmentation patterns) — http://ms2lda.org/
- **PALS Viewer** (Interactive web interface for running PALS, browsing activity results, and prioritizing Molecular Families or Mass2Motifs by activity level) — https://pals.glasgowcompbio.org/app/

## Examples

```
python pals/run.py PLAGE intensity_peaks.csv annotation_mf.csv output_mf_activity.csv --db COMPOUND --comparisons treatment/control --min_replace 5000
```

## Evaluation signals

- Output activity scores sum to non-zero across replicates within each group, indicating successful SVD decomposition.
- Coverage (fraction of group members detected in dataset) is > 0 for all output groups; groups with zero coverage should be excluded.
- P-values decrease monotonically with increasing group size (all else equal), confirming statistical power scales with group membership.
- Results are qualitatively concordant with known treatment effects or biomarkers (if independent validation is available).
- Robustness check: re-run analysis after artificially zeroing 10–20% of low-intensity peaks; activity ranks should remain stable for highly significant groups.

## Limitations

- PLAGE activity scores are unsupervised; high scores do not indicate direction (up or down) of metabolite abundance without additional contrast-based post-processing.
- Molecular Families and Mass2Motifs are instrument-dependent; clustering generated on different MS platforms (e.g., Q-TOF vs. Orbitrap) may not transfer.
- Missing peak annotations reduce effective group membership; imputation via minimum intensity occurs but does not recover undetected features, limiting power for sparse groups.
- SVD-based decomposition assumes linear independence within groups; groups with highly correlated members may yield unstable or uninterpretable activity scores.

## Evidence

- [readme] the decomposition approach in PALS is amenable to the analysis of any group of metabolite sets, not just pathways: "the [decomposition approach] in PALS is amenable to the analysis of any group of metabolite sets, not just pathways"
- [readme] Molecular Families from GNPS and Mass2Motifs from MS2LDA can be analysed in PALS: "metabolite sets obtained from the grouping of metabolites according to their fragmentation spectra can also be analysed. This includes in particular *Molecular Families* from"
- [readme] PALS results are more robust to noise and missing peaks than ORA and GSEA: "The results are found to be more robust to noise and missing peaks compared to the alternatives (ORA, GSEA). This is particularly important for metabolomics peak data, where noise and missing peaks"
- [readme] PALS decomposes activity via the PLAGE method: "decomposes activity levels in pathways via [the PLAGE method]"
- [readme] Data imputation strategy for handling missing values: "if all of the samples in a single experimental factor have intensities of zero these are replaced by the minimum intensity value (which can be set by the user); and if only some of the sample values"
