---
name: fragment-length-estimation-cross-correlation
description: Use when when beginning ChIP-Seq analysis with single-end BED/SAM input and no prior knowledge of the library's fragment length.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3218
  edam_topics:
  - http://edamontology.org/topic_3169
  - http://edamontology.org/topic_3674
  tools:
  - macs3 predictd
  - macs3 filterdup
  - macs3 pileup
  - macs3 bdgpeakcall
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

# fragment-length-estimation-cross-correlation

## Summary

Estimate the DNA fragment length d in ChIP-Seq experiments by cross-correlation analysis of read pileups, a critical parameter that determines downstream peak calling accuracy and local background normalization. This skill uses MACS3's predictd subcommand to infer the typical distance between forward and reverse strand reads.

## When to use

When beginning ChIP-Seq analysis with single-end BED/SAM input and no prior knowledge of the library's fragment length. The fragment length is essential before generating coverage tracks and building local bias backgrounds, as it directly controls peak calling resolution (minimum peak length) and background normalization scales. Apply this skill immediately after duplicate filtering but before pileup track generation.

## When NOT to use

- Input is paired-end BED (BEDPE format) — use fragment length from BEDPE read pairs directly instead.
- Fragment length is already known from prior QC (e.g., Bioanalyzer, library prep documentation) — skip prediction and use known value to save compute time.
- Control-only or Input-only samples — predictd requires ChIP sample; cannot infer fragment length from background alone.

## Inputs

- Deduplicated ChIP-Seq BED file (single-end, post-filterdup)
- Genome size (integer, e.g., 'hs' for human haploid ~2.7 billion bp)
- mfold range (integers, default 5 50; defines fold-enrichment window for cross-correlation peak detection)

## Outputs

- Predicted fragment length d (integer, in base pairs)
- Cross-correlation plot (diagnostic, optional PDF output)
- Shift distance metrics (diagnostic output from predictd analysis)

## How to apply

Run macs3 predictd on deduplicated ChIP sample using default parameters: macs3 predictd -i <filtered_chip.bed> -g <genome_size> -m 5 50 (mfold range). The tool performs cross-correlation analysis by shifting reads across strands and identifying the lag distance with maximum correlation, yielding fragment length d (e.g., 254 bp for CTCF data). The predicted d is then used as --extsize parameter in macs3 pileup (ChIP coverage extension), as the extension size in control background tracks (d/2 for d-background, typically 127 bp), and as minimum peak length constraint in macs3 bdgpeakcall. Validate by checking that d is biologically plausible for your protocol (typically 100–500 bp for sonication-based ChIP).

## Related tools

- **macs3 predictd** (Cross-correlation-based fragment length inference from deduplicated ChIP reads; directly outputs d parameter for downstream pileup and peak calling) — https://github.com/macs3-project/MACS
- **macs3 filterdup** (Prerequisite: removes duplicate reads before predictd input to ensure fair cross-correlation signal) — https://github.com/macs3-project/MACS
- **macs3 pileup** (Consumes predicted d as --extsize parameter to generate strand-extended ChIP coverage track) — https://github.com/macs3-project/MACS
- **macs3 bdgpeakcall** (Uses d as minimum peak length constraint during final peak calling from q-value bedgraph) — https://github.com/macs3-project/MACS

## Examples

```
macs3 predictd -i CTCF_ChIP_200K.bed -g hs -m 5 50
```

## Evaluation signals

- Predicted d should be within expected range for the experimental protocol (sonication-based ChIP typically 100–500 bp; verify against Bioanalyzer/Agilent QC if available)
- Cross-correlation peak should be visually distinct and unambiguous in the shift distance plot (diagnostic output); bimodal or flat correlation suggests poor quality or over-sonication
- Downstream peak calls should be reproducible and consistent with biological expectations (e.g., CTCF peaks at known binding sites, comparable peak counts to published datasets)
- Local background scaling factors (0.254 and 0.0254 for slocal/llocal in default MACS3) should produce reasonable signal-to-noise ratios; extreme background values indicate problematic d estimation
- Peak minimum length (set to d in bdgpeakcall) should filter out spurious single-read peaks while retaining true ChIP-enriched regions

## Limitations

- Assumes mononucleosome library (~147 bp plus linker) or monoclonal antibody-driven fragment size distribution; fails or becomes unreliable for oligomeric protein complexes with heterogeneous footprints (e.g., multi-protein arrays).
- Sensitive to duplicate filtering settings (--keep-dup parameter); over-aggressive duplicate removal removes valid PCR replicates, reducing cross-correlation signal; under-filtering inflates d artificially.
- Genome size parameter (−g) must be accurate; miscalibration propagates to local lambda scaling and may distort q-value thresholds.
- Does not account for strand-specific biases or adapter contamination in single-end libraries; low-quality or contaminated reads may yield misleading d estimates.
- Cross-correlation method assumes ChIP reads follow expected positive strand/negative strand distribution; heavily degraded or fragmented samples may produce noisy or ambiguous predictions.

## Evidence

- [other] Predict fragment length d from filtered ChIP data using macs3 predictd with default mfold parameters -m 5 50 and genome size -g hs, yielding d=254 bp: "Predict fragment length d from filtered ChIP data using macs3 predictd with default mfold parameters -m 5 50 and genome size -g hs, yielding d=254 bp"
- [methods] This is a crucial step for analyzing ChIP-Seq with MACS3, as well as other types of data: "This is a crucial step for analyzing ChIP-Seq with MACS3, as well as other types of data"
- [methods] This can also be accomplished using the `predictd` subcommand, which we need to apply only to ChIP data: "This can also be accomplished using the `predictd` subcommand, which we need to apply only to ChIP data"
- [methods] Now that you've estimated the fragment length, we can proceed to generate a pileup track for the ChIP sample using the MACS3 `pileup` subcommand: "Now that you've estimated the fragment length, we can proceed to generate a pileup track for the ChIP sample using the MACS3 `pileup` subcommand"
- [methods] The final step in peak calling is to identify regions that surpass a specific score cutoff using the `bdgpeakcall` function for narrow peak calling: "identify regions that surpass a specific score cutoff using the `bdgpeakcall` function for narrow peak calling"
