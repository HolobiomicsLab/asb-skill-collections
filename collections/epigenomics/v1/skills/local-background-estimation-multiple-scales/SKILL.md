---
name: local-background-estimation-multiple-scales
description: Use when when performing ChIP-Seq peak calling with MACS3, after duplicate filtering and fragment length prediction (d), to construct the background model that will be compared against ChIP signal.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3445
  edam_topics:
  - http://edamontology.org/topic_3169
  - http://edamontology.org/topic_0749
  tools:
  - macs3 pileup
  - macs3 bdgopt
  - macs3 bdgcmp
  - macs3 filterdup
  - macs3 predictd
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

# local-background-estimation-multiple-scales

## Summary

Estimate local background noise in ChIP-Seq data by computing bias tracks at multiple genomic scales (fragment length d, 1 kb slocal, and 10 kb llocal windows) from control samples, then combining them to generate a normalized local lambda track. This multi-scale approach accounts for distance-dependent sequencing bias and improves the specificity of peak calling.

## When to use

When performing ChIP-Seq peak calling with MACS3, after duplicate filtering and fragment length prediction (d), to construct the background model that will be compared against ChIP signal. This is essential for any ChIP-Seq analysis where control samples are available and accurate peak calling requires accounting for regional sequencing biases beyond genome-wide background.

## When NOT to use

- When no control sample is available — genome-wide background only should be used instead.
- When input is single-end reads with fragment length d not yet predicted — predictd must be run first.
- When working with paired-end data in BEDPE format without converting to single-end fragment representation — pileup assumes single-end BED input.

## Inputs

- Filtered control BED file (deduplicated reads)
- Predicted fragment length d (in base pairs)
- Genome size (integer, e.g., 'hs' for human)
- ChIP and control read counts (for sequencing depth ratio calculation)

## Outputs

- d-background bedGraph track (fragment-length-scale local bias)
- slocal-background bedGraph track (1 kb window local bias)
- llocal-background bedGraph track (10 kb window local bias)
- Combined maximum background bedGraph track
- Normalized local lambda bedGraph track (final background model)

## How to apply

First, generate three control-derived background tracks using macs3 pileup with -B flag at three complementary scales: d-background at extension size d/2 (half the predicted fragment length), slocal background at 500 bp (or 1 kb default window), and llocal background at 5000 bp (or 10 kb default window). Normalize slocal and llocal backgrounds using macs3 bdgopt multiply with factors 0.254 and 0.0254 respectively (ratios of extension size to original scale). Combine the three background tracks using macs3 bdgcmp max operation to determine the maximum bias at each genomic position. Add the genome-wide background constant (calculated as number_of_control_reads × fragment_length / genome_size) using macs3 bdgopt. Finally, scale the combined background by the ChIP-to-control sequencing depth ratio using macs3 bdgopt multiply to create the final local lambda track. This multi-scale combination ensures that local enrichment is measured relative to the most relevant background at each genomic location.

## Related tools

- **macs3 pileup** (Generate control pileup coverage tracks at multiple extension sizes (d/2, 500 bp, 5000 bp) to quantify local background bias) — https://github.com/macs3-project/MACS
- **macs3 bdgopt** (Normalize slocal and llocal backgrounds by multiplication factors (0.254, 0.0254) and scale combined background by sequencing depth ratio) — https://github.com/macs3-project/MACS
- **macs3 bdgcmp** (Combine three background tracks using max operation to select the highest local bias at each genomic position) — https://github.com/macs3-project/MACS
- **macs3 filterdup** (Pre-processing step to remove duplicate reads from control sample before background estimation) — https://github.com/macs3-project/MACS
- **macs3 predictd** (Pre-processing step to determine fragment length d used to set the d-background extension size (d/2)) — https://github.com/macs3-project/MACS

## Examples

```
macs3 pileup -i CTCF_Control_200K.bed -o control_d_bg.bdg -B --extsize 127 && macs3 pileup -i CTCF_Control_200K.bed -o control_slocal_bg.bdg -B --extsize 500 && macs3 pileup -i CTCF_Control_200K.bed -o control_llocal_bg.bdg -B --extsize 5000 && macs3 bdgopt -i control_slocal_bg.bdg -m multiply -p 0.254 -o control_slocal_norm.bdg && macs3 bdgcmp -t control_d_bg.bdg -c control_slocal_norm.bdg -m max -o control_max_bg.bdg
```

## Evaluation signals

- d-background, slocal-background, and llocal-background bedGraph tracks each contain exactly one score per genomic position with no gaps or overlaps.
- Normalized slocal and llocal values should be proportional to extension size; verify that scaling factors (0.254 and 0.0254) produce reasonable value ranges (order of magnitude check).
- Combined maximum background track contains, at each position, the maximum value observed across the three input background tracks.
- Final local lambda track values should be strictly positive and scale with ChIP-to-control read count ratio; genome-wide background constant should be visible in regions with uniform control coverage.
- Local lambda values should increase with larger genomic scales (d < slocal < llocal) in high-coverage regions, reflecting the progressively larger windows used to estimate bias.

## Limitations

- Multi-scale background estimation assumes that control samples represent true background; if control samples contain biological signal or contamination, bias estimates will be inflated and peak calling specificity may be reduced.
- The default scales (d/2, 1 kb, 10 kb) are heuristic and may not be optimal for all ChIP-Seq experiments; very weak or very strong enrichment patterns may require parameter tuning.
- Normalization factors (0.254, 0.0254) are fixed and derived from default scale ratios; custom window sizes require recalculation of these factors.
- The max-background-combination strategy prioritizes local bias over other scales; in regions with extremely high local coverage, very large-scale (llocal) bias may be masked, potentially underestimating background in sparse genomic regions.

## Evidence

- [methods] By default, the MACS3 `callpeak` function calculates local bias by considering the maximum bias from the surrounding 1kb, 10kb, the fragment length `d`, and the whole genome background: "By default, the MACS3 `callpeak` function calculates local bias by considering the maximum bias from the surrounding 1kb, 10kb, the fragment length `d`, and the whole genome background"
- [other] Build local bias tracks from filtered control data using macs3 pileup with -B option at three scales (d/2=127 bp for d-background, 500 bp for 1 kb slocal, 5000 bp for 10 kb llocal), then normalize slocal and llocal backgrounds with macs3 bdgopt multiply operation (factors 0.254 and 0.0254 respectively).: "Build local bias tracks from filtered control data using macs3 pileup with -B option at three scales (d/2=127 bp for d-background, 500 bp for 1 kb slocal, 5000 bp for 10 kb llocal), then normalize"
- [other] Combine background tracks using macs3 bdgcmp max operation to determine maximum bias, then incorporate genome-wide background (0.0188023) via macs3 bdgopt.: "Combine background tracks using macs3 bdgcmp max operation to determine maximum bias, then incorporate genome-wide background (0.0188023) via macs3 bdgopt."
- [other] Scale combined background by ChIP-to-control ratio (0.99858) using macs3 bdgopt multiply to create local lambda track.: "Scale combined background by ChIP-to-control ratio (0.99858) using macs3 bdgopt multiply to create local lambda track."
- [methods] To create the background noise track, extend the control read to both sides using the `-B` option in the `pileup` function: "To create the background noise track, extend the control read to both sides using the `-B` option in the `pileup` function"
