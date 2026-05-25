---
name: industrial-gradient-metadata-categorization
description: "Stratifies fecal samples into four discrete industrialization categories (urban industrialized, rural industrialized, rural traditional, isolated traditional) and uses these assignments as the primary grouping variable for downstream metabolomic and microbiomic analyses. This skill is foundational for detecting and quantifying the impact of industrialization on metabolome composition and microbiome-metabolome interactions."
when_to_use_negative: |
  - "Samples lack geographic or contextual information to justify industrialization assignment"
  - "Your research focuses on within-population heterogeneity rather than between-population comparisons"
  - "Industrialization is already coded as a continuous variable (e.g., urbanization index) rather than discrete categories"
edam_operation: "http://edamontology.org/operation_3435"
edam_topics: |
  - "http://edamontology.org/topic_3172"
  - "http://edamontology.org/topic_3697"
tools: |
  - name: "QIIME2"
  role: "Load metadata and assign industrialization groups to samples; enable stratified PERMANOVA and PCoA by group"
  - name: "R"
  role: "Create, validate, and manipulate sample metadata tables; assign and verify industrialization category assignments"
  repo: "https://github.com/jhaffner09/core_metabolome_2021"
  - name: "PERMANOVA"
  role: "Test statistical significance of industrialization group on metabolome variance (downstream use of metadata)"
provenance: |
  source_task_ids:
  - task_001
  source_papers:
  - doi: "10.1128/msystems.00710-22"
  title: "Untargeted Fecal Metabolomic Analyses across an Industrialization Gradient Reveal Shared Metabolites and Impact of Industrialization on Fecal Microbiome-Metabolome Interactions"
schema_version: "0.2.0"
metadata:
  iri: https://w3id.org/holobiomicslab/asb-skill/industrial-gradient-metadata-categorization@sha256:8e6ede44c31668d04c29176f0996f8fcbed9aa43eb21927d863f81701f2e5160
---

# industrial-gradient-metadata-categorization

## Summary

Stratifies fecal samples into four discrete industrialization categories (urban industrialized, rural industrialized, rural traditional, isolated traditional) and uses these assignments as the primary grouping variable for downstream metabolomic and microbiomic analyses. This skill is foundational for detecting and quantifying the impact of industrialization on metabolome composition and microbiome-metabolome interactions.

## When to use

When you have fecal samples collected from populations spanning a gradient of industrial development and your research question concerns whether metabolomic or microbiotic composition differs by degree of urbanization or access to industrial food systems. Use this skill before PCoA, PERMANOVA, or differential abundance testing to ensure samples are correctly assigned to their industrialization context.

## When NOT to use

- Samples lack geographic or contextual information to justify industrialization assignment
- Your research focuses on within-population heterogeneity rather than between-population comparisons
- Industrialization is already coded as a continuous variable (e.g., urbanization index) rather than discrete categories

## Inputs

- Fecal sample collection metadata (sample ID, geographic location, population)
- Population-level descriptors (urbanization level, food system type, industrial infrastructure access)

## Outputs

- Sample metadata table with industrialization group assignments (four-level categorical variable)
- Validated sample-to-group mapping for use in PERMANOVA, ANOVA, and ordination analyses

## How to apply

Assign each fecal sample to one of four industrialization categories based on the sampling location's infrastructure, food system type, and degree of urban development: (1) urban industrialized (cities with processed food access), (2) rural industrialized (rural areas with industrial food availability), (3) rural traditional (rural areas with subsistence-based food practices), (4) isolated traditional (geographically remote populations with minimal industrial contact). Document the rationale for each assignment in sample metadata. Load this metadata into your analysis framework (QIIME2, R, or Python) alongside sample identifiers. Validate that all samples have non-null industrialization assignments before proceeding to ordination or statistical testing. This categorization directly enables PERMANOVA to quantify the R² and P-value of industrialization as a driver of metabolome variance (as demonstrated in the article: R² = 0.140, P = 0.001).

## Related tools

- **QIIME2** (Load metadata and assign industrialization groups to samples; enable stratified PERMANOVA and PCoA by group)
- **R** (Create, validate, and manipulate sample metadata tables; assign and verify industrialization category assignments) — https://github.com/jhaffner09/core_metabolome_2021
- **PERMANOVA** (Test statistical significance of industrialization group on metabolome variance (downstream use of metadata))

## Examples

```
# Load sample metadata and assign industrialization groups in R
metadata <- read.csv('sample_metadata.csv')
metadata$industrialization_group <- factor(c('urban_industrialized', 'rural_industrialized', 'rural_traditional', 'isolated_traditional')[match(metadata$population, c('NYC', 'Kentucky', 'Tunapuco', 'Matses'))], levels=c('isolated_traditional', 'rural_traditional', 'rural_industrialized', 'urban_industrialized'))
# Verify all samples assigned
table(metadata$industrialization_group)
```

## Evaluation signals

- All samples have non-null industrialization group assignments; no missing values in the grouping variable
- Four groups are represented in the metadata table (urban industrialized, rural industrialized, rural traditional, isolated traditional)
- PERMANOVA on industrialization group yields P ≤ 0.05 and R² ≥ 0.08 (article achieved P = 0.001, R² = 0.140), confirming that industrialization explains meaningful metabolomic variance
- Sample counts per group are balanced or documented; groups with n < 5 are flagged for potential power issues
- Metadata assignments are traceable to publication or supplementary materials; rationale for each population's category is documented

## Limitations

- Categorization into four discrete groups may oversimplify continuous variation in industrialization; intermediate or mixed-exposure populations may not fit neatly into a single category
- Geographic and cultural context is required to defensibly assign populations; without on-site knowledge or published ethnographic data, assignments risk being inaccurate or culturally insensitive
- The article's sample populations (Norman, Tunapuco, Matses, and industrialized cohorts) may not generalize; industrialization drivers and metabolic responses may differ in other geographic or cultural contexts
- Confounding variables (age, sex, diet composition, medication, sample storage delay) can influence metabolomic patterns independently of industrialization; these must be tested separately or controlled for in statistical models

## Evidence

- [results] populations exhibited similar metabolomes based on the degree of industrialization determined by principal-coordinate analysis (PCoA): "populations exhibited similar metabolomes based on the degree of industrialization determined by principal-coordinate analysis (PCoA"
- [results] permutational multivariate analysis of variance [PERMANOVA] (38) P = 0.001, R2 = 0.140: "permutational multivariate analysis of variance [PERMANOVA] (38) P = 0.001, R2 = 0.140"
- [results] industrialization had a stronger influence on metabolic similarity between populations than geographic origin, age, or sex: "industrialization had a stronger influence on metabolic similarity between populations than geographic origin, age, or sex"
- [methods] Instructions for recreating data analyses in R and Python are available as Jupyter Notebook (85) links at: https://github.com/jhaffner09/core_metabolome_2021.: "Instructions for recreating data analyses in R and Python are available as Jupyter Notebook (85) links at: https://github.com/jhaffner09/core_metabolome_2021."
