# Evaluation Strategy

## Direct Checks

- verify that github:glasgowcompbio__PALS repository contains executable PALS implementation with PLAGE-based scoring
- verify that a metabolomics peak dataset (with noise and missing peak variants) is available in the repository or a linked public deposit (Zenodo/GitHub/MassIVE/MetaboLights)
- verify that ORA and GSEA implementations are available as callable tools or Python/R packages with pinned versions
- verify that comparison script produces three sets of pathway/metabolite-set scores (PALS, ORA, GSEA) on identical input
- verify output files contain quantitative robustness metrics (e.g., correlation, F1-score, or error rate) across noise levels and missing-peak percentages
- robust to parameter choices: confirm that metrics show PALS with lower variance or higher accuracy than ORA and GSEA across at least two independent noise-injection or peak-removal regimes

## Expert Review

- confirm that noise injection and missing-peak simulation strategies are methodologically sound and reproducible (e.g., Gaussian noise, random peak dropout percentages)
- confirm that reported robustness advantage (PALS vs ORA/GSEA) is statistically significant and not attributable to tuning bias or parameter mismatch
- confirm that the same metabolite-set annotations and pathway database are used for all three methods to ensure fair comparison
