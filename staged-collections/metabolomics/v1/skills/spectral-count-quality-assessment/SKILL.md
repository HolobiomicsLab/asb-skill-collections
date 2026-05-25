---
name: spectral-count-quality-assessment
description: Quantitatively assess the quality and completeness of a mass spectral library by executing a reproducible cleaning pipeline that tracks spectrum counts through retention, removal, and repair stages. This skill measures data curation effectiveness by comparing input vs. retained vs. removed vs. repaired spectrum counts and reporting metadata repair success rates for each filter applied.
when_to_use_negative:
- Input library is already curated by hand or has been previously cleaned by this same pipeline with identical settings and snapshot date (rerunning adds no new signal).
- Spectra are from proprietary or small in-house datasets (<1000 spectra) where library-wide statistics are not meaningful.
- Your goal is to identify individual miscurated spectra, not to measure aggregate curation quality—this skill is aggregate-focused and will not flag which specific spectrum entry is wrong.
edam_operation: http://edamontology.org/operation_3802
edam_topics:
- http://edamontology.org/topic_3172
- http://edamontology.org/topic_0091
tools:
- name: matchms
  role: Core library-cleaning framework that executes the filter chain, repair functions, and tracks spectrum counts through each stage
  repo: https://github.com/matchms/matchms
- name: matchms 0.26.4
  role: Specific version used in the published pipeline; includes newly introduced repair functions (repair SMILES of salts, repair parent mass, repair adduct and parent mass based on SMILES, repair not-matching annotation)
- name: RDKit
  role: Used by matchms filters to parse and validate SMILES, InChI, and InChIKey during structure annotation repair and comparison
- name: PubChem
  role: Reference database queried by 'derive annotation from compound name' filter to look up canonical SMILES, InChI, and InChIKey
- name: Python
  role: Execution environment for matchms pipelines and custom counting/reporting scripts
provenance:
  source_task_ids:
  - task_001
  source_papers:
  - doi: 10.1186/s13321-024-00878-1
    title: Reproducible MS/MS library cleaning pipeline in matchms
schema_version: 0.2.0
metadata:
  iri: https://w3id.org/holobiomicslab/asb-skill/spectral-count-quality-assessment@sha256:4510f102e482997402b6a0bd2f08692885104b1e68424e52f88b5f92bd9d103a
---

# spectral-count-quality-assessment

## Summary

Quantitatively assess the quality and completeness of a mass spectral library by executing a reproducible cleaning pipeline that tracks spectrum counts through retention, removal, and repair stages. This skill measures data curation effectiveness by comparing input vs. retained vs. removed vs. repaired spectrum counts and reporting metadata repair success rates for each filter applied.

## When to use

When you have a public mass spectral library in MGF format (e.g., GNPS no-propagated, MoNA, or MassBank) and need to understand: (1) what fraction of spectra survive quality gates, (2) how many spectra are repaired vs. discarded at each filter step, (3) whether repair functions recover spectra that would otherwise be removed, or (4) reproducibility of curation outcomes across library snapshots or versions. Concrete trigger: library has >100k spectra and you need quantitative evidence that cleaning was applied correctly before downstream use.

## When NOT to use

- Input library is already curated by hand or has been previously cleaned by this same pipeline with identical settings and snapshot date (rerunning adds no new signal).
- Spectra are from proprietary or small in-house datasets (<1000 spectra) where library-wide statistics are not meaningful.
- Your goal is to identify individual miscurated spectra, not to measure aggregate curation quality—this skill is aggregate-focused and will not flag which specific spectrum entry is wrong.

## Inputs

- MGF file (mass spectral library in mzSpecLib or mzML-compatible format)
- YAML configuration file specifying filter chain, parameters, and thresholds
- Spectrum metadata (ionmode, precursor m/z, compound name, SMILES, InChI, InChIKey)
- Reference annotations (PubChem for canonical SMILES lookup)

## Outputs

- Summary statistics file with spectrum counts: input, retained, removed, repaired
- Per-filter retention/removal/repair counts and success rates
- Cleaned library (MGF) with repaired metadata
- Metadata curation report (e.g., % of spectra with derived vs. original SMILES, % with corrected adducts)

## How to apply

Download the library (MGF format) and retrieve the YAML configuration file specifying all filter and repair parameters (available from Zenodo for published pipelines). Parse the MGF using matchms 0.26.4 to load spectra and metadata. Execute the library cleaning pipeline sequentially, which includes: basic metadata harmonization, default filters (requiring ionmode and precursor m/z, normalizing intensities), and library-cleaning filters (derive annotation from compound name via PubChem, repair SMILES of salts, repair parent mass using monoisotopic mass instead of molar mass, repair adduct and parent mass based on SMILES, repair not-matching annotations, require valid annotation). At each step, count and record: (a) input spectrum count, (b) retained spectra after passing all filters, (c) removed spectra that failed filters, and (d) repaired spectra that were corrected by repair functions before potential removal. Compare output counts to expected values (e.g., GNPS 2023-08-21: 500,569 input → 448,485 retained, 31,758 removed, 52,084 repaired) to confirm pipeline reproducibility. Report per-filter success rates (e.g., 'derive annotation from compound name': 72.4% successfully derived; 'repair adduct and parent mass based on SMILES': 99.98% derived adduct, 0.024% had incorrect adduct).

## Related tools

- **matchms** (Core library-cleaning framework that executes the filter chain, repair functions, and tracks spectrum counts through each stage) — https://github.com/matchms/matchms
- **matchms 0.26.4** (Specific version used in the published pipeline; includes newly introduced repair functions (repair SMILES of salts, repair parent mass, repair adduct and parent mass based on SMILES, repair not-matching annotation))
- **RDKit** (Used by matchms filters to parse and validate SMILES, InChI, and InChIKey during structure annotation repair and comparison)
- **PubChem** (Reference database queried by 'derive annotation from compound name' filter to look up canonical SMILES, InChI, and InChIKey)
- **Python** (Execution environment for matchms pipelines and custom counting/reporting scripts)

## Evaluation signals

- Output spectrum counts match expected values within ±1% (e.g., 448,485 ± 4,485 retained spectra for GNPS 2023-08-21 with published pipeline).
- Sum of retained + removed + (repaired − overlap) equals input count, confirming no spectra are double-counted or lost.
- Per-filter success rates align with published benchmarks (e.g., 'derive annotation from compound name' ≥72% success, 'repair adduct and parent mass based on SMILES' ≥99.98% adduct derivation).
- Repair function counts are >0 and non-trivial (e.g., repaired count is >5% of removed count, showing repair is effective vs. trivial).
- Pipeline runtime is documented and reasonable for library size (e.g., ~6 h 45 min for 500k spectra, ~0.05 ms per spectrum).

## Limitations

- Pipeline will not catch wrong chemical annotations that are consistent with the measured precursor m/z; annotations with incorrect 2D structure will only be detected if SMILES/InChI comparison reveals conflict.
- Repair functions address metadata errors but do not validate whether observed fragments actually match the assigned molecular structure; plausibility checks integrating both metadata and measured peaks are not yet implemented.
- Additional metadata fields such as instrument type and collision energy are not cleaned by the current matchms filters and thus cannot be assessed or repaired by this skill.
- Success of 'derive annotation from compound name' depends on exact compound name matching in PubChem; ambiguous or misspelled names will fail to derive (27.6% failure rate observed on GNPS).
- Repair functions may inadvertently correct to wrong but plausible values (e.g., choosing a structurally similar isomer with matching mass); manual review of high-stakes repairs is advised.

## Evidence

- [abstract] input_output_counts: "Before cleaning, the GNPS library contained 500,569 spectra...The final cleaned GNPS public mass spectral library contains 448.485 curated mass spectra"
- [abstract] repair_effectiveness: "a total of 83,843 spectra were removed...In the library cleaning pipeline only 31,758 spectra were removed showing that combined the newly introduced repair functions repaired the metadata of 52,084"
- [abstract] derive_annotation_success_rate: "For 27,6% of the spectra, the SMILES could not be derived from the compound name. Of the spectra that were annotated (72,4%), 1,62% were annotated with a different 2D structure"
- [abstract] repair_adduct_success_rate: "The 'Repair adduct and parent mass based on SMILES' filter did not derive an adduct for 0,02%. Of the 99,98% of the spectra, 0,024% of the spectra had an incorrect adduct"
- [abstract] pipeline_runtime: "Running the machms pipeline with the filters given in Supplementary Table S1 on the GNPS library of 500,569 spectra took 6 h and 45 min"
- [abstract] comprehensive_filter_chain: "metadata cleaning, peak filtering, intensity normalization, and structure annotation validation through adduct, precursor m/z, and annotation comparison and harmonization"
- [discussion] limitation_structural_plausibility: "Wrong chemical annotations that are consistent with the measured mass, for instance, will go unnoticed in the current pipeline."
- [discussion] library_metadata_issues: "Current publicly available libraries often have incorrect or inaccuracies, they currently still lack plausibility checks that consider both metadata and measured fragments."
