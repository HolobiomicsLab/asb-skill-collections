---
name: irreversible-model-conversion
description: Use when you have a constraint-based metabolic model in SBML or similar
  format with reversible reactions and need to sample the feasible steady-state flux
  region using optGpSampler or other samplers that require an irreversible stoichiometric
  matrix.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_2259
  - http://edamontology.org/topic_3307
  tools:
  - eFlux
  - TRFBA
  - scFBA
  - GX-FBA
  - optGpSampler
  - COBRApy
  - MATLAB/libSBML
  license_tier: open
derived_from:
- doi: 10.1371/journal.pcbi.1009337
  title: INTEGRATE
evidence_spans:
- we set flux boundaries as a function of gene expression as done, among others, by
  eFlux [36] and TRFBA
- We scaled metabolic fluxes relative to the maximum flux identified using Flux Variability
  Analysis, as in scFBA
- We used relative gene-expression values as in GX-FBA
- We exploited the implementation of optGpSampler algorithm [71] available in COBRApy
  [72], and we sampled a million steady state solutions
- In this work, we exploited the implementation of optGpSampler algorithm [71] available
  in COBRApy [72], and we sampled a million steady state solutions
- We exploited the implementation of optGpSampler algorithm [71] available in COBRApy
  [72]
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_integrate_cq
    doi: 10.1371/journal.pcbi.1009337
    title: INTEGRATE
  dedup_kept_from: coll_integrate_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1371/journal.pcbi.1009337
  all_source_dois:
  - 10.1371/journal.pcbi.1009337
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Convert constraint-based metabolic model from reversible to irreversible format

## Summary

Transform a reversible constraint-based stoichiometric metabolic model into irreversible form by splitting each reversible reaction into distinct forward and backward variants. This conversion is necessary to enable uniform sampling of the feasible flux region using optGpSampler and other sampling algorithms that operate on irreversible model representations.

## When to use

You have a constraint-based metabolic model in SBML or similar format with reversible reactions and need to sample the feasible steady-state flux region using optGpSampler or other samplers that require an irreversible stoichiometric matrix. This is a required preprocessing step before applying uniform sampling to generate feasible flux distribution (FFD) datasets.

## When NOT to use

- Model is already in irreversible form (check reaction list for absence of forward/backward pairs)
- Sampling method in use is designed for reversible models (e.g., some thermodynamic-based samplers)
- Goal is FBA or FVA optimization (these methods work directly on reversible models without conversion overhead)

## Inputs

- SBML metabolic model file with reversible reactions (e.g., ENGRO2_MCF102A.xml)
- Cell-specific constraint bounds: RAS-dependent flux boundaries (from Step 4), nutrient availability constraints, and extracellular flux ratio constraints

## Outputs

- Irreversible model in SBML format (e.g., ENGRO2_MCF102A_wIrrRxns.xml)
- Irreversible model in mat file format compatible with optGpSampler (for MATLAB-based sampling)
- Updated reaction ID mapping (reversible → forward/backward pairs)

## How to apply

Load the cell-relative metabolic model (SBML format) containing all three constraint types: nutrient availability, extracellular flux ratios, and transcriptomics-derived RAS-dependent bounds. Split each reversible reaction into forward (positive flux) and backward (negative flux) variants, creating new reaction IDs and updating the stoichiometric matrix accordingly. Convert the model to irreversible form (typically via mat file export for MATLAB-based tools or native COBRApy conversion) while preserving all constraint bounds and GPR rules. The conversion maintains mass balance and reaction constraints; verify by checking that the total number of reactions increases (each reversible reaction becomes two) and that the nullspace dimension remains constant. This converted model is then passed to Step 6 (randomSampling) in the INTEGRATE pipeline.

## Related tools

- **COBRApy** (Python library for loading, manipulating, and converting metabolic models; provides native reversible-to-irreversible model conversion and constraint application) — https://github.com/opencobra/cobrapy
- **optGpSampler** (Sampling algorithm that requires irreversible model format to uniformly sample the constrained null space and generate feasible flux distributions)
- **MATLAB/libSBML** (MATLAB-based model I/O and format conversion to mat file for use with MATLAB sampling routines)

## Examples

```
python pipeline/randomSampling.py 100000 10
# This assumes Step 5 (Models splitting to irreversible) has already converted ENGRO2_MCF102A.xml to ENGRO2_MCF102A_wIrrRxns.mat for input to optGpSampler
```

## Evaluation signals

- Verify reaction count increase: for each reversible reaction in original model, two new reactions appear in irreversible model (forward and backward variants with distinct IDs)
- Stoichiometric matrix rank unchanged: nullspace dimension of irreversible stoichiometric matrix equals that of reversible model (both satisfy mass balance)
- Flux bound consistency: for any solution in irreversible space, the net flux (forward − backward) falls within the original reversible reaction's bounds
- Successful model loading in optGpSampler: irreversible model is accepted as input for randomSampling step (Step 6 of INTEGRATE) without parsing errors
- RAS and constraint preservation: all RAS-dependent bounds and nutrient/extracellular flux constraints are maintained and enforceable in the irreversible formulation

## Limitations

- Conversion increases model size and computational cost: irreversible model has approximately 2× the number of variable reactions compared to reversible model, requiring more memory and CPU during sampling
- GPR rules and gene-reaction associations must be explicitly transferred or duplicated for both forward and backward reaction variants to preserve transcriptomic constraint interpretation
- Reversible reaction splitting is lossy in the reverse direction: solver may not distinguish between true backward flux and a zero forward + positive backward flux; this affects interpretation of cofactor balance in highly reversible pathways
- Model validation tools expect reversible format: some metabolic model checking routines (e.g., dead-end metabolite detection) may report false positives on irreversible models unless adapted

## Evidence

- [full_text] Convert each constrained model to irreversible form by splitting reversible reactions into forward and backward variants.: "Convert each constrained model to irreversible form by splitting reversible reactions into forward and backward variants."
- [full_text] Uniformly sample the constrained null space of the stoichiometric matrix for each cell line using optGpSampler with thinning value 10, generating 1 million total steady-state solutions (10 batches of 100,000 each) while maintaining the growth yield constraint.: "Uniformly sample the constrained null space of the stoichiometric matrix for each cell line using optGpSampler with thinning value 10, generating 1 million total steady-state solutions"
- [readme] Each model needs to be converted to a mat file in order to exploit the MATLAB function to convert model from the reversible into the irreversible format: "Each model needs to be converted to a mat file in order to exploit the MATLAB function to convert model from the reversible into the irreversible format"
- [full_text] Apply all three constraint types (nutrient availability, extracellular flux ratios, and transcriptomics-derived flux boundaries) to each of the five cell-relative metabolic models.: "Apply all three constraint types (nutrient availability, extracellular flux ratios, and transcriptomics-derived flux boundaries) to each of the five cell-relative metabolic models."
