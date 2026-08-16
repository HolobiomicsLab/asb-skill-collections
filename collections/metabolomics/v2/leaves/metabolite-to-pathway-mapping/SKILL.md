---
name: metabolite-to-pathway-mapping
description: Use when you have a peak intensity matrix (samples × metabolites) with
  assigned metabolite annotations (peak ID → KEGG or ChEBI compound ID), and you need
  to link those identities to known metabolic pathways, molecular families, or mass2motifs
  before computing pathway activity scores.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3172
  tools:
  - PALS (Pathway Activity Level Scoring)
  - PALS
  - PALS Viewer
  - GNPS
  - MS2LDA
  license_tier: open
derived_from:
- doi: 10.3390/metabo11020103
  title: pals
evidence_spans:
- we introduce **PALS (Pathway Activity Level Scoring)**, a complete tool that performs
  database queries of pathways
- we introduce **PALS (Pathway Activity Level Scoring)**, a complete tool that performs
  database queries of pathways,
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

# metabolite-to-pathway-mapping

## Summary

Map individual metabolite intensity features to curated pathway definitions (KEGG, Reactome, or user-defined metabolite sets) in order to aggregate intensities at the pathway level for downstream activity scoring. This is a prerequisite step for pathway-level analysis methods like PLAGE, ORA, and GSEA.

## When to use

You have a peak intensity matrix (samples × metabolites) with assigned metabolite annotations (peak ID → KEGG or ChEBI compound ID), and you need to link those identities to known metabolic pathways, molecular families, or mass2motifs before computing pathway activity scores. Use this skill when annotation uncertainty exists (multiple peaks mapping to one compound, or vice versa) and you need a systematic, database-backed approach to define which metabolites belong to which pathways.

## When NOT to use

- If intensity data is already aggregated at the pathway level (i.e., pathway activity scores or pathway-level features already computed) — mapping has already been performed.
- If you lack valid metabolite annotations (peak identifications) for your dataset — mapping requires KEGG or ChEBI IDs and cannot proceed with unidentified peaks.
- If your experimental design involves proteomics (UniProt) or transcriptomics (ENSEMBL) but you are analyzing metabolomics data — use the metabolomics-appropriate database (COMPOUND, ChEBI, or PiMP_KEGG).

## Inputs

- Peak intensity matrix (CSV: samples as columns, peaks as rows with peak IDs in first column; optionally a second row specifying sample group membership)
- Peak annotation dataframe (two columns: peak ID → KEGG/ChEBI metabolite ID; multiple annotations per peak allowed)
- Pathway database specification (database name: PiMP_KEGG, COMPOUND, ChEBI, UniProt, or ENSEMBL; species name for Reactome queries; optional flag for metabolic-only vs. all pathways)

## Outputs

- Pathway × metabolite membership matrix (sparse, defining which metabolites belong to each pathway)
- Pathway-specific intensity submatrices (one submatrix per pathway, dimensions: samples × metabolites_in_pathway)
- Annotation coverage report (number of peaks mapped, unmapped, multi-annotated; pathway coverage statistics)

## How to apply

First, load the peak intensity matrix (log2-transformed and standardized across samples) and a two-column annotation dataframe where rows are peak IDs and the second column contains KEGG or ChEBI identifiers. Query a pathway database (PiMP_KEGG, Reactome COMPOUND/ChEBI, or a user-defined metabolite set) to retrieve pathway definitions as mappings from pathway identifiers to sets of metabolite IDs. For each pathway, extract the subset of intensity columns corresponding to metabolites in that pathway's definition. Retain only peaks with valid annotations; discard unannotated peaks. The result is a collection of pathway-specific metabolite intensity submatrices, one per pathway, ready for SVD-based decomposition or other pathway activity calculations. Handle missing data before mapping: impute zero intensities within experimental factors using minimum intensity (typically 5000) or the mean of non-zero samples in that factor.

## Related tools

- **PALS (Pathway Activity Level Scoring)** (Performs pathway queries and decomposes activity levels after metabolite-to-pathway mapping; integrates mapping with PLAGE/ORA/GSEA methods) — https://github.com/glasgowcompbio/PALS
- **PALS Viewer** (Web interface for interactive pathway mapping, visualization, and prioritization of metabolite sets (pathways, Molecular Families, Mass2Motifs)) — https://pals.glasgowcompbio.org/app/
- **GNPS** (Source of Molecular Families (metabolite sets) that can be mapped and analyzed as alternatives to canonical pathways) — http://gnps.ucsd.edu/
- **MS2LDA** (Source of Mass2Motifs (metabolite spectral motif groupings) that can be mapped and prioritized by pathway activity) — http://ms2lda.org/

## Examples

```
python pals/run.py PLAGE notebooks/test_data/HAT/int_df.csv notebooks/test_data/HAT/annotation_df.csv test_output.csv --db PiMP_KEGG --comparisons Stage_1/Control Stage_2/Control --min_replace 5000
```

## Evaluation signals

- Coverage check: percentage of peaks with valid KEGG/ChEBI annotations successfully mapped to pathways (typically >50% in well-curated metabolomics datasets); count of unmapped peaks should be recorded.
- Pathway coverage: for each pathway, the number of metabolites in the intensity data that match the pathway definition (F_coverage metric in output: tot_ds_F / unq_pw_F); pathways with <10% coverage may be excluded or flagged.
- No information loss: verify that the pathway-specific submatrices retain all intensity values for mapped metabolites and that the sum of submatrices equals the original intensity matrix (sample-wise).
- Consistency with multiple annotations: confirm that peaks annotated to multiple metabolites are represented in all corresponding pathway submatrices (or documented as handled correctly per the mapping rule).
- Robustness to imputation: verify that data imputation (zero-fill and mean-fill per factor) was applied before mapping, and that log2-transformation and standardization are reflected in the submatrix statistics (zero mean, unit variance across samples).

## Limitations

- Annotation uncertainty: multiple peaks can map to the same metabolite, and one peak can have multiple annotations; this ambiguity is preserved in the output and may inflate or deflate pathway signal depending on the downstream analysis.
- Database incompleteness: pathways in PiMP_KEGG or Reactome may not capture all metabolites in your sample; metabolites with no known pathway assignments will be discarded.
- Species specificity: Reactome pathway definitions are species-dependent; mapping with the wrong species parameter (default: Homo sapiens) will omit species-specific pathways or include irrelevant ones.
- Missing peaks in pathway definitions: if a pathway is defined in the database but none of its metabolites are detected in your samples, that pathway will have an empty or very sparse submatrix, reducing power for downstream activity scoring.
- Data imputation sensitivity: the choice of minimum intensity threshold (default: 5000) for zero-fill imputation can affect which pathways pass downstream filtering; users should document and justify this parameter.

## Evidence

- [other] Extract the corresponding subset of metabolite columns from the intensity matrix. 3. Apply singular value decomposition (SVD) to each pathway-specific metabolite submatrix.: "For each pathway, extract the corresponding subset of metabolite columns from the intensity matrix."
- [readme] Annotations are provided as another matrix having two columns. The first column (or DataFrame index) is the peak ID while the second column is the assigned metabolite annotation as either KEGG or ChEBI database IDs.: "Annotations are provided as another matrix having two columns. The first column (or DataFrame index) is the peak ID while the second column is the assigned metabolite annotation as either KEGG or"
- [readme] Data imputation is performed to the intensity matrix when it is loaded: if all of the samples in a single experimental factor have intensities of zero these are replaced by the minimum intensity value (which can be set by the user); and if only some of the sample values in a factor are zero then these are replaced by the mean value of the non-zero samples in that factor.: "Data imputation is performed to the intensity matrix when it is loaded: if all of the samples in a single experimental factor have intensities of zero these are replaced by the minimum intensity"
- [readme] peaks that do not have annotations will not be used for pathway analysis: "peaks that do not have annotations will not be used for pathway analysis"
- [readme] The most basic usage of PALS is to run it in offline-mode using PLAGE as the decomposition method. This uses the downloaded KEGG database for pathways.: "The most basic usage of PALS is to run it in offline-mode using PLAGE as the decomposition method. This uses the downloaded KEGG database for pathways."
