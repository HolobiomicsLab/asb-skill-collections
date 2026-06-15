---
name: sam-record-parsing-and-validation
description: Use when salmon quant is run with the --writeMappings/-z flag and you need to verify that all mapped reads appear in the SAM output file.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3198
  edam_topics:
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_0080
  tools:
  - pufferfish
  - salmon
  - salmon quant
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

# SAM record parsing and validation

## Summary

Parse and validate SAM output records from salmon's mapping stage to ensure record completeness and detect data loss from buffer flushing failures. This skill diagnoses whether mapped reads are correctly serialized to disk by comparing SAM record counts against the NumReads quantification summary.

## When to use

Apply this skill when salmon quant is run with the --writeMappings/-z flag and you need to verify that all mapped reads appear in the SAM output file. Use it as a diagnostic check after rebuilding salmon code or when quantification results unexpectedly drop, to detect whether buffered records are being lost due to stream closure without explicit flush.

## When NOT to use

- salmon quant is run without the --writeMappings flag; no SAM output will be generated for validation.
- Input is already a quantified transcript abundance table (quant.sf only); SAM record parsing requires the raw mapping output.
- Validating single-cell or single-nucleus quantification; use alevin-fry ecosystem instead of salmon 2.0's removed salmon alevin mode.

## Inputs

- SAM output file from salmon quant --writeMappings
- quant.sf quantification summary file
- RNA-seq reads (FASTQ format)
- Transcript reference index (salmon index format)

## Outputs

- SAM record count (integer)
- NumReads total from quant.sf (integer)
- Record completeness validation report (boolean: counts match or mismatch)
- Per-record mapping agreement metrics (if comparing across versions)

## How to apply

Run salmon quant with --writeMappings/-z on a test dataset (e.g., ERR458493 yeast reads against Ensembl R64-1-1 index) to generate both SAM output and the quant.sf quantification summary. Parse the SAM output file and count the number of valid alignment records (lines not starting with '@'). Compare this count against the NumReads total reported in the quant.sf file's quantification summary. Record completeness is verified when SAM record count matches the NumReads value; a discrepancy indicates that buffered records were not flushed to disk before stream closure. The root cause is typically the force_flush parameter in the ostream_sink_mt configuration being set to false, which can be corrected by modifying src/util/QuantOptionsUtils.cpp and rebuilding.

## Related tools

- **salmon** (performs read mapping and writes SAM records with optional explicit flush to disk) — https://github.com/COMBINE-lab/salmon
- **salmon quant** (quantifies transcript abundance from reads and reports NumReads metric for comparison against SAM record count) — https://github.com/COMBINE-lab/salmon
- **pufferfish** (upstream k-mer indexing and lookup component used by salmon's selective alignment mapper)

## Examples

```
salmon quant -i salmon_index -l A -r reads.fastq.gz -p 16 -o sample_quant --writeMappings -z; wc -l sample_quant/mappings.sam; grep -v '^@' sample_quant/mappings.sam | wc -l; tail sample_quant/quant.sf | grep NumReads
```

## Evaluation signals

- SAM record count equals NumReads total from quant.sf; no buffered records were lost.
- Per-record mapping agreement ≥99% when comparing C++ salmon 1.12.0 to Rust salmon 2.0 on byte-identical index (e.g., 99.83% observed in benchmark).
- NumReads Pearson correlation ≥0.998 between quantification runs on different code versions or configurations.
- No truncation or corruption of SAM records at end-of-file; final records are complete and not partial writes.
- ostream_sink_mt force_flush parameter is set to true in QuantOptionsUtils.cpp, ensuring buffer flush before stream close.

## Limitations

- The findability of data loss depends on the size of the buffered records and the flush buffer capacity; small datasets may not exhibit loss even without explicit flush.
- Comparing SAM record counts across different salmon versions requires controlling for k-mer orientation bugs (e.g., pufferfish SSHash bug exposed ~2% mapping discrepancy in Rust port before fix) and chain-pruning threshold defaults (~80% of mapping gap between C++ and Rust due to orphanChainSubThresh=0.95 vs. default differences).
- The NumReads metric in quant.sf represents mapped reads assigned to transcripts; unmapped or fully orphaned reads may not appear in either SAM or NumReads counts, so absence from both sources does not indicate data loss.
- Single-cell quantification has moved to alevin-fry ecosystem; salmon 2.0 no longer supports --alevin mode, so this validation applies only to bulk RNA-seq or transcript-level workflows.

## Evidence

- [other] The writeMappings flush bug occurs when the SAM output stream buffer is not explicitly flushed before the stream closes, which causes buffered records to be lost.: "The writeMappings flush bug occurs when the SAM output stream buffer is not explicitly flushed before the stream closes, which causes buffered records to be lost."
- [other] Flushing the ostream buffer before close ensures that all in-flight records are written to disk, preventing data loss and making the SAM record count match the number of mapped reads reported by salmon quant.: "Flushing the ostream buffer before close ensures that all in-flight records are written to disk, preventing data loss and making the SAM record count match the number of mapped reads reported by"
- [other] Run salmon quant with --writeMappings/-z flag on a test dataset (e.g., ERR458493 yeast reads against Ensembl R64-1-1 index), capturing both the SAM output and the quantification summary.: "Run salmon quant with --writeMappings/-z flag on a test dataset (e.g., ERR458493 yeast reads against Ensembl R64-1-1 index), capturing both the SAM output and the quantification summary."
- [other] Count the number of SAM records in the output file and compare against the NumReads total reported in quant.sf to verify record count matches the mapped read count.: "Count the number of SAM records in the output file and compare against the NumReads total reported in quant.sf to verify record count matches the mapped read count."
- [methods] per-read mapping agreement | 99.83%: "per-read mapping agreement between C++ 1.12.0 and Rust is 99.83% on byte-identical index"
- [readme] It keeps the same workflow (`salmon index` → `salmon quant` → `quant.sf`) and the same output formats downstream tools read: "It keeps the same workflow (`salmon index` → `salmon quant` → `quant.sf`) and the same output formats downstream tools read"
- [methods] Reads: ERR458493 (Gierliński/Schurch S. cerevisiae benchmark), 1,093,957 single-end 51 bp reads; Reference: Ensembl R64-1-1 cDNA, 6,612 transcripts: "ERR458493 (Gierliński/Schurch S. cerevisiae benchmark), 1,093,957 single-end 51 bp reads; Reference: Ensembl R64-1-1 cDNA, 6,612 transcripts"
