# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Does kmer size (6-mer vs 7-mer) affect the magnitude of chromatin accessibility variability scores computed by chromVAR?: 'Using kmers + PCA appears to be the best variant of chromVAR for clustering'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] chromVAR supports kmer-based annotation approaches as a viable method for analyzing chromatin accessibility variability, with kmers being suitable for deviation computation workflows.: 'Using kmers + PCA appears to be the best variant of chromVAR for clustering'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] example_counts dataset (SummarizedExperiment with peak-by-sample count matrix and rowRanges): 'data(example_counts, package = "chromVAR")'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] BSgenome.Hsapiens.UCSC.hg19 reference genome sequence: 'library(BSgenome.Hsapiens.UCSC.hg19)'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Numeric summary table with mean, median, and standard deviation of kmer variability scores for 6-mers and 7-mers: 'in general 7mers yield higher variability and are better starting points for assembling de novo motifs'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Kmer deviation object for 6-mers (RangedSummarizedExperiment with deviations and deviationScores assays): 'kmer_dev <- computeDeviations(counts_filtered, kmer_ix)'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Kmer deviation object for 7-mers (RangedSummarizedExperiment with deviations and deviationScores assays): 'kmer_dev <- computeDeviations(counts_filtered, kmer_ix)'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] chromVAR: 'library(chromVAR)'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] R: 'chromVAR is an R package'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] motifmatchr: 'library(motifmatchr)'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] SummarizedExperiment: 'library(SummarizedExperiment)'

## ev_012

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Matrix: 'library(Matrix)'

## ev_013

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] BiocParallel: 'library(BiocParallel)'

## ev_014

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] BSgenome.Hsapiens.UCSC.hg19: 'library(BSgenome.Hsapiens.UCSC.hg19)'

## ev_015

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog documenting version history, bug fixes, feature additions, or known issues for chromVAR: '_No changelog found._'
