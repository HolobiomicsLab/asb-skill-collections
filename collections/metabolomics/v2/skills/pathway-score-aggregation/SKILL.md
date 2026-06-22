---
name: pathway-score-aggregation
description: Use when you have a metabolite intensity matrix (samples × metabolites) or gene expression matrix (samples × genes) with corresponding pathway definitions (pathway IDs mapped to feature sets), and you need to rank pathways by activity level to identify which biological processes are most affected.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3762
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_0160
  tools:
  - PALS (Pathway Activity Level Scoring)
  - PALS
  - PALS Viewer
  - Reactome
  - KEGG
  - GNPS (Global Natural Products Social Molecular Networking)
  - MS2LDA
derived_from:
- doi: 10.3390/metabo11020103
  title: pals
evidence_spans:
- we introduce **PALS (Pathway Activity Level Scoring)**, a complete tool that performs database queries of pathways
- we introduce **PALS (Pathway Activity Level Scoring)**, a complete tool that performs database queries of pathways,
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pals_cq
    doi: 10.3390/metabo11020103
    title: pals
  dedup_kept_from: coll_pals_cq
schema_version: 0.2.0
---

# pathway-score-aggregation

## Summary

Decompose metabolite or gene intensity data into pathway-level activity scores using singular value decomposition (SVD), enabling robust identification of significantly perturbed pathways. The PLAGE method aggregates multiple features (metabolites or genes) within each pathway into a single activity level vector per sample, making results more robust to noise and missing data than alternatives like ORA or GSEA.

## When to use

Apply this skill when you have a metabolite intensity matrix (samples × metabolites) or gene expression matrix (samples × genes) with corresponding pathway definitions (pathway IDs mapped to feature sets), and you need to rank pathways by activity level to identify which biological processes are most affected across your experimental conditions. Use PLAGE specifically when your input data contains substantial noise or missing peaks/probes, which is typical in metabolomics and proteomics datasets.

## When NOT to use

- Input contains only a few features per pathway (< 3–5): SVD requires sufficient features within each pathway to estimate stable singular vectors; pathways with very few members may produce unreliable activity scores.
- Pathway definitions are unknown or unavailable: PLAGE requires explicit mapping of features to pathways; if no pathway database is applicable or accessible, use single-feature or feature-set-free ranking methods instead.
- Input is already a pre-aggregated feature table or pathway score matrix: PLAGE is designed to operate on raw or minimally processed intensity data; applying it to already-summarized data is redundant and may obscure the underlying decomposition.

## Inputs

- Intensity matrix (CSV): samples × features (metabolites/genes/proteins); rows are feature IDs, columns are sample names; optional second row indicates experimental group assignments
- Annotation matrix (CSV): two-column table mapping feature IDs to pathway member IDs (KEGG IDs, ChEBI IDs, UniProt IDs, ENSEMBL IDs, or user-defined identifiers)
- Pathway definitions (database query result): pathway identifiers mapped to sets of member feature IDs retrieved from KEGG, Reactome, or custom source
- Experimental design (dict or metadata): group assignments and case/control comparisons for each sample

## Outputs

- Pathway activity level matrix (CSV): pathways × samples, where each cell is a single numeric score representing the aggregated pathway activity for that sample
- Pathway ranking table (CSV): pathways ranked by statistical significance (p-value), with columns for pathway ID, activity scores per comparison, and coverage metrics (unique features in pathway vs. features observed in dataset)

## How to apply

Load the intensity matrix (log2-transformed and standardized to zero mean and unit variance) alongside pathway definitions from a database query (e.g., KEGG, Reactome, or user-defined metabolite sets). For each pathway, extract the subset of intensity columns corresponding to that pathway's member features. Apply singular value decomposition (SVD) to each pathway-specific submatrix. Extract the first left singular vector and multiply it by the first singular value to produce a pathway activity level vector (one score per sample). Stack all pathway activity vectors into a final pathway × sample matrix. Optionally apply data imputation before SVD: replace all-zero intensities in a factor with the minimum intensity value (default 5000), and replace partial-zero intensities with the mean of non-zero samples in that factor.

## Related tools

- **PALS (Pathway Activity Level Scoring)** (Reference implementation of PLAGE decomposition; performs database queries, applies SVD-based pathway scoring, and ranks pathways by statistical significance) — https://github.com/glasgowcompbio/PALS
- **PALS Viewer** (Interactive web interface for running PALS, visualizing pathway ranking results, and inspecting significantly changing pathways in metabolomics and proteomics experiments) — https://pals.glasgowcompbio.org/app/
- **Reactome** (Pathway database queried by PALS for metabolic, signaling, and protein interaction pathways across multiple species; supports KEGG compound, ChEBI, UniProt, and ENSEMBL ID matching)
- **KEGG** (Metabolic pathway and compound database integrated into PALS via PiMP export; provides pathway definitions and compound annotations for metabolomics analysis)
- **GNPS (Global Natural Products Social Molecular Networking)** (Source of molecular family groupings that can be analyzed using the PLAGE decomposition approach in PALS as an alternative to curated pathways) — http://gnps.ucsd.edu/
- **MS2LDA** (Produces Mass2Motifs (groupings of metabolites by fragmentation patterns) that can be scored using PLAGE decomposition alongside traditional pathway analysis) — http://ms2lda.org/

## Examples

```
python pals/run.py PLAGE notebooks/test_data/HAT/int_df.csv notebooks/test_data/HAT/annotation_df.csv test_output.csv --db PiMP_KEGG --comparisons Stage_1/Control Stage_2/Control --min_replace 5000
```

## Evaluation signals

- Output pathway activity matrix has dimensions [n_pathways, n_samples] with numeric scores; no NaN values in core columns; scores vary across samples and pathways (not uniform or constant).
- Pathway ranking p-values are well-distributed across the [0, 1] range; median p-value is not extreme (not clustered near 0 or 1), indicating reasonable statistical power.
- Pathway scores for replicate samples within the same experimental group are highly correlated (Pearson r > 0.9), and scores for samples from different case/control groups show expected separation in direction or magnitude.
- Coverage column (tot_ds_F / unq_pw_F) is documented for each pathway; pathways with very low coverage (< 0.1) are flagged and can be re-ranked or filtered if desired.
- Rerunning PLAGE on a subset of samples (e.g., samples 1–10) produces pathway rankings qualitatively consistent with full-dataset results for high-significance pathways (Spearman correlation of p-value ranks > 0.8).

## Limitations

- Pathways with fewer than 3–5 member features may produce unstable SVD estimates due to insufficient degrees of freedom; consider merging small pathways or filtering by minimum size.
- Data imputation strategy (mean or minimum replacement) can bias pathway scores if missingness is non-random (e.g., systematically lower intensities in certain samples); inspect missingness patterns before and after imputation.
- PLAGE scores reflect linear combinations of pathway members and are sensitive to the choice of standardization (log2 transform and z-score normalization); deviations from this preprocessing can affect reproducibility.
- Multiple pathway definitions may contain overlapping feature sets (e.g., shared metabolites across KEGG pathways); this can inflate correlation between pathway scores and inflate false-positive pathway associations.
- The method requires explicit experimental design specification (group assignments and case/control pairs); ambiguous or missing group metadata will cause the analysis to fail or produce misleading results.

## Evidence

- [other] For each pathway, extract the corresponding subset of metabolite columns from the intensity matrix. 3. Apply singular value decomposition (SVD) to each pathway-specific metabolite submatrix. 4. Extract the first left singular vector and multiply by the first singular value to obtain the pathway activity level vector: "Extract the first left singular vector and multiply by the first singular value to obtain the pathway activity level vector across all samples."
- [readme] The results are found to be more robust to noise and missing peaks compared to the alternatives (ORA, GSEA). This is particularly important for metabolomics peak data, where noise and missing peaks are prevalent.: "The results are found to be more robust to noise and missing peaks compared to the alternatives (ORA, GSEA). This is particularly important for metabolomics peak data, where noise and missing peaks"
- [readme] if all of the samples in a single experimental factor have intensities of zero these are replaced by the minimum intensity value (which can be set by the user); and if only some of the sample values in a factor are zero then these are replaced by the mean value of the non-zero samples in that factor. The data is subsequently transformed to log-2 base and standardised using the preprocessing module in Scipy: "The data is subsequently transformed to log-2 base and standardised using the preprocessing module in Scipy such that the intensity matrix has a zero mean and unit variance across the samples."
- [intro] decomposes activity levels in pathways via the PLAGE method: "decomposes activity levels in pathways via the PLAGE method"
- [intro] the decomposition approach in PALS is amenable to the analysis of any group of metabolite sets, not just pathways: "the decomposition approach in PALS is amenable to the analysis of any group of metabolite sets, not just pathways"
