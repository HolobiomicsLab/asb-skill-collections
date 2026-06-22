---
name: set-activity-prioritization-ranking
description: Use when after computing activity scores for a collection of metabolite sets (pathways, GNPS Molecular Families, or MS2LDA Mass2Motifs) from intensity and annotation data.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
  tools:
  - PALS (Pathway Activity Level Scoring)
  - PALS Viewer
  - GNPS
  - MS2LDA
  - Reactome
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
---

# Set Activity Prioritization Ranking

## Summary

Rank metabolite sets (pathways, Molecular Families, Mass2Motifs) by their activity scores computed via singular value decomposition (PLAGE method) to prioritize functionally or compositionally coherent metabolite groups for downstream investigation. This skill is essential when multiple metabolite sets compete for analytical focus and noise/missing peaks make simpler scoring methods unreliable.

## When to use

Apply this skill after computing activity scores for a collection of metabolite sets (pathways, GNPS Molecular Families, or MS2LDA Mass2Motifs) from intensity and annotation data. Use it when you need to rank sets by biological or chemical relevance—particularly when metabolomics data contains significant noise and missing peaks, where the PLAGE decomposition approach is more robust than ORA or GSEA alternatives.

## When NOT to use

- Input intensity data is already preprocessed and normalized by an external tool; PALS performs log₂ transformation and standardization internally, which may introduce unwanted re-scaling.
- Metabolite sets are already individually ranked or filtered by external criteria; re-ranking may contradict prior prioritization logic.
- Feature-to-set annotations are sparse or unreliable (i.e., many features lack metabolite identifiers); coverage will be low and rankings unstable.

## Inputs

- Metabolite feature intensity matrix (CSV: rows=peak features with ID in column 1, columns=individual samples; optional second row specifies group assignments)
- Annotation matrix (CSV: two columns—peak ID and metabolite identifier as KEGG/ChEBI/GNPS/MS2LDA ID)
- Experimental design specification (case/control group pairings and comparison names)
- Pathway/metabolite set database selection (PiMP_KEGG, Reactome COMPOUND/ChEBI, GNPS Molecular Families, MS2LDA Mass2Motifs)

## Outputs

- Ranked metabolite set activity scores table (CSV with columns: set ID, activity score, p-value, unique pathway features, total dataset features, feature coverage)
- PALS Viewer–compatible prioritized results file
- Per-comparison activity score rankings

## How to apply

After loading a metabolite feature intensity matrix and assigning features to metabolite set annotations (via KEGG, ChEBI, GNPS, or MS2LDA databases), apply PALS decomposition via the PLAGE method to compute activity scores for each set. The method performs log₂ transformation and standardization (zero mean, unit variance) on the intensity matrix, then decomposes activity levels using singular value decomposition. Rank metabolite sets by the magnitude of their activity scores and export prioritized results in PALS Viewer–compatible format. Multiple comparisons (e.g., case/control pairs) can be specified; each comparison yields separate rankings. Export the ranked output as a CSV file with columns for set ID, activity score, p-value, and feature coverage metrics (unique features in set, dataset hits, and coverage fraction).

## Related tools

- **PALS (Pathway Activity Level Scoring)** (Core decomposition and ranking engine; applies PLAGE method to compute activity scores for metabolite sets) — https://github.com/glasgowcompbio/PALS
- **PALS Viewer** (Interactive web interface for running PALS, visualizing ranked results, and filtering/inspecting significantly changing metabolite sets) — https://pals.glasgowcompbio.org/app/
- **GNPS** (Provides Molecular Families metabolite set annotations for ranking) — http://gnps.ucsd.edu/
- **MS2LDA** (Provides Mass2Motifs metabolite set annotations for ranking) — http://ms2lda.org/
- **Reactome** (Pathway database for metabolic and non-metabolic pathway queries; supports COMPOUND, ChEBI, UniProt, and ENSEMBL ID matching)

## Examples

```
python pals/run.py PLAGE notebooks/test_data/HAT/int_df.csv notebooks/test_data/HAT/annotation_df.csv ranked_sets.csv --db PiMP_KEGG --comparisons Stage_1/Control Stage_2/Control --min_replace 5000
```

## Evaluation signals

- Output CSV contains exactly as many rows as input metabolite sets; no sets are dropped or duplicated during ranking.
- Activity scores and p-values are numeric; p-values are in [0, 1] range; no NaN or infinite values in output.
- Feature coverage (F_coverage) for each set is ≤ 1.0 (total dataset features ÷ unique pathway features); sets with zero coverage are either excluded or clearly marked.
- Rankings are consistent across re-runs with identical input data; deterministic sorting by activity score magnitude produces same order.
- Top-ranked sets show qualitatively higher feature coverage and lower p-values than bottom-ranked sets; visual inspection of top 10 vs bottom 10 confirms biological plausibility.

## Limitations

- PALS requires complete specification of experimental design (case/control pairings); missing or ambiguous comparisons cause errors or silent fallbacks.
- Data imputation (replacement of zero intensities by minimum or factor mean) introduces a small distortion; all-zero samples across a factor are replaced by the user-specified min_replace threshold (default 5000), which may be inappropriate for very low-abundance features.
- Reactome offline mode provides only metabolic pathways for most species; online mode (Neo4j server) required for all pathway types or less common organisms.
- Multiple peak IDs may map to multiple metabolite IDs (many-to-many); the annotation matrix preserves this ambiguity, which can inflate or deflate set coverage depending on deduplication strategy.
- PLAGE decomposition via singular value decomposition assumes linear activity relationships; non-linear pathway cross-talk or epistasis may not be captured.

## Evidence

- [readme] The results are found to be more robust to noise and missing peaks compared to the alternatives (ORA, GSEA). This is particularly important for metabolomics peak data, where noise and missing peaks are prevalent.: "The results are found to be more robust to noise and missing peaks compared to the alternatives (ORA, GSEA). This is particularly important for metabolomics peak data, where noise and missing peaks"
- [readme] the decomposition approach in PALS is amenable to the analysis of any group of metabolite sets, not just pathways: "the [decomposition approach] in PALS is amenable to the analysis of any group of metabolite sets, not just pathways"
- [readme] metabolite sets obtained from the grouping of metabolites according to their fragmentation spectra can also be analysed. This includes in particular Molecular Families from GNPS, as well as Mass2Motifs from MS2LDA.: "metabolite sets obtained from the grouping of metabolites according to their fragmentation spectra can also be analysed. This includes in particular *Molecular Families* from"
- [readme] decomposes activity levels in pathways via the PLAGE method: "decomposes activity levels in pathways via [the PLAGE method]"
- [readme] Data imputation is performed to the intensity matrix when it is loaded: if all of the samples in a single experimental factor have intensities of zero these are replaced by the minimum intensity value (which can be set by the user); and if only some of the sample values in a factor are zero then these are replaced by the mean value of the non-zero samples in that factor. The data is subsequently transformed to log-2 base and standardised using the preprocessing module in Scipy such that the intensity matrix has a zero mean and unit variance across the samples.: "Data imputation is performed to the intensity matrix when it is loaded: if all of the samples in a single experimental factor have intensities of zero these are replaced by the minimum intensity"
- [readme] Pathways are identified by their id and can be sorted by the p-value columns. The column unq_pw_F lists the unique formulae found in that pathway, tot_ds_F lists the formula hits found in the dataset, and F_coverage is the proportion of tot_ds_F to unq_pw_F.: "Pathways are identified by their id and can be sorted by the p-value columns. The column `unq_pw_F` lists the unique formulae found in that pathway, `tot_ds_F` lists the formula hits found in the"
