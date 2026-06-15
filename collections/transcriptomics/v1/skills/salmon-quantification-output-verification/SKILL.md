---
name: salmon-quantification-output-verification
description: Use when after running salmon quant with the --writeMappings/-z flag to produce SAM output, or when investigating discrepancies between the number of mapped reads reported in quant.sf and the actual number of records written to the output SAM file.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3184
  edam_topics:
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_0199
  tools:
  - salmon 2.0
  - salmon 1.12.0
  - pufferfish
  - salmon
  - salmon 1.12.0 (C++ release)
derived_from:
- doi: 10.1038/nmeth.4197
  title: salmon
evidence_spans:
- Rust port
- 'salmon 2.0 (Rust): a user-facing summary of removed/ignored/new options lives in MIGRATION.md'
- C++ 1.12.0
- C++ 1.12.0 mapped | 33,446,029 (92.011%)
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

# salmon-quantification-output-verification

## Summary

Verify that salmon quantification output is complete and correct by cross-checking SAM record counts against reported transcript abundance metrics and ensuring buffer flushing prevents data loss during output stream closure.

## When to use

After running salmon quant with the --writeMappings/-z flag to produce SAM output, or when investigating discrepancies between the number of mapped reads reported in quant.sf and the actual number of records written to the output SAM file. Essential when data loss is suspected due to incomplete stream flushing.

## When NOT to use

- When using salmon in sketch mode (--sketch) without --writeMappings; SAM output is not generated in this mode.
- When quantifying from pre-computed BAM/SAM alignments via salmon quant -a; the input alignment file is not produced by salmon's output stream and does not require flush verification.
- When the quantification is run without the --writeMappings flag; no SAM output file is produced, so record count verification is not applicable.

## Inputs

- salmon quant output directory containing quant.sf
- SAM file produced by --writeMappings flag
- salmon 2.0 or salmon 1.12.0 compiled binary

## Outputs

- record count comparison (SAM records vs. NumReads)
- verification report confirming completeness
- flushed SAM file with all mapped reads present

## How to apply

First, ensure the salmon codebase is compiled with force_flush = true in the SAM output stream sink configuration (src/util/QuantOptionsUtils.cpp) to guarantee all buffered records are written before stream closure. Run salmon quant with --writeMappings/-z flag on your dataset, generating both a SAM output file and a quant.sf summary. Count the total number of SAM records in the output file using standard line-counting tools. Extract the NumReads value from the quant.sf file (the sum of reads assigned to all transcripts). Compare the SAM record count against NumReads: they should match exactly. If counts diverge significantly, verify that force_flush was enabled during compilation and re-run quantification. The flush mechanism ensures that in-flight records held in the ostream buffer are persisted to disk before the stream closes, preventing silent data loss.

## Related tools

- **salmon** (primary quantification and SAM output generation tool; requires --writeMappings flag to produce verifiable output) — https://github.com/COMBINE-lab/salmon
- **salmon 1.12.0 (C++ release)** (legacy quantification backend; final C++ version available for comparison against Rust rewrite) — https://github.com/COMBINE-lab/salmon/tree/cpp

## Examples

```
salmon quant -i salmon_index -l A -1 reads_1.fastq.gz -2 reads_2.fastq.gz -p 16 -o sample_quant --writeMappings && wc -l sample_quant/mappings.sam && grep -v '^@' sample_quant/quant.sf | awk '{sum+=$5} END {print sum}'
```

## Evaluation signals

- SAM record count equals NumReads total in quant.sf file (exact match required)
- No truncated or partial records at end of SAM file; file size is non-zero and stream closure is clean
- ostream_sink_mt configured with force_flush = true in compiled binary
- Byte-identical output across repeated runs with identical inputs, indicating deterministic flushing
- Per-read mapping agreement between multiple runs is ≥99.83% on identical index (reference baseline from article)

## Limitations

- Record count verification does not assess mapping quality or alignment correctness; it only confirms completeness of stream output.
- The flush mechanism assumes the ostream_sink_mt is properly initialized; misconfiguration in other parts of the pipeline may still cause data loss before records reach the sink.
- SAM output file verification requires read access and sufficient disk space; very large output files may be impractical to count with simple tools.
- Pearson correlation of NumReads between C++ 1.12.0 and Rust salmon 2.0 is 0.99854, indicating minor differences in mapping that are expected and not indicative of flush errors.

## Evidence

- [other] The writeMappings flush bug occurs when the SAM output stream buffer is not explicitly flushed before the stream closes, which causes buffered records to be lost.: "The writeMappings flush bug occurs when the SAM output stream buffer is not explicitly flushed before the stream closes, which causes buffered records to be lost."
- [other] Flushing the ostream buffer before close ensures that all in-flight records are written to disk, preventing data loss and making the SAM record count match the number of mapped reads reported by salmon quant.: "Flushing the ostream buffer before close ensures that all in-flight records are written to disk, preventing data loss and making the SAM record count match the number of mapped reads reported by"
- [other] Modify the sink configuration to set force_flush = true to ensure mapping records are flushed to disk before stream closure.: "Modify the sink configuration to set force_flush = true to ensure mapping records are flushed to disk before stream closure."
- [other] Run salmon quant with --writeMappings/-z flag on a test dataset (e.g., ERR458493 yeast reads against Ensembl R64-1-1 index), capturing both the SAM output and the quantification summary.: "Run salmon quant with --writeMappings/-z flag on a test dataset (e.g., ERR458493 yeast reads against Ensembl R64-1-1 index), capturing both the SAM output and the quantification summary."
- [other] Count the number of SAM records in the output file and compare against the NumReads total reported in quant.sf to verify record count matches the mapped read count.: "Count the number of SAM records in the output file and compare against the NumReads total reported in quant.sf to verify record count matches the mapped read count."
- [readme] salmon provides fast and bias-aware quantification of transcript expression by pairing a fast mapping stage with a massively-parallel statistical model (EM/VBEM over equivalence classes) to estimate transcript abundances.: "salmon is a wicked-fast program for highly-accurate, transcript-level quantification from RNA-seq data. It pairs a fast mapping stage — selective alignment, or alignment-free sketch mode — with a"
- [intro] salmon 2.0 maintains the same workflow (salmon index → salmon quant → quant.sf) and output formats as the previous version.: "It keeps the same workflow (`salmon index` → `salmon quant` → `quant.sf`) and the same output formats downstream tools read"
