---
name: simulation-dataset-validation-benchmarking
description: Use when when you have installed or updated a DNA methylation analysis tool (e.g., ChAMP) and need to verify that it produces documented expected outputs on a reference simulation dataset before applying it to real experimental data.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3295
  - http://edamontology.org/topic_3673
  tools:
  - ChAMP
  - ChAMPdata
derived_from:
- doi: 10.1093/bioinformatics/btx513
  title: champ
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/epigenomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_champ
    doi: 10.1093/bioinformatics/btx513
    title: champ
  dedup_kept_from: coll_champ
schema_version: 0.2.0
---

# simulation-dataset-validation-benchmarking

## Summary

Validate that a DNA methylation analysis tool produces expected results when applied to a known simulation dataset with documented behavior. This skill ensures tool functionality and correct parameter settings by comparing observed outputs against established ground truth for synthetic data.

## When to use

When you have installed or updated a DNA methylation analysis tool (e.g., ChAMP) and need to verify that it produces documented expected outputs on a reference simulation dataset before applying it to real experimental data. Specifically useful after version upgrades, parameter changes, or when integrating a tool into a new analysis pipeline.

## When NOT to use

- When analyzing real experimental methylation data—simulation datasets are synthetic and do not represent true biological variation; use them only for tool validation, not for biological interpretation.
- When the simulation dataset's documented expected behavior is unknown or unavailable—validation requires an explicit ground-truth specification.

## Inputs

- Simulation methylation dataset (e.g., EPICSimData loaded via data() in R)
- Array-type identifier string (e.g., 'EPIC', '450k')

## Outputs

- Block detection results object or report
- Interactive visualization (e.g., Block.GUI() output)
- Validation pass/fail confirmation against expected behavior

## How to apply

Load the simulation dataset (e.g., EPICSimData for EPIC array type) into the R environment using the appropriate data() call. Execute the analysis function with explicitly declared array-type parameters matching the simulation dataset's design (arraytype='EPIC'). Run any associated interactive visualization or inspection tools (e.g., Block.GUI()) to examine results. Verify that the observed output matches the documented expected behavior for that synthetic dataset—in this case, confirming the absence of differentially methylated blocks when none should be detected. If outputs deviate from expectations, investigate parameter settings or tool version compatibility before proceeding to real data.

## Related tools

- **ChAMP** (Primary analysis tool for differentially methylated block detection on EPIC and 450k array data) — https://github.com/YuanTian1991/ChAMP
- **ChAMPdata** (Data package providing EPICSimData simulation dataset and array annotations required for ChAMP) — https://github.com/YuanTian1991/ChAMPdata

## Examples

```
data(EPICSimData); champ.Block(arraytype='EPIC'); Block.GUI()
```

## Evaluation signals

- Output matches documented expected result for the simulation dataset (e.g., correct count of detected blocks or confirmation of absence of blocks)
- Interactive visualization tool (e.g., Block.GUI()) executes without errors and displays results interpretable by the tool's documentation
- Array-type parameter passed to the function matches the simulation dataset's specification (e.g., arraytype='EPIC' for EPICSimData)
- ChAMP version is compatible with ChAMPdata version (ChAMP ≥ 2.29.1 with ChAMPdata ≥ 2.23.1)
- No unexpected warnings or errors reported during function execution that would indicate parameter mismatch or incompatibility

## Limitations

- Simulation datasets represent idealized synthetic methylation patterns and may not reflect all edge cases or biological complexity present in real experimental data.
- Validation against one simulation dataset does not guarantee correct behavior on all array types or experimental designs—multiple simulation datasets (450k, EPIC, EPICv2) should be tested for comprehensive validation.
- EPICSimData is specifically designed for EPIC array validation; separate datasets exist for 450k and EPICv2 arrays, requiring separate validation runs for each array type.
- Tool version mismatches between ChAMP and ChAMPdata can cause unexpected behavior; the documented compatibility constraint (ChAMPdata ≥ 2.23.1) must be respected.

## Evidence

- [other] Simulation dataset validation approach: "Load EPICSimData into R environment using data(EPICSimData). Call champ.Block() function with arraytype='EPIC' to perform differentially methylated block detection on the simulation dataset."
- [other] Expected behavior documentation: "No differentially methylated blocks are detected when champ.Block() is executed on the EPICSimData simulation dataset with arraytype='EPIC' parameter."
- [other] Visualization verification: "Launch Block.GUI() interactive interface to visualize and inspect the block detection results. Verify that no differentially methylated blocks are reported in the output"
- [readme] Version compatibility requirement: "Current latest version: `2.29.1`, which support EPICv2, but it must be used along with ChAMPdata >= 2.23.1"
- [readme] Dataset loading method: "For the EPIC Simulation Data Set, user may use following code to load it: data(EPICSimData)"
