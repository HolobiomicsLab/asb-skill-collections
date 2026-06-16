# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] How do getAnnotationCorrelation and getAnnotationSynergy quantify redundancy and synergy between two annotation sets in a chromVARDeviations object?: 'chromVAR is an R package for the analysis of sparse chromatin accessibility data from single cell or bulk ATAC or DNAse-seq data. The package aims to identify motifs or other genomic annotations'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] chromVAR provides functions to identify motifs or other genomic annotations associated with variability in chromatin accessibility between individual cells or samples, enabling analysis of annotation relationships within chromatin data.: 'The package aims to identify motifs or other genomic annotations associated with variability in chromatin accessibility between individual cells or samples.'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] chromVARDeviations object with computed deviations and z-scores, and rowData containing annotation metadata (fractionMatches, fractionBackgroundOverlap): 'dev <- computeDeviations(object = counts_filtered, annotations = motif_ix)'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Filtered peak count matrix (RangedSummarizedExperiment) with GC bias and sample/cell metadata: 'counts_filtered <- filterPeaks(counts_filtered, non_overlapping = TRUE)'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Two annotation matrices (e.g., motif and kmer matches) stored as assays in separate SummarizedExperiment objects or subset from the same object: 'getAnnotationCorrelation(counts_filtered, motif_ix[,c(83,24,20)])'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Named correlation matrix (CSV format) with annotation pair identifiers as row and column names and Pearson correlation coefficients as values, rows ordered by decreasing correlation magnitude: 'The function `getAnnotationCorrelation` first removes highly correlated annotations and low variability annotations and then computes the correlation between the cells for the remaining annotations'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Synergy score table (CSV format) with columns: annotation_pair, z_score, p_value, and variability_excess; one row per unique pairwise combination: 'The result is a matrix with Z-scores for the variability synergy of each possible pairing'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] chromVAR: 'getAnnotationSynergy(counts_filtered, motif_ix[,c(83,24,20)])'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] R: 'library(chromVAR)'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] SummarizedExperiment: 'library(SummarizedExperiment)'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Matrix: 'library(Matrix)'

## ev_012

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog documenting version history, API changes, or deprecated functions for chromVAR: '_No changelog found._'
