---
name: chromatin-domain-boundary-detection
description: Use when you have generated a .hic contact map from Hi-C raw sequencing data and need to identify topologically associating domains (TADs) or other chromatin structural boundaries.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3222
  edam_topics:
  - http://edamontology.org/topic_3173
  - http://edamontology.org/topic_0654
  tools:
  - Juicer
  - juicer_tools
  - Juicebox
  - ENCODE Hi-C uniform processing pipeline
derived_from:
- doi: 10.1016/j.cels.2016.07.002
  title: juicer
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/epigenomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_juicer
    doi: 10.1016/j.cels.2016.07.002
    title: juicer
  dedup_kept_from: coll_juicer
schema_version: 0.2.0
---

# chromatin-domain-boundary-detection

## Summary

Detect chromatin domain boundaries (TADs and other structural domains) on kilobase-resolution Hi-C contact maps using Juicer command-line feature annotation tools. This skill applies domain-detection algorithms to pre-generated .hic files to identify and output domain boundary coordinates.

## When to use

You have generated a .hic contact map from Hi-C raw sequencing data and need to identify topologically associating domains (TADs) or other chromatin structural boundaries. Apply this skill when your analysis goal is to map the physical boundaries of self-interacting chromatin regions at kilobase resolution, typically as a post-processing step after Hi-C map generation.

## When NOT to use

- Input is raw FASTQ sequencing data — the Hi-C map must be pre-generated first using the Juicer pipeline.
- You only need loop-level features (e.g., enhancer–promoter loops) rather than domain-level structure — use loop-calling tools instead.
- Your contact map is at single-cell or very low resolution where domain structure is not reliably detectable.

## Inputs

- .hic contact map file (pre-generated from aligned Hi-C data)
- genome identifier (e.g., 'hg19', 'mm10')

## Outputs

- Domain boundary coordinate file (e.g., domain list with chromosome, start, end positions)
- Annotated feature file in format specified by domain-detection tool

## How to apply

Load the pre-generated .hic contact map file into Juicer command-line tools, which provide a suite of post-processing feature annotation tools including domain-detection algorithms. Select and execute the appropriate domain-detection command from the Juicer CLI (e.g., arrowhead or other domain-calling methods available in juicer_tools). The algorithm analyzes the contact frequency patterns in the Hi-C matrix to identify boundaries where inter-domain contacts drop sharply. Execute the tool with parameters appropriate to your resolution and genome; the tool outputs domain boundary coordinates in a structured format (e.g., BED-like or coordinate list). Validate output by comparing domain sizes and boundaries against known TAD structures or by visual inspection in Juicebox.

## Related tools

- **Juicer** (Platform providing command-line tools for domain-detection feature annotation on Hi-C maps) — https://github.com/aidenlab/juicer
- **juicer_tools** (Command-line suite within Juicer containing domain-detection algorithms (e.g., arrowhead)) — https://github.com/aidenlab/juicer/wiki/Download
- **Juicebox** (Visualization tool for validating and inspecting annotated domain boundaries on Hi-C maps) — https://github.com/theaidenlab/Juicebox
- **ENCODE Hi-C uniform processing pipeline** (Dockerized, cloud-compatible wrapper around Juicer for end-to-end Hi-C processing including domain annotation) — https://github.com/ENCODE-DCC/hic-pipeline

## Evaluation signals

- Output file exists and contains non-empty domain boundary coordinates with valid chromosome and genomic position ranges.
- Domain sizes fall within expected range for the organism and resolution (e.g., typically 100 kb–1 Mb for mammalian TADs at 5–10 kb resolution).
- Domain boundaries align with known chromatin structural features (e.g., CTCF binding sites, visible diagonal patterns in Hi-C heatmaps).
- Visual inspection in Juicebox shows clear transitions in contact frequency at detected boundaries.
- Comparison with reference domain sets (e.g., published TAD catalogs for the same cell type/genome) shows substantial overlap.

## Limitations

- Domain detection is sensitive to sequencing depth and contact map quality; low-coverage regions may yield spurious or missing boundaries.
- Algorithm performance depends on appropriate choice of resolution; kilobase-resolution maps are required; lower resolutions (100 kb+) reduce boundary precision.
- Domain detection assumes typical mammalian-scale chromatin organization; may not perform well on highly rearranged or aneuploid genomes.
- Juicer 2.0 is under active development; stable domain-calling tools are available in Juicer 1.6.
- GPU requirements (CUDA) for some peak-calling methods; CPU-only alternatives available but slower.

## Evidence

- [other] Juicer includes command line tools designed for feature annotation on Hi-C maps, enabling users to annotate features on pre-generated Hi-C map artifacts.: "command line tools for feature annotation on the Hi-C maps"
- [other] The workflow explicitly loads a pre-generated .hic contact map file into Juicer command-line tools and executes feature annotation algorithms such as domain-detection.: "Load the pre-generated .hic contact map file into Juicer command-line tools. 2. Select and execute the appropriate feature annotation tool (e.g., loop-calling or domain-detection algorithm) from the"
- [readme] Juicer is positioned as a platform for analyzing kilobase resolution Hi-C data with tools for both pipeline generation and post-processing.: "Juicer is a platform for analyzing kilobase resolution Hi-C data. In this distribution, we include the pipeline for generating Hi-C maps from fastq raw data files and command line tools for feature"
- [readme] Juicer supports processing at kilobase resolution, which is the standard for detecting chromatin domain structure.: "Juicer is a platform for analyzing kilobase resolution Hi-C data"
- [readme] Post-processing feature annotation is a distinct pipeline stage in Juicer, performed after .hic file creation.: "Use 'postproc' when the hic files have been created and only postprocessing feature annotation remains to be completed."
