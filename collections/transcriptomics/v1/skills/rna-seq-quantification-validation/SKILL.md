---
name: rna-seq-quantification-validation
description: Use when you have quantification output from two versions or implementations of the same tool (e.g., C++ vs. Rust rewrites, pre- and post-bugfix releases) and need to verify that they produce equivalent results before deploying the new version.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3258
  edam_topics:
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_0769
  tools:
  - pufferfish
  - piscem-rs
  - minimap2
  - salmon
derived_from:
- doi: 10.1038/nmeth.4197
  title: salmon
evidence_spans:
- pufferfish's SSHash k-mer lookup, now fixed upstream
- The Rust port (built on piscem-rs, which derives orientation correctly)
- The Rust port (built on piscem-rs, which derives orientation correctly) was right all along
- minimap2 (full SW) on these reads gives near-identical quality profiles in both directions
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/transcriptomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_salmon
    doi: 10.1038/nmeth.4197
    title: salmon
  dedup_kept_from: coll_salmon
schema_version: 0.2.0
---

# RNA-seq Quantification Validation

## Summary

Validate transcript abundance quantification results across different implementations or versions by comparing mapping rates, per-read mapping agreement, and quantification metrics (NumReads, EffectiveLength) using equivalence-class correlation and differential mapping analysis. This skill detects hidden algorithmic bugs (e.g., k-mer orientation errors) that manifest as small but systematic mapping differences on real sequencing data.

## When to use

Apply this skill when you have quantification output from two versions or implementations of the same tool (e.g., C++ vs. Rust rewrites, pre- and post-bugfix releases) and need to verify that they produce equivalent results before deploying the new version. Use it to expose subtle algorithmic discrepancies that would otherwise go undetected in single-implementation workflows, especially when minor mapping-rate differences (~2%) are observed on real short-read data.

## When NOT to use

- When quantifying from alignments (BAM input mode) rather than raw reads, because SAM/BAM production depends on the upstream aligner and will embed those differences; use raw-read quantification (selective-alignment or sketch mode) for fair tool comparison.
- When inputs are not byte-identical (different index formats, reference versions, or k-mer lengths), because parameter divergence will mask algorithmic bugs; rebuild indices with identical k-mer lengths and decoy settings.
- When comparing single-cell quantification (alevin) outputs between versions, because single-cell workflows involve cell-barcode error correction and permit-list inference that add degrees of freedom; use bulk quantification validation first, then validate single-cell separately with alevin-fry.

## Inputs

- RNA-seq reads (FASTQ format): single-end or paired-end, e.g., ERR458493 (1,093,957 × 51 bp)
- Transcript reference (FASTA): cDNA or genomic annotation, e.g., Ensembl R64-1-1 (6,612 transcripts)
- Quantification output quant.sf files from both tool versions
- SAM/BAM alignments with mappings flag (-z flag in salmon quant)

## Outputs

- Mapping rate comparison table (percentage mapped per tool)
- Per-read mapping agreement matrix (read ID, tool A locus/strand, tool B locus/strand, agreement boolean)
- Pearson correlation report for NumReads and EffectiveLength metrics
- Differential mapping summary (reads uniquely mapped by one tool, fully unmapped in the other, orphaned, etc.)
- Chain pruning threshold audit (if applicable) showing orphanChainSubThresh and postMergeChainSubThresh effects

## How to apply

Quantify the same RNA-seq dataset (e.g., single-end or paired-end reads from a public benchmark like ERR458493) using both implementations with byte-identical parameters (library type, alignment mode, seed settings, bias-correction flags). Extract mapping rates (percentage of reads mapped) and per-read mapping agreement counts from each run's output log and SAM/quant.sf files. Compute Pearson correlation coefficients for quantification metrics (NumReads and EffectiveLength) between the two outputs using their quant.sf files. Cross-check placement of differentially mapped reads identified at the per-read level by inspecting SAM output to confirm strand and locus agreement and distinguish true algorithmic divergence from parameter-induced differences. Establish equivalence thresholds: mapping rates should match to within 1 read, per-read agreement should exceed 99%, and NumReads correlation should exceed 0.998. If gaps remain, use chain-pruning threshold profiles and k-mer lookup orientation traces to localize the source.

## Related tools

- **salmon** (Primary quantification tool; run twice (pre- and post-fix versions, or C++ vs. Rust) to produce quant.sf and SAM outputs for comparison) — https://github.com/COMBINE-lab/salmon
- **pufferfish** (Underlying k-mer index and orientation-lookup library; bug fixes in pufferfish (e.g., commit 5dce7f4) directly affect mapping-rate parity)
- **piscem-rs** (Rust-based mapper used in Rust salmon port; derives orientation correctly and serves as reference for validating C++ behavior)
- **minimap2** (Reference short-read aligner; use for independent alignment-based validation of differential mapping reads)

## Examples

```
salmon quant -i salmon_index -l U --validateMappings -z -o quant_v1 -r ERR458493.fastq && salmon quant -i salmon_index -l U --validateMappings -z -o quant_v2 -r ERR458493.fastq && python compare_quant.py --v1 quant_v1/quant.sf --v2 quant_v2/quant.sf --threshold 0.998
```

## Evaluation signals

- Mapping rate agreement within 1 read between tool versions (e.g., 85.55% vs. 85.55% on ERR458493 after pufferfish fix).
- Per-read mapping agreement ≥99.8% (e.g., 99.83% observed); reads mapping to different loci or strands flag algorithmic divergence.
- Pearson correlation of NumReads metric ≥0.998 (e.g., 0.99854 achieved post-fix); lower values indicate systematic quantification bias.
- Differential mapping breakdown accounting for ≥80% of unmapped discrepancy (e.g., chain-pruning threshold differences explain ~49k of ~62k reads).
- Cross-validation with minimap2 on differentially mapped reads confirms strand and locus placement consistency with external aligner.

## Limitations

- Chain-pruning thresholds (orphanChainSubThresh, postMergeChainSubThresh) differ between C++ and Rust implementations by design; ~80% of mapping gaps are describable and deferred, making perfect equivalence infeasible without threshold harmonization.
- Poly-A tail clipping (≥10 trailing As) is default in salmon; this preprocessing step must be identical across both tool versions or it will introduce spurious mapping differences unrelated to core algorithm bugs.
- Index format changes between major versions (e.g., salmon 1.x to 2.0) require complete index rebuilds; validation cannot proceed on mismatched index formats, even if the underlying reference is identical.
- Some less-frequently-used flags (e.g., --minAssignedFrags, --eqclasses, alternative inference modes) are not implemented in the Rust port, so validation is restricted to common workflows; niche features cannot be validated.
- Short-read datasets (e.g., 51 bp) are more sensitive to k-mer orientation bugs than longer reads; validation on short reads may over-detect minor algorithmic differences that do not materially affect typical 75+ bp RNA-seq workflows.

## Evidence

- [other] After the pufferfish SSHash streaming orientation bug fix, C++ salmon achieved 85.55% mapping rate, matching the Rust port to within 1 read, and NumReads Pearson correlation between C++ and Rust reached 0.99854 on byte-identical index.: "After fixing pufferfish (commit 5dce7f4, salmon pin bumped), C++ salmon maps the same reads: 83.48% → 85.55%, matching the Rust port to within 1 read"
- [methods] On real short reads the Rust port mapped ~2% more reads than C++ salmon. That extra ~2% was not a Rust 'sensitivity choice' — it exposed a k-mer-orientation bug in pufferfish's SSHash streaming lookup.: "On real short reads the Rust port mapped ~2% more reads than C++ salmon. That extra ~2% was not a Rust 'sensitivity choice' — it exposed a k-mer-orientation bug in pufferfish's SSHash streaming lookup"
- [methods] Per-read mapping agreement between C++ 1.12.0 and Rust is 99.83% on byte-identical index; NumReads Pearson correlation is 0.99854.: "per-read mapping agreement | 99.83%; NumReads Pearson | 0.99854"
- [methods] C++ prunes low-coverage chains/orphans before alignment using orphanChainSubThresh = 0.95 and postMergeChainSubThresh = 0.9; approximately 80% of the mapping gap between versions is due to these chain-sub-optimality defaults.: "~80% (~49k): a chain-sub-optimality default difference (describable, deferred). C++ prunes low-coverage chains/orphans before alignment using orphanChainSubThresh = 0.95 and postMergeChainSubThresh ="
- [methods] Extract mapping rates (percentage of reads mapped) from each run's output and compute NumReads and EffectiveLength Pearson correlation coefficients between C++ and Rust outputs using quant.sf files. Cross-check placement of reads identified as differentially mapped using writeMappings SAM output to confirm strand and locus agreement.: "Extract mapping rates (percentage of reads mapped) from each run's output. Compute NumReads and EffectiveLength Pearson correlation coefficients between C++ post-fix and Rust outputs using quant.sf"
- [methods] Quantify reads with C++ salmon 1.11.4 using salmon quant in selective-alignment mode with -l U (unstranded), no bias correction, writing mappings with -z flag. Repeat with the Rust salmon port using identical parameters.: "Quantify reads with C++ salmon 1.11.4 using salmon quant in selective-alignment mode with -l U (unstranded), no bias correction, writing mappings with -z flag. Repeat with the Rust salmon port with"
- [readme] It keeps the same workflow (`salmon index` → `salmon quant` → `quant.sf`) and the same output formats downstream tools read, but it is a new major version with some breaking changes. The most important one: **the index format changed, so you must rebuild your index.**: "It keeps the same workflow (`salmon index` → `salmon quant` → `quant.sf`) and the same output formats downstream tools read, but it is a new major version with some breaking changes. The most"
