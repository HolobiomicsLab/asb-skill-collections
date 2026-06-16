# Evaluation Strategy

## Direct Checks

- File exists: GitHub repository at https://github.com/qLSLab/integrate is accessible and contains scripts for reproducible workflow
- File exists: Zenodo deposit 10.5281/zenodo.5824504 is accessible and contains downloadable INTEGRATE code and documentation
- File exists: ENGRO2 metabolic model file in SBML format (S2 File) can be loaded from article SI or Zenodo deposit
- File exists: ENGRO2 metabolic model file in XLSX format (S3 File) is present in SI or Zenodo deposit
- File exists: Breast cell line multi-omics datasets (transcriptomics FPKM values, intracellular metabolomics profiles, extracellular flux measurements) are available in S1 File or deposited at MTBLS3597 and PRJNA767228
- File exists: Cell-relative metabolic models in SBML format for all five breast cell lines (MCF102A, MCF7, MDAMB231, MDAMB361, SKBR3) present in S1 Compressed File Archive
- Script runs: INTEGRATE pipeline scripts execute without errors when applied to ENGRO2 model with all three constraint types (nutrient availability type 1, extracellular fluxes type 2, transcriptomics-derived type 3)
- Output file format is: t-SNE plot image generated from uniform sampling of feasible flux distributions (FFD) for five cell lines, matching Fig 3D of published paper
- Value in range: t-SNE visualization shows clear spatial separation of five cell-line clusters in two-dimensional embedding space, consistent with qualitative appearance of Fig 3D
- Output matches reference: Computed FFD t-SNE coordinates cluster by cell line with inter-model separation greater than intra-model separation, matching the pattern shown in Fig 3D—robust to random seed initialization within expected variance for t-SNE algorithm
- Value in range: Correlation between experimental growth yield on glucose and in silico growth yield predictions is positive when all three constraint types are applied together (Fig 3E comparison), with Spearman correlation coefficient and p-value reported matching or closely approximating published values

## Expert Review

- Verify that the three constraint types (type 1: nutrient availability, type 2: extracellular flux ratios, type 3: transcriptomics-derived RAS bounds) are correctly formulated and applied according to equations (4), (6), (7), and (8) in the Methods section
- Verify that Reaction Activity Scores (RAS) are correctly computed from transcriptomics data using equations (1)–(3) and GPR logical operators (AND as minimum, OR as sum), with appropriate normalization
- Verify that uniform sampling of the constrained null space via optGpSampler achieves sufficient coverage of feasible flux region (one million samples across ten batches of 100,000 samples each as stated)
- Verify that t-SNE dimensionality reduction parameters (perplexity, learning rate, iteration count) are either specified in the code repository or match standard COBRApy/scikit-learn defaults used in scFBA and similar prior work
- Verify that cell-relative model construction correctly incorporates relative constraints that preserve within-cell and across-cell metabolic heterogeneity without making models cell-specific in absolute terms
- Verify that the five cell lines represent genuinely heterogeneous metabolic phenotypes based on measured intracellular metabolomics profiles (Fig 2D–E) and extracellular flux ratios (Fig 2F), confirming biological motivation for separation in constraint space
