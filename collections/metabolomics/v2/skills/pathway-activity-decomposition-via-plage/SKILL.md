---
name: pathway-activity-decomposition-via-plage
description: Use when you have a log2-transformed, standardized peak intensity matrix (rows = metabolite features, columns = samples) with compound annotations mapped to curated pathway databases (KEGG, Reactome, or custom metabolite sets), and you need to rank pathways by their activity level while tolerating.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3501
  edam_topics:
  - http://edamontology.org/topic_0621
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0601
  tools:
  - PALS (Pathway Activity Level Scoring)
  - PALS Viewer
  - ORA (Over-Representation Analysis)
  - GSEA (Gene Set Enrichment Analysis)
  - GNPS (Global Natural Products Social Molecular Networking)
  - MS2LDA
derived_from:
- doi: 10.3390/metabo11020103
  title: pals
- doi: 10.1186/1471-2105-6-225
  title: ''
evidence_spans:
- we introduce **PALS (Pathway Activity Level Scoring)**, a complete tool that performs database queries of pathways, decomposes activity levels in pathways
- we introduce PALS (Pathway Activity Level Scoring), a complete tool that performs database queries of pathways, decomposes activity levels in pathways
- PALS Viewer
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# pathway-activity-decomposition-via-plage

## Summary

PLAGE (Pathway Level Analysis using Gene Expression) decomposes peak intensity or gene expression matrices into pathway activity scores by applying singular value decomposition to metabolite or gene groups within curated pathways. This rank-based approach is more robust to noise and missing peaks than alternatives like ORA and GSEA, making it well-suited for metabolomics datasets with incomplete or noisy peak detection.

## When to use

Apply this skill when you have a log2-transformed, standardized peak intensity matrix (rows = metabolite features, columns = samples) with compound annotations mapped to curated pathway databases (KEGG, Reactome, or custom metabolite sets), and you need to rank pathways by their activity level while tolerating missing peaks or detection noise. Particularly useful when comparing metabolomics samples across experimental groups where peak absence due to instrumental noise or stochastic ionization is common.

## When NOT to use

- Do not use if you have already collapsed your peak data into a pre-computed pathway activity or summary table; PLAGE requires raw or minimally processed intensity values.
- Do not use if your metabolite annotations are sparse (<<5% of peaks) or your pathway definitions contain almost no detected metabolites—SVD will be unreliable with too few features per pathway.
- Do not use if you need gene expression pathway analysis with transcript-level data (use UniProt or ENSEMBL database options in PALS instead).

## Inputs

- Peak intensity matrix (CSV): rows = peak IDs, columns = sample measurements, optional second row for sample group labels
- Compound annotation matrix (CSV): two columns (peak ID, KEGG/ChEBI/custom metabolite ID); multiple peaks can map to one metabolite
- Experimental design specification: dictionary or CSV defining groups (sample→group) and comparisons (case vs. control)
- Pathway or metabolite set database: KEGG (via PiMP), Reactome COMPOUND/ChEBI/protein (local or Neo4j server), or user-supplied CSV/JSON of metabolite set memberships

## Outputs

- Pathway ranking table (CSV or DataFrame): pathway ID, pathway name, pathway activity score (first SVD component weight), p-value, adjusted p-value, metabolite coverage (unique pathway metabolites vs. detected metabolites)
- Per-sample pathway activity levels (if programmatic output): activity score for each pathway in each sample comparison

## How to apply

Load the peak intensity matrix and annotation file (peak ID → KEGG/ChEBI/custom metabolite ID mapping) into a DataSource object specifying the pathway database (PiMP_KEGG, COMPOUND, ChEBI, or user-defined). Apply data imputation: replace all-zero values in a factor with the minimum intensity threshold (default 5000); replace partial-zero values with the non-zero factor mean. Log2-transform and standardize (zero mean, unit variance across samples). Decompose each pathway (or custom metabolite set) using singular value decomposition: compute the first principal component (eigenvector) across the matched metabolites within that group, then weight samples by this component to obtain a pathway activity score. Compute p-values for each pathway activity score under the null hypothesis of no association. Rank pathways by p-value or activity magnitude. The robustness comes from SVD's tolerance to missing values and noise—single missing or noisy peaks have minimal influence on the principal component.

## Related tools

- **PALS (Pathway Activity Level Scoring)** (Complete implementation of PLAGE decomposition method; performs database queries, applies PLAGE, and outputs ranked pathway activity scores) — https://github.com/glasgowcompbio/PALS
- **PALS Viewer** (Web interface (Streamlit-based) for running PALS interactively, visualizing pathway rankings, and inspecting significantly changing pathways) — https://pals.glasgowcompbio.org/app/
- **ORA (Over-Representation Analysis)** (Alternative pathway ranking method included in PALS for benchmarking; does not decompose activity, uses presence/absence of pathway members) — https://github.com/glasgowcompbio/PALS
- **GSEA (Gene Set Enrichment Analysis)** (Alternative pathway ranking method included in PALS for benchmarking; less robust to missing peaks than PLAGE) — https://github.com/glasgowcompbio/PALS
- **GNPS (Global Natural Products Social Molecular Networking)** (Source of Molecular Family metabolite groupings that can be analyzed using PLAGE via PALS Viewer) — http://gnps.ucsd.edu/
- **MS2LDA** (Source of Mass2Motif metabolite groupings that can be analyzed using PLAGE via PALS Viewer) — http://ms2lda.org/

## Examples

```
python pals/run.py PLAGE notebooks/test_data/HAT/int_df.csv notebooks/test_data/HAT/annotation_df.csv test_output.csv --db PiMP_KEGG --comparisons Stage_1/Control Stage_2/Control --min_replace 5000
```

## Evaluation signals

- Rank-order correlation (Spearman's ρ or Kendall's τ) between pathway rankings from noisy/incomplete vs. clean baseline data should remain >0.8 across ≤20% Gaussian noise and ≤15% random peak removal rates, demonstrating robustness.
- Top-K pathway retention: ≥80% of top-5 pathways should persist in the top-K set across simulated noise and peak dropout, indicating stable ranking despite perturbation.
- Coverage metric plausibility: the proportion of pathway metabolites detected in the dataset should be >0 and reasonably match database expectations; pathways with zero-coverage metabolites should be excluded or flagged.
- P-value distribution: p-values across the ranked pathway list should show a U-shaped or monotonic increasing pattern; extreme clustering (all near 0 or all near 1) suggests computation or calibration errors.
- Comparison to ORA/GSEA: PLAGE rankings should show lower rank-correlation degradation under noise than ORA or GSEA applied to the same data, confirming improved robustness.

## Limitations

- PLAGE performance degrades if pathways have very few detected metabolites (<3–5); filtering out small pathways or pooling related pathways is recommended.
- Annotations are source-limited: if peak identification is uncertain (one peak maps to multiple metabolites or vice versa), pathway assignments will propagate this ambiguity; high-confidence annotation is prerequisite.
- Database completeness: pathways from KEGG or Reactome may not reflect all relevant metabolic processes for a given organism or tissue; missing or outdated pathway definitions limit interpretability.
- Activity scores are relative, not absolute: they represent the singular value (variance explained by the first principal component) within each pathway, not a biochemical flux or concentration. Comparisons across pathways with very different pathway sizes should be interpreted cautiously.
- Data preprocessing is critical: PLAGE assumes log2-transformed, standardized intensity data; improper imputation thresholds or skipped standardization can inflate or deflate activity scores unpredictably.

## Evidence

- [intro] PLAGE method and robustness claim: "performs database queries of pathways, decomposes activity levels in pathways via the PLAGE method, as well as presents the results in a user-friendly manner. The results are found to be more robust"
- [intro] Extensibility to custom metabolite sets: "the decomposition approach in PALS is amenable to the analysis of any group of metabolite sets, not just pathways"
- [other] Workflow: establish baseline, perturb, score, compare: "Establish clean baseline by running PALS on unperturbed data and record ranked pathway activity scores. For each noise level... create a perturbed copy of the dataset. Run PALS on each perturbed"
- [readme] Data imputation details: "if all of the samples in a single experimental factor have intensities of zero these are replaced by the minimum intensity value (which can be set by the user); and if only some of the sample values"
- [readme] Importance for metabolomics: "This is particularly important for metabolomics peak data, where noise and missing peaks are prevalent."
- [readme] Output columns and interpretation: "Pathways are identified by their id and can be sorted by the p-value columns. The column unq_pw_F lists the unique formulae found in that pathway, tot_ds_F lists the formula hits found in the"
