---
name: spectral-fragmentation-motif-analysis
description: Use when when you have metabolomics intensity data with metabolites grouped by fragmentation spectral similarity (Molecular Families or Mass2Motifs) and need to rank or score these groups by their differential activity across experimental conditions, especially when traditional pathway databases.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3646
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
  tools:
  - GNPS
  - MS2LDA
  - PALS (Pathway Activity Level Scoring)
  - PALS Viewer
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-fragmentation-motif-analysis

## Summary

Analyze metabolite groupings derived from fragmentation spectra (Molecular Families from GNPS and Mass2Motifs from MS2LDA) using the PLAGE decomposition method to compute activity scores across experimental samples. This extends pathway-level activity scoring to spectral-motif-based metabolite sets.

## When to use

When you have metabolomics intensity data with metabolites grouped by fragmentation spectral similarity (Molecular Families or Mass2Motifs) and need to rank or score these groups by their differential activity across experimental conditions, especially when traditional pathway databases are unavailable or when spectral relationships are more informative than curated pathways.

## When NOT to use

- Peak data lack spectral clustering or Molecular Family/Mass2Motif assignments — use pathway-based PLAGE instead
- Sample sizes are extremely small (n < 3 per group) — SVD-based decomposition requires sufficient degrees of freedom
- Input data are already normalized to z-scores or other standardized scales — PLAGE performs its own log₂ transform and standardization, double-processing corrupts assumptions

## Inputs

- peak intensity CSV matrix (rows=peak_id with GNPS/MS2LDA identifiers, columns=samples with optional second row for sample group assignments)
- annotation CSV with two columns: peak_id and spectral_group_identifier (Molecular Family ID or Mass2Motif ID)
- experimental design specification (groups and pairwise comparisons, e.g. {'comparisons': [{'case': 'treatment', 'control': 'control', 'name': 'treatment/control'}]})

## Outputs

- ranked spectral-group activity table (CSV) with columns: spectral_group_id, activity_score, p-value, unique_formulae_count, dataset_formula_hits, formula_coverage_fraction
- decomposed activity levels per spectral group across samples
- comparative robustness metrics vs. ORA/GSEA alternatives

## How to apply

Load metabolomics peak intensity data (CSV matrix with rows=peaks, columns=samples) and a two-column annotation file mapping peak IDs to spectral-group identifiers (Molecular Family IDs or Mass2Motif IDs). Apply singular value decomposition (SVD) via the PLAGE method to compute activity scores for each spectral group across samples, after log₂-transforming and standardizing intensities to zero mean and unit variance. Data imputation is performed: replace all-zero factor entries with minimum intensity value (default 5000) and partial-zero entries with the non-zero mean within that factor. The PLAGE approach is robust to noise and missing peaks common in metabolomics, making it superior to ORA or GSEA alternatives for this data type. Output ranked spectral groups by p-value, with coverage metrics (unique formula count, dataset hit count, coverage fraction) enabling prioritization of Mass2Motifs or Molecular Families by activity.

## Related tools

- **PALS (Pathway Activity Level Scoring)** (Primary decomposition engine implementing PLAGE method for activity scoring of spectral-group sets) — https://github.com/glasgowcompbio/PALS
- **PALS Viewer** (Interactive web interface for running PLAGE on spectral groups and prioritizing Molecular Families and Mass2Motifs by activity scores) — https://pals.glasgowcompbio.org/app/
- **GNPS** (Source of Molecular Family spectral groupings used as input metabolite sets) — http://gnps.ucsd.edu/
- **MS2LDA** (Source of Mass2Motif spectral groupings used as input metabolite sets) — http://ms2lda.org/

## Examples

```
python pals/run.py PLAGE peak_intensities.csv peak_annotations.csv output_motifs.csv --db COMPOUND --comparisons treatment/control --min_replace 5000
```

## Evaluation signals

- Activity scores for spectral groups are computed and reported; p-values are assigned and sortable, indicating successful SVD decomposition
- Formula coverage for each spectral group (ratio of dataset hits to unique formulae) is ≤ 1.0 and ≥ 0; coverage < 0.1 may indicate sparse group membership
- Results are more robust to synthetic noise and missing peak simulation compared to ORA and GSEA outputs on the same data
- Output p-values and activity scores are mathematically consistent with the log₂-transformed, standardized input intensity matrix
- Spectral groups with high activity scores correlate visually or statistically with known experimental phenotypes (e.g., treatment vs. control differences)

## Limitations

- Requires functional Molecular Family or Mass2Motif assignments from upstream GNPS or MS2LDA analysis; garbage input annotations yield meaningless rankings
- SVD-based decomposition may be sensitive to outlier samples or extreme intensity ranges; robustness depends on quality of data imputation and standardization
- Multiple peak-to-compound and compound-to-metabolite mappings can inflate or obscure group membership; no built-in deduplication or confidence filtering
- PLAGE assumes linear activity relationships within spectral groups; highly non-additive or epistatic metabolite interactions may not be captured
- No correction for multiple testing across spectral groups in baseline output; practitioners should apply multiple-hypothesis correction (e.g., FDR) when comparing many groups

## Evidence

- [readme] the decomposition approach in PALS is amenable to the analysis of any group of metabolite sets, not just pathways: "the decomposition approach in PALS is amenable to the analysis of any group of metabolite sets, not just pathways"
- [readme] metabolite sets obtained from the grouping of metabolites according to their fragmentation spectra can also be analysed. This includes in particular Molecular Families from GNPS, as well as Mass2Motifs from MS2LDA.: "metabolite sets obtained from the grouping of metabolites according to their fragmentation spectra can also be analysed. This includes in particular *Molecular Families* from"
- [intro] decomposes activity levels in pathways via the PLAGE method: "decomposes activity levels in pathways via [the PLAGE method]"
- [readme] The results are found to be more robust to noise and missing peaks compared to the alternatives (ORA, GSEA). This is particularly important for metabolomics peak data, where noise and missing peaks are prevalent.: "The results are found to be more robust to noise and missing peaks compared to the alternatives (ORA, GSEA). This is particularly important for metabolomics peak data"
- [readme] The intensity matrix is subsequently transformed to log-2 base and standardised using the preprocessing module in Scipy such that the intensity matrix has a zero mean and unit variance across the samples.: "The intensity matrix is subsequently transformed to log-2 base and standardised using the preprocessing module in Scipy such that the intensity matrix has a zero mean and unit variance"
