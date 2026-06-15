---
name: genomic-feature-annotation-overlap
description: Use when after you have identified a set of differentially methylated bases or regions (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3222
  edam_topics:
  - http://edamontology.org/topic_3295
  - http://edamontology.org/topic_0622
  tools:
  - genomation
  - GenomicFeatures
  - R
  - methylKit
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

# genomic-feature-annotation-overlap

## Summary

Classify differentially methylated bases or regions by their overlap with gene annotation features (promoters, exons, introns) and CpG island contexts (islands vs. shores) using genomation's annotateWithGeneParts() and annotateWithFeatureFlank() functions. This skill quantifies the genomic distribution of methylation signals to identify which regulatory and structural features are enriched for differential methylation.

## When to use

Apply this skill after you have identified a set of differentially methylated bases or regions (e.g., from calculateDiffMeth() in methylKit) and need to determine whether these sites are enriched in specific gene annotation contexts (promoters, exons, introns, intergenic regions) or CpG island landscapes (CpGi islands vs. shores). Use it when you need to report the percentage breakdown of your differential methylation signal across these annotation categories.

## When NOT to use

- Your input is raw methylation call files that have not yet been filtered or merged across samples—first use methRead(), unite(), and calculateDiffMeth() to generate a methylDiff object.
- You lack appropriate gene annotation or CpG island annotation files for your reference genome; annotation must be in BED format and correspond to the correct genome build.
- Your analysis goal is to identify novel regulatory elements or perform de novo peak calling—this skill requires pre-existing annotation and only classifies known features.

## Inputs

- methylDiff object from calculateDiffMeth() containing differentially methylated bases with q-value and percent methylation difference statistics
- RefSeq gene annotation BED file (e.g., refseq.hg18.bed.txt) as GRanges object
- CpG island annotation BED file (e.g., cpgi.hg18.bed.txt) as GRanges object

## Outputs

- Percentage overlap table classifying differentially methylated bases by promoter/exon/intron features
- Percentage overlap table classifying differentially methylated bases by CpG island vs. shore context
- Summary statistics matching vignette format with counts and percentages per feature class

## How to apply

Load a methylDiff object containing differentially methylated bases and a gene annotation file (RefSeq BED format) as a GRanges object using GenomicFeatures. Execute annotateWithGeneParts() to overlap the methylated bases with promoter, exon, and intron regions, recording the proportion of bases in each category. Then load a CpG island annotation file (cpgi.hg18.bed.txt or equivalent) as a GRanges object and execute annotateWithFeatureFlank() to annotate methylated bases relative to CpG islands and their flanking shores, capturing the percentage overlap for each feature class. The output is a percentage overlap table that summarizes the genomic distribution of your differential methylation signal—this enables interpretation of whether methylation changes are concentrated in regulatory regions (promoters) or other gene body features.

## Related tools

- **methylKit** (Calculate differential methylation (calculateDiffMeth()) and provide methylDiff input object for annotation; filter by q-value and methylation difference cutoffs) — https://github.com/al2na/methylKit
- **genomation** (Execute annotateWithGeneParts() and annotateWithFeatureFlank() functions to perform overlap analysis with gene and CpG island annotations)
- **GenomicFeatures** (Parse and manage BED file gene annotation and CpG island annotation as GRanges objects for genomic overlap computation)
- **R** (Environment for running methylKit, genomation, and GenomicFeatures packages and formatting output statistics tables)

## Examples

```
# Load methylDiff object and annotate with RefSeq and CpG islands
data(methylDiffExample)
annotate.with.genes <- annotateWithGeneParts(as(methylDiffExample,"GRanges"),refseq.hg18.bed.txt)
annotate.with.cpgi <- annotateWithFeatureFlank(as(methylDiffExample,"GRanges"),cpgi.hg18.bed.txt)
```

## Evaluation signals

- Output percentage overlap table sums to 100% across all feature categories (promoters + exons + introns + intergenic = 100%)
- Output percentages for CpG island and shore annotations align with manually computed coverage fractions using bedtools intersect or similar tool
- Row and column counts in summary table match the input methylDiff object base count and the number of expected annotation categories
- Differentially methylated bases in promoter regions show expected bias toward hypo-methylation in regulatory contexts (if prior knowledge supports this)
- Output table format and counts reproduce the published vignette format exactly, including all feature classes and summary statistics

## Limitations

- annotateWithGeneParts() and annotateWithFeatureFlank() treat annotation features as discrete non-overlapping categories; bases at feature boundaries may be misclassified depending on function implementation
- Results are genome-build specific—RefSeq and CpG island annotations must exactly match the genome build used for read alignment and methylation calling (e.g., hg18 vs. hg38)
- No statistical test is performed to assess whether observed enrichment in a feature (e.g., promoters) is significant relative to random expectation—annotation is purely descriptive
- CpG island definitions vary by source (UCSC, Ensembl, custom)—shore boundaries and island thresholds are not standardized and may affect reproducibility

## Evidence

- [intro] Load the methylDiff object and RefSeq annotation: "Load the methylDiff object produced by calculateDiffMeth() containing differentially methylated bases. Load the refseq.hg18.bed.txt gene annotation file as a GRanges object using genomation or"
- [intro] Execute annotateWithGeneParts for gene feature overlap: "Execute annotateWithGeneParts() function to overlap differentially methylated bases with promoter, exon, and intron genomic regions, recording the proportion of bases in each category."
- [intro] Execute annotateWithFeatureFlank for CpG island context: "Execute annotateWithFeatureFlank() function to annotate bases relative to CpG islands and their flanking shores, capturing the percentage overlap for each feature class."
- [intro] Format output as percentage overlap table: "Compile and format the percentage overlap statistics into a summary table matching the vignette's reported format and counts."
- [readme] Annotation explains feature distribution of methylation: "This annotation operation will tell us what percentage of our differentially methylated regions are on promoters/introns/exons/intergenic region."
