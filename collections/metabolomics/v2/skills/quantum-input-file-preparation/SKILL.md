---
name: quantum-input-file-preparation
description: Use when you have a set of RDKit-generated conformers ranked by ASE-ANI single-point energies, and you need to submit the lowest-energy subset to quantum software (e.g. QUICK) for CCS-relevant electronic structure calculations.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_0176
  - http://edamontology.org/topic_3314
  tools:
  - ASE-ANI
  - RDKit
  - QUICK
  - Dimorphite-DL
derived_from:
- doi: 10.1021/jasms.1c00315
  title: POMICS
evidence_spans:
- 'ASE-ANI: For conformation filtering'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pomics_cq
    doi: 10.1021/jasms.1c00315
    title: POMICS
  dedup_kept_from: coll_pomics_cq
schema_version: 0.2.0
---

# quantum-input-file-preparation

## Summary

Prepare conformer geometries filtered by neural-network potential energies into formats compatible with quantum-chemical software for downstream CCS prediction. This skill bridges molecular conformation generation and single-point quantum calculations by standardizing geometry representation and ensuring only low-energy conformers are submitted to expensive quantum workflows.

## When to use

You have a set of RDKit-generated conformers ranked by ASE-ANI single-point energies, and you need to submit the lowest-energy subset to quantum software (e.g. QUICK) for CCS-relevant electronic structure calculations. Use this when the number of conformers from RDKit exceeds your quantum compute budget and you want to maximize the chemical relevance of the subset by retaining geometries with lowest predicted energies.

## When NOT to use

- Input is already a pre-validated quantum input file (.in, .com) from a prior run—skip to direct submission.
- All conformers must be evaluated (no energy-based culling is allowed by your experimental protocol)—use the full set without filtering.
- Quantum software expects a different input protocol (e.g. GAMESS, Psi4, Gaussian) with incompatible geometry specifications—verify software-specific format requirements first.

## Inputs

- Ranked conformer structures from ASE-ANI (SDF or XYZ format)
- Energy scores for each conformer (eV)
- Ionization state metadata from Dimorphite-DL

## Outputs

- Filtered conformer set in quantum-software-compatible format (SDF or XYZ)
- Metadata file mapping conformer IDs to ASE-ANI energies
- Validation log confirming format compliance and charge preservation

## How to apply

After ASE-ANI ranking, select the lowest-energy conformer subset by either retaining the top N conformers (e.g. top 5–10) or applying an energy threshold (e.g. within 5 kcal/mol of the minimum). Export the filtered conformer set into a format compatible with the downstream quantum software—typically SDF or XYZ files. Verify that all bond connectivity, formal charges, and ionization states (already determined by Dimorphite-DL upstream) are preserved in the export. Ensure the file format exactly matches the input specification of QUICK or your chosen quantum package, and that 3D coordinates are properly normalized.

## Related tools

- **ASE-ANI** (Computes single-point energies for conformer ranking and selection) — https://github.com/isayev/ASE_ANI
- **RDKit** (Generates initial conformer structures that are ranked and formatted) — https://www.rdkit.org
- **QUICK** (Target quantum-chemical software that consumes prepared conformer input files)
- **Dimorphite-DL** (Provides ionization state information that must be preserved during export) — https://durrantlab.pitt.edu/dimorphite-dl

## Evaluation signals

- Exported file parses without errors in QUICK or target quantum software (test with dry run or schema validation)
- Conformer count equals the specified subset size (e.g. top N or energy-windowed set) with no duplicates
- All formal charges and ionization states match the upstream Dimorphite-DL output; verify by comparing charge field in input file to metadata
- Energy ranking is monotonically increasing within the exported set; spot-check via re-reading energies from exported coordinates
- 3D coordinates are non-zero and geometrically reasonable (e.g. no atom overlaps, sensible bond lengths for organic molecules)

## Limitations

- ASE-ANI is deprecated (README states 'DEPRECATED and no longer supported, please use TorchANI'); users should migrate to TorchANI for new work.
- ASE-ANI requires Python 3.6, CUDA 9.2, and an NVIDIA GPU with compute capability ≥5.0; compatibility with modern CUDA and Python versions is not guaranteed.
- ASE-ANI element support is limited to CHNO (or CHNOSFCl for ANI-2x prototype); molecules outside this set cannot be filtered.
- Energy-based conformer selection assumes low ASE-ANI energy correlates with low quantum-chemical energy; this heuristic may fail for certain functional classes or ionization states.
- Export format must match QUICK input specification exactly; any mismatch in file format, coordinate units, or connectivity encoding will cause downstream calculation failures.

## Evidence

- [other] Initialize ASE-ANI potential and compute single-point energy for each conformer. Rank conformers by energy and select the lowest-energy subset (retain top N conformers or apply an energy threshold). Export filtered conformer set in a format compatible with downstream quantum-chemical software (QUICK).: "Initialize ASE-ANI potential and compute single-point energy for each conformer. Rank conformers by energy and select the lowest-energy subset (retain top N conformers or apply an energy threshold)."
- [readme] ASE-ANI: For conformation filtering. Available at: [https://github.com/isayev/ASE_ANI]: "ASE-ANI: For conformation filtering. Available at: [https://github.com/isayev/ASE_ANI]"
- [readme] DEPRECATED and no longer supported, please use TorchANI implementation: "DEPRECATED and no longer supported, please use TorchANI implementation"
- [readme] Current ANI-1x and ANI-1ccx potentials provide predictions for the CHNO elements.: "Current ANI-1x and ANI-1ccx potentials provide predictions for the CHNO elements."
