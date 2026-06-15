---
name: statistical-overlap-proportion-reporting
description: Use when after identifying differentially methylated bases (q-value < 0.01, methylation difference > 25%) using calculateDiffMeth(), use this skill to determine what fraction of those bases overlap with specific gene features (promoters, exons, introns) and CpG contexts (islands vs. shores).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3237
  edam_topics:
  - http://edamontology.org/topic_3295
  - http://edamontology.org/topic_0080
  - http://edamontology.org/topic_3674
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

# Statistical Overlap Proportion Reporting

## Summary

Quantify and report the percentage distribution of differentially methylated bases across genomic feature classes (gene annotation: promoter/exon/intron; CpG context: island/shore) using overlap-based annotation functions. This skill generates proportion tables that classify methylation changes by their genomic location and regulatory context, enabling interpretation of where methylation differences occur in the genome.

## When to use

After identifying differentially methylated bases (q-value < 0.01, methylation difference > 25%) using calculateDiffMeth(), use this skill to determine what fraction of those bases overlap with specific gene features (promoters, exons, introns) and CpG contexts (islands vs. shores). Apply when your research question requires reporting the genomic distribution of methylation changes relative to annotated regulatory and sequence features.

## When NOT to use

- Input is raw methylation call files that have not yet been filtered by q-value and methylation difference thresholds — apply filtering first using getMethylDiff().
- Input is already a regional or tiling-window level summary rather than base-pair resolution methylation data — overlap-based annotation is designed for base-pair granularity.
- Gene annotation or CpG island BED files are missing or in incompatible genome coordinates (e.g., hg19 vs. hg18 mismatch) — coordinate systems must match the methylation data.

## Inputs

- methylDiff object (from calculateDiffMeth() with q-value < 0.01 and methylation difference > 25% filtering)
- refseq gene annotation BED file (e.g., refseq.hg18.bed.txt) loaded as GRanges
- CpG island annotation BED file (e.g., cpgi.hg18.bed.txt) loaded as GRanges

## Outputs

- Percentage overlap table: proportion of differentially methylated bases in promoter/exon/intron features
- Percentage overlap table: proportion of differentially methylated bases in CpG island/shore contexts
- Compiled summary table with both counts and percentages matching vignette-reported format

## How to apply

Load a methylDiff object (output from calculateDiffMeth()) containing differentially methylated bases. Load reference gene annotation (refseq.hg18.bed.txt) and CpG island annotation (cpgi.hg18.bed.txt) as GRanges objects using genomation or GenomicFeatures. Execute annotateWithGeneParts() to overlap differentially methylated bases with promoter, exon, and intron regions, recording the percentage of bases in each category. Execute annotateWithFeatureFlank() to annotate bases relative to CpG islands and their flanking shores, capturing percentage overlap for each class. Compile the resulting percentage statistics into a summary table reporting the distribution of differential methylation across these feature classes. Report both absolute counts and percentages to match standard vignette formats.

## Related tools

- **methylKit** (Primary R package providing calculateDiffMeth() for identifying differentially methylated bases and getMethylDiff() for filtering by statistical and effect-size cutoffs) — https://github.com/al2na/methylKit
- **genomation** (Provides annotateWithGeneParts() and annotateWithFeatureFlank() functions that perform overlap-based annotation and generate percentage tables)
- **GenomicFeatures** (Enables reading BED file gene annotations and CpG island definitions as GRanges objects compatible with overlap operations)
- **Bismark** (Upstream bisulfite alignment tool that produces methylation call files consumed by methRead() in the methylKit workflow) — https://github.com/FelixKrueger/Bismark

## Examples

```
library(methylKit); library(genomation); am <- annotateWithGeneParts(methylDiff_object, gene_parts); af <- annotateWithFeatureFlank(methylDiff_object, cpgi_granges); print(getMembers(am))
```

## Evaluation signals

- Percentage values for each feature class (promoter, exon, intron, CpG island, shore) sum to 100% or account for all differentially methylated bases with documented overlap rules.
- Counts of overlapping bases match the filtering applied (q-value < 0.01, methylation difference > 25%) and can be traced back to the input methylDiff object.
- Output table format matches published vignette examples in methylKit documentation, with both counts and percentages reported.
- GRanges objects for annotation files have consistent genome build and coordinate system with the methylDiff object (verified via seqlevels and metadata).
- Spot-check: manually verify a small subset of reported overlaps by inspecting the bed file coordinates and the methylation positions.

## Limitations

- Overlap annotation is sensitive to the choice of gene annotation source (refseq, ensembl, etc.) and CpG island definition database — results may vary if different annotation versions are used.
- Bases that fall in intergenic regions or outside provided annotation BED files will not be captured; ensure annotation files are comprehensive for the genome and regions of interest.
- annotateWithFeatureFlank() requires specification of flank width for CpG shores (e.g., 2 kb); results are sensitive to this parameter and should be documented.
- For overlapping features (e.g., a base in both a promoter and a CpG island), overlap classification rules depend on function implementation; consult genomation documentation for precedence rules.
- Minimum coverage threshold of 10 reads per base applied in methRead() may exclude low-coverage methylated regions; verify that filtering is appropriate for your downstream annotation goals.

## Evidence

- [other] annotateWithGeneParts() and annotateWithFeatureFlank() functions generate percentage overlap tables that classify differentially methylated regions by their overlap with promoter/exon/intron features and CpGi/shore genomic contexts: "The annotateWithGeneParts() and annotateWithFeatureFlank() functions generate percentage overlap tables that classify differentially methylated regions by their overlap with promoter/exon/intron"
- [other] Load the methylDiff object produced by calculateDiffMeth() containing differentially methylated bases: "Load the methylDiff object produced by calculateDiffMeth() containing differentially methylated bases."
- [other] Execute annotateWithGeneParts() function to overlap differentially methylated bases with promoter, exon, and intron genomic regions, recording the proportion of bases in each category: "Execute annotateWithGeneParts() function to overlap differentially methylated bases with promoter, exon, and intron genomic regions, recording the proportion of bases in each category."
- [other] Execute annotateWithFeatureFlank() function to annotate bases relative to CpG islands and their flanking shores, capturing the percentage overlap for each feature class: "Execute annotateWithFeatureFlank() function to annotate bases relative to CpG islands and their flanking shores, capturing the percentage overlap for each feature class."
- [intro] We can annotate our differentially methylated regions/bases based on gene annotation using genomation package: "We can annotate our differentially methylated regions/bases based on gene annotation using genomation package"
- [intro] Following bit selects the bases that have q-value<0.01 and percent methylation difference larger than 25%: "Following bit selects the bases that have q-value<0.01 and percent methylation difference larger than 25%"
- [intro] By default methRead requires a minimum coverage of 10 reads per base to ensure good quality of the data and a high confidence methylation percentage: "By default methRead requires a minimum coverage of 10 reads per base to ensure good quality of the data and a high confidence methylation percentage"
