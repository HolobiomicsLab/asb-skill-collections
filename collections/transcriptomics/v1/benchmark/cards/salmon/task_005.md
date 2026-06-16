# SciTask Card: Reconstruct the writeMappings SAM-flush bug fix and verify output record completeness

- Task ID: `task_005`
- Schema version: `0.18.0`
- Created at: `2026-06-15T18:27:16.217915+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_transcriptomics/coll_salmon/synthesized_package`
- Domain: `bioinformatics`
- Subtask categories: `data-processing`, `benchmark-evaluation`
- DOI: `10.1038/nmeth.4197`
- GitHub: `COMBINE-lab/salmon`
- Input from: `task_002`

## Classification

- Task kind: `component_reconstruction`
- Article type: `research-article`
- Primary domain: `transcriptomics`
- Subdomains: `rna-seq`, `differential-expression`
- Techniques: `quantitative-structure-activity`, `statistical-analysis`

## Research Question
How does the writeMappings flush bug in SAM output streaming affect record completeness, and what is the mechanism by which flushing the ostream buffer before close ensures all mapped reads appear in the output file?

## Connected Finding
The writeMappings flush bug occurs when the SAM output stream buffer is not explicitly flushed before the stream closes, which causes buffered records to be lost. Flushing the ostream buffer before close ensures that all in-flight records are written to disk, preventing data loss and making the SAM record count match the number of mapped reads reported by salmon quant.

## Task Description
Implement the writeMappings SAM output flush fix (enable force_flush on the ostream_sink_mt to prevent record loss from unflushed buffers), then verify the corrected code produces a SAM file whose record count matches the number of mapped reads reported by salmon quant on a test dataset.

## Inputs
- salmon C++ source code repository (cpp branch)
- Test dataset: ERR458493 single-end 51 bp reads (S. cerevisiae)
- Reference transcriptome: Ensembl R64-1-1 cDNA (6,612 transcripts)

## Expected Outputs
- Modified QuantOptionsUtils.cpp with force_flush = true on ostream_sink_mt
- SAM file containing all mapped read records without truncation or buffer loss
- Verification report confirming SAM record count equals reported NumReads in quant.sf

## Expected Output File

- `quant_mappings.sam`

## Landmark Outputs

- `QuantOptionsUtils.cpp.patch`
- `salmon_rebuilt.log`
- `quant.sf`
- `record_count_validation.txt`

## Tools
- salmon 2.0
- salmon 1.12.0
- pufferfish

## Skills
- sam-record-parsing-and-validation
- c++-stream-io-debugging
- buffer-management-and-flush-protocols
- salmon-quantification-output-verification
- biological-sequence-read-mapping

## Workflow Description
1. Locate the SAM output stream initialization in src/util/QuantOptionsUtils.cpp where the ostream_sink_mt is created with force_flush = false. 2. Modify the sink configuration to set force_flush = true to ensure mapping records are flushed to disk before stream closure. 3. Rebuild the salmon codebase with the corrected flush configuration. 4. Run salmon quant with --writeMappings/-z flag on a test dataset (e.g., ERR458493 yeast reads against Ensembl R64-1-1 index), capturing both the SAM output and the quantification summary. 5. Count the number of SAM records in the output file and compare against the NumReads total reported in quant.sf to verify record count matches the mapped read count.

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `paper.md` | main_article | True |

## Data Deposits

| Kind | Accession | URL | Evidence |
|---|---|---|---|
| sra_run | `ERR458493` | https://www.ncbi.nlm.nih.gov/sra/?term=ERR458493 | tion correctly) was right all along.  ## Dataset  - Reads: `ERR458493` (Gierliński/Schurch *S. cerevisiae* benchmark),   1,093,95 |
| sra_run | `ERR188044` | https://www.ncbi.nlm.nih.gov/sra/?term=ERR188044 | set), so the only variable is the mapper. Reads: GEUVADIS `ERR188044` (36.35M 76bp PE); default selective alignment, `-l A`, no |

## Missing Information
- No explicit mention of a writeMappings flush bug or its fix in the provided discussion section text
- No specification of which salmon version (C++ 1.11.x, 1.12.0, or Rust 2.0.x) contained the writeMappings bug or when it was fixed
- No quantitative benchmarking details (runtime in seconds, peak memory in GB) are reported for the test datasets
- No specification of which flag or option enables SAM output (writeMappings or equivalent) in salmon 2.0

## Domain Knowledge
- The ostream_sink_mt with force_flush=false allowed mapping records to accumulate in the output buffer and be lost on stream closure if the buffer had not naturally overflowed.
- For small inputs, the large SAM @SQ header would overflow the buffer and mask the problem, but most records would be lost; verification requires matching record counts against the quantification summary.
- The --writeMappings/-z flag enables SAM output of per-read mapping details, essential for diagnosing mis-orientation and locus placement issues like the pufferfish SSHash k-mer bug.
- The fix must preserve all mapping records written during the quant phase; enabling force_flush ensures the trailing buffer is flushed before stream closure, even for small datasets.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.
- Synthesis grounding: the following tools/outputs were NOT found in the source paper and are inferred — verify before use: salmon 1.12.0, pufferfish, Modified QuantOptionsUtils.cpp with force_flush = true on ostream_sink_mt, SAM file containing all mapped read records without truncation or buffer loss, Verification report confirming SAM record count equals reported NumReads in quant.sf.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [methods] How does the writeMappings flush bug in SAM output streaming affect record completeness, and what is the mechanism by which flushing the ostream buffer before close ensures all mapped reads appear in the output file?: 'the SAM output stream was wrapped in an ostream buffer that was not flushed before close, causing record loss'
- `ev_002` from `agent2_synthesis` (agent2_traced): [methods] The writeMappings flush bug occurs when the SAM output stream buffer is not explicitly flushed before the stream closes, which causes buffered records to be lost. Flushing the ostream buffer before close ensures that all in-flight records are written to disk, preventing data loss and making the SAM record count match the number of mapped reads reported by salmon quant.: 'the SAM output stream was wrapped in an ostream buffer that was not flushed before close, causing record loss'
- `ev_003` from `agent2_synthesis` (agent2_traced): [methods] salmon C++ source code repository (cpp branch): 'Its source is preserved on the [`cpp`](https://github.com/COMBINE-lab/salmon/tree/cpp) branch'
- `ev_004` from `agent2_synthesis` (agent2_traced): [methods] Test dataset: ERR458493 single-end 51 bp reads (S. cerevisiae): 'Reads: `ERR458493` (Gierliński/Schurch *S. cerevisiae* benchmark), 1,093,957 single-end 51 bp reads'
- `ev_005` from `agent2_synthesis` (agent2_traced): [methods] Reference transcriptome: Ensembl R64-1-1 cDNA (6,612 transcripts): 'Reference: Ensembl R64-1-1 cDNA, 6,612 transcripts'
- `ev_006` from `agent2_synthesis` (agent2_traced): [methods] Modified QuantOptionsUtils.cpp with force_flush = true on ostream_sink_mt: 'Fixed by enabling `force_flush` on the sink (`src/util/QuantOptionsUtils.cpp`)'
- `ev_007` from `agent2_synthesis` (agent2_traced): [methods] SAM file containing all mapped read records without truncation or buffer loss: 'mapping records (written per batch) only reached disk when the `ofstream` buffer overflowed, so the trailing buffer was lost when the stream wasn't explicitly closed'
- `ev_008` from `agent2_synthesis` (agent2_traced): [methods] Verification report confirming SAM record count equals reported NumReads in quant.sf: 'with the placement diagnosis above possible'
- `ev_009` from `agent2_synthesis` (agent2_traced): [methods] salmon 1.12.0: 'C++ salmon 1.11.4 vs. this Rust port, both selective-alignment mode'
- `ev_010` from `agent2_synthesis` (agent2_traced): [methods] pufferfish: 'pufferfish's SSHash k-mer lookup, now fixed upstream'
- `ev_011` from `agent2_synthesis` (agent2_traced): [discussion] No explicit mention of a writeMappings flush bug or its fix in the provided discussion section text: 'The section provides no technical details about the writeMappings function, buffer flushing, or any related bug fix'
- `ev_012` from `agent2_synthesis` (agent2_traced): [discussion] No specification of which salmon version (C++ 1.11.x, 1.12.0, or Rust 2.0.x) contained the writeMappings bug or when it was fixed: 'No version-specific discussion of the writeMappings issue is provided in the available text'
- `ev_013` from `agent2_synthesis` (agent2_traced): [discussion] No quantitative benchmarking details (runtime in seconds, peak memory in GB) are reported for the test datasets: 'index construction is faster, and peak memory is lower'
- `ev_014` from `agent2_synthesis` (agent2_traced): [discussion] No specification of which flag or option enables SAM output (writeMappings or equivalent) in salmon 2.0: 'The discussion does not list the command-line flag or option required to produce SAM output in salmon 2.0'

## Evaluation Strategy
### Direct Checks
- file_exists: verify that salmon 2.0 source code repository (github:COMBINE-lab/salmon) contains a writeMappings function or equivalent SAM output handler
- script_runs: execute salmon 2.0 quant on a test dataset (human GEUVADIS ERR188044 or yeast ERR458493) with SAM output enabled (if available via --writeMappings or similar flag) and confirm the command completes without error
- output_matches_reference: retrieve the reported mapping count (total mapped reads) from salmon quant's standard output or log file on the test dataset
- row_count_equals: verify that the SAM output file record count (excluding header lines, byte-for-byte) matches the mapping count reported by salmon quant on the same test run
- file_format_is: verify that the SAM output file conforms to SAM format specification (header lines starting with @, data lines with tab-delimited fields)
- value_in_range: confirm that per-transcript selective-alignment quantification Pearson correlation vs. C++ salmon 1.12.0 remains at or above 0.999 on byte-identical index (robust to parameter choices)

### Expert Review
- Review salmon 2.0 source code (cpp branch and Rust rewrite) to identify and document the exact nature of the writeMappings flush bug: confirm whether an ostream buffer was indeed not flushed before close, and verify that the fix (if applied) correctly calls flush() or uses a non-buffered stream
- Verify that the fix does not introduce off-by-one errors, duplicate records, or corrupted SAM records in the output
- Assess whether the fix is consistent with SAM specification and whether downstream tools (e.g., samtools, alignment viewers) successfully parse the corrected SAM file without warnings or errors

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Methodology Summary
1. Inspect salmon C++ source code to locate ostream_sink_mt initialization in QuantOptionsUtils.cpp where force_flush is set to false.
2. Modify the sink configuration to enable force_flush = true, ensuring all buffered mapping records are written to disk before stream closure.
3. Rebuild salmon from the modified source code.
4. Execute salmon index on the Ensembl R64-1-1 reference transcriptome.
5. Run salmon quant in selective-alignment mode with --writeMappings flag on ERR458493 test reads.
6. Extract the SAM record count (grep '^[^@]' output.sam | wc -l) and compare against the NumReads field in the generated quant.sf file.
7. Validation: SAM record count must equal the reported NumReads in quant.sf, confirming no records were lost to buffer truncation.
8. References: source article (DOI: 10.1038/nmeth.4197); ERR458493 (https://www.ncbi.nlm.nih.gov/sra/?term=ERR458493); ERR188044 (https://www.ncbi.nlm.nih.gov/sra/?term=ERR188044)

## Workflow Ports

**Inputs:**

- `salmon_cpp_source` — salmon C++ source code repository ← `task_002/mapping_rate_cpp_prefix`
- `test_reads_fastq` — ERR458493 single-end 51 bp reads
- `reference_transcripts` — Ensembl R64-1-1 cDNA transcriptome

**Outputs:**

- `modified_source` — QuantOptionsUtils.cpp with force_flush enabled
- `sam_output` — SAM file from salmon quant --writeMappings
- `verification_report` — Record count verification against quant.sf NumReads

**Used:** `urn:asb:port:task_002/mapping_rate_cpp_prefix`

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:COMBINE-lab__salmon`
- **Synthesized at:** 2026-06-15T18:38:25+00:00

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
