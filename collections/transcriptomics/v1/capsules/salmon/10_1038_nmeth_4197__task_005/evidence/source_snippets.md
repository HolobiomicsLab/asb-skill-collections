# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] How does the writeMappings flush bug in SAM output streaming affect record completeness, and what is the mechanism by which flushing the ostream buffer before close ensures all mapped reads appear in the output file?: 'the SAM output stream was wrapped in an ostream buffer that was not flushed before close, causing record loss'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] The writeMappings flush bug occurs when the SAM output stream buffer is not explicitly flushed before the stream closes, which causes buffered records to be lost. Flushing the ostream buffer before close ensures that all in-flight records are written to disk, preventing data loss and making the SAM record count match the number of mapped reads reported by salmon quant.: 'the SAM output stream was wrapped in an ostream buffer that was not flushed before close, causing record loss'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] salmon C++ source code repository (cpp branch): 'Its source is preserved on the [`cpp`](https://github.com/COMBINE-lab/salmon/tree/cpp) branch'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Test dataset: ERR458493 single-end 51 bp reads (S. cerevisiae): 'Reads: `ERR458493` (Gierliński/Schurch *S. cerevisiae* benchmark), 1,093,957 single-end 51 bp reads'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Reference transcriptome: Ensembl R64-1-1 cDNA (6,612 transcripts): 'Reference: Ensembl R64-1-1 cDNA, 6,612 transcripts'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Modified QuantOptionsUtils.cpp with force_flush = true on ostream_sink_mt: 'Fixed by enabling `force_flush` on the sink (`src/util/QuantOptionsUtils.cpp`)'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] SAM file containing all mapped read records without truncation or buffer loss: 'mapping records (written per batch) only reached disk when the `ofstream` buffer overflowed, so the trailing buffer was lost when the stream wasn't explicitly closed'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Verification report confirming SAM record count equals reported NumReads in quant.sf: 'with the placement diagnosis above possible'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] salmon 1.12.0: 'C++ salmon 1.11.4 vs. this Rust port, both selective-alignment mode'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] pufferfish: 'pufferfish's SSHash k-mer lookup, now fixed upstream'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No explicit mention of a writeMappings flush bug or its fix in the provided discussion section text: 'The section provides no technical details about the writeMappings function, buffer flushing, or any related bug fix'

## ev_012

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No specification of which salmon version (C++ 1.11.x, 1.12.0, or Rust 2.0.x) contained the writeMappings bug or when it was fixed: 'No version-specific discussion of the writeMappings issue is provided in the available text'

## ev_013

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No quantitative benchmarking details (runtime in seconds, peak memory in GB) are reported for the test datasets: 'index construction is faster, and peak memory is lower'

## ev_014

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No specification of which flag or option enables SAM output (writeMappings or equivalent) in salmon 2.0: 'The discussion does not list the command-line flag or option required to produce SAM output in salmon 2.0'
