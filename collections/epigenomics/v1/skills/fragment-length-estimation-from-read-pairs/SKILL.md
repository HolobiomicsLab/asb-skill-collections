---
name: fragment-length-estimation-from-read-pairs
description: Use when you have paired-end ChIP-Seq data (BEDPE format) and need to determine the empirical fragment length (insertion length) before peak calling. This is mandatory for paired-end ChIP-Seq workflows to ensure MACS3 correctly extends coverage tracks and calculates local bias;
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3218
  edam_topics:
  - http://edamontology.org/topic_3169
  - http://edamontology.org/topic_3673
  tools:
  - macs3 predictd
  - macs3 callpeak
  - MACS3
derived_from:
- doi: 10.1186/gb-2008-9-9-r137
  title: macs
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/epigenomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_macs
    doi: 10.1186/gb-2008-9-9-r137
    title: macs
  dedup_kept_from: coll_macs
schema_version: 0.2.0
---

# fragment-length-estimation-from-read-pairs

## Summary

Estimate the average sequencing fragment length from paired-end ChIP-Seq reads using cross-correlation analysis of read pair coordinates. This is a critical preliminary step that informs downstream pileup extension and peak calling sensitivity in ChIP-Seq analysis.

## When to use

Apply this skill when you have paired-end ChIP-Seq data (BEDPE format) and need to determine the empirical fragment length (insertion length) before peak calling. This is mandatory for paired-end ChIP-Seq workflows to ensure MACS3 correctly extends coverage tracks and calculates local bias; it is especially important when the biological fragment length is unknown or expected to deviate significantly from default assumptions.

## When NOT to use

- Input is single-end ChIP-Seq data (SAM, BAM, or BED format without read-pair information); fragment length estimation requires paired-end coordinate information.
- Fragment length has already been determined by external methods (e.g., Illumina fragment analyzer) and is being supplied manually via `--extsize` parameter; predictd estimation is redundant.
- Sample is a control/input library rather than the ChIP library; the article states predictd should be applied only to ChIP data, not controls.

## Inputs

- BEDPE file (paired-end ChIP sample, e.g., CTCF_PE_ChIP_chr22_50k.bedpe.gz)

## Outputs

- Fragment length estimate (scalar, reported in base pairs)
- Cross-correlation profile (internal, used to determine d)

## How to apply

Run `macs3 predictd` with the `-f BEDPE` flag on the paired-end ChIP sample to estimate the average insertion length via cross-correlation of forward and reverse reads. The subcommand analyzes the distribution of distances between paired reads and outputs a single fragment length estimate (typically reported in base pairs, e.g., ~253 bp for the CTCF_PE_ChIP_chr22_50k.bedpe.gz dataset). Record this estimated fragment length for use in subsequent `macs3 callpeak` and `macs3 pileup` steps. The estimated value should be validated against known biology (e.g., typical ChIP sonication fragment sizes) and inspected for outliers that suggest read-pair artifacts or misalignment. When fragment length is successfully estimated, proceed to peak calling without manually specifying `--extsize` in callpeak mode, allowing the paired-end mode to automatically handle fragment extent during pileup.

## Related tools

- **macs3 predictd** (Estimate average insertion length by cross-correlation analysis of paired-end read positions) — https://github.com/macs3-project/MACS
- **macs3 callpeak** (Peak calling with paired-end mode that consumes the estimated fragment length for automatic pileup extension) — https://github.com/macs3-project/MACS
- **MACS3** (Umbrella toolset providing paired-end ChIP-Seq analysis subcommands including predictd) — https://github.com/macs3-project/MACS

## Examples

```
macs3 predictd -i CTCF_PE_ChIP_chr22_50k.bedpe.gz -f BEDPE
```

## Evaluation signals

- Fragment length estimate is a positive integer within the expected range for sonicated DNA (typically 150–500 bp); check against known sonication target size or prior ChIP-Seq experiments.
- Cross-correlation profile converges to a single clear peak (not bimodal or noisy); inspect diagnostic plots if available.
- Subsequent `macs3 callpeak` with paired-end mode and no manual `--extsize` produces narrowPeak output with valid peak coordinates and summit positions.
- Genome background and local bias tracks calculated in downstream steps reflect the estimated fragment length (e.g., d background calculated using the reported d value).
- Peak coordinates and fold-enrichment metrics are stable when re-run on the same data; instability suggests unreliable fragment length estimation.

## Limitations

- Cross-correlation method requires sufficient paired-end read depth; sparse or low-quality read pairs may produce noisy or unreliable estimates.
- Estimate is global across the genome; local variation in fragment length due to chromatin structure or PCR bias is not captured.
- Method assumes reads are properly paired; misaligned or corrupted BEDPE files may yield erroneous estimates.
- Single estimate may not be appropriate for mixed-fragment-length libraries; predictd cannot segment fragments by source or PCR cycle.
- The article does not specify expected error bounds or confidence intervals for the fragment length estimate; no quantified uncertainty measure is documented.

## Evidence

- [methods] Decide the fragment length d: "This is a crucial step for analyzing ChIP-Seq with MACS3, as well as other types of data"
- [methods] macs3 predictd subcommand: "This can also be accomplished using the `predictd` subcommand, which we need to apply only to ChIP data"
- [methods] BEDPE input format for paired-end data: "if you run this on the `CTCF_PE_ChIP_chr22_50k.bedpe.gz` file in the test directory"
- [methods] Fragment length estimate use in callpeak: "Run macs3 callpeak with -f BEDPE flag on the paired-end ChIP sample without specifying --extsize (pileup automatically handles paired-end fragment extent)"
- [methods] Expected fragment length magnitude: "to estimate average insertion length (~253 bp) when processing paired-end ChIP-Seq data in the CTCF_PE_ChIP_chr22_50k.bedpe.gz file"
