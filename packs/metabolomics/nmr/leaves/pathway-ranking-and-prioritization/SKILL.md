---
name: pathway-ranking-and-prioritization
description: 'Use when after peak annotation when you have: (1) a peak intensity matrix (rows=peaks with KEGG/ChEBI/UniProt IDs, columns=samples) with group labels; (2) a pathway database (KEGG, Reactome, or user-defined metabolite sets); (3) a comparative experimental design (case vs. control groups).'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_1812
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0601
  tools:
  - PALS (Pathway Activity Level Scoring)
  - PALS Viewer
  - PLAGE (Pathway Level Analysis of Gene Expression)
  - ORA (Over-Representation Analysis)
  - GSEA (Gene Set Enrichment Analysis)
  - GNPS (Global Natural Products Social Molecular Networking)
  - MS2LDA
  techniques:
  - LC-MS
  - NMR
derived_from:
- doi: 10.3390/metabo11020103
  title: pals
- doi: 10.1186/1471-2105-6-225
  title: ''
evidence_spans:
- we introduce **PALS (Pathway Activity Level Scoring)**, a complete tool that performs database queries of pathways, decomposes activity levels in pathways
- we introduce PALS (Pathway Activity Level Scoring), a complete tool that performs database queries of pathways, decomposes activity levels in pathways
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pals
    doi: 10.3390/metabo11020103
    title: pals
  dedup_kept_from: coll_pals
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3390/metabo11020103
  all_source_dois:
  - 10.3390/metabo11020103
  - 10.1186/1471-2105-6-225
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# pathway-ranking-and-prioritization

## Summary

Rank and prioritize metabolic or molecular pathways by computing activity level scores from intensity data and pathway definitions, then sorting by statistical significance. This skill enables hypothesis generation by identifying which pathways are most perturbed in a dataset, particularly robust to noise and missing peaks in metabolomics.

## When to use

Apply this skill after peak annotation when you have: (1) a peak intensity matrix (rows=peaks with KEGG/ChEBI/UniProt IDs, columns=samples) with group labels; (2) a pathway database (KEGG, Reactome, or user-defined metabolite sets); (3) a comparative experimental design (case vs. control groups). Use it to discover which pathways are significantly active or altered between conditions, especially when noise and missing peaks are prevalent in your data.

## When NOT to use

- Input peaks lack compound annotation — PALS requires metabolite identifiers (KEGG/ChEBI IDs) and will discard unannotated peaks, reducing power.
- You seek to identify novel/unannotated features — PALS relies entirely on pathway database membership; unmapped metabolites will not contribute to pathway scores.
- You have only a single sample or no biological replicates within groups — PALS requires group-level comparisons; insufficient replication precludes robust statistical inference.

## Inputs

- Peak intensity matrix (CSV: rows=peak IDs with KEGG/ChEBI/UniProt IDs, columns=samples; second row optionally encodes group membership)
- Peak annotation file (CSV: two columns — peak ID and metabolite entity ID, allowing many-to-many mappings)
- Pathway database identifier (e.g., PiMP_KEGG, COMPOUND, ChEBI, UniProt, ENSEMBL, or user-defined metabolite sets)
- Experimental design specification (case and control group names from sample columns)

## Outputs

- Ranked pathway table (CSV/DataFrame with columns: pathway ID, pathway name, activity score, p-value, unq_pw_F [unique formulae in pathway], tot_ds_F [formula hits in dataset], F_coverage [proportion])
- Prioritized list of pathways sorted by statistical significance (p-value)
- Optional: annotated visualization showing active pathways and metabolite coverage

## How to apply

Load the intensity matrix (log₂-transformed and standardized to zero mean and unit variance) and annotation file (peak ID → metabolite entity ID) into PALS. Specify the pathway database (PiMP_KEGG, COMPOUND, ChEBI for metabolomics; UniProt/ENSEMBL for proteomics/transcriptomics), the analysis method (PLAGE preferred for robustness to noise), and comparisons as case/control pairs (e.g., 'Stage_1/Control'). Data imputation replaces zero intensities: all zeros in a group → minimum value; partial zeros → group mean. PALS decomposes each pathway via singular value decomposition (SVD), extracts the first principal component as the pathway activity score, scales across all pathways, and ranks by p-value. The output table lists pathway IDs, activity scores, p-values, unique metabolites in pathway, dataset hits, and coverage fraction.

## Related tools

- **PALS (Pathway Activity Level Scoring)** (Primary tool: performs pathway database queries, decomposes activity levels via PLAGE, scales and ranks pathways, outputs ranked results) — https://github.com/glasgowcompbio/PALS
- **PALS Viewer** (Interactive web interface for running PALS, visualizing pathway ranking results, and inspecting significantly changing pathways) — https://pals.glasgowcompbio.org/app/
- **PLAGE (Pathway Level Analysis of Gene Expression)** (Decomposition method embedded in PALS that applies SVD to each pathway's metabolites to compute activity scores) — https://bmcbioinformatics.biomedcentral.com/articles/10.1186/1471-2105-6-225
- **ORA (Over-Representation Analysis)** (Alternative pathway ranking method included in PALS for benchmarking; less robust to noise than PLAGE) — https://github.com/glasgowcompbio/PALS
- **GSEA (Gene Set Enrichment Analysis)** (Alternative pathway ranking method included in PALS for benchmarking; less robust to noise than PLAGE) — https://github.com/glasgowcompbio/PALS
- **GNPS (Global Natural Products Social Molecular Networking)** (Source of Molecular Families metabolite groupings that can be analyzed as metabolite sets in PALS) — http://gnps.ucsd.edu/
- **MS2LDA** (Source of Mass2Motifs metabolite groupings that can be analyzed as metabolite sets in PALS) — http://ms2lda.org/

## Examples

```
python pals/run.py PLAGE notebooks/test_data/HAT/int_df.csv notebooks/test_data/HAT/annotation_df.csv test_output.csv --db PiMP_KEGG --comparisons Stage_1/Control Stage_2/Control
```

## Evaluation signals

- Pathway coverage metrics are realistic: F_coverage (ratio of tot_ds_F to unq_pw_F) is typically 5–30% for well-matched datasets; suspiciously high coverage (>50%) suggests over-annotation or database mismatch.
- Ranked pathways are biologically coherent: top-ranked pathways share metabolites and are connected in known biochemical networks (e.g., related amino acid metabolism pathways rank together).
- Robustness check: rerun with ORA and GSEA; PLAGE results should show lower p-values and higher rank stability when data contain noise or missing peaks, confirming PLAGE's stated robustness advantage.
- P-value distribution is sensible: a few pathways with p < 0.05, majority with p > 0.1; extreme clustering (all p ≈ 0 or all p ≈ 1) indicates data imputation or scaling failure.
- Sample reproducibility: repeat on subsampled or hold-out data; top-ranked pathways should remain stable and maintain consistent directionality of activity scores across runs.

## Limitations

- Pathway ranking depends critically on annotation quality: many-to-many peak-to-metabolite mappings can inflate or deflate coverage; orthogonal validation (e.g., NMR, targeted MS/MS) of top candidates is advisable.
- PLAGE assumes metabolites in a pathway contribute independently to the first principal component (SVD assumption); if metabolites are highly correlated or kinetically coupled, the first PC may not capture true pathway activity.
- Limited metabolite set scope: PALS analysis is restricted to metabolites present in the chosen database (KEGG, Reactome, GNPS, MS2LDA); novel or non-standard metabolites will be ignored.
- Data imputation introduces bias: replacing all-zero groups with minimum intensity or partial-zero samples with group mean assumes missing values are missing-at-random; systematic loss (e.g., instrument dynamic range exceeded) will bias activity scores.
- Requires sufficient replication within groups to support statistical inference; single-sample or small-sample designs (n < 3 per group) yield unstable p-value estimates and are not recommended.

## Evidence

- [other] For each pathway, apply PLAGE (Pathway Level Analysis of Gene Expression) decomposition via singular value decomposition (SVD) on the subset of metabolites assigned to that pathway.: "For each pathway, apply PLAGE (Pathway Level Analysis of Gene Expression) decomposition via singular value decomposition (SVD) on the subset of metabolites assigned to that pathway."
- [other] Extract the first principal component (singular vector) from each pathway's SVD as the pathway activity score.: "Extract the first principal component (singular vector) from each pathway's SVD as the pathway activity score."
- [readme] The results are found to be more robust to noise and missing peaks compared to the alternatives (ORA, GSEA). This is particularly important for metabolomics peak data, where noise and missing peaks are prevalent.: "The results are found to be more robust to noise and missing peaks compared to the alternatives (ORA, GSEA). This is particularly important for metabolomics peak data, where noise and missing peaks"
- [readme] Data imputation is performed to the intensity matrix when it is loaded: if all of the samples in a single experimental factor have intensities of zero these are replaced by the minimum intensity value (which can be set by the user); and if only some of the sample values in a factor are zero then these are replaced by the mean value of the non-zero samples in that factor.: "if all of the samples in a single experimental factor have intensities of zero these are replaced by the minimum intensity value; and if only some of the sample values in a factor are zero then these"
- [readme] The data is subsequently transformed to log-2 base and standardised using the preprocessing module in Scipy such that the intensity matrix has a zero mean and unit variance across the samples.: "The data is subsequently transformed to log-2 base and standardised using the preprocessing module in Scipy such that the intensity matrix has a zero mean and unit variance across the samples."
- [readme] Pathways are identified by their id and can be sorted by the `p-value` columns. The column `unq_pw_F` lists the unique formulae found in that pathway, `tot_ds_F` lists the formula hits found in the dataset, and `F_coverage` is the proportion of `tot_ds_F` to `unq_pw_F`.: "Pathways are identified by their id and can be sorted by the `p-value` columns. The column `unq_pw_F` lists the unique formulae found in that pathway, `tot_ds_F` lists the formula hits found in the"
- [readme] performs database queries of pathways, decomposes activity levels in pathways via the PLAGE method, as well as presents the results in a user-friendly manner: "performs database queries of pathways, decomposes activity levels in pathways via the PLAGE method, as well as presents the results in a user-friendly manner"
- [readme] the decomposition approach in PALS is amenable to the analysis of any group of metabolite sets, not just pathways: "the decomposition approach in PALS is amenable to the analysis of any group of metabolite sets, not just pathways"
