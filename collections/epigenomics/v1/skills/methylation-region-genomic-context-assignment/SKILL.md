---
name: methylation-region-genomic-context-assignment
description: Use when after identifying differentially methylated bases or regions (via calculateDiffMeth() and getMethylDiff()), when you need to characterize WHERE these methylation changes occur relative to gene structure and CpG density landscapes.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3680
  edam_topics:
  - http://edamontology.org/topic_3674
  - http://edamontology.org/topic_3169
  tools:
  - genomation
  - GenomicFeatures
  - R
  - methylKit
  - Bismark
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

# methylation-region-genomic-context-assignment

## Summary

Assign differentially methylated bases and regions to genomic annotation features (promoters, exons, introns, intergenic regions) and CpG island contexts (CpG islands vs. shores) using overlap-based annotation functions. This skill quantifies the spatial distribution of methylation changes across functional and sequence-context categories.

## When to use

After identifying differentially methylated bases or regions (via calculateDiffMeth() and getMethylDiff()), when you need to characterize WHERE these methylation changes occur relative to gene structure and CpG density landscapes. Use this skill to generate percentage-overlap tables that answer: Are hyper-methylated bases enriched in promoters or gene bodies? Do hyper-methylated regions cluster in CpG islands or shores?

## When NOT to use

- Input methylDiff object has not been filtered by q-value and methylation difference thresholds — apply getMethylDiff() first to define the set of differentially methylated bases.
- Gene annotation or CpG island BED files are from a different genome build than the methylation data (e.g., mixing hg18 and hg19 coordinates) — coordinates will not match.
- You need single-base-resolution methylation calls without overlap-based aggregation — use raw methylRawList or methylBase objects directly instead.

## Inputs

- methylDiff object (output from calculateDiffMeth() filtered by getMethylDiff())
- RefSeq gene annotation BED file (e.g., refseq.hg18.bed.txt) containing promoter, exon, intron coordinates
- CpG island annotation BED file (e.g., cpgi.hg18.bed.txt) with island and shore boundaries

## Outputs

- Percentage overlap table: differentially methylated bases classified by gene annotation feature (promoter/exon/intron/intergenic)
- Percentage overlap table: differentially methylated bases classified by CpG context (island/shore)
- Summary statistics table with row counts and proportions matching vignette reference format

## How to apply

Load the methylDiff object containing differentially methylated bases (q-value < 0.01 and percent methylation difference > 25% by default) into memory. Load RefSeq gene annotation (promoter, exon, intron regions) and CpG island annotation (islands and flanking shores) as GRanges objects from BED files using genomation or GenomicFeatures. Execute annotateWithGeneParts() to compute the percentage of differentially methylated bases overlapping promoters, exons, introns, and intergenic regions. Execute annotateWithFeatureFlank() to assign bases relative to CpG islands and shores, capturing percentage overlap for each class. Compile the resulting percentage-overlap statistics into a summary table and validate that counts sum to 100% per methylation class and match published reference formats.

## Related tools

- **methylKit** (R package that provides calculateDiffMeth() and getMethylDiff() to generate and filter the methylDiff input object; also provides integrated support for methylation reading and filtering) — https://github.com/al2na/methylKit
- **genomation** (R package providing annotateWithGeneParts() and annotateWithFeatureFlank() functions to assign methylated bases to gene annotation features and CpG island contexts)
- **GenomicFeatures** (Bioconductor R package for reading and manipulating BED files as GRanges objects for overlap operations)
- **Bismark** (Generates the aligned BAM files and methylation calls that feed into methylKit's methRead() function) — https://github.com/FelixKrueger/Bismark

## Examples

```
# Load methylDiff object, filter to significant bases, then annotate
diff.meth <- getMethylDiff(meth.diff.obj, difference=25, qvalue=0.01)
annotated <- annotateWithGeneParts(diff.meth, refseq.gr)
feature.flank <- annotateWithFeatureFlank(diff.meth, cpgi.gr)
# Compile percentages into summary table
```

## Evaluation signals

- Percentage overlap table sums to 100% across all annotation feature classes (promoter + exon + intron + intergenic = 100%)
- Percentage overlap table sums to 100% across all CpG contexts (island + shore = 100%)
- Row counts match the total number of differentially methylated bases in the input methylDiff object
- Output format and magnitude of percentages match published vignette or reference tables (e.g., if reference shows 30% bases in promoters, output should be in same range for equivalent data)
- No bases are lost or double-counted; total bases in overlap table equals input methylDiff object size

## Limitations

- Overlap-based annotation depends on the quality and completeness of the BED annotation files; missing or outdated gene models (e.g., RefSeq) will not capture novel or non-coding features.
- Genome build mismatch between methylation data and annotation files (e.g., hg18 vs. hg19) causes silent coordinate failures; users must verify genome version consistency.
- Bases at feature boundaries (e.g., exon–intron junctions) may be assigned to one feature or the other depending on overlap algorithm details; percentages can shift with different BED definitions.
- methylKit requires a minimum coverage of 10 reads per base by default; lower-coverage bases are filtered during methRead() and will not appear in the methylDiff object fed to annotation.

## Evidence

- [other] The annotateWithGeneParts() and annotateWithFeatureFlank() functions generate percentage overlap tables that classify differentially methylated regions by their overlap with promoter/exon/intron features and CpGi/shore genomic contexts.: "The annotateWithGeneParts() and annotateWithFeatureFlank() functions generate percentage overlap tables that classify differentially methylated regions by their overlap with promoter/exon/intron"
- [intro] We can annotate our differentially methylated regions/bases based on gene annotation using genomation package: "We can annotate our differentially methylated regions/bases based on gene annotation using genomation package"
- [intro] This annotation operation will tell us what percentage of our differentially methylated regions are on promoters/introns/exons/intergenic region.: "This annotation operation will tell us what percentage of our differentially methylated regions are on promoters/introns/exons/intergenic region."
- [intro] Following bit selects the bases that have q-value<0.01 and percent methylation difference larger than 25%: "Following bit selects the bases that have q-value<0.01 and percent methylation difference larger than 25%"
- [intro] The calculateDiffMeth() function is the main function to calculate differential methylation. Depending on the sample size per each set it will either use Fisher's exact or logistic regression: "The calculateDiffMeth() function is the main function to calculate differential methylation. Depending on the sample size per each set it will either use Fisher's exact or logistic regression"
