# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Does standardising the raw strain correlation score by its hypergeometric expectation and variance improve comparability of scores across GCF-MF links of different sizes?: 'This effect of GCF and MF sizes on the strain correlation score can be mitigated by standardising the score. For a given GCF and MF, let G and M be the sets of strains contributing to the GCF and the'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] The standardised correlation score achieves a mean of -0.0060 for all links and 3.6717 for validated links (p=6.8302 × 10−64), compared to the raw score's means of 83.5144 and 14.6667 respectively, demonstrating that standardisation successfully enables comparison across links with different GCF and MF sizes.: 'Raw correlation 83.5144 (all), 14.6667 (validated); Standardised correlation -0.0060 (all), 3.6717 (validated), p-value 6.8302 × 10−64'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Crüsemann dataset: genomic data (antiSMASH-predicted BGCs and BiG-SCAPE GCFs) and metabolomic data (MS2 spectra grouped into MFs) with 120 strains and 8 validated links: 'The Crüsemann data set consists of 120 microbial strains with 8 validated links between a BGC and a MF'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Gross dataset: genomic and metabolomic data with 7 strains and 9 validated links between a BGC and a MF: 'the Gross data set consists of 7 strains with 9 validated links between a BGC and a MF'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Leão dataset: genomic and metabolomic data with 4 strains and 5 validated links between a BGC and a specific MS2 spectrum: 'the Leão data set contains 4 strains with 5 validated links between a BGC and a specific MS2 spectrum'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Raw strain correlation scores computed for all GCF-MF pairs in each dataset using the scoring function: start at zero; add 10 if strain produces metabolite and has BGC in GCF; subtract 10 if strain produces metabolite but no BGC in GCF; add 1 if strain has BGC but no metabolite; leave unchanged otherwise: 'starting from zero, for each strain in the population, add 10 to the score if the strain produces the metabolite and has a BGC in the GCF, subtract 10 from the score if the strain produces the'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Standardised strain correlation scores (s*_corr) for all GCF-MF pairs in the three datasets, including mean score for all links and validated links with p-value: 'Standardising the score gives a mean score of -0.006 for all links, and 3.6717 for validated links (Table 1)'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Distribution histograms and scatter plots (Figure 5 / S1 Fig) showing raw versus standardised strain correlation scores for validated links relative to all links in the three datasets: 'Distribution of the raw and standardised strain correlation scores, as well as the distribution of the scores for validated links (in black) relative to the distribution of scores for all links'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Statistical test results (t-test p-values) comparing mean scores for validated links versus all links under both raw and standardised scoring, demonstrating that standardisation enables reliable comparison: 'the null hypothesis for testing the validity of the scoring function is that both distributions of scores (for validated links and all links) have the same mean'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Table of proportions of validated links among top-scoring links (90th percentile and above) for raw, standardised, and combined scores across all three datasets: 'Table 2 shows the proportion of validated links among all possible GCF-MF links in the three data sets, both for all the potential links (first row), and for the links scoring above the 90th'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] antiSMASH: 'after downloading the strain assemblies and metabolomics data, the genomes were run through antiSMASH v5.0.0 for BGC detection'

## ev_012

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] BiG-SCAPE: 'and BiG-SCAPE v1.0.0 to cluster the BGCs into GCFs'

## ev_013

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] GNPS: 'the metabolomics data, the genomes were run through antiSMASH v5.0.0 for BGC detection and BiG-SCAPE v1.0.0 to cluster the BGCs into GCFs'

## ev_014

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] MIBiG: 'To assign one or more molecular structures to BGCs, according to how many high-scoring matches are found in MIBiG'

## ev_015

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] Exact mathematical formula for the hypergeometric expectation and variance used to standardise the raw strain correlation score σ_corr into σ*_corr: 'The standardised strain correlation score makes it more effective at prioritising validated links relative to all links, and introduced IOKR as a complementary feature-based scoring function.'

## ev_016

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] Detailed algorithm or pseudocode for computing standardised strain correlation score across all potential GCF-spectrum pairs in each dataset: 'The standardised strain correlation score still suffers from the drawback inherent in correlation-based scoring, of not being able to distinguish between potential links showing the same pattern of'

## ev_017

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] Specification of how many strains were shared between GCFs and MFs in the Crüsemann, Gross, and Leão datasets, and how this affects the hypergeometric calculation: 'An obvious example is prioritising multiple singleton GCFs and MFs for the same strain. As a complementary scoring function to the strain correlation score, IOKR does not have this limitation.'

## ev_018

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] Threshold or cutoff criteria for including or excluding strain correlation pairs in the standardisation computation (e.g., minimum strain overlap, maximum background correlation): 'The standardised strain correlation score makes it more effective at prioritising validated links relative to all links'
