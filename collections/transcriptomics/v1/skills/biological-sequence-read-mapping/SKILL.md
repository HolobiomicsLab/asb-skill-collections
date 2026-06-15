---
name: biological-sequence-read-mapping
description: Use when you have raw FASTQ sequencing reads (single-end or paired-end) and a reference transcriptome FASTA file, and you need to determine which transcript(s) each read aligns to in order to quantify transcript abundance. This is the core mapping stage in a salmon quant workflow;
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3198
  edam_topics:
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_0654
  tools:
  - pufferfish
  - salmon 2.0
  - salmon 1.12.0 (C++)
  - piscem-rs
  - alevin-fry
derived_from:
- doi: 10.1038/nmeth.4197
  title: salmon
evidence_spans:
- pufferfish's SSHash k-mer lookup, now fixed upstream
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

# biological-sequence-read-mapping

## Summary

Map RNA-seq reads to a reference transcriptome using selective alignment (chaining, MEM extraction, and alignment scoring) or sketch-based mode to assign reads to transcript positions, enabling quantification of transcript abundances. This is a foundational step in RNA-seq pipelines that determines which reads contribute to the inference of transcript expression levels.

## When to use

You have raw FASTQ sequencing reads (single-end or paired-end) and a reference transcriptome FASTA file, and you need to determine which transcript(s) each read aligns to in order to quantify transcript abundance. This is the core mapping stage in a salmon quant workflow; apply it before abundance inference when you have reads but no pre-computed alignments, or when you want alignment-aware quantification with selective alignment mode (default) rather than alignment-free sketch mode.

## When NOT to use

- Input is already a BAM/SAM alignment file — use `salmon quant -a/--alignments` instead to skip the mapping stage and proceed directly to abundance inference.
- You require single-cell quantification — this skill is for bulk RNA-seq; single-cell processing has moved to the alevin-fry ecosystem (salmon alevin removed in 2.0).
- Your reference is genomic DNA rather than transcriptome — salmon is optimized for transcript-level mapping; genomic mapping requires different tools and settings.

## Inputs

- FASTQ reads (single-end or paired-end, gzip-compressed or uncompressed)
- reference transcriptome FASTA
- salmon index (pre-built from transcriptome)
- optional: decoy sequence FASTA (e.g., genomic DNA to absorb spurious hits)

## Outputs

- quant.sf file with per-transcript NumReads and TPM abundance estimates
- SAM/BAM alignment file (if --writeMappings flag used)
- quantification metadata (lib_format_counts.json, aux_info/)
- inferential replicates (if --numBootstraps or --numGibbsSamples used)

## How to apply

Build a salmon index from the reference transcriptome FASTA using `salmon index`, specifying k-mer length (default k=31), thread count, and optionally decoy sequences to absorb spurious alignments. Then run `salmon quant` with the reads and index, selecting library type (auto-detect with `-l A` or specify explicitly), mapping mode (default is selective alignment with chaining, MEM extraction, and alignment scoring; alternatively use `--sketch` for alignment-free mode), and key filtering parameters: `--minScoreFraction` (minimum alignment score as fraction of max possible), `--decoyThreshold` (decoy-aware filtering), and `--orphanChainSubThresh` / `--postMergeChainSubThresh` for chain pruning thresholds (C++ defaults 0.95 and 0.9). The selective alignment stage automatically clips poly-A tails (≥10 trailing As) matching pufferfish behavior. Output is a SAM/BAM alignment file (if `--writeMappings` is used) and quantification results in quant.sf with per-transcript NumReads and estimated abundances.

## Related tools

- **salmon 2.0** (primary mapper using selective alignment or sketch mode to assign reads to transcripts and compute per-transcript NumReads) — https://github.com/COMBINE-lab/salmon
- **salmon 1.12.0 (C++)** (legacy bulk-RNA mapper; final C++ release with identical workflow but older codebase) — https://github.com/COMBINE-lab/salmon/tree/cpp
- **pufferfish** (k-mer lookup and chaining engine underlying selective alignment; SSHash provides canonical/raw k-mer orientation determination)
- **piscem-rs** (Rust-based k-mer mapper used in single-cell pipelines (alevin-fry successor)) — https://github.com/COMBINE-lab/piscem
- **alevin-fry** (downstream quantification for single-cell/nucleus data; reads salmon RAD output) — https://github.com/COMBINE-lab/alevin-fry

## Examples

```
salmon index -t transcripts.fa -i salmon_index -p 16 && salmon quant -i salmon_index -l A -1 reads_1.fastq.gz -2 reads_2.fastq.gz -p 16 -o sample_quant --writeMappings
```

## Evaluation signals

- SAM record count matches or is within 1 read of the NumReads total reported in quant.sf (verifying no buffered records lost; relevant when using --writeMappings with force_flush=true)
- Per-read mapping agreement ≥99.83% between reference C++ and Rust implementations on byte-identical index (indicates correct orientation/chaining)
- NumReads Pearson correlation ≥0.9985 between two quantification runs or implementations on identical data (stability of mapping assignment)
- Mapping rate and per-transcript TPM values are consistent with published benchmarks (e.g., yeast ERR458493 maps 85.55% of reads to Ensembl R64-1-1 transcripts)
- Chain pruning and MEM extraction parameters produce expected trade-off: ~2% more reads mapped with Rust vs. C++ is expected only due to prior k-mer-orientation bugs (now fixed); post-fix, implementations should match within <0.01%

## Limitations

- Selective alignment is always on in salmon 2.0; cannot be disabled (unlike C++ 1.12.0). Trade performance/accuracy—sketch mode available as alternative if exact chaining is not needed.
- Index format changed between salmon 1.x and 2.0; users must rebuild indices from source transcriptome FASTA.
- Orphan chain pruning and post-merge chain subset thresholds differ between C++ and Rust by default (~80% of the ~2% mapping gap is due to chain-sub-optimality threshold differences), causing slight divergence in unmapped vs. mapped counts across versions.
- minAssignedFrags, eqclasses, alternativeInitMode, bootstrapReproject, numBiasSamples, sampleOut, and writeOrphanLinks flags are not implemented in Rust 2.0, limiting compatibility with some downstream workflows.
- Poly-A clipping (≥10 trailing As) is on by default; all-A sequences are dropped, which may affect rare transcript isoforms with genuine homopolymer regions.

## Evidence

- [methods] Selective alignment is always on; default clips poly-A tails: "Selective alignment is always on; default clips poly-A tails"
- [intro] salmon index → salmon quant → quant.sf workflow: "It keeps the same workflow (`salmon index` → `salmon quant` → `quant.sf`) and the same output formats downstream tools read"
- [methods] Per-read mapping agreement 99.83% between implementations: "per-read mapping agreement | 99.83%"
- [methods] Rust port mapped ~2% more reads than C++ due to k-mer-orientation bug: "On real short reads the Rust port mapped ~2% more reads than C++ salmon. That extra ~2% was not a Rust 'sensitivity choice' — it exposed a k-mer-orientation bug in pufferfish's SSHash streaming lookup"
- [methods] Chain pruning thresholds differ between versions: "~80% (~49k): a chain-sub-optimality default difference (describable, deferred). C++ prunes low-coverage chains/orphans before alignment using orphanChainSubThresh = 0.95 and postMergeChainSubThresh ="
- [readme] Decoy-aware indexing improves quantification: "Accounting for fragments of unexpected origin improves quantification. salmon can index decoy sequence (e.g. the genome) alongside the transcriptome so reads that would otherwise be spuriously"
- [methods] ERR458493 yeast dataset mapping rate: "Reads: ERR458493 (Gierliński/Schurch S. cerevisiae benchmark), 1,093,957 single-end 51 bp reads"
- [intro] Index format changed in salmon 2.0: "the index format changed, so you must rebuild your index"
- [readme] salmon is a wicked-fast program for transcript-level quantification: "`salmon` is a **wicked**-fast program for highly-accurate, transcript-level quantification from RNA-seq data. It pairs a fast mapping stage — *selective alignment*, or alignment-free *sketch* mode"
- [other] Flushing ostream buffer prevents buffered record loss: "Flushing the ostream buffer before close ensures that all in-flight records are written to disk, preventing data loss and making the SAM record count match the number of mapped reads reported by"
