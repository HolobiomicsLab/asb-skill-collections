# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] How does the choice of exponent p in the ℓp-norm combination function affect the enrichment of validated links in the top-ranking BGC-metabolite predictions?: 'Fig 8 shows the set of points (x, y) such that ℓp(x, y) = 1 for three values of p, demonstrating the parallels of the circle in ℓp to the distribution of scores'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] The ℓ1/2-norm combination function assigned the best rank to validated links in 10 out of 15 cases, including three instances where it substantially outperformed either individual scoring function alone (e.g., retimycin A ranked at 253 vs. much higher individual ranks).: 'In 10 out of the 15 validated links considered, the ℓ'1/2 score assigns the best rank to the validated link, including in three out of the first five cases where the link is unambiguous. For'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Standardised strain correlation scores (s'_corr) and standardised IOKR scores (s'_IOKR) for all GCF-MF links in Crüsemann, Gross, and Leão datasets: 'Table 2 shows the proportion of validated links among all possible GCF-MF links in the three data sets, both for all the potential links (first row), and for the links scoring above the 90th'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Validated link ground truth annotations for Crüsemann (8 validated links), Gross (9 validated links), and Leão (5 validated links) datasets: 'The Crüsemann data set consists of 120 microbial strains with 8 validated links between a BGC and a MF, the Gross data set consists of 7 strains with 9 validated links between a BGC and a MF, and the'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Table of validated-link enrichment ratios (proportion of validated links / proportion of all links) indexed by combination function type and exponent p, for 90th and 95th percentiles across all three datasets: 'Table 2 shows the proportion of validated links among all possible GCF-MF links in the three data sets, both for all the potential links (first row), and for the links scoring above the 90th'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Heatmap visualisation of validated-link enrichment as a function of exponent p (0.5–3.0) and combination function type, with colour intensity proportional to enrichment ratio: 'Fig 8 shows the set of points (x, y) such that ℓ_p(x, y) = 1, for three different values of p. This shows the form of the iso-lines of scores using the ℓ_p function for different values of p to'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Statistical significance test results (chi-square or Fisher exact p-values) comparing validated-link enrichment for each combination function against the baseline (either score alone) and against the reported ℓ₁/₂ function: 'Considering the 90th percentile per data set for both scores, and adding up the numbers of links in each category (validated or unvalidated, and scoring above 90th percentile for either or both'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Line plot showing rank improvement (median percentile rank of validated links) as a function of p for the ℓ_p family of norms: 'Table 4. The first two columns show the number of links scoring higher or equal to the validated link ordered by the IOKR and the standardised correlation scores, while the next three columns show'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Python (numpy, scipy.stats, pandas, matplotlib, seaborn): 'NPLinker creates objects for spectra, MFs, BGCs and GCFs in the data set, maintaining the hierarchical relationship between them'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No explicit statement of which values of p (exponent) were tested beyond those shown in Table 4, or whether additional combination function forms were evaluated at all.: 'Various values of p, or other functions to combine the scores, may improve the results'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] No reporting of validated-link enrichment ratios or p-values for the sensitivity analysis across different p values; only the baseline result (p=0.5 in combined function) is reported in Table 2.: 'Table 2 shows the proportion of validated links among all possible GCF-MF links in the three data sets, both for all the potential links, and for the links scoring above the 90th percentile'

## ev_012

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No supplementary figure or table explicitly presenting enrichment metrics as a function of combination function parameters for the three datasets.: 'By using both scores simultaneously, the prioritisation of hypothetical links can be made more effective'

## ev_013

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No quantitative guidance on optimal choice of p or combination function form; discussion mentions potential improvements but provides no empirical justification for which variant performs best.: 'Various values of p, or other functions to combine the scores, may improve the results'
