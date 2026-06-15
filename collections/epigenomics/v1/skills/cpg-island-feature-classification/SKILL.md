---
name: cpg-island-feature-classification
description: Use when you have a methylDiff object containing differentially methylated bases or regions from bisulfite sequencing, gene annotation in BED or similar format (RefSeq, Ensembl), and CpG island coordinate files, and need to understand what fraction of your differential methylation signal falls.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3671
  edam_topics:
  - http://edamontology.org/topic_3295
  - http://edamontology.org/topic_0749
  tools:
  - genomation
  - GenomicFeatures
  - R
  - methylKit
  - Bismark
  - MethylDackel
derived_from:
- doi: 10.1186/gb-2012-13-10-r87
  title: methylkit
evidence_spans:
- We can annotate our differentially methylated regions/bases based on gene annotation using genomation package
- This annotation operation will tell us what percentage of our differentially methylated regions are on promoters/introns/exons/intergenic region. In this case we read annotation from a BED file,
- packageVersion('methylKit')
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/epigenomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_methylkit
    doi: 10.1186/gb-2012-13-10-r87
    title: methylkit
  dedup_kept_from: coll_methylkit
schema_version: 0.2.0
---

# CpG Island Feature Classification

## Summary

Classify differentially methylated bases and regions relative to CpG islands, their flanking shores, and gene annotation features (promoters, exons, introns) to determine the genomic context and functional relevance of methylation changes. This skill uses genomation's annotation functions to generate percentage overlap tables that stratify differential methylation by feature class.

## When to use

You have a methylDiff object containing differentially methylated bases or regions from bisulfite sequencing, gene annotation in BED or similar format (RefSeq, Ensembl), and CpG island coordinate files, and need to understand what fraction of your differential methylation signal falls within promoters vs. exons vs. introns and whether it clusters in CpG islands or their flanking shores.

## When NOT to use

- Your input is already a feature-annotated table or matrix (i.e., annotation has already been performed).
- You have only raw bisulfite sequencing reads (FASTQ) and have not yet called methylation; use methylation callers (Bismark, MethylDackel) first.
- Your differentially methylated regions are from a non-mammalian organism for which CpG island definitions do not apply or are not validated.

## Inputs

- methylDiff object (output from methylKit::calculateDiffMeth())
- RefSeq or Ensembl gene annotation BED file
- CpG island coordinate BED file (e.g., cpgi.hg18.bed.txt)

## Outputs

- Percentage overlap table: differentially methylated bases by gene part (promoter/exon/intron/intergenic)
- Percentage overlap table: differentially methylated bases by CpG island context (CpGi/shore)
- Summary statistics table matching vignette format and counts

## How to apply

Load your methylDiff object and convert gene annotation (RefSeq, Ensembl) and CpG island BED files into GRanges objects using GenomicFeatures or genomation. Execute annotateWithGeneParts() to overlap differentially methylated bases with promoter, exon, intron, and intergenic regions, recording the percentage of bases in each category. Then execute annotateWithFeatureFlank() to annotate the same bases relative to CpG islands and their flanking shores (typically 2 kb on each side), capturing the percentage overlap for CpGi vs. shore contexts. Compile the resulting percentage overlap statistics into a summary table. The rationale is that promoter and island contexts are functionally distinct from intergenic and shore contexts; stratification reveals whether differential methylation is enriched in regulatory or structural genomic compartments.

## Related tools

- **methylKit** (Provides methylDiff objects from calculateDiffMeth(); handles differential methylation statistical testing) — https://github.com/al2na/methylKit
- **genomation** (Provides annotateWithGeneParts() and annotateWithFeatureFlank() functions for overlapping methylated bases with gene and CpG island annotations)
- **GenomicFeatures** (Converts BED and GFF gene annotation files into GRanges objects for genomic overlap operations)
- **Bismark** (Upstream tool: performs bisulfite read alignment and methylation calling, generating input methylation call files for methylKit) — https://github.com/FelixKrueger/Bismark
- **MethylDackel** (Alternative upstream tool: extracts per-base methylation metrics from BAM files for input to methylKit) — https://github.com/dpryan79/MethylDackel

## Examples

```
annotateWithGeneParts(methylDiff_obj, gene.parts); annotateWithFeatureFlank(methylDiff_obj, cpgi.obj, cpgi.flank=2000)
```

## Evaluation signals

- Percentage overlap sums to 100% across all gene part classes (promoter + exon + intron + intergenic = 100%)
- Percentage overlap sums to 100% across all CpG island context classes (CpGi + shore = 100%)
- Output table format and row/column structure match the published vignette's reported format (no missing or malformed cells)
- Counts of bases in each feature class are integers and non-negative
- Enrichment patterns are biologically sensible (e.g., promoter-enriched differential methylation should exceed random expectation given genome-wide promoter fraction)

## Limitations

- CpG island definitions are genome- and assembly-specific; annotations for hg18, hg19, and hg38 differ; ensure your annotation file matches your reference genome.
- The skill assumes non-overlapping or minimally-overlapping gene features; overlaps between exons and introns or between promoters and exons may lead to ambiguous or double-counted classifications depending on the order of operations.
- Shore flank width (typically 2 kb) is a convention; different flank definitions will produce different percentage distributions.
- Differential methylation bases with very low effect size (q-value just below threshold, small percent methylation difference) may not show clear feature enrichment and could be noise.
- CpG island definitions are absent in non-mammalian genomes or may not be validated for non-model organisms.

## Evidence

- [other] The annotateWithGeneParts() and annotateWithFeatureFlank() functions generate percentage overlap tables that classify differentially methylated regions by their overlap with promoter/exon/intron features and CpGi/shore genomic contexts.: "The annotateWithGeneParts() and annotateWithFeatureFlank() functions generate percentage overlap tables that classify differentially methylated regions by their overlap with promoter/exon/intron"
- [intro] We can annotate our differentially methylated regions/bases based on gene annotation using genomation package: "We can annotate our differentially methylated regions/bases based on gene annotation using genomation package"
- [intro] This annotation operation will tell us what percentage of our differentially methylated regions are on promoters/introns/exons/intergenic region.: "This annotation operation will tell us what percentage of our differentially methylated regions are on promoters/introns/exons/intergenic region."
- [other] Load the methylDiff object produced by calculateDiffMeth() containing differentially methylated bases. Load the refseq.hg18.bed.txt gene annotation file as a GRanges object using genomation or GenomicFeatures.: "Load the methylDiff object produced by calculateDiffMeth() containing differentially methylated bases. Load the refseq.hg18.bed.txt gene annotation file as a GRanges object using genomation or"
- [other] Execute annotateWithFeatureFlank() function to annotate bases relative to CpG islands and their flanking shores, capturing the percentage overlap for each feature class.: "Execute annotateWithFeatureFlank() function to annotate bases relative to CpG islands and their flanking shores, capturing the percentage overlap for each feature class."
