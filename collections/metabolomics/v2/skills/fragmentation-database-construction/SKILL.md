---
name: fragmentation-database-construction
description: Use when when you have completed ORCA single-point energy calculations on interpolated reaction pathway geometries and need to convert quantum mechanical fragment energies and molecular properties into a structured fragmentation channel database suitable for automated EI mass spectrum simulation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3456
  edam_topics:
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_3318
  - http://edamontology.org/topic_0081
  tools:
  - QCxMS2
  - xtb
  - ORCA
  - molbar
  - geodesic_interpolate
derived_from:
- doi: 10.1021/jasms.5c00234
  title: QCxMS2
evidence_spans:
- Program package for the quantum mechanical calculation of EI mass spectra using automated reaction network exploration
- '**xtb** (version > 6.7.1 - bleeding edge version)'
- '**orca** (version >= 6.0.0)'
- '**molbar** (version >= 1.1.3)'
- '**geodesic_interpolate** (version'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_qcxms2_cq
    doi: 10.1021/jasms.5c00234
    title: QCxMS2
  dedup_kept_from: coll_qcxms2_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jasms.5c00234
  all_source_dois:
  - 10.1021/jasms.5c00234
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# fragmentation-database-construction

## Summary

Construction of a molecular fragmentation database by processing high-level quantum mechanical energies and properties through a specialized aggregation tool (molbar), enabling subsequent EI mass spectrum simulation and interpretation. This skill bridges quantum mechanical calculations with fragment-level analysis required for electron ionization mass spectra prediction.

## When to use

When you have completed ORCA single-point energy calculations on interpolated reaction pathway geometries and need to convert quantum mechanical fragment energies and molecular properties into a structured fragmentation channel database suitable for automated EI mass spectrum simulation. Specifically triggered when ORCA output files containing fragment energies, charges, and structural information are available and must be aggregated into reaction channels before final spectrum calculation.

## When NOT to use

- Input consists of experimental mass spectrum data rather than computed fragments — use this skill only for ab initio fragmentation predictions, not reverse lookup.
- Fragment energies have not been calculated at the required quantum mechanical level (ORCA >= 6.0.0) — preprocessing must complete before molbar aggregation.
- Target is conformer ensemble analysis rather than fragmentation pathways — use CREST output analysis instead.

## Inputs

- ORCA single-point energy output files (from interpolated geometries)
- Fragment molecular geometries (XYZ format)
- Fragment charge and multiplicity states
- Computed energies and molecular orbital properties

## Outputs

- Structured fragmentation database (relational format with reaction channels)
- Fragment m/z assignments and energy barriers
- Aggregated reaction network representation
- Input file for EI mass spectrum simulation algorithm

## How to apply

Execute molbar (version >= 1.1.3) to process ORCA output energies and molecular properties from high-level quantum mechanical single-point calculations. The tool ingests individual fragment geometries and their computed energies, consolidates them into discrete fragmentation channels, and constructs a relational database encoding reaction pathways—including parent ion, fragment masses (m/z), and transition energy barriers. Apply molbar's output aggregation rules to group isobaric fragments and assign relative intensities based on energetic favorability. The resulting fragmentation database serves as the direct input to the EI mass spectrum simulation algorithm, making data consistency (energy units, charge states, mass accuracy) critical for downstream spectrum fidelity.

## Related tools

- **molbar** (Aggregates ORCA-computed fragment energies and molecular properties into structured fragmentation database and reaction channels) — https://git.rwth-aachen.de/bannwarthlab/molbar
- **ORCA** (Provides high-level quantum mechanical single-point energies and molecular properties for fragments that molbar ingests and aggregates) — https://orcaforum.kofo.mpg.de
- **QCxMS2** (Consumes the fragmentation database constructed by molbar to simulate final EI mass spectrum) — https://github.com/grimme-lab/QCxMS2

## Evaluation signals

- Output fragmentation database contains all computed fragments with internally consistent m/z values and energy barriers; no missing or orphaned fragments from input ORCA runs.
- Energy values in database preserve precision and units from ORCA output (verify no truncation or unit conversion errors).
- Reaction channels correctly encode parent–fragment relationships; isobaric fragments are appropriately grouped and ranked by computed favorability.
- Subsequent EI mass spectrum simulation (QCxMS2) produces spectrum peaks at expected m/z positions with intensities correlating to fragment formation energies.
- Database schema validates against QCxMS2 input specification (no format mismatches, required fields populated).

## Limitations

- molbar version >= 1.1.3 is strict; earlier versions may have incompatible output formats or bugs that break downstream spectrum calculation.
- Fragmentation database quality is entirely dependent on upstream ORCA geometry optimization and energy accuracy; systematic errors in quantum mechanical calculations are not corrected by aggregation.
- Isobaric fragment discrimination relies on computed energetics; if two fragments have degenerate or nearly degenerate energies, the database representation may not disambiguate them sufficiently for experimental validation.
- No changelog is available for molbar, limiting version-to-version compatibility assessment; manual testing across versions is recommended.

## Evidence

- [other] Submit interpolated geometries to ORCA (version >= 6.0.0) for high-level quantum mechanical single-point energy and property calculations.: "Submit interpolated geometries to ORCA (version >= 6.0.0) for high-level quantum mechanical single-point energy and property calculations."
- [other] Process ORCA output energies and molecular properties via molbar (version >= 1.1.3) to construct fragmentation database and reaction channels.: "Process ORCA output energies and molecular properties via molbar (version >= 1.1.3) to construct fragmentation database and reaction channels."
- [other] Aggregate reaction network fragment data and apply EI mass spectrum simulation algorithm to produce final mass spectrum.: "Aggregate reaction network fragment data and apply EI mass spectrum simulation algorithm to produce final mass spectrum."
- [readme] molbar (version >= 1.1.3): "**molbar** (version >= 1.1.3)"
- [readme] For any installation make sure that you have correctly installed and sourced the following external programs before attempting any calculations with QCxMS2: "For any installation make sure that you have correctly installed and sourced the following external programs before attempting any calculations with QCxMS2"
