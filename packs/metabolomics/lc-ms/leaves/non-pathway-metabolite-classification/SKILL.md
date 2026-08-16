---
name: non-pathway-metabolite-classification
description: Use when you have metabolomics intensity data with peak annotations, and you want to rank and prioritize metabolite groupings (Molecular Families, Mass2Motifs, or other non-pathway metabolite sets) by their activity levels across experimental contrasts.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3680
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3172
  tools:
  - PALS (Pathway Activity Level Scoring)
  - GNPS
  - MS2LDA
  - PALS Viewer
  - GNPS (Global Natural Products Social Molecular Networking)
  techniques:
  - LC-MS
derived_from:
- doi: 10.3390/metabo11020103
  title: pals
- doi: 10.1186/1471-2105-6-225
  title: ''
evidence_spans:
- we introduce **PALS (Pathway Activity Level Scoring)**, a complete tool that performs database queries of pathways, decomposes activity levels in pathways
- we introduce PALS (Pathway Activity Level Scoring), a complete tool that performs database queries of pathways, decomposes activity levels in pathways
- Molecular Families from GNPS
- Mass2Motifs from MS2LDA
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

# Non-pathway metabolite classification

## Summary

Apply the PLAGE decomposition method to metabolite groupings beyond canonical pathways—such as Molecular Families from GNPS or Mass2Motifs from MS2LDA—to compute activity scores and rank metabolite sets by differential abundance across experimental conditions. This generalizes pathway-level scoring to any coherent metabolite classification scheme.

## When to use

You have metabolomics intensity data with peak annotations, and you want to rank and prioritize metabolite groupings (Molecular Families, Mass2Motifs, or other non-pathway metabolite sets) by their activity levels across experimental contrasts. Use this when pathway databases are unavailable, inapplicable, or when you want to leverage spectral clustering outputs (GNPS or MS2LDA) instead of curated pathway resources.

## When NOT to use

- Your input is already a pre-computed feature/metabolite set activity table or abundance matrix—you would use this skill to generate such a table, not consume it.
- You have no metabolite grouping scheme (neither pathways nor spectral clustering) and want to analyze individual metabolites instead; use univariate differential abundance testing.
- Your goal is to validate pathway annotations or curate metabolite networks; this skill ranks sets but does not curate or validate them.

## Inputs

- Metabolomics intensity matrix (CSV): peak IDs × samples, with optional group labels row
- Peak annotation file (CSV): peak ID → metabolite database ID (KEGG, ChEBI, or custom identifier)
- Non-pathway metabolite set definitions (dict or file): set name/ID → list of member peak/metabolite IDs (e.g., from GNPS Molecular Families or MS2LDA Mass2Motifs)
- Experimental design specification: sample-to-group mapping and case/control comparisons

## Outputs

- Ranked metabolite set activity table (CSV or DataFrame): columns include set ID, activity score per sample/comparison, p-value, fold-change, member coverage
- Activity score matrix: metabolite sets × samples (log2-standardized)
- Visualization (optional): plots of significantly changing sets across experimental contrasts

## How to apply

Load your metabolomics intensity CSV (rows=peak IDs, columns=samples, optional second row=group labels) and a two-column annotation CSV (peak ID → metabolite identifier) into PALS. Instead of querying a pathway database, supply your own metabolite groupings as a dictionary or data structure mapping each group (e.g., 'MF0001', 'Mass2Motif_42') to member peak/compound IDs. Apply the PLAGE method to compute log2-standardized activity scores for each metabolite set per sample, using singular value decomposition to extract the first principal component as the set-level activity. Optionally impute zero intensities (default minimum 5000) and specify experimental comparisons (e.g., case/control pairs) to rank sets by p-value or fold-change. The resulting ranked table will show activity scores, p-values, and metabolite coverage for each grouping, ranked by statistical significance.

## Related tools

- **PALS (Pathway Activity Level Scoring)** (Core tool that performs PLAGE decomposition and activity scoring on metabolite sets (pathways or non-pathway groupings); accepts intensity and annotation matrices and outputs ranked set-level activity tables.) — https://github.com/glasgowcompbio/PALS
- **PALS Viewer** (Web interface (Streamlit-based) for running PALS, visualizing ranked metabolite set results, and prioritizing Molecular Families and Mass2Motifs by activity levels from GNPS/MS2LDA analyses.) — https://pals.glasgowcompbio.org/app/
- **GNPS (Global Natural Products Social Molecular Networking)** (Source of Molecular Family groupings; PALS can import and rank Molecular Families as metabolite sets.) — http://gnps.ucsd.edu/
- **MS2LDA** (Source of Mass2Motif groupings; PALS can import and rank Mass2Motifs as metabolite sets.) — http://ms2lda.org/

## Examples

```
python pals/run.py PLAGE intensity_data.csv annotations.csv output_ranked_sets.csv --db COMPOUND --comparisons treatment/control --min_replace 5000
```

## Evaluation signals

- Activity scores are computed for every metabolite set and every sample/comparison; no missing or NaN values where data is present.
- Sets with higher activity scores (larger first principal component magnitude) should correspond to metabolites with consistently higher or lower intensity across samples in their comparison group; validate by spot-checking members of top-ranked sets.
- P-values should be well-distributed and monotonic with effect size (sets with larger fold-changes or more consistent activity patterns should have lower p-values).
- Results are more robust to noise and missing peak intensity values compared to ORA (Over-Representation Analysis) or GSEA (Gene Set Enrichment Analysis); compare activity rankings across replicates or subsampled datasets to confirm stability.
- Metabolite coverage (proportion of set members found in the input dataset) should be transparent and reported; sets with very low coverage (< 10% of members detected) may be unreliable.

## Limitations

- PLAGE assumes that metabolite intensities within a set are correlated and can be summarized by a single principal component; sets with heterogeneous or antagonistic intensity patterns may not be well-represented.
- Accuracy depends on quality of peak annotations and assignment to metabolite groupings; many-to-many mappings (multiple peaks per compound, multiple compounds per peak) can introduce ambiguity.
- Requires user to define or import metabolite groupings (Molecular Families, Mass2Motifs, etc.); no automatic discovery of sets from raw data.
- Data imputation strategy (replace zeros with minimum intensity or group mean) is crude and may introduce bias if missingness is non-random (e.g., below detection limit); preprocessing and missing-value handling should be validated on domain-specific grounds.

## Evidence

- [readme] the decomposition approach in PALS is amenable to the analysis of any group of metabolite sets, not just pathways: "the [decomposition approach] in PALS is amenable to the analysis of any group of metabolite sets, not just pathways"
- [readme] metabolite sets obtained from the grouping of metabolites according to their fragmentation spectra can also be analysed. This includes in particular Molecular Families from GNPS, as well as Mass2Motifs from MS2LDA: "metabolite sets obtained from the grouping of metabolites according to their fragmentation spectra can also be analysed. This includes in particular *Molecular Families* from"
- [intro] decomposes activity levels in pathways via the PLAGE method: "decomposes activity levels in pathways via [the PLAGE method]"
- [readme] The results are found to be more robust to noise and missing peaks compared to the alternatives (ORA, GSEA). This is particularly important for metabolomics peak data, where noise and missing peaks are prevalent.: "The results are found to be more robust to noise and missing peaks compared to the alternatives (ORA, GSEA). This is particularly important for metabolomics peak data, where noise and missing peaks"
- [readme] Data imputation is performed to the intensity matrix when it is loaded: if all of the samples in a single experimental factor have intensities of zero these are replaced by the minimum intensity value (which can be set by the user); and if only some of the sample values in a factor are zero then these are replaced by the mean value of the non-zero samples in that factor.: "Data imputation is performed to the intensity matrix when it is loaded: if all of the samples in a single experimental factor have intensities of zero these are replaced by the minimum intensity"
