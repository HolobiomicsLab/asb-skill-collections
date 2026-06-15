---
name: buffer-management-and-flush-protocols
description: Use when when quantifying or mapping RNA-seq reads with salmon quant using the --writeMappings (-z) flag, or in any streaming output scenario where record count discrepancies appear between reported totals (e.g., NumReads in quant.sf) and file contents (SAM record count).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3198
  edam_topics:
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_0199
  tools:
  - pufferfish
  - salmon
  - salmon 2.0
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

# buffer-management-and-flush-protocols

## Summary

Explicit flushing of output stream buffers before closure ensures that all in-flight records are written to disk, preventing data loss in streaming genomic applications. This skill is critical when SAM/BAM mappings or other streaming records risk being silently dropped due to unbuffered or lazy-flush I/O.

## When to use

When quantifying or mapping RNA-seq reads with salmon quant using the --writeMappings (-z) flag, or in any streaming output scenario where record count discrepancies appear between reported totals (e.g., NumReads in quant.sf) and file contents (SAM record count). Symptoms include fewer SAM records in the output file than the number of mapped reads reported by the quantification tool.

## When NOT to use

- Input is already a pre-aligned BAM file without streaming output requirements.
- Quantification mode does not produce SAM/BAM output (e.g., sketch mode without --writeMappings).
- Output streams are already configured with explicit force_flush=true or equivalent non-buffering I/O.

## Inputs

- SAM output stream with buffered mapping records
- quantification summary file (quant.sf) or equivalent record-count metadata
- streaming sequencing reads (FASTQ, BAM, or SAM input)

## Outputs

- Flushed SAM file with all mapped records persisted to disk
- Complete quantification output (quant.sf or equivalent) with record counts matching file contents

## How to apply

Locate the output stream initialization in the relevant source file (e.g., src/util/QuantOptionsUtils.cpp for salmon) where an ostream_sink_mt is created. Check whether force_flush is set to false (the default, non-flushing behavior). Set force_flush = true to ensure the ostream buffer is explicitly flushed before the stream closes, guaranteeing all buffered records are written to disk. Rebuild the tool with the corrected flush configuration. Validate by running the tool on test data (e.g., ERR458493 yeast reads against Ensembl R64-1-1), then count SAM records in the output file and confirm the count matches the NumReads total reported in quant.sf. Mismatch between reported and file-resident records indicates the flush was not applied.

## Related tools

- **salmon** (RNA-seq quantification tool whose SAM output stream buffer must be explicitly flushed before closure to prevent record loss) — https://github.com/COMBINE-lab/salmon
- **salmon 2.0** (Rust rewrite of salmon supporting --writeMappings flag; inherits buffer-flushing architecture from C++ 1.12.0) — https://github.com/COMBINE-lab/salmon
- **pufferfish** (k-mer index and streaming lookup backend for salmon; contributes to read mapping pipeline that feeds buffered SAM output)

## Examples

```
salmon quant -i salmon_index -l A -1 reads_1.fastq.gz -2 reads_2.fastq.gz -p 16 -o sample_quant -z; samtools view -c sample_quant/alignments.sam
```

## Evaluation signals

- SAM record count in output file equals NumReads total reported in quant.sf (or equivalent quantification summary).
- No discrepancy between 'number of mapped reads' (from quantification log or report) and 'number of SAM records' (wc -l or samtools view -c on output file).
- Rebuild source with force_flush=true and re-run on same test dataset; verify record count matches expected total.
- Byte-for-byte reproducibility of SAM output across multiple runs with identical input (deterministic flush order and buffer contents).
- Log output or tool diagnostics confirm 'flush completed before stream close' without warnings or buffering-related exceptions.

## Limitations

- Explicit flushing may incur modest I/O overhead on very large datasets; impact depends on system disk speed and buffer size configuration.
- Some streaming pipelines (e.g., those using custom ostream_sink implementations not derived from standard library) may require alternative flushing mechanisms or may not support force_flush parameter.
- Flush protocol does not guarantee atomicity across distributed or networked filesystems; local or SAN-mounted storage is assumed.
- If upstream mapping tool does not fully populate records before stream closure, flushing alone cannot recover data; the root mapping failure must be diagnosed separately.

## Evidence

- [other] The writeMappings flush bug occurs when the SAM output stream buffer is not explicitly flushed before the stream closes, which causes buffered records to be lost.: "The writeMappings flush bug occurs when the SAM output stream buffer is not explicitly flushed before the stream closes, which causes buffered records to be lost."
- [other] Flushing the ostream buffer before close ensures that all in-flight records are written to disk, preventing data loss and making the SAM record count match the number of mapped reads reported by salmon quant.: "Flushing the ostream buffer before close ensures that all in-flight records are written to disk, preventing data loss and making the SAM record count match the number of mapped reads"
- [other] Locate the SAM output stream initialization in src/util/QuantOptionsUtils.cpp where the ostream_sink_mt is created with force_flush = false. Modify the sink configuration to set force_flush = true to ensure mapping records are flushed to disk before stream closure.: "Locate the SAM output stream initialization in src/util/QuantOptionsUtils.cpp where the ostream_sink_mt is created with force_flush = false. Modify the sink configuration to set force_flush = true"
- [other] Count the number of SAM records in the output file and compare against the NumReads total reported in quant.sf to verify record count matches the mapped read count.: "Count the number of SAM records in the output file and compare against the NumReads total reported in quant.sf to verify record count matches the mapped read count."
- [other] Run salmon quant with --writeMappings/-z flag on a test dataset (e.g., ERR458493 yeast reads against Ensembl R64-1-1 index), capturing both the SAM output and the quantification summary.: "Run salmon quant with --writeMappings/-z flag on a test dataset (e.g., ERR458493 yeast reads against Ensembl R64-1-1 index)"
