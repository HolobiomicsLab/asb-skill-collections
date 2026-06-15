---
name: sam-bam-mapping-record-inspection
description: Use when after quantifying the same read set with two versions of a mapping/quantification tool (e.g., C++ salmon 1.11.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3198
  edam_topics:
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_0654
  tools:
  - pufferfish
  - piscem-rs
  - minimap2
  - salmon quant
  - samtools
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

# SAM/BAM Mapping Record Inspection

## Summary

Inspect individual read mappings in SAM/BAM output to validate strand orientation, locus placement, and per-read agreement between two quantification tools or versions. This skill is critical for diagnosing systematic biases in k-mer lookup, chain pruning, or alignment scoring that manifest as read-level discrepancies.

## When to use

After quantifying the same read set with two versions of a mapping/quantification tool (e.g., C++ salmon 1.11.4 vs. Rust salmon, or before/after a bug fix), use this skill when overall mapping-rate metrics agree but you need to verify that individual reads are assigned to the same strand and locus. Specifically apply it when a known fraction of reads maps differently between versions and you need to confirm whether the difference is spurious (bug) or a real sensitivity choice.

## When NOT to use

- When comparing quantifications across different reference transcriptomes (e.g., GRCh38 vs. GRCh37), as locus and strand comparisons will be non-deterministic.
- When one tool uses a different selective-alignment or chain-pruning mode (e.g., C++ orphanChainSubThresh = 0.95 vs. Rust default 0.75), as systematic mapping differences are expected; focus instead on abundance correlation.
- When the two quantifications used different library-type parameters (-l flag), as strand assignment is library-dependent and disagreement is not a bug.

## Inputs

- SAM file from version 1 (salmon quant with -z flag)
- SAM file from version 2 (salmon quant with -z flag)
- quant.sf abundance table from version 1
- quant.sf abundance table from version 2
- List or set of read IDs flagged as differentially mapped (optional but recommended)

## Outputs

- Per-read mapping agreement percentage (e.g., 99.83%)
- Strand and locus mismatch report (count of reads with RNAME or strand disagreement)
- Cross-referenced placement summary linking SAM discrepancies to abundance correlation impact
- Diagnostic SAM record pairs (QNAME, RNAME, POS, FLAG) for high-impact mismatches

## How to apply

Extract SAM output from both tool versions using the `-z` or `--writeMappings` flag during quantification, ensuring identical index and parameters (library type, bias correction mode, thread count). Parse the SAM files for reads identified as differentially mapped (e.g., by comparing NumReads counts or by sampling known outliers like ERR458493.850). For each differentially mapped read, inspect the RNAME (reference name), POS (position), and strand (FLAG field bit 4, reverse-complement indicator) to determine whether both versions map to the same transcript and strand. Cross-reference these records against the quant.sf output to understand whether the mapping disagreement affects abundance estimation or remains a minority edge case. Calculate per-read mapping agreement as (total reads with identical SAM placement) / (total mapped reads) × 100% and compare to a baseline of >99% agreement on byte-identical indices.

## Related tools

- **salmon quant** (Generate SAM output with -z/--writeMappings flag for per-read inspection) — https://github.com/COMBINE-lab/salmon
- **samtools** (Parse, filter, and compare SAM/BAM records by QNAME, RNAME, POS, and FLAG)
- **pufferfish** (Underlying k-mer index and lookup engine; bugs here (e.g., SSHash streaming orientation) manifest as strand/locus mismatches)
- **piscem-rs** (Rust mapper used in salmon 2.0; correct orientation handling can be verified by SAM inspection)

## Examples

```
salmon quant -i salmon_index -l U -r ERR458493.fastq --writeMappings=mappings.sam -o quant_v1 && salmon quant -i salmon_index -l U -r ERR458493.fastq --writeMappings=mappings_fixed.sam -o quant_v2 && samtools view -f 0x10 mappings.sam | awk '{print $1}' | sort > unmapped_v1.txt && diff <(samtools view mappings.sam | cut -f1,3,4) <(samtools view mappings_fixed.sam | cut -f1,3,4) | head -20
```

## Evaluation signals

- Per-read mapping agreement ≥99.8% on byte-identical index (ERR458493 test case achieved 99.83%)
- RNAME (transcript ID) is identical for ≥99.5% of reads mapped by both versions
- Strand (FLAG bit 4, reverse-complement flag) is identical for ≥99.5% of mapped reads
- Reads flagged as differentially mapped (e.g., mapped in version 1, unmapped in version 2) are <2% of total reads and correlate with known pruning threshold differences (e.g., orphanChainSubThresh)
- NumReads Pearson correlation between quant.sf files from both versions is ≥0.998 (indicating per-read mapping agreement does not degrade abundance estimation)

## Limitations

- SAM inspection is labor-intensive at scale; prioritize high-variance or known-problematic read IDs (e.g., very short reads, poly-A-rich sequences) rather than exhaustive comparison.
- Chain-pruning defaults (orphanChainSubThresh, postMergeChainSubThresh) can create systematic mapping differences (~80% of the mapping gap in ERR458493 test case) that are not bugs; SAM inspection alone cannot distinguish intentional sensitivity choices from orientation bugs without additional metadata (e.g., minimap2 validation).
- Per-read agreement does not directly measure abundance accuracy; a read mapped to the wrong isoform will reduce correlation even if strand and locus appear 'correct' within the quantification's own frame.
- Library-type detection (-l A, auto) can vary between versions; ensure identical library-type flags are used, or agreement comparisons become meaningless.

## Evidence

- [methods] Cross-check placement of reads identified as differentially mapped (e.g., ERR458493.850) using writeMappings SAM output to confirm strand and locus agreement.: "Cross-check placement of reads identified as differentially mapped (e.g., ERR458493.850) using writeMappings SAM output to confirm strand and locus agreement."
- [methods] After fixing pufferfish (commit 5dce7f4, salmon pin bumped), C++ salmon maps the same reads: 83.48% → 85.55%, matching the Rust port to within 1 read; per-read mapping agreement | 99.83%: "per-read mapping agreement | 99.83%"
- [methods] NumReads Pearson correlation between C++ and Rust on byte-identical index reached 0.99854, demonstrating that per-read mapping agreement translates to abundance correlation.: "NumReads Pearson | 0.99854"
- [methods] On real short reads the Rust port mapped ~2% more reads than C++ salmon. That extra ~2% was not a Rust 'sensitivity choice' — it exposed a k-mer-orientation bug in pufferfish's SSHash streaming lookup: "On real short reads the Rust port mapped ~2% more reads than C++ salmon. That extra ~2% was not a Rust 'sensitivity choice' — it exposed a k-mer-orientation bug in pufferfish's SSHash streaming lookup"
- [methods] C++ prunes low-coverage chains/orphans before alignment using orphanChainSubThresh = 0.95 and postMergeChainSubThresh = 0.9; ~80% of mapping gap is chain-sub-optimality default difference: "~80% (~49k): a chain-sub-optimality default difference (describable, deferred). C++ prunes low-coverage chains/orphans before alignment using orphanChainSubThresh = 0.95"
