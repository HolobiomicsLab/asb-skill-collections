# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] How does the MACS3 callpeak pipeline decompose into individual subcommands (filterdup, predictd, pileup, bdgcmp, bdgopt, bdgpeakcall) that progressively transform ChIP-Seq data into peak calls?: 'MACS3 does offer a range of subcommands that allow you to customize every step of your analysis'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] The MACS3 callpeak pipeline operates through sequential subcommands: filterdup removes duplicate reads, predictd estimates fragment length d from ChIP data, pileup generates coverage tracks, bdgcmp compares ChIP and control signals to compute p/q-value scores, bdgopt applies optimization to score tracks, and bdgpeakcall identifies peaks by filtering regions above a score cutoff.: 'we'll explain how you can accomplish this using the `filterdup` subcommand...This can also be accomplished using the `predictd` subcommand...generate a pileup track for the ChIP sample using the'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] CTCF_ChIP_200K.bed.gz (gzipped BED file with ChIP-Seq reads): 'We'll use two test files, `CTCF_ChIP_200K.bed.gz` and `CTCF_Control_200K.bed.gz`, which you can find in the MACS3 GitHub repository in the `test` directory'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] CTCF_Control_200K.bed.gz (gzipped BED file with control reads): 'We'll use two test files, `CTCF_ChIP_200K.bed.gz` and `CTCF_Control_200K.bed.gz`, which you can find in the MACS3 GitHub repository in the `test` directory'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] CTCF_ChIP_200K_filterdup.pileup.bdg (ChIP sample pileup track in BEDGRAPH format with fragment-extended coverage signals): 'This command produces a file in BEDGRAPH format, `CTCF_ChIP_200K_filterdup.pileup.bdg`, which contains the fragment pileup signals for the ChIP sample'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] local_lambda.bdg (local lambda bias track in BEDGRAPH format scaled to ChIP sequencing depth for statistical comparison): 'The output file is named `local_lambda.bdg`, as it contains values that represent the lambda (or expected value), which can be compared with ChIP signals using the local Poisson test'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] CTCF_ChIP_200K_qvalue.bdg or CTCF_ChIP_200K_pvalue.bdg (score track in BEDGRAPH format with -log10(q-values) or -log10(p-values) from local Poisson test): 'The `CTCF_ChIP_200K_pvalue.bdg` or `CTCF_ChIP_200K_qvalue.bdg` file contains the `-log10(p-values)` or `-log10(q-values)` for each base pair, derived through a local Poisson test'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] CTCF_ChIP_200K_peaks.bed (narrowPeak format BED file with called peak coordinates and summit locations): 'The output is essentially a narrowPeak format file (a type of BED file), which includes the locations of peaks with the summit location noted in the last column'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] macs3 filterdup: 'we'll explain how you can accomplish this using the `filterdup` subcommand'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] macs3 predictd: 'This can also be accomplished using the `predictd` subcommand, which we need to apply only to ChIP data'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] macs3 pileup: 'generate a pileup track for the ChIP sample using the MACS3 `pileup` subcommand'

## ev_012

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] macs3 bdgcmp: 'using the `bdgcmp` module, which outputs a score for each base pair in the genome'

## ev_013

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] macs3 bdgopt: 'apply the `bdgopt` subcommand'

## ev_014

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] macs3 bdgpeakcall: 'identify regions that surpass a specific score cutoff using the `bdgpeakcall` function for narrow peak calling'

## ev_015

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog or version history is available for the MACS3 project or this specific tutorial.: '_No changelog found._'
