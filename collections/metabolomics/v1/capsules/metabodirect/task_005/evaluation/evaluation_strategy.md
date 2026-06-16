# Evaluation Strategy

## Direct Checks

- verify file exists at https://doi.org/10.17605/OSF.IO/XFHZ9 containing S. fallax leachate peak-abundance data
- verify MetaboDirect version 0.3.4 (or later) is accessible at https://github.com/Coayala/MetaboDirect
- verify chemodiversity analysis step (Step 4) executes without runtime errors on S. fallax peak-abundance input files
- verify output contains numeric values for Shannon index, Gini-Simpson index, Chao1 richness estimator for both inoculated and control samples
- verify output contains numeric values for Rao's quadratic entropy computed using elemental composition, DBE, AImod, and Gibbs free energy as traits
- value of Chao1 richness estimator for inoculated samples is greater than control samples (higher metabolite richness in inoculated condition); exact threshold and statistical significance require expert review
- value of Rao's quadratic entropy (functional diversity) for inoculated samples is lower than control samples (lower functional diversity in inoculated condition); exact threshold and statistical significance require expert review

## Expert Review

- evaluate whether reported differences in richness and functional diversity between inoculated and control conditions match the quantitative results from Step 4 chemodiversity analysis
- assess biological plausibility: whether the pattern of higher richness but lower functional diversity in inoculated S. fallax leachate is consistent with known metabolic responses to microbial inoculation
- review trait selection for Rao's quadratic entropy calculation (elemental composition, DBE, AImod, Gibbs free energy) as appropriate proxies for functional diversity in dissolved organic matter context
- confirm that the S. fallax dataset structure and pre-processing (filtering, normalization) are correctly applied before chemodiversity step and match documented methods (Additional file 1, Table S3)
