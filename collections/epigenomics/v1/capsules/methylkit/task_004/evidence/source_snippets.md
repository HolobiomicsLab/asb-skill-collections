# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Does overdispersion correction in calculateDiffMeth() with overdispersion='MN' produce more stringent statistical tests (higher q-values) compared to uncorrected differential methylation analysis?: 'This scaling parameter also effects the statistical tests and if there is overdispersion correction the tests will be more stringent in general.'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] The calculateDiffMeth() function with overdispersion='MN' parameter calculates a scaling parameter φ = X²/(N-P) to adjust variance as φ·n_i·π̂_i·(1-π̂_i), which makes statistical tests more stringent by correcting for variance in excess of binomial expectations and automatically switches from Chisq to F-test.: 'This can be corrected by calculating a scaling parameter φ and adjusting the variance as φ n_i \hat{\pi_i}(1-\hat{\pi_i}). `calculateDiffMeth` can calculate that scaling parameter and use it in'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] methylKit package with dataSim() and calculateDiffMeth() functions available in R environment: 'title: "methylKit: User Guide v`r packageVersion('methylKit')`"'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] methylDiff object containing differential methylation test statistics, p-values, and q-values from the overdispersion-corrected run: 'The calculateDiffMeth() function is the main function to calculate differential methylation'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Comparison report or figure showing q-value distributions (corrected vs. uncorrected) demonstrating that MN-corrected q-values are higher on average: 'Depending on the sample size per each set it will either use Fisher's exact or logistic regression'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] methylKit: 'title: "methylKit: User Guide v`r packageVersion('methylKit')`"'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] R: 'packageVersion('methylKit')'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog found.: '_No changelog found._'
