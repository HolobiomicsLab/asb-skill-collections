---
name: peak-calling-output-interpretation
description: Use when you have run a peak-calling algorithm on sparse CUT&RUN bedGraph data and received a BED-format output file;
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0230
  edam_topics:
  - http://edamontology.org/topic_3169
  - http://edamontology.org/topic_3295
  tools:
  - git
  - SEACR
  - bedtools
derived_from:
- doi: 10.1186/s13072-019-0287-4
  title: seacr
evidence_spans:
- Clone the SEACR repository
- github:FredHutch__SEACR
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/epigenomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_seacr
    doi: 10.1186/s13072-019-0287-4
    title: seacr
  dedup_kept_from: coll_seacr
schema_version: 0.2.0
---

# peak-calling-output-interpretation

## Summary

Interpret and validate the BED-format output from sparse peak-calling tools (e.g. SEACR) applied to CUT&RUN or chromatin profiling data, understanding the semantic meaning of each output field and assessing peak quality based on signal composition and genomic span.

## When to use

You have run a peak-calling algorithm on sparse CUT&RUN bedGraph data and received a BED-format output file; you need to understand what each column represents, verify that the peaks meet biological and statistical criteria (total signal, max signal, span), and decide whether to accept, filter, or re-threshold the peak set.

## When NOT to use

- Input data is already a curated feature table or a manually annotated region set; peak calling and output interpretation are only needed when starting from raw or sparse bedGraph density.
- Your analysis goal does not require peak-level interpretation; e.g., if you only need summary statistics (total number of peaks, genome coverage), a direct query of the BED file suffices.
- Output is from a peak-calling tool with a different schema (e.g., narrowPeak with p-values and q-values); SEACR output lacks statistical significance estimates and uses signal-based metrics instead.

## Inputs

- SEACR output BED file (6-column: chr, start, end, total_signal, max_signal, max_signal_region)
- Input bedGraph file (reference, for validation and cross-checking signal values)

## Outputs

- Validated or filtered peak set (BED format)
- Quality report or metrics (peak count, signal distribution, pass/fail flags per peak)

## How to apply

Open the output BED file (e.g., <prefix>.stringent.bed or <prefix>.relaxed.bed) and examine the six columns: chromosome, start, end, total signal, maximum bedgraph signal, and the coordinates of the maximum signal region. For each peak, verify that the total signal and max signal values are above the threshold used during calling (empirical control-based or numeric fractile). Check that the maximum signal region (field 6) falls within the peak coordinates (fields 2–3), indicating proper boundary detection. Cross-reference peaks against the input bedgraph to confirm that signal blocks were correctly merged and that zero-signal regions were properly omitted. Filter or flag peaks composed of very few input bedgraph lines (v1.2+ adds a line-count filter to remove artifacts from sparse composition). Use the choice of 'relaxed' versus 'stringent' mode (determined by the threshold applied: knee vs. peak of the total signal curve) to interpret expected sensitivity and specificity trade-offs.

## Related tools

- **bedtools** (Used internally by SEACR to generate bedGraph from BAM/BED input and to support peak coordinate manipulation and validation) — https://bedtools.readthedocs.io/en/latest/
- **SEACR** (Peak-calling tool that produces the 6-column BED output being interpreted) — https://github.com/FredHutch/SEACR

## Examples

```
# Examine output peaks and cross-check signal values against input bedGraph:
head -20 output.stringent.bed
grep -w 'chr1' output.stringent.bed | awk '{sum+=$4; print $0, "(fields: chr start end total_signal max_signal max_region)"}' | head -5
```

## Evaluation signals

- Each peak's maximum signal region (field 6) is a valid sub-interval of the peak coordinates (fields 2–3).
- Total signal (field 4) and max signal (field 5) values are consistent with the underlying bedGraph: summing bedGraph values within the peak coordinates should approximately equal field 4, and the maximum bedGraph value within the peak should equal or closely match field 5.
- Peaks called in 'relaxed' mode have lower or equal max-signal thresholds compared to 'stringent' mode peaks, reflecting the use of the knee vs. peak of the total signal curve.
- Peaks do not overlap or overlap only at boundary coordinates (indicating proper merging of adjacent bedGraph blocks).
- For v1.2+, peaks are not composed of extremely few bedGraph lines (the line-count filter should have removed sparse artifacts); inspect the composition to confirm reasonable coverage depth per peak.

## Limitations

- SEACR output contains no statistical significance estimates (p-values, q-values, or false-discovery rates); interpretation relies solely on signal magnitude and composition, which may not distinguish true peaks from high-amplitude noise in some datasets.
- The 6-column BED output omits bedgraph lines containing zero signal (as noted in v1.3), meaning gaps in coverage within or near peaks are not explicitly represented; cross-reference with input bedGraph to assess gap frequency and size.
- Threshold selection is sensitive to the empirical control data or numeric fractile chosen; 'relaxed' vs. 'stringent' mode affects sensitivity, but no automatic consensus or validation method is provided for choosing between them.
- Normalization of control to target data (Field 3: 'norm' vs. 'non') is user-controlled; if experimental and control data are not rigorously normalized (e.g., via spike-in), peak interpretation may be biased.
- The line-count filtering introduced in v1.2 (to remove peaks composed of very few bedGraph lines) uses a dynamic threshold based on the control dataset; this threshold may not generalize across datasets with different sequencing depths or fragment size distributions.

## Evidence

- [readme] Output data structure and field definitions: "<chr>	<start>	<end>	<total signal>	<max signal>	<max signal region>"
- [readme] Definition of each output field: "Field 1: Chromosome; Field 2: Start coordinate; Field 3: End coordinate; Field 4: Total signal contained within denoted coordinates; Field 5: Maximum bedgraph signal attained at any base pair within"
- [readme] Version 1.3 signal filtering logic: "Added a check to filter out any input bedgraph lines containing zero signal."
- [readme] Version 1.2 line-count and threshold filtering: "Added a counter to keep track of the number of component bedgraph lines that compose each signal block, and a function to calculate the minimum threshold of lines per signal block at which there is a"
- [readme] Relaxed vs. stringent mode interpretation: "'relaxed' uses a total signal threshold between the knee and peak of the total signal curve, and corresponds to the 'relaxed' mode described in the text, whereas 'stringent' uses the peak of the"
