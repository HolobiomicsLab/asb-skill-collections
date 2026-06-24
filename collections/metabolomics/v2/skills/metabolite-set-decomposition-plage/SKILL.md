---
name: metabolite-set-decomposition-plage
description: Use when you have peak intensity data from metabolomics experiments with
  annotated metabolites assigned to known groupings (KEGG pathways, Reactome, GNPS
  Molecular Families, or MS2LDA Mass2Motifs) and need to identify which metabolite
  sets change significantly across experimental comparisons while.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - GNPS
  - MS2LDA
  - PALS (Pathway Activity Level Scoring)
  - PALS Viewer
  - Reactome
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.3390/metabo11020103
  title: pals
- doi: 10.1186/1471-2105-6-225
  title: ''
evidence_spans:
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

# metabolite-set-decomposition-plage

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Apply the PLAGE (Pathway Level Analysis using Gene Expression) singular value decomposition method to compute activity scores for metabolite groupings (pathways, Molecular Families, Mass2Motifs) across experimental samples. This method decomposes metabolite set expression patterns into a single robust score per grouping and comparison, yielding results more robust to noise and missing peaks than ORA or GSEA.

## When to use

You have peak intensity data from metabolomics experiments with annotated metabolites assigned to known groupings (KEGG pathways, Reactome, GNPS Molecular Families, or MS2LDA Mass2Motifs) and need to identify which metabolite sets change significantly across experimental comparisons while tolerating missing or noisy peak measurements.

## When NOT to use

- Peak intensities have not been normalized or log2-transformed; PLAGE assumes standardized input.
- Metabolite annotations are sparse or absent for most peaks; PLAGE requires sufficient mapping to pathway/set definitions.
- You need to identify individual metabolite drivers rather than aggregate set-level activity; PLAGE produces a single score per set and is not suited for feature-level ranking.

## Inputs

- Peak intensity CSV matrix (row_id and sample columns, optional group annotation row)
- Peak annotation CSV (peak ID → KEGG/ChEBI/UniProt/ENSEMBL identifier mapping)
- Experimental design specification (group names and case/control comparisons)
- Metabolite set definitions from selected database (KEGG, Reactome, GNPS, MS2LDA)

## Outputs

- Ranked metabolite set activity scores table (by p-value)
- Pathway/metabolite-set identifiers with unique metabolite count, dataset metabolite hits, and coverage proportion
- Activity score decompositions per comparison
- Optionally: visualizations of significant metabolite sets (PALS Viewer)

## How to apply

Load log2-transformed, mean-centered intensity matrix (rows=peak features, columns=samples) and annotation matrix (peak ID → metabolite identifier) into PALS. Specify the pathway/metabolite-set database (PiMP_KEGG, COMPOUND, ChEBI, GNPS Molecular Families, or MS2LDA Mass2Motifs), experimental design (group assignments and case/control comparisons), and data imputation minimum (default 5000). PALS will impute zero values: all-zero samples replaced by min_replace; partial-zero samples replaced by group mean. Apply PLAGE decomposition to compute a single activity score per metabolite set per comparison using singular value decomposition of the normalized expression matrix within each set. Output ranked metabolite sets by p-value, with metrics for metabolite coverage and robustness to noise.

## Related tools

- **PALS (Pathway Activity Level Scoring)** (Core decomposition engine implementing PLAGE method and pathway/metabolite-set database queries) — https://github.com/glasgowcompbio/PALS
- **PALS Viewer** (Web interface (Streamlit-based) for running PALS, visualizing results, and prioritizing Molecular Families and Mass2Motifs) — https://pals.glasgowcompbio.org/app/
- **GNPS** (Source of Molecular Families metabolite groupings for analysis) — http://gnps.ucsd.edu/
- **MS2LDA** (Source of Mass2Motifs metabolite groupings for analysis) — http://ms2lda.org/
- **Reactome** (Pathway database for metabolic (and all-pathway) queries in online or offline mode) — http://reactome.org

## Examples

```
python pals/run.py PLAGE notebooks/test_data/HAT/int_df.csv notebooks/test_data/HAT/annotation_df.csv test_output.csv --db PiMP_KEGG --comparisons Stage_1/Control Stage_2/Control
```

## Evaluation signals

- Activity scores are computed and output for every metabolite set in at least one specified comparison.
- P-values and coverage statistics (F_coverage = tot_ds_F / unq_pw_F) are calculated and ranked; coverage > 0 indicates metabolite matches.
- Robustness check: activity scores remain stable when noise is added to peak intensities or peaks are randomly removed, compared to ORA/GSEA baseline.
- Log2 transformation and standardization (zero mean, unit variance) are applied to the intensity matrix before SVD decomposition.
- Missing-peak tolerance: all-zero samples replaced by min_replace value; partial-zero samples replaced by group mean per documentation.

## Limitations

- PLAGE requires sufficient metabolite coverage within each pathway or set; sets with very few matches to the input data will have high uncertainty in activity scores.
- Data imputation relies on a user-specified minimum intensity threshold (default 5000); choice of this value can influence downstream rankings and may require validation.
- Offline Reactome queries provide only metabolic pathways for most species; all-pathway analysis requires online mode and a local Neo4j server.
- Multiple peak-to-metabolite mappings are allowed but not explicitly disambiguated in the scoring; the method treats all mappings equally.
- PLAGE is less sensitive than ORA or GSEA to small effect sizes in individual metabolites; the aggregation smooths singleton findings.

## Evidence

- [readme] we introduce **PALS (Pathway Activity Level Scoring)**, a complete tool that performs database queries of pathways, decomposes activity levels in pathways via [the PLAGE method], as well as presents the results in a user-friendly manner: "performs database queries of pathways, decomposes activity levels in pathways via [the PLAGE method]"
- [readme] The results are found to be more robust to noise and missing peaks compared to the alternatives (ORA, GSEA). This is particularly important for metabolomics peak data, where noise and missing peaks are prevalent.: "more robust to noise and missing peaks compared to the alternatives (ORA, GSEA). This is particularly important for metabolomics peak data"
- [readme] the [decomposition approach] in PALS is amenable to the analysis of any group of metabolite sets, not just pathways: "decomposition approach in PALS is amenable to the analysis of any group of metabolite sets, not just pathways"
- [readme] As demonstrated in PALS Viewer, metabolite sets obtained from the grouping of metabolites according to their fragmentation spectra can also be analysed. This includes in particular *Molecular Families* from [GNPS], as well as *Mass2Motifs* from [MS2LDA].: "metabolite sets obtained from the grouping of metabolites according to their fragmentation spectra can also be analysed. This includes in particular *Molecular Families* from [GNPS], as well as"
- [readme] Data imputation is performed to the intensity matrix when it is loaded: if all of the samples in a single experimental factor have intensities of zero these are replaced by the minimum intensity value (which can be set by the user); and if only some of the sample values in a factor are zero then these are replaced by the mean value of the non-zero samples in that factor. The data is subsequently transformed to log-2 base and standardised using the preprocessing module in Scipy such that the intensity matrix has a zero mean and unit variance across the samples.: "intensity matrix when it is loaded: if all of the samples in a single experimental factor have intensities of zero these are replaced by the minimum intensity value; and if only some of the sample"
