# Workflow Challenge: `coll_salmon_workflow`


> Salmon 2.0 is a from-scratch Rust rewrite of the widely-used salmon RNA-seq quantification tool, maintaining the same workflow and output formats while achieving quantitative parity with the C++ 1.12.0 release on both simulated and real data.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 5-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

This work describes salmon 2.0, a complete Rust port of salmon that preserves the familiar index → quant workflow and downstream-compatible output formats. On a byte-identical reference index, salmon 2.0 achieves per-transcript Pearson correlations of 0.99854 (NumReads) and 0.99897 (TPM) with C++ salmon 1.12.0 on real short-read data (GEUVADIS ERR188044), with per-read mapping agreement at 99.83%. After fixing a genuine k-mer-orientation bug in pufferfish's SSHash streaming lookup (which affected C++ salmon 1.11.4), both implementations achieve 85.55% mapping rate on yeast benchmark data (ERR458493), matching within 1 read and reaching 0.99854 NumReads Pearson correlation. The ~0.19% total-count difference on byte-identical indices is attributable to default chain pruning thresholds: C++ salmon applies orphanChainSubThresh=0.95 and postMergeChainSubThresh=0.9 before alignment, while salmon 2.0 defaults both to 0.0, accounting for ~80% of the 62.8k-read mapping-count gap; matching these thresholds brings the tools to 92.038% agreement. The Rust port also documents the writeMappings SAM-output mechanism, which requires explicit buffer flushing to prevent record loss when the output stream is closed.

## Research questions

- How closely do the quantification results (NumReads and TPM) from salmon 2.0 (Rust rewrite) agree with salmon 1.12.0 (C++ version) when run in selective-alignment mode on the same dataset and index?
- Does the Rust port of salmon achieve equivalent mapping rates and correlation metrics to C++ salmon 1.11.4 after the pufferfish SSHash streaming orientation bug is fixed?
- Does applying C++ salmon 1.12.0's chain score thresholds (orphanChainSubThresh=0.95, postMergeChainSubThresh=0.9) to the Rust salmon port on ERR188044 reduce the mapping count gap and confirm that ~80% of the discrepancy is attributable to the orphan/post-merge pruning default difference?
- Does the mapping rate and NumReads Pearson correlation remain stable when the Rust mapper uses alternative seed representations (sparse fixed-k anchors, reference k-mer variants) instead of the default unitig-constrained approach?
- How does the writeMappings flush bug in SAM output streaming affect record completeness, and what is the mechanism by which flushing the ostream buffer before close ensures all mapped reads appear in the output file?

## Methods overview

Prepare a cleaned GRCh38 cDNA FASTA with deterministic non-ACGT replacement to ensure byte-identical indices across both salmon versions. Build a selective-alignment index using salmon 2.0 (Rust) with default parameters (k-mer length, threads, no special decoy handling unless documented). Build an identical index using C++ salmon 1.12.0 from the same cleaned FASTA with matching parameters. Quantify ERR188044 paired-end reads (36.35M, 76 bp) using salmon 2.0 in selective-alignment mode with auto-detect library type (-l A), no bias correction, and Rust-default chain-pruning thresholds (orphanChainSubThresh=0.0, postMergeChainSubThresh=0.0). Quantify the same reads using C++ salmon 1.12.0 with identical mapping settings (-l A, no bias) and C++ defaults (orphanChainSubThresh=0.95, postMergeChainSubThresh=0.9). Extract NumReads and TPM per transcript from both quant.sf files and compute Pearson correlations; compute total assigned NumReads difference as (Rust total − C++ total) / C++ total × 100%. Compare unmapped_names.txt files from both runs, extracting only fully-unmapped reads (code 'u'), and compute per-read mapping agreement as the fraction of reads on which both tools agree (mapped or unmapped). Validation: Pearson correlations for NumReads and TPM must both exceed 0.998 (reported 0.99854 and 0.99897); per-read mapping agreement must reach ≥99.8% (reported 99.83%); total NumReads difference must stay within ±0.5% (reported −0.19%). References: source article (DOI: 10.1038/nmeth.4197); ERR458493 (https://www.ncbi.nlm.nih.gov/sra/?term=ERR458493); ERR188044 (https://www.ncbi.nlm.nih.gov/sra/?term=ERR188044) Acquire ERR458493 single-end reads and Ensembl R64-1-1 cDNA reference. Build salmon index from reference using default parameters. Quantify reads with C++ salmon 1.11.4 (pre-fix) in selective-alignment mode (-l U, no bias, writeMappings enabled), extract mapping rate and quant.sf abundance table. Apply pufferfish commit 5dce7f4 (SSHash streaming orientation correction) and re-quantify with identical parameters; compare mapping rate and quant.sf to pre-fix run. Quantify reads using Rust salmon port with identical parameters; extract mapping rate and quant.sf. Compute NumReads and EffectiveLength Pearson correlations between C++ post-fix and Rust outputs. Cross-validate strand and locus placement of discordant reads (e.g., ERR458493.850) using SAM writeMappings output to confirm orientation fix causation. Validation: C++ pre-fix mapping rate = 83.48% ± 1 read, C++ post-fix = 85.55% ± 1 read matching Rust, NumReads Pearson ≥ 0.998, EffectiveLength Pearson ≥ 0.999. References: source article (DOI: 10.1038/nmeth.4197); ERR458493 (https://www.ncbi.nlm.nih.gov/sra/?term=ERR458493); ERR188044 (https://www.ncbi.nlm.nih.gov/sra/?term=ERR188044) Obtain a byte-identical reference index (GRCh38 cDNA, 193,759 transcripts) and GEUVADIS ERR188044 paired-end reads (36.35M, 76 bp). Execute salmon 2.0 quant on ERR188044 with selective alignment enabled, chain-pruning parameters set to C++ salmon 1.12.0 defaults (orphanChainSubThresh=0.95, postMergeChainSubThresh=0.9), and no bias correction. Extract and tabulate mapping outcomes: total mapped reads, mapping rate (%), per-read agreement with C++ baseline, Rust-only and C++-only read counts, NumReads and TPM Pearson correlations. Re-align boundary-case reads (those mapped by one tool but not the other) using minimap2 full Smith-Waterman to classify each as strong/weak/unaligned, assessing the symmetry and genuine-alignment quality of the residual disagreement. Validation: Rust mapping rate ≥92.03% (within 0.02% of C++ 1.12.0 baseline 92.011%); residual per-read disagreement <20,000 reads; per-read mapping agreement ≥99.8%; NumReads Pearson ≥0.998. References: source article (DOI: 10.1038/nmeth.4197); ERR458493 (https://www.ncbi.nlm.nih.gov/sra/?term=ERR458493); ERR188044 (https://www.ncbi.nlm.nih.gov/sra/?term=ERR188044) Load GEUVADIS ERR188044 (36.35M paired-end 76 bp reads) and byte-identical GRCh38 cDNA reference index (193,759 transcripts). Execute salmon 2.0 Rust mapper in selective-alignment mode with default seed representation (libType A, no bias, multi-threaded) and record mapping rate and NumReads per transcript. Re-run salmon mapper three times, each with an alternative seed representation (sparse fixed-k anchors, reference-extended MEMs, unitig-constrained uni-MEMs), recording mapping rate and per-transcript NumReads. Calculate Pearson correlation coefficient between NumReads vectors from each variant and the baseline default. Validation: confirm all variants achieve mapping rate within ≤0.01% of baseline and Pearson r ≥ 0.99999995 for NumReads, establishing seed granularity was not the root cause of prior C++ vs. Rust mapping discrepancies. References: source article (DOI: 10.1038/nmeth.4197); ERR458493 (https://www.ncbi.nlm.nih.gov/sra/?term=ERR458493); ERR188044 (https://www.ncbi.nlm.nih.gov/sra/?term=ERR188044) Inspect salmon C++ source code to locate ostream_sink_mt initialization in QuantOptionsUtils.cpp where force_flush is set to false. Modify the sink configuration to enable force_flush = true, ensuring all buffered mapping records are written to disk before stream closure. Rebuild salmon from the modified source code. Execute salmon index on the Ensembl R64-1-1 reference transcriptome. Run salmon quant in selective-alignment mode with --writeMappings flag on ERR458493 test reads. Extract the SAM record count (grep '^[^@]' output.sam | wc -l) and compare against the NumReads field in the generated quant.sf file. Validation: SAM record count must equal the reported NumReads in quant.sf, confirming no records were lost to buffer truncation. References: source article (DOI: 10.1038/nmeth.4197); ERR458493 (https://www.ncbi.nlm.nih.gov/sra/?term=ERR458493); ERR188044 (https://www.ncbi.nlm.nih.gov/sra/?term=ERR188044)

**Domain:** transcriptomics

**Techniques:** quantitative-structure-activity, statistical-analysis

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** Salmon 2.0 is a from-scratch Rust rewrite of the previous C++ salmon implementation. _[grounded: salmon_2_0]_
- **(finding)** Salmon 2.0 maintains the same workflow of salmon index → salmon quant → quant.sf. _[grounded: salmon_2_0]_
- **(finding)** The index format changed in salmon 2.0, requiring users to rebuild their indices. _[grounded: salmon_2_0]_
- **(finding)** Salmon 2.0 cannot read C++ (pufferfish) indices from the previous version. _[grounded: salmon_2_0]_
- **(finding)** Single-cell quantification functionality has been removed from salmon and moved to the alevin-fry ecosystem. _[grounded: alevin_fry]_
- **(finding)** The final C++ release of salmon is version 1.12.0.
- **(finding)** On clean/simulated data, C++ salmon and the Rust port both mapped 100% of sample_data with counts Pearson r = 0.99998.
- **(finding)** The Rust port mapped approximately 2% more reads than C++ salmon on real short reads.
- **(finding)** C++ salmon mapping rate on yeast reads was 83.48% before the pufferfish fix. _[grounded: pufferfish]_
- **(finding)** Rust port mapping rate on yeast reads was 85.55%. _[grounded: metric_rust_mapping_rate_yeast]_
- **(finding)** After the pufferfish fix, C++ salmon mapping rate increased to 85.55%. _[grounded: pufferfish]_
- **(finding)** The difference turned out to be a genuine bug in C++ salmon's pufferfish SSHash k-mer lookup. _[grounded: pufferfish]_
- **(finding)** The pufferfish orientation bug was introduced in the SSHash index refactor at salmon version 1.11.0 or later. _[grounded: pufferfish]_
- **(finding)** Pre-1.11 pufferfish using BooPHF is not affected by the orientation bug. _[grounded: pufferfish]_
- **(finding)** On a byte-identical index, per-read mapping agreement between C++ 1.12.0 and Rust is 99.83%. _[grounded: metric_per_read_agreement_human]_
- **(finding)** NumReads Pearson correlation between C++ 1.12.0 and Rust is 0.99854 on a byte-identical index. _[grounded: metric_numreads_pearson_yeast]_
- **(finding)** TPM Pearson correlation between C++ 1.12.0 and Rust is 0.99897. _[grounded: metric_tpm_pearson_human]_
- **(finding)** Total assigned NumReads difference between C++ and Rust is −0.19%. _[grounded: metric_numreads_diff_human]_
- **(finding)** C++ 1.12.0 mapped 33,446,029 reads (92.011%) on GEUVADIS ERR188044. _[grounded: dataset_err188044]_
- **(finding)** Rust mapped 33,508,687 reads (92.184%) on GEUVADIS ERR188044. _[grounded: dataset_err188044]_
- **(finding)** Rust maps 62,812 reads that C++ leaves fully unmapped.
- **(finding)** C++ maps only 154 reads that Rust doesn't map.
- **(finding)** Approximately 80% of the 62.8k mapping gap is due to chain-sub-optimality default difference.
- **(finding)** C++ salmon uses orphanChainSubThresh = 0.95 and postMergeChainSubThresh = 0.9 by default.
- **(finding)** Rust port defaults orphanChainSubThresh and postMergeChainSubThresh to 0.0 (off).
- **(finding)** Re-running Rust with C++ thresholds (0.95/0.9) brings mapping to 33,455,950 (92.038%).
- **(finding)** Selective-alignment quantification reproduces C++ salmon to per-transcript Pearson approximately 0.999.
- **(finding)** Index construction is faster in salmon 2.0 compared to the C++ version. _[grounded: salmon_2_0]_
- **(finding)** Peak memory is lower in salmon 2.0 compared to the C++ version. _[grounded: salmon_2_0]_
- **(finding)** Salmon 2.0 ships as a single portable binary with no Boost, CMake, or system libraries required. _[grounded: salmon_2_0]_
- **(finding)** Salmon 2.0 includes a new alignment-free --sketch mode for pseudoalignment. _[grounded: salmon_2_0]_
- **(finding)** Salmon 2.0 is licensed under BSD-3-Clause license. _[grounded: salmon_2_0]_
- **(finding)** Salmon results files (quant.sf, cmd_info.json, lib_format_counts.json, aux_info/meta_info.json) are unchanged between versions. _[grounded: quant_sf]_
- **(finding)** The Rust port (based on piscem-rs) was unaffected by the pufferfish k-mer orientation bug. _[grounded: piscem_rs]_
- **(finding)** The pufferfish orientation bug caused incorrect placement of reads with single non-canonical k-mers. _[grounded: pufferfish]_
- **(finding)** The --writeMappings flag in C++ salmon was silently dropping SAM records due to buffer flushing issues. _[grounded: write_mappings]_
- **(finding)** Commit 5dce7f4 in pufferfish fixed the k-mer orientation bug in the streaming lookup. _[grounded: pufferfish]_
- **(finding)** The dataset ERR458493 contains 1,093,957 single-end 51 bp yeast reads. _[grounded: dataset_err458493]_
- **(finding)** The reference used for yeast benchmarking contains 6,612 transcripts from Ensembl R64-1-1 cDNA. _[grounded: ref_ensembl_r64]_
- **(finding)** NumReads Pearson correlation between C++ and Rust on confidently mapped transcripts is 0.9989. _[grounded: metric_numreads_pearson_yeast]_
- **(finding)** EffectiveLength Pearson correlation between C++ and Rust is 0.9996. _[grounded: metric_effectivelength_pearson_yeast]_
- **(finding)** The ~2.8% total-count gap on mismatched indices was entirely due to per-index random N-replacement of ~100k non-ACGT bases.
- **(finding)** Approximately 20% (~17k) of the mapping gap is due to benign symmetric tie-break/chaining residual.
- **(finding)** The GEUVADIS ERR188044 dataset contains 36.35M paired-end 76bp reads. _[grounded: dataset_err188044]_
- **(finding)** Code contributions to salmon must use conventional commits format.
- **(finding)** Code contributed to salmon is licensed under GPLv3 with permission for re-licensing under BSD 3-clause.
- **(finding)** Pull requests to salmon should be made to the develop branch, not the master branch.
- **(finding)** Salmon 2.0 detects and rejects attempts to read C++ indices with a clear error message. _[grounded: salmon_2_0]_
- **(finding)** The canonical salmon citation is Patro et al. (2017) in Nature Methods.
- **(finding)** Salmon 2.0 can be installed via prebuilt binaries for x86-64 and aarch64 Linux and macOS. _[grounded: salmon_2_0]_
- **(finding)** Salmon 2.0 can be installed via cargo with Rust 1.91 or later. _[grounded: salmon_2_0]_
- **(finding)** The new --sketch mode is competitive in accuracy with dedicated pseudoaligners. _[grounded: sketch_mode]_

## Sanctioned method substitutions
Using any of these instead of the source method is **not penalized**:
- minimap2 full Smith-Waterman as alternative to selective alignment for validation
- sparse fixed-k anchors, reference-extended MEMs, or unitig-constrained uni-MEMs instead of piscem-rs MEM extraction
- C++ salmon (legacy) as alternative for reproducibility of older results
- Dedicated pseudoaligners as alternatives to sketch mode

## Invariants (must not change)
Changing any of these **is** a failure regardless of openness:
- preMergeChainSubThresh cannot be separately CLI-set in Rust port; uses loss-less ref-distance early-break instead of salmon's 0.75 pre-alignment prune
- cf1-rs cDBG builder does not expose bloom-filter size configuration unlike C++ salmon
- salmon 2.0 cannot read C++ (pufferfish) indices and requires index rebuild
- salmon alevin is removed; users must migrate to alevin-fry ecosystem

## Steps

### Step `task_001`
- Title: Reproduce per-transcript quantification agreement between Rust salmon 2.0 and C++ salmon 1.12.0 on ERR188044
- Task kind: `reproduction`
- Task: Run salmon 2.0 (Rust) and C++ salmon 1.12.0 in selective-alignment mode on GEUVADIS ERR188044 paired-end reads against a byte-identical GRCh38 cDNA index, then compute per-transcript Pearson correlations (NumReads and TPM), total NumReads difference, and per-read mapping agreement to reproduce reported parity metrics.
- Inputs:
  - GEUVADIS ERR188044 paired-end reads (36.35M reads, 76 bp)
  - GRCh38 cDNA reference (193,759 transcripts after deterministic N-replacement and cleaning)
  - salmon 2.0 (Rust implementation)
  - C++ salmon 1.12.0
- Expected outputs:
  - NumReads Pearson correlation coefficient between salmon 2.0 and C++ 1.12.0 (target: 0.99854)
  - TPM Pearson correlation coefficient between salmon 2.0 and C++ 1.12.0 (target: 0.99897)
  - Total assigned NumReads difference as percentage (target: −0.19%)
  - Per-read mapping agreement percentage (target: 99.83%)
  - Comparison table with salmon 2.0 and C++ 1.12.0 metrics and per-read disagreement details
- Tools: salmon 2.0, salmon 1.12.0, piscem-rs
- Landmark output files: salmon_2_0_index/, salmon_1_12_0_index/, salmon_2_0_quant/quant.sf, salmon_1_12_0_quant/quant.sf, correlation_analysis.csv, per_read_agreement.txt
- Primary expected artifact: `parity_metrics.csv`

### Step `task_002`
- Depends on: `task_001`
- Title: Reproduce mapping-rate parity between Rust salmon port and C++ salmon after pufferfish orientation fix on ERR458493
- Task kind: `reproduction`
- Task: Reproduce the mapping-rate and correlation metrics reported for yeast ERR458493 (single-end 51 bp reads, Ensembl R64-1-1 cDNA reference) using C++ salmon 1.11.4 before and after the SSHash k-mer-orientation fix, and the Rust salmon port, verifying the reported parity: C++ pre-fix 83.48%, post-fix 85.55%, Rust 85.55%, NumReads Pearson ≈0.99, EffectiveLength Pearson 0.9996.
- Inputs:
  - ERR458493 single-end 51 bp reads (1,093,957 reads) from ENA
  - Ensembl R64-1-1 cDNA reference (6,612 transcripts)
  - C++ salmon 1.11.4 (pre-fix) source code or binary
  - pufferfish commit 5dce7f4 (SSHash orientation fix patch)
  - Rust salmon port source code or binary
- Expected outputs:
  - Mapping rate (percentage of reads mapped) from C++ salmon 1.11.4 pre-fix: 83.48% (913,271 reads)
  - Mapping rate from C++ salmon 1.11.4 post-fix: 85.55% (935,851 reads)
  - Mapping rate from Rust salmon port: 85.55% (935,850 reads)
  - NumReads Pearson correlation between C++ post-fix and Rust (confidently mapped): ≥0.99
  - EffectiveLength Pearson correlation between C++ post-fix and Rust: 0.9996
  - Summary table with mapping rates, read counts, and Pearson correlations for all three runs
- Tools: salmon 2.0, salmon 1.11.4 (C++ version, pre-fix), salmon (Rust port), pufferfish, piscem-rs, minimap2
- Landmark output files: cpp_salmon_1.11.4_prefix.quant.sf, cpp_salmon_1.11.4_postfix.quant.sf, rust_salmon_port.quant.sf, cpp_prefix_mappings.sam, cpp_postfix_mappings.sam, rust_mappings.sam
- Primary expected artifact: `yeast_err458493_mapping_parity_report.csv`

### Step `task_003`
- Depends on: `task_001`
- Title: Reproduce the chain sub-threshold default as the primary explanation of the human mapping-rate gap
- Task kind: `reproduction`
- Task: Re-run Rust salmon on GEUVADIS ERR188044 with C++ salmon's chain-pruning thresholds (orphanChainSubThresh=0.95, postMergeChainSubThresh=0.9) and confirm mapping count converges to C++ 1.12.0's 92.011%, validating that ~80% of the observed gap is attributable to default threshold differences rather than algorithmic divergence.
- Inputs:
  - GEUVADIS ERR188044 paired-end RNA-seq reads (76 bp, 36.35M reads)
  - Byte-identical salmon index built from clean.fa (GRCh38 cDNA, 193,759 transcripts, deterministic N-replacement)
  - C++ salmon 1.12.0 reference mapping statistics (92.011%, 33,446,029 mapped reads, per-read agreement 99.83%)
- Expected outputs:
  - Salmon quantification output directory (quant.sf, aux_info/, lib_format_counts.json) for ERR188044 with orphanChainSubThresh=0.95 and postMergeChainSubThresh=0.9
  - Mapping statistics summary table: total mapped reads, mapping rate (%), per-read agreement with C++ 1.12.0, Rust-only and C++-only read counts, NumReads and TPM Pearson correlations
  - Classification of residual boundary-case reads (Rust-only, C++-only) by minimap2 full Smith-Waterman alignment quality (strong/weak/unaligned)
- Tools: salmon 2.0, salmon 1.12.0, minimap2, piscem-rs
- Landmark output files: quant.sf, aux_info/eq_classes.txt, mapping_rate.txt, residual_reads_quality.tsv
- Primary expected artifact: `mapping_stats_comparison.csv`

### Step `task_004`
- Depends on: `task_001`
- Title: Analyze the effect of seed representation variants on mapping rate and NumReads Pearson
- Task kind: `analysis`
- Task: Re-run the Rust salmon mapper on the GEUVADIS ERR188044 dataset using three alternative seed representations (sparse fixed-k anchors, reference-extended MEMs, and true unitig-constrained uni-MEMs), measure mapping rate and NumReads Pearson correlation under each variant, and verify that Pearson r remains ≥0.99999995 across all variants to confirm seed granularity was not the cause of prior mapping discrepancies.
- Inputs:
  - GEUVADIS ERR188044 paired-end 76 bp reads (36.35M reads)
  - Byte-identical GRCh38 cDNA reference index (193,759 transcripts)
- Expected outputs:
  - Mapping rate (%) for default seed representation
  - Mapping rate and NumReads Pearson r for sparse fixed-k anchor variant
  - Mapping rate and NumReads Pearson r for reference-extended MEM variant
  - Mapping rate and NumReads Pearson r for unitig-constrained uni-MEM variant
  - Summary table with per-variant mapping rate and Pearson r values
- Tools: salmon 2.0, piscem-rs
- Landmark output files: default_baseline_quant.sf, sparse_k_quant.sf, refmem_quant.sf, unimem_quant.sf, pearson_correlation_matrix.csv
- Primary expected artifact: `seed_variant_comparison.csv`

### Step `task_005`
- Depends on: `task_002`
- Title: Reconstruct the writeMappings SAM-flush bug fix and verify output record completeness
- Task kind: `component_reconstruction`
- Task: Implement the writeMappings SAM output flush fix (enable force_flush on the ostream_sink_mt to prevent record loss from unflushed buffers), then verify the corrected code produces a SAM file whose record count matches the number of mapped reads reported by salmon quant on a test dataset.
- Inputs:
  - salmon C++ source code repository (cpp branch)
  - Test dataset: ERR458493 single-end 51 bp reads (S. cerevisiae)
  - Reference transcriptome: Ensembl R64-1-1 cDNA (6,612 transcripts)
- Expected outputs:
  - Modified QuantOptionsUtils.cpp with force_flush = true on ostream_sink_mt
  - SAM file containing all mapped read records without truncation or buffer loss
  - Verification report confirming SAM record count equals reported NumReads in quant.sf
- Tools: salmon 2.0, salmon 1.12.0, pufferfish
- Landmark output files: QuantOptionsUtils.cpp.patch, salmon_rebuilt.log, quant.sf, record_count_validation.txt
- Primary expected artifact: `quant_mappings.sam`

## Final expected outputs

- `Salmon quantification output directory (quant.sf, aux_info/, lib_format_counts.json) for ERR188044 with orphanChainSubThresh=0.95 and postMergeChainSubThresh=0.9` (type: file, tolerance: hash)
- `Mapping statistics summary table: total mapped reads, mapping rate (%), per-read agreement with C++ 1.12.0, Rust-only and C++-only read counts, NumReads and TPM Pearson correlations` (type: file, tolerance: hash)
- `Classification of residual boundary-case reads (Rust-only, C++-only) by minimap2 full Smith-Waterman alignment quality (strong/weak/unaligned)` (type: file, tolerance: hash)
- `Mapping rate (%) for default seed representation` (type: file, tolerance: hash)
- `Mapping rate and NumReads Pearson r for sparse fixed-k anchor variant` (type: file, tolerance: hash)
- `Mapping rate and NumReads Pearson r for reference-extended MEM variant` (type: file, tolerance: hash)
- `Mapping rate and NumReads Pearson r for unitig-constrained uni-MEM variant` (type: file, tolerance: hash)
- `Summary table with per-variant mapping rate and Pearson r values` (type: file, tolerance: hash)
- `Modified QuantOptionsUtils.cpp with force_flush = true on ostream_sink_mt` (type: file, tolerance: hash)
- `SAM file containing all mapped read records without truncation or buffer loss` (type: file, tolerance: hash)
- `Verification report confirming SAM record count equals reported NumReads in quant.sf` (type: file, tolerance: hash)

## How your attempt will be scored

ASB defines seven rubrics in `workflow_rubric.py` (STEP_ORDERING, INTERMEDIATE_FIDELITY, END_TO_END_OUTPUT, TOOL_SELECTION, EFFICIENCY, CLAIM_VALIDATION, ADVERSARIAL_TRAP_AVOIDANCE). Which of them bind for *this* challenge depends on the tier and openness below.

### Tier evaluation profile

**Evaluator:** automated — filesystem presence + type-port resolution; END_TO_END_OUTPUT with declared per-output tolerance.
**Binding rubrics:** STEP_ORDERING, END_TO_END_OUTPUT (typed/tolerance), TOOL_SELECTION, CLAIM_VALIDATION.

### Openness stance

**Openness: closed — reproduction-first.** The deterministic rubrics above bind. A different method is acceptable ONLY if it appears under *Sanctioned method substitutions*; outputs are compared with the declared tolerance. Different is wrong here only when it departs from the sanctioned set or breaks an invariant.

## Workflow characterisation

_Suter et al. 2025 (DOI 10.1016/j.future.2025.107974)._

- **Coupling:** loose

- **Composition modularity:** flat

- **Abstraction level:** concrete

- **Orchestration planning:** static

- **Data transport:** file

- **Characterisation confidence:** inferred


## Submission

Produce two artifacts in your output directory:

1. The output files at the paths declared under **Final expected outputs**.
2. An `attempt.json` matching the schema below.
3. _(Optional)_ `attempt_metrics.json` with `wall_time_s`, `total_tokens`, `cost_usd` for the EFFICIENCY rubric.

### `attempt.json` schema

```json
{
  "workflow_id": "coll_salmon_workflow",
  "agent_order": [
    "task_001",
    "task_002",
    "task_003",
    "task_004",
    "task_005"
  ],
  "intermediate_outputs": {
    "task_001": {
      "<output_name>": "<locator>"
    },
    "task_002": {
      "<output_name>": "<locator>"
    },
    "task_003": {
      "<output_name>": "<locator>"
    },
    "task_004": {
      "<output_name>": "<locator>"
    },
    "task_005": {
      "<output_name>": "<locator>"
    }
  },
  "final_outputs": {
    "Salmon quantification output directory (quant.sf, aux_info/, lib_format_counts.json) for ERR188044 with orphanChainSubThresh=0.95 and postMergeChainSubThresh=0.9": "<locator>",
    "Mapping statistics summary table: total mapped reads, mapping rate (%), per-read agreement with C++ 1.12.0, Rust-only and C++-only read counts, NumReads and TPM Pearson correlations": "<locator>",
    "Classification of residual boundary-case reads (Rust-only, C++-only) by minimap2 full Smith-Waterman alignment quality (strong/weak/unaligned)": "<locator>",
    "Mapping rate (%) for default seed representation": "<locator>",
    "Mapping rate and NumReads Pearson r for sparse fixed-k anchor variant": "<locator>",
    "Mapping rate and NumReads Pearson r for reference-extended MEM variant": "<locator>",
    "Mapping rate and NumReads Pearson r for unitig-constrained uni-MEM variant": "<locator>",
    "Summary table with per-variant mapping rate and Pearson r values": "<locator>",
    "Modified QuantOptionsUtils.cpp with force_flush = true on ostream_sink_mt": "<locator>",
    "SAM file containing all mapped read records without truncation or buffer loss": "<locator>",
    "Verification report confirming SAM record count equals reported NumReads in quant.sf": "<locator>"
  },
  "chosen_tools": {
    "task_001": "<tool_name>",
    "task_002": "<tool_name>",
    "task_003": "<tool_name>",
    "task_004": "<tool_name>",
    "task_005": "<tool_name>"
  }
}
```

---
_Generated by `asb workflow-challenge` (see ASB docs/superpowers/specs/2026-05-12-workflow-evaluation-and-reviewer-ui-design.md)._
