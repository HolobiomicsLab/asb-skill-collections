---
name: read-mapping-rate-calculation
description: Use when when comparing mapping performance between two mapper implementations (e.g., C++ salmon vs. Rust salmon), validating that a bug fix or algorithmic change did not degrade sensitivity, or establishing baseline quantification quality on benchmark datasets with known characteristics.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3198
  edam_topics:
  - http://edamontology.org/topic_3308
  - http://edamontology.org/topic_3320
  tools:
  - pufferfish
  - piscem-rs
  - minimap2
  - salmon quant
  - salmon 2.0 (Rust)
  - salmon 1.12.0 (C++)
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

# read-mapping-rate-calculation

## Summary

Calculate the percentage of sequencing reads successfully mapped to a reference transcriptome after quantification, a core metric for validating mapper agreement and sensitivity across implementations and parameter configurations.

## When to use

When comparing mapping performance between two mapper implementations (e.g., C++ salmon vs. Rust salmon), validating that a bug fix or algorithmic change did not degrade sensitivity, or establishing baseline quantification quality on benchmark datasets with known characteristics.

## When NOT to use

- Input is already a quantification table (quant.sf) from a previous run — calculate mapping rate directly from the original quantification logs instead.
- Comparing across different reference transcriptomes or decoy configurations — mapping rate is not directly comparable unless index and reference are byte-identical.
- Assessing transcript-level abundance accuracy — use NumReads Pearson correlation or EffectiveLength agreement instead; mapping rate alone does not validate inference quality.

## Inputs

- sequencing reads (FASTQ or FASTA format; single-end or paired-end)
- reference transcriptome (FASTA)
- salmon index (or equivalent k-mer index)
- salmon quant output (standard output or log with mapping statistics)

## Outputs

- mapping rate (percentage of input reads mapped)
- absolute count of mapped reads
- quant.sf file (per-transcript quantification)
- per-read mapping agreement statistic (% of reads assigned identically across runs)

## How to apply

Run salmon quant (or equivalent mapper) on the same read dataset with identical parameters, extract the total number of reads mapped from the quantifier's standard output or log, then divide by the total number of input reads and multiply by 100 to yield mapping rate as a percentage. For byte-identical indices and fixed parameters, mapping rate should remain stable within ≤0.01% across runs; larger deviations (e.g., >0.5%) suggest algorithmic or implementation differences. Compare raw mapping-rate percentages alongside per-transcript output (quant.sf) and read-level agreement statistics (percent of reads assigned identically) to distinguish between sensitivity changes (different read counts mapped) and inference differences (same reads mapped, different abundance estimates).

## Related tools

- **salmon quant** (Quantify reads against transcriptome index and report mapping rate; standard output or log contains total mapped and unmapped read counts.) — https://github.com/COMBINE-lab/salmon
- **salmon 2.0 (Rust)** (Reference implementation for read quantification and mapping-rate reporting in selective-alignment mode.) — https://github.com/COMBINE-lab/salmon
- **salmon 1.12.0 (C++)** (Legacy C++ implementation for cross-version mapping-rate validation; available on cpp branch.) — https://github.com/COMBINE-lab/salmon/tree/cpp
- **pufferfish** (Underlying k-mer index and lookup engine; bugs in SSHash streaming orientation directly affect mapping-rate parity.)

## Examples

```
salmon quant -i salmon_index -l U -r reads.fastq -o quant_output && grep 'Mapping rate' quant_output/logs/salmon_quant.log
```

## Evaluation signals

- Mapping rate within ≤0.01% of baseline for byte-identical indices and fixed parameters; discrepancies >0.5% indicate algorithmic divergence.
- Per-read mapping agreement ≥99.83% when comparing two mapper implementations on the same reads (e.g., C++ vs. Rust salmon).
- Absolute read count difference between implementations ≤1 read on small datasets (<2M reads) or <0.001% relative difference on large datasets.
- NumReads Pearson correlation ≥0.99854 between quant.sf outputs from compared mappers, confirming that mapped reads are assigned to transcripts consistently.
- Chain-pruning and seed-representation defaults documented and held constant across comparison runs; if defaults differ, ~80% of observed mapping-rate gaps should be attributable to chain-suboptimality thresholds (orphanChainSubThresh, postMergeChainSubThresh).

## Limitations

- Mapping rate is sensitive to index byte-identity and k-mer lookup orientation; k-mer-orientation bugs in the underlying pufferfish SSHash can cause ~2% spurious sensitivity gains that do not reflect true mapper improvements.
- Chain pruning defaults (orphanChainSubThresh=0.95, postMergeChainSubThresh=0.9) differ between C++ and Rust implementations; ~80% of apparent mapping-rate divergence may be deferred parameter harmonization rather than fundamental algorithmic difference.
- Mapping rate does not directly measure inference accuracy; two mappers with identical mapping rates may produce different per-transcript abundance estimates if alignment scoring or equivalence-class assignment differs.
- Poly-A tail trimming (≥10 trailing As) is applied by default in salmon 2.0; disabling or changing this threshold alters mapping rate and must be held constant for valid comparison.

## Evidence

- [methods] After fixing pufferfish (commit 5dce7f4, salmon pin bumped), C++ salmon maps the same reads: 83.48% → 85.55%, matching the Rust port to within 1 read: "After fixing pufferfish (commit 5dce7f4, salmon pin bumped), C++ salmon maps the same reads: 83.48% → 85.55%, matching the Rust port to within 1 read"
- [methods] On real short reads the Rust port mapped ~2% more reads than C++ salmon. That extra ~2% was not a Rust 'sensitivity choice' — it exposed a k-mer-orientation bug in pufferfish's SSHash streaming lookup: "On real short reads the Rust port mapped ~2% more reads than C++ salmon. That extra ~2% was not a Rust 'sensitivity choice' — it exposed a k-mer-orientation bug in pufferfish's SSHash streaming lookup"
- [methods] Extract mapping rates (percentage of reads mapped) from each run's output. Compute NumReads and EffectiveLength Pearson correlation coefficients between C++ post-fix and Rust outputs using quant.sf files.: "Extract mapping rates (percentage of reads mapped) from each run's output. Compute NumReads and EffectiveLength Pearson correlation coefficients between C++ post-fix and Rust outputs using quant.sf"
- [methods] per-read mapping agreement | 99.83%: "per-read mapping agreement | 99.83%"
- [methods] C++ prunes low-coverage chains/orphans before alignment using orphanChainSubThresh = 0.95 and postMergeChainSubThresh = 0.9: "C++ prunes low-coverage chains/orphans before alignment using orphanChainSubThresh = 0.95 and postMergeChainSubThresh = 0.9"
