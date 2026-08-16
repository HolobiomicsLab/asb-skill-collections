---
name: fragmentation-pattern-annotation-magma
description: Use when you have a tandem MS/MS spectrum of a structurally modified
  compound and a known reference structure (SMILES), and you need to annotate which
  fragment ions correspond to specific bonds or atoms in the molecule.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3631
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - ModiFinder
  - Python
  - RDKit
  - matplotlib
  techniques:
  - CE-MS
  license_tier: restricted
derived_from:
- doi: 10.1021/jasms.4c00061
  title: ModiFinder
evidence_spans:
- mf = ModiFinder(known_compound, modified_compound, mz_tolerance=0.01, ppm_tolerance=40)
- mf = ModiFinder(known_compound, modified_compound, helpers=helpers_array, **args)
- ModiFinder requires Python 3.9 or above.
- ModiFinder requires Python 3.9 or above
- 'rdkit: http://www.rdkit.org/'
- ModiFinder includes powerful visualization tools built on RDKit and matplotlib for
  creating publication-quality figures.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_modifinder_cq
    doi: 10.1021/jasms.4c00061
    title: ModiFinder
  dedup_kept_from: coll_modifinder_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jasms.4c00061
  all_source_dois:
  - 10.1021/jasms.4c00061
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Fragmentation Pattern Annotation with MAGMa

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

MAGMa annotation engine assigns fragment ions in tandem MS/MS spectra to specific neutral losses and bond cleavages within a known molecular structure, enabling structural localization of modifications. This skill is essential when you need to trace MS/MS peaks back to exact atoms or functional groups to localize where a modification has occurred on a known compound.

## When to use

Apply this skill when you have a tandem MS/MS spectrum of a structurally modified compound and a known reference structure (SMILES), and you need to annotate which fragment ions correspond to specific bonds or atoms in the molecule. This is particularly valuable prior to or in tandem with spectral alignment when comparing a known compound spectrum to a modified analog spectrum, as it grounds each MS/MS peak in the chemical structure, enabling atom-level modification site probability scoring.

## When NOT to use

- Spectrum is purely de novo (no known reference structure available); MAGMa requires a reference SMILES to perform in silico fragmentation.
- Fragment ion masses are outside the specified m/z_tolerance or ppm_tolerance windows; peaks will not be annotated and will not contribute to structural localization.
- Only qualitative peak presence/absence is needed, not structural assignment; simpler cosine similarity or spectral matching may suffice.

## Inputs

- Compound object with SMILES string and tandem MS/MS spectrum (peak list with m/z and intensity)
- Precursor m/z and charge state
- MAGMa annotation engine configuration (mz_tolerance, ppm_tolerance)

## Outputs

- peak_fragment_dict: dictionary mapping observed m/z values to annotated fragment structures and bond cleavage information
- Fragment annotation metadata: neutral loss masses, cleavage positions, and confidence scores for each peak

## How to apply

Instantiate a MAGMaAnnotationEngine and pass it both the known Compound object (with SMILES and spectrum) and the ModiFinder instance. The engine processes the tandem MS/MS spectrum by fragmenting the known structure in silico and matching observed m/z peaks to predicted fragment masses (using mz_tolerance=0.01 and ppm_tolerance=40 by default). Each matched fragment is annotated with the bond(s) cleaved and atom(s) retained, producing a peak-to-fragment dictionary that maps m/z values to specific structural elements. This annotation output is then used by ModiFinder's probability generation to weight per-atom modification scores: peaks with strong MAGMa annotations (high match confidence) contribute more heavily to atom-level probability estimates than ambiguous or unannotated peaks.

## Related tools

- **ModiFinder** (Consumer of MAGMa annotation output; integrates fragment annotations into modification site probability generation) — https://github.com/Wang-Bioinformatics-Lab/ModiFinder_base
- **RDKit** (Underlying chemistry engine for in silico fragmentation, structure parsing, and mass calculation) — http://www.rdkit.org/
- **Python** (Execution language for MAGMa annotation engine and ModiFinder workflow)

## Examples

```
siteLocator = ModiFinder(main_compound, mod_compound, helpers=None); peaksObj, fragmentsObj = siteLocator.get_result(); print(fragmentsObj['frags_map'])  # inspect peak-to-fragment annotations
```

## Evaluation signals

- Every observed peak with mass within mz_tolerance (±0.01 m/z) or ppm_tolerance (40 ppm) of a predicted fragment should receive an annotation entry in peak_fragment_dict; check for completeness.
- Annotated fragments should correspond to chemically valid bond cleavages in the reference structure (no impossible fragments); inspect peak_fragment_dict entries for chemical plausibility.
- Per-atom modification site probabilities should show higher values at atoms involved in frequently matched fragments and lower values at unmatched or weakly matched atoms; verify correlation between annotation coverage and probability distribution.
- When comparing known vs. modified compound, peaks that match only in the modified spectrum should map to regions near the modification site, confirming annotation is localizing changes correctly.
- Unannotated peaks (those outside tolerance windows) should be rare (<5% of spectrum intensity) for high-quality spectra; high rates suggest tolerance parameters need adjustment or spectrum quality issues exist.

## Limitations

- MAGMa annotation depends critically on accurate SMILES input; incorrect or incomplete SMILES will produce spurious or missing annotations.
- In silico fragmentation complexity grows exponentially with molecular weight; very large molecules may have incomplete fragment coverage or excessive computational cost.
- Isomeric structures cannot be distinguished by MAGMa annotation alone; if the reference structure is ambiguous, annotation ambiguity will propagate into modification site scoring.
- Neutral losses and multi-step fragmentations are not systematically enumerated in the base MAGMa implementation; simple bond cleavages are well-annotated but complex rearrangements may be missed.
- Modification-induced shifts in fragmentation patterns (e.g., post-translational modification changing local chemistry) may cause annotated fragments to no longer match observed peaks, reducing signal for those atoms.

## Evidence

- [other] ModiFinder generates per-atom modification site probabilities through tandem mass spectral alignment, enabling structural modification site localization.: "ModiFinder generates per-atom modification site probabilities through tandem mass spectral alignment, enabling structural modification site localization"
- [other] MAGMaAnnotationEngine is instantiated alongside CosineAlignmentEngine when constructing a ModiFinder object for probability generation.: "Instantiate a ModiFinder object with the known compound, modified compound, and default CosineAlignmentEngine and MAGMaAnnotationEngine"
- [other] Peak preprocessing uses specific tolerance and normalization parameters that control fragment matching.: "default preprocessing (mz_tolerance=0.01, ppm_tolerance=40, ratio_to_base_peak=0.01, normalize_peaks=True)"
- [other] ModiFinder integrates fragment annotation into per-atom scoring.: "fragmentation annotation to a known/unknown compound pair"
- [readme] ModiFinder API produces fragment metadata alongside peak data.: "fragmentsObj = { "frags_map": knownCompound.spectrum.peak_fragment_dict, "structure": knownCompound.structure, "peaks": main_compound_peaks"
