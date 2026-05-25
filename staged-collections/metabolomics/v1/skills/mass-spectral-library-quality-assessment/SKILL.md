---
name: mass-spectral-library-quality-assessment
description: "Comprehensive evaluation of mass spectral library metadata integrity and annotation consistency using automated validation filters (basic, default, library-cleaning tiers) to identify and quantify structural and chemical inconsistencies before curation. This skill assesses whether spectra retain valid SMILES/InChI/InChIKey annotations, correct adduct assignments, consistent precursor m/z values, and properly normalized peak intensities across large spectral repositories (e.g., GNPS, MoNA)."
when_to_use_negative: |
  - "Input library is already curated (e.g., NIST private library or post-peer-review subset) and lacks known annotation artifacts — assessment overhead outweighs benefit."
  - "Library contains primarily unannotated spectra (e.g., experimental untargeted metabolomics data) — this skill targets *library* metadata consistency, not unknown compound discovery."
  - "Downstream analysis requires fragment-ion-to-annotation matching that this pipeline explicitly does not perform (article notes: 'wrong chemical annotations consistent with measured mass will go unnoticed')."
edam_operation: "http://edamontology.org/operation_3695"
edam_topics: |
  - "http://edamontology.org/topic_0091"
  - "http://edamontology.org/topic_3172"
tools: |
  - name: "matchms"
  role: "Core framework for loading spectra, applying tiered filter pipelines (basic, default, library-cleaning), and exporting curated libraries with metadata repair and validation"
  repo: "https://github.com/matchms/matchms"
  - name: "RDKit"
  role: "Cross-validates SMILES, InChI, and InChIKey consistency; derives canonical structures from compound names; checks adduct–SMILES compatibility"
  - name: "PubChem API"
  role: "Supplies canonical SMILES, InChI, and InChIKey when deriving annotations from compound names"
  - name: "Git / Conda / pip"
  role: "Version control and environment management for reproducible matchms installation and filter configurations (YAML-based)"
provenance: |
  source_task_ids:
  - task_006
  source_papers:
  - doi: "10.1186/s13321-024-00878-1"
  title: "Reproducible MS/MS library cleaning pipeline in matchms"
schema_version: "0.2.0"
metadata:
  iri: https://w3id.org/holobiomicslab/asb-skill/mass-spectral-library-quality-assessment@sha256:ff575373de16fcb13b57db61b4918115784076af1eed944691217e698aca6868
---

# mass-spectral-library-quality-assessment

## Summary

Comprehensive evaluation of mass spectral library metadata integrity and annotation consistency using automated validation filters (basic, default, library-cleaning tiers) to identify and quantify structural and chemical inconsistencies before curation. This skill assesses whether spectra retain valid SMILES/InChI/InChIKey annotations, correct adduct assignments, consistent precursor m/z values, and properly normalized peak intensities across large spectral repositories (e.g., GNPS, MoNA).

## When to use

Apply this skill when you have loaded a large, public mass spectral library (500K+ spectra) with heterogeneous annotation sources and need to establish baseline quality metrics before downstream analysis. Use it when the business goal is to quantify how many spectra fail annotation consistency checks (e.g., SMILES–InChI mismatch via RDKit), how many can be repaired by applying harmonization functions, and what fraction of the library remains curated after strict validation. Specifically, trigger this skill when you suspect the library contains incomplete metadata (missing ionmode, precursor m/z, or chemical structures), wrong chemical assignments consistent with observed mass, or incorrect adduct/parent mass assignments derived from molar mass rather than monoisotopic mass.

## When NOT to use

- Input library is already curated (e.g., NIST private library or post-peer-review subset) and lacks known annotation artifacts — assessment overhead outweighs benefit.
- Library contains primarily unannotated spectra (e.g., experimental untargeted metabolomics data) — this skill targets *library* metadata consistency, not unknown compound discovery.
- Downstream analysis requires fragment-ion-to-annotation matching that this pipeline explicitly does not perform (article notes: 'wrong chemical annotations consistent with measured mass will go unnoticed').

## Inputs

- Mass spectral library in matchms-compatible format (mzML, mzXML, or native library files with metadata JSON)
- Spectral records with fields: compound_name, SMILES, InChI, InChIKey, precursor_mz, parent_mass, adduct, ionmode, peaks (m/z–intensity pairs)
- Optionally: PubChem compound name mapping file for deriving missing annotations

## Outputs

- Cleaned mass spectral library (matchms SpectrumList or export to mzML/JSON)
- Curation report (CSV or JSON) with: total input spectra, counts removed per filter, counts repaired per repair function, final retention rate (%), per-checkpoint statistics
- Quality metrics: % spectra with valid SMILES/InChI/InChIKey, % with correct adduct, % with consistent precursor m/z, intensity normalization histogram

## How to apply

Load the spectral library into matchms (v0.26.4 or later) and apply three successive filter tiers in order: (1) Basic filters — run metadata harmonization (field standardization, case normalization). (2) Default filters — derive missing metadata from other fields (e.g., infer precursor m/z from parent mass + adduct), require ionmode and precursor m/z presence, and normalize peak intensities to [0–1] range. (3) Library-cleaning filters — apply repair functions (repair SMILES of salts, correct parent mass using monoisotopic mass not molar mass, derive canonical SMILES/InChI/InChIKey from PubChem via compound name when missing, repair adduct and parent mass consistency from SMILES using RDKit), then enforce require_valid_annotation, which uses RDKit to load all three chemical identifiers and cross-validate their internal consistency. At each step, record counts and fractions of spectra removed or repaired. Generate a structured report (CSV or JSON) documenting total input spectra, counts/fractions failing each validation checkpoint, counts repaired per repair function, and final curation rate. The key rationale: repair-first-then-validate recovers spectra with repairable inconsistencies (e.g., 52,084 of 83,843 originally flagged spectra in GNPS), increasing library yield from 89.7% to 89.6% while maintaining consistency.

## Related tools

- **matchms** (Core framework for loading spectra, applying tiered filter pipelines (basic, default, library-cleaning), and exporting curated libraries with metadata repair and validation) — https://github.com/matchms/matchms
- **RDKit** (Cross-validates SMILES, InChI, and InChIKey consistency; derives canonical structures from compound names; checks adduct–SMILES compatibility)
- **PubChem API** (Supplies canonical SMILES, InChI, and InChIKey when deriving annotations from compound names)
- **Git / Conda / pip** (Version control and environment management for reproducible matchms installation and filter configurations (YAML-based))

## Evaluation signals

- Curation report produced; total input spectra matches library size (e.g., GNPS: 500,569); final curated count matches expected range (e.g., GNPS: 448,485 = 89.6% retention).
- Repair-then-validate flow reduces removal count: spectra removed by require_valid_annotation *before* repair is substantially higher than *after* repair (e.g., 83,843 → 31,758), confirming repair functions recovered repairable spectra.
- Per-filter statistics consistent with article benchmarks: 'derive annotation from compound name' shows 27.6% of spectra could not be derived, 1.62% of annotated spectra had different 2D structure; 'repair adduct and parent mass based on SMILES' shows 0.02% had no derived adduct, 0.024% of the 99.98% had incorrect adduct.
- Intensity normalization histogram shows [0–1] range with no outliers or unintended zero-intensity peaks; normalized spectra are binary-comparable across library.
- SMILES/InChI/InChIKey round-trip validation passes: RDKit can parse all three fields, compute InChI and InChIKey from SMILES, and verify they match stored values for ≥99% of retained spectra.

## Limitations

- Pipeline does not validate whether fragment ions actually match the chemical structure implied by the annotation; wrong chemical assignments consistent with observed precursor m/z will pass all filters (article: 'wrong chemical annotations that are consistent with the measured mass… will go unnoticed').
- Currently lacks filters for instrument type, collision energy, and other metadata fields that may be important for future use cases; these fields are not yet harmonized.
- Repair functions depend on external data sources (PubChem for compound name lookups, RDKit for structure inference), so missing or incorrect compound names cannot be auto-corrected beyond SMILES/InChI harmonization.
- Large-scale curation is computationally expensive: processing 500,569 spectra takes 6 hours 45 minutes (article benchmark), limiting interactive exploration on personal machines.
- Library-cleaning tier is strictest and removes most spectra; users requiring higher yield must choose default or basic tier, with reduced metadata completeness guarantees.

## Evidence

- [abstract] Basic metadata consistency and annotation completeness: "metadata cleaning, peak filtering, intensity normalization, and structure annotation validation through adduct, precursor m/z, and annotation comparison and harmonization"
- [abstract] RDKit cross-validation of chemical identifiers: "SMILES, InChI and InChIKey are loaded by RDKit [18] and compared to each other"
- [abstract] Quantified impact of repair functions on curation yield: "a total of 83,843 spectra were removed...In the library cleaning pipeline only 31,758 spectra were removed showing that combined the newly introduced repair functions repaired the metadata of 52,084"
- [abstract] Require valid annotation filter removes spectra with inconsistent or missing annotations: "Require valid annotation"
- [discussion] Limitation: fragment-ion consistency not checked: "Wrong chemical annotations that are consistent with the measured mass, for instance, will go unnoticed in the current pipeline."
- [abstract] Three-tier filter strategy with different strictness levels: "Library cleaning. Runs all default filters, but in addition repairs errors in the annotations and requires complete annotations after all repairs were run."
