---
name: k-mer-orientation-bug-diagnosis
description: Use when a Rust port or alternative implementation of a mapper (e.g., salmon, piscem) consistently maps 2–3% more reads than a C++ reference, especially on short reads.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3198
  edam_topics:
  - http://edamontology.org/topic_0080
  - http://edamontology.org/topic_3511
  tools:
  - pufferfish
  - piscem-rs
  - minimap2
  - salmon 1.11.4 (C++ version, pre-fix)
  - salmon (Rust port)
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

# k-mer-orientation-bug-diagnosis

## Summary

Diagnose and validate k-mer orientation bugs in SSHash-based k-mer lookup that manifest as spurious mapping-rate discrepancies between reference implementations (e.g., C++ vs. Rust ports). This skill isolates whether elevated mapping rates in one implementation reflect genuine sensitivity gains or expose upstream lookup logic errors by comparing per-read placements, correlation metrics, and strand-locus agreement on byte-identical indices.

## When to use

A Rust port or alternative implementation of a mapper (e.g., salmon, piscem) consistently maps 2–3% more reads than a C++ reference, especially on short reads. The discrepancy is unexplained by documented algorithmic choices (pruning thresholds, orphan handling) and per-read mapping agreement is high (>99%) but not perfect. Before attributing the gap to improved sensitivity, use this skill to rule out orientation bugs in underlying k-mer indexing (pufferfish's SSHash streaming lookup).

## When NOT to use

- Mapping-rate discrepancy is already explained by documented algorithmic choices (e.g., chain pruning thresholds documented as differing between implementations).
- Per-read mapping agreement is <95%, indicating a fundamental difference in read processing (e.g., adapter trimming, quality filtering) rather than orientation lookup.
- One implementation uses alignment-free (sketch) mode and the other selective-alignment; the modes are not directly comparable.

## Inputs

- single-end or paired-end FASTQ reads (e.g., ERR458493: 1,093,957 × 51 bp reads)
- reference cDNA transcriptome in FASTA format (e.g., Ensembl R64-1-1, 6,612 transcripts)
- two compiled mapper versions (pre-fix C++ and post-fix C++, or two ports) with identical k-mer length

## Outputs

- mapping rate (%) for each implementation
- per-read mapping agreement percentage (e.g., 99.83%)
- NumReads and EffectiveLength Pearson correlation coefficients between implementations
- differential-mapping read counts (reads mapped by one, fully unmapped by other)
- SAM alignments from writeMappings output for discordant reads (locus, strand, MAPQ)

## How to apply

Build a byte-identical k-mer index (same k-mer length, same reference, same index format) and run both implementations (pre-fix and post-fix, or two ports) on the same read set with identical parameters (e.g., selective-alignment mode, -l U, no bias correction, -z for mapping output). Extract and compare: (1) overall mapping rates (percentage of reads mapped); (2) per-read mapping agreement (count reads mapped to identical locus and strand in both runs); (3) NumReads and EffectiveLength Pearson correlations from quant.sf outputs; (4) differential-mapping subsets (reads one port maps that the other leaves fully unmapped, u). Examine SAM output via writeMappings flag for a subset of discordant reads to confirm strand and locus placement. If per-read agreement is >99.8% and correlation is >0.998 but mapping-rate gap persists, the discrepancy is likely due to chain pruning or alignment-scoring thresholds, not orientation. If agreement is lower and a specific git commit (e.g., pufferfish commit 5dce7f4) in the SSHash streaming overload resolves the gap, confirm that the commit addresses k-mer orientation (canonical vs. raw query) in the non-streaming lookup path.

## Related tools

- **salmon 1.11.4 (C++ version, pre-fix)** (Reference mapper implementation before pufferfish bug fix; run in selective-alignment mode with selective-alignment-specific parameters (-l U, -z for mappings)) — https://github.com/COMBINE-lab/salmon/tree/cpp
- **salmon (Rust port)** (Alternative implementation to compare; built on piscem-rs, which derives orientation correctly; run with identical parameters to C++ version) — https://github.com/COMBINE-lab/salmon
- **pufferfish** (Underlying SSHash-based k-mer index queried by both mappers; pufferfish commit 5dce7f4 (SSHash streaming orientation fix) is the suspected bug site) — https://github.com/COMBINE-lab/pufferfish
- **minimap2** (Full Smith-Waterman aligner used as orthogonal validation to confirm read placements are correct and to rule out mapper-specific issues)

## Examples

```
salmon quant -i salmon_index -l U --validateMappings -z -1 ERR458493.fastq.gz -o c_cpp_prefix_quant && salmon quant -i salmon_index -l U --validateMappings -z -1 ERR458493.fastq.gz -o rust_port_quant && paste c_cpp_prefix_quant/quant.sf rust_port_quant/quant.sf | awk '{print ($2-$5)^2}' | paste <(seq 1 6612) - | awk '{sum+=$2} END {print "RMSE=",sqrt(sum/NR)}'
```

## Evaluation signals

- Per-read mapping agreement ≥99.8% (e.g., 99.83%) between pre-fix and post-fix runs on byte-identical index; exact counts match within ≤1 read difference (e.g., 943,635 vs. 943,636).
- NumReads Pearson correlation ≥0.998 (e.g., 0.99854) between quant.sf outputs; EffectiveLength correlation similarly high (indicating systematic, not random, discrepancy resolution).
- Overall mapping rate converges after bug fix (e.g., C++ pre-fix 83.48% → post-fix 85.55%, matching Rust port 85.55%).
- Differential-mapping subset (reads one port leaves unmapped, the other maps) shrinks dramatically after fix; if ~80% of the gap is explained by known chain-pruning threshold differences, remaining discrepancy is attributable to orientation or other indexing logic.
- SAM-level strand and locus placement for discordant reads are identical post-fix across both implementations; locus agreement visible in writeMappings output.

## Limitations

- Orientation bugs may only manifest on short reads (<60 bp) where k-mer coverage and chaining are sparse; long reads may mask the issue due to multiple k-mer hits per read.
- Per-read agreement can be high (>99%) even if orientation is wrong in a small, low-coverage subset of reads; use NumReads/EffectiveLength correlation and overall mapping rate as tie-breakers.
- Chain pruning and alignment-scoring threshold differences (e.g., orphanChainSubThresh, postMergeChainSubThresh) can explain 50–80% of mapping-rate gaps independent of orientation bugs; differential-mapping analysis is necessary to rule out pruning as the sole cause.
- Bug fixes in upstream libraries (pufferfish) may not propagate immediately to all mapper versions; version pinning and git commit tracking are essential.

## Evidence

- [methods] On real short reads the Rust port mapped ~2% more reads than C++ salmon. That extra ~2% was not a Rust 'sensitivity choice' — it exposed a k-mer-orientation bug in pufferfish's SSHash streaming lookup: "On real short reads the Rust port mapped ~2% more reads than C++ salmon. That extra ~2% was not a Rust 'sensitivity choice' — it exposed a k-mer-orientation bug in pufferfish's SSHash streaming lookup"
- [methods] After fixing pufferfish (commit 5dce7f4, salmon pin bumped), C++ salmon maps the same reads: 83.48% → 85.55%, matching the Rust port to within 1 read: "After fixing pufferfish (commit 5dce7f4, salmon pin bumped), C++ salmon maps the same reads: 83.48% → 85.55%, matching the Rust port to within 1 read"
- [methods] per-read mapping agreement | 99.83%: "per-read mapping agreement | 99.83%"
- [methods] NumReads Pearson | 0.99854: "NumReads Pearson | 0.99854"
- [methods] Non-streaming lookups query the canonical k-mer word; The streaming lookup queries the raw query k-mer string: "Non-streaming lookups query the canonical k-mer word; The streaming lookup queries the raw query k-mer string"
- [methods] The Rust port (built on piscem-rs, which derives orientation correctly) was right all along: "The Rust port (built on piscem-rs, which derives orientation correctly) was right all along"
- [methods] Extract mapping rates (percentage of reads mapped) from each run's output. 7. Compute NumReads and EffectiveLength Pearson correlation coefficients between C++ post-fix and Rust outputs using quant.sf files. 8. Cross-check placement of reads identified as differentially mapped (e.g., ERR458493.850) using writeMappings SAM output to confirm strand and locus agreement.: "Extract mapping rates (percentage of reads mapped) from each run's output. 7. Compute NumReads and EffectiveLength Pearson correlation coefficients between C++ post-fix and Rust outputs using"
- [methods] ~80% (~49k): a chain-sub-optimality default difference (describable, deferred). C++ prunes low-coverage chains/orphans before alignment using orphanChainSubThresh = 0.95 and postMergeChainSubThresh =: "~80% of mapping gap due to chain-sub-optimality default difference; C++ prunes low-coverage chains with orphanChainSubThresh = 0.95"
