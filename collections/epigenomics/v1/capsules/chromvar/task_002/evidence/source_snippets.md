# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] How can motifs be ranked by their variability in chromatin accessibility across cell populations, and which motifs show statistically significant differential deviation between distinct cell types?: 'aims to identify motifs or other genomic annotations associated with variability in chromatin accessibility between individual cells or samples'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] chromVAR is designed to identify motifs or other genomic annotations associated with variability in chromatin accessibility between individual cells or samples, enabling ranking and differential analysis of motif usage.: 'aims to identify motifs or other genomic annotations associated with variability in chromatin accessibility between individual cells or samples'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] chromVARDeviations object (dev) containing bias-corrected deviations and z-scores for JASPAR motifs matched to filtered peaks from 10 GM + 10 H1 example cells: 'dev <- computeDeviations(object = counts_filtered, annotations = motif_ix)'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Ranked variability data frame with motif names, standard deviation of z-scores, bootstrap confidence intervals, and p-values for variability > 1: 'variability <- computeVariability(dev)'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Differential-deviations results table with per-motif statistics comparing GM vs H1 cell types (p-values, test statistics): 'diff_acc <- differentialDeviations(dev, "Cell_Type")'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] chromVAR: 'computeVariability(dev)'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] R: 'library(chromVAR)'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] SummarizedExperiment: 'library(SummarizedExperiment)'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog found: '_No changelog found._'
