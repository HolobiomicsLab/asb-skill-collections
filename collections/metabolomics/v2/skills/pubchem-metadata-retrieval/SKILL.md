---
name: pubchem-metadata-retrieval
description: Use when after compound database dereplication (via SIRIUS or MetFrag) has produced per-spectrum candidate annotation lists with putative compound identifiers, and before applying selection criteria to rank and filter candidates.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0224
  edam_topics:
  - http://edamontology.org/topic_0599
  - http://edamontology.org/topic_3172
  tools:
  - RDKit
  - PubChemPy
  - Python
  - Spectra
  - SIRIUS
  - MetFrag
  - R
  - PubChem
derived_from:
- doi: 10.1186/s13321-023-00695-y
  title: MAW
evidence_spans:
- Final candidate selection is done in Python using RDKit and PubChemPy
- performs spectral database dereplication using R Package
- spectral database dereplication using R Package Spectra
- compound database dereplication using SIRIUS OR MetFrag
- compound database dereplication using SIRIUS
- workflow takes MS2 .mzML format data files as an input in R
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_maw_cq
    doi: 10.1186/s13321-023-00695-y
    title: MAW
  dedup_kept_from: coll_maw_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-023-00695-y
  all_source_dois:
  - 10.1186/s13321-023-00695-y
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# pubchem-metadata-retrieval

## Summary

Retrieve molecular properties and chemical validity metadata from PubChem for compound candidates using PubChemPy, enabling downstream filtering and ranking in metabolome annotation workflows. This skill bridges spectral/compound database dereplication results with structural validation by querying PubChem's chemical registry.

## When to use

After compound database dereplication (via SIRIUS or MetFrag) has produced per-spectrum candidate annotation lists with putative compound identifiers, and before applying selection criteria to rank and filter candidates. Use this skill when you have CSV or JSON candidate annotations from SIRIUS/MetFrag and need to validate chemical identity and retrieve molecular descriptors (molecular weight, InChI, SMILES, validity flags) to assess annotation confidence.

## When NOT to use

- Candidates already have validated PubChem InChI/SMILES and do not require redundant metadata retrieval.
- Input compound identifiers are not resolvable in PubChem (e.g., proprietary or novel compounds without PubChem records).
- The workflow goal is de novo structure elucidation rather than database annotation; PubChem retrieval is not appropriate for unknown structures.

## Inputs

- CSV or JSON candidate annotation table from SIRIUS or MetFrag dereplication
- Compound identifiers or chemical names (per-candidate)
- MS1 mass data (for cross-validation)

## Outputs

- Enriched candidate table with PubChem metadata (InChI, SMILES, molecular weight)
- Molecular fingerprints and structural descriptors (RDKit-computed)
- Ranked and filtered candidate list with selection scores
- CSV output of curated candidates sorted by confidence

## How to apply

Load candidate annotations from SIRIUS or MetFrag dereplication output (CSV or JSON format), extracting compound identifiers or names. For each candidate, query PubChem via PubChemPy to retrieve molecular properties (molecular weight, InChI, SMILES, validity status). Combine retrieved metadata with RDKit-computed structural descriptors (fingerprints, descriptor ranges). Apply selection criteria based on chemical validity flags, descriptor ranges, and PubChem match confidence scores. Rank and filter candidates by cumulative selection score, retaining only those meeting confidence thresholds before output. This ensures that final candidate annotations are chemically valid and grounded in PubChem's curated registry.

## Related tools

- **PubChemPy** (Query PubChem chemical registry to retrieve molecular properties, InChI, SMILES, and validity metadata for each candidate compound) — https://pubchempy.readthedocs.io/en/latest/
- **RDKit** (Compute molecular fingerprints and structural descriptors from retrieved SMILES or InChI strings to support selection filtering) — https://www.rdkit.org/
- **SIRIUS** (Upstream compound database dereplication tool that produces candidate annotations to be enriched via PubChem metadata retrieval) — https://bio.informatik.uni-jena.de/software/sirius/
- **MetFrag** (Alternative upstream compound database dereplication tool that produces candidate annotations to be enriched via PubChem metadata retrieval) — https://ipb-halle.github.io/MetFrag/

## Examples

```
python3.10 Workflow_Python_Script_all_MetFrag.py --msp_file your_file_name/spectral_dereplication/spectral_results.csv --ms1data your_file_name/insilico/MS1DATA.csv --score_thresh 0.75
```

## Evaluation signals

- All candidate rows in output table contain non-null PubChem metadata fields (InChI, SMILES, molecular weight)
- Chemical validity flags match expected status (e.g., 'valid' for known compounds, 'invalid' for chemically implausible structures)
- Molecular weight values retrieved from PubChem agree with MS1 precursor mass within specified tolerance (e.g., ±5 ppm or Da)
- Candidates are ranked by selection score in descending order, with scores reflecting combined validity and descriptor confidence
- Output CSV contains all required columns: candidate ID, compound name, InChI, SMILES, molecular weight, RDKit descriptors, and selection score

## Limitations

- PubChem query success depends on internet connectivity and PubChem API availability; rate limiting may slow retrieval for large candidate sets.
- Candidates without PubChem records (novel, proprietary, or rare compounds) will fail retrieval or return null metadata, excluding them from downstream selection.
- PubChem InChI/SMILES may differ from de novo structure determination results; conflicts should be flagged for manual review.
- Molecular weight agreement with MS1 data is approximate and depends on mass accuracy; 5 ppm tolerance may not catch systematic instrument calibration errors.

## Evidence

- [intro] Query PubChem via PubChemPy to retrieve molecular properties and chemical validity for each candidate: "Query PubChem via PubChemPy to retrieve molecular properties and chemical validity for each candidate."
- [intro] Load candidate annotations from SIRIUS or MetFrag dereplication output (CSV or JSON format): "Load candidate annotations from SIRIUS or MetFrag dereplication output (CSV or JSON format)."
- [intro] Compute molecular fingerprints and structural descriptors using RDKit for each candidate: "Compute molecular fingerprints and structural descriptors using RDKit for each candidate."
- [readme] Final candidate selection is done in Python using RDKit and PubChemPy: "Final candidate selection is done in Python using RDKit and PubChemPy."
- [intro] Apply selection criteria (e.g., chemical validity, descriptor ranges, PubChem match confidence) to filter and rank candidates: "Apply selection criteria (e.g., chemical validity, descriptor ranges, PubChem match confidence) to filter and rank candidates."
