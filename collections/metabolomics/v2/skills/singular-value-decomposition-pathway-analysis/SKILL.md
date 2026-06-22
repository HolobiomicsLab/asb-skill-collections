---
name: singular-value-decomposition-pathway-analysis
description: Use when when you have a peak intensity matrix (rows = metabolite features, columns = samples) with corresponding compound annotations (peak ID → KEGG/ChEBI ID mapping), and you need to rank pathways or metabolite set groupings (KEGG pathways, Reactome pathways, GNPS Molecular Families, MS2LDA.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3768
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0092
  tools:
  - PALS (Pathway Activity Level Scoring)
  - PALS Viewer
  - GNPS
  - MS2LDA
  - ORA, GSEA
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.3390/metabo11020103
  title: pals
evidence_spans:
- we introduce **PALS (Pathway Activity Level Scoring)**, a complete tool that performs database queries of pathways
- we introduce **PALS (Pathway Activity Level Scoring)**, a complete tool that performs database queries of pathways,
- To access our interactive Web application PALS Viewer, please visit [https://pals.glasgowcompbio.org/app/]
- Molecular Families from GNPS
- This includes in particular *Molecular Families* from [GNPS](http://gnps.ucsd.edu/)
- Mass2Motifs from MS2LDA
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pals_cq
    doi: 10.3390/metabo11020103
    title: pals
  dedup_kept_from: coll_pals_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3390/metabo11020103
  all_source_dois:
  - 10.3390/metabo11020103
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Singular Value Decomposition Pathway Analysis

## Summary

Apply PLAGE (Pathway Level Analysis of Gene Expression), a singular value decomposition–based method, to decompose metabolite or gene activity levels across pathways or metabolite sets and compute robust activity scores. This approach is particularly suited for metabolomics peak data where noise and missing values are prevalent.

## When to use

When you have a peak intensity matrix (rows = metabolite features, columns = samples) with corresponding compound annotations (peak ID → KEGG/ChEBI ID mapping), and you need to rank pathways or metabolite set groupings (KEGG pathways, Reactome pathways, GNPS Molecular Families, MS2LDA Mass2Motifs) by their collective activity or dysregulation in experimental comparisons. Use this skill when alternative methods (ORA, GSEA) may be unreliable due to high noise and frequent missing peak values in mass spectrometry data.

## When NOT to use

- Input is already a pre-computed pathway activity matrix or p-value table (skill operates on raw peak intensities and annotations, not pre-ranked results)
- You have no pathway or metabolite set annotation reference (PLAGE requires mapping peaks to known pathway members or metabolite groupings; unannotated peaks are discarded)
- Your data lacks clear experimental grouping or case–control comparisons (PLAGE is designed for comparative analysis; single-group or time-series-only designs require adaptation)

## Inputs

- Peak intensity CSV matrix (rows = peak feature IDs with KEGG/ChEBI annotations, columns = individual MS samples; optional second line indicating sample groupings)
- Annotation CSV matrix (two columns: peak ID and entity ID [KEGG or ChEBI identifier])
- Experimental design specification (sample-to-group mapping and case–control comparison pairs)
- Pathway or metabolite set database selection (PiMP_KEGG, Reactome COMPOUND/ChEBI/UniProt/ENSEMBL, or custom user-defined sets)
- Optional: species name for Reactome queries (default: Homo sapiens); minimum intensity threshold for imputation (default: 5000)

## Outputs

- Ranked pathway/metabolite set activity scores with p-values and FDR-corrected significance
- Coverage statistics per pathway (unique formulae in pathway, total dataset hits, coverage fraction)
- Activity-ranked list in CSV format compatible with PALS Viewer for interactive inspection
- Optional: PALS Viewer–compatible JSON export for visualization and interactive filtering of Molecular Families or Mass2Motifs

## How to apply

Load the intensity matrix (log₂-transformed, standardized to zero mean and unit variance) and annotation matrix into PALS. Specify the pathway database (PiMP_KEGG, Reactome COMPOUND/ChEBI, or custom metabolite set groupings) and define experimental comparisons as case/control pairs. Apply the PLAGE decomposition method, which uses singular value decomposition to extract the dominant activity mode of each pathway or metabolite set. Data imputation is performed automatically: missing intensities within a factor are replaced by factor minimum or mean; missing across all samples in a factor are replaced by the user-defined minimum intensity threshold (default 5000). The method outputs a ranked list of pathways/sets with p-values, coverage statistics (unique formulae vs. dataset hits), and activity scores that reflect the magnitude and direction of pathway activity in each comparison.

## Related tools

- **PALS (Pathway Activity Level Scoring)** (Implements the PLAGE decomposition method and pathway ranking; performs database queries of pathways, applies singular value decomposition to compute activity scores, and ranks pathways by significance) — https://github.com/glasgowcompbio/PALS
- **PALS Viewer** (Interactive web application for running PALS, inspecting pathway ranking results, visualizing significantly changing pathways, and prioritizing Molecular Families and Mass2Motifs by activity level) — https://pals.glasgowcompbio.org/app/
- **GNPS** (Source of Molecular Families metabolite groupings that can be imported into PALS for activity-based ranking and prioritization) — http://gnps.ucsd.edu/
- **MS2LDA** (Source of Mass2Motifs metabolite groupings (fragmentation spectrum–based clusters) that can be analyzed in PALS as alternative metabolite set annotations) — http://ms2lda.org/
- **ORA, GSEA** (Alternative pathway ranking methods included in PALS for benchmarking and comparison; less robust to noise and missing peaks than PLAGE in metabolomics contexts)

## Examples

```
python pals/run.py PLAGE notebooks/test_data/HAT/int_df.csv notebooks/test_data/HAT/annotation_df.csv test_output.csv --db PiMP_KEGG --comparisons Stage_1/Control Stage_2/Control
```

## Evaluation signals

- Ranked output includes p-values ≤ 0.05 for significantly active pathways; p-value distribution is consistent with multiple-testing-corrected significance thresholds
- Coverage statistics (F_coverage) are between 0 and 1, with most significant pathways showing >10% of unique pathway members detected in the dataset
- Activity scores are robust across technical replicates or independent samples within the same experimental group (verify by re-running with subsampled data or leave-one-out validation)
- Pathways ranked by PLAGE activity show biological coherence with known regulation in the experimental context; cross-validation with independent methods (qPCR, targeted assays) or literature confirms top-ranked pathways
- Comparison with ORA and GSEA results shows PLAGE is less affected by sporadic missing peaks; remove random peaks from intensity matrix and verify PLAGE ranking stability

## Limitations

- All peaks must have KEGG, ChEBI, or custom annotation; unannotated peaks are excluded, potentially biasing results toward well-characterized metabolites and away from unknowns
- PLAGE assumes a dominant linear mode of variation within each pathway; pathways with complex, multi-modal, or nonlinear activity patterns may be poorly represented
- Data imputation strategy (mean or minimum replacement) is fixed; highly sparse or zero-inflated intensity matrices may be distorted by imputation, reducing downstream reliability
- Reactome offline mode provides only metabolic pathways for common species; all-pathway analysis requires online mode with a local Neo4j Reactome server, adding infrastructure dependency
- PLAGE performance depends on pathway size and member overlap; very small pathways (<3 members) or highly overlapping pathways may produce unstable or redundant rankings

## Evidence

- [readme] PALS is amenable to analysis of any group of metabolite sets beyond pathways, including Molecular Families from GNPS and Mass2Motifs from MS2LDA: "the [decomposition approach] in PALS is amenable to the analysis of any group of metabolite sets, not just pathways"
- [readme] PLAGE results are more robust to noise and missing peaks than ORA and GSEA, which is critical for metabolomics data: "The results are found to be more robust to noise and missing peaks compared to the alternatives (ORA, GSEA). This is particularly important for metabolomics peak data, where noise and missing peaks"
- [readme] PALS decomposes pathway activity via the PLAGE singular value decomposition method: "decomposes activity levels in pathways via [the PLAGE method]"
- [readme] Data imputation replaces all-zero intensities with minimum value or factor mean; data is log₂-transformed and standardized: "if all of the samples in a single experimental factor have intensities of zero these are replaced by the minimum intensity value (which can be set by the user); and if only some of the sample values"
- [readme] PALS accepts peak intensity matrices and compound annotations; multiple peaks may map to multiple compounds: "As a result of the uncertainty in peak identification, multiple peak IDs may be mapped to multiple compound IDs and vice versa. As such, annotations are provided as another matrix having two columns."
