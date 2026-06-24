---
name: qvalue-threshold-filtering
description: Use when after loading search result files (e.g., from DIA-NN or OpenSwath)
  containing feature identification results with associated Q-value scores, apply
  this filter when you need to select a subset of high-confidence identifications
  before generating comparison plots or summary statistics across.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Streamlit
  - ResultsLoader
  - OSWDataAccess
  - InteractivePlotter
  - MassDash
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1021/acs.jproteome.4c00026
  title: MassDash
evidence_spans:
- streamlit graphical user interface (GUI)
- ResultsLoader
- OSWDataAccess
- InteractivePlotter
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_massdash_cq
    doi: 10.1021/acs.jproteome.4c00026
    title: MassDash
  dedup_kept_from: coll_massdash_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.4c00026
  all_source_dois:
  - 10.1021/acs.jproteome.4c00026
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Q-value-threshold filtering

## Summary

Apply a statistical confidence threshold (Q-value cutoff) to peptide feature identifications from DIA-MS search results, retaining only high-confidence analyte detections for downstream visualization and comparison. This filtering step reduces false positives and ensures that comparative analyses focus on reliable identifications across different search algorithms.

## When to use

After loading search result files (e.g., from DIA-NN or OpenSwath) containing feature identification results with associated Q-value scores, apply this filter when you need to select a subset of high-confidence identifications before generating comparison plots or summary statistics across multiple tools or experiments. Use this when the analyte selection dropdown must be restricted to statistically confident features (e.g., a 1% FDR threshold is typical in proteomics).

## When NOT to use

- When input search results do not include Q-value or FDR scores (filtering would not be applicable).
- When you need to visualize or compare ALL identifications including low-confidence hits (an unfiltered or permissive threshold may be more appropriate).
- When the analysis goal is exploratory and does not require statistical confidence guarantees (raw or pre-filtered results may suffice).

## Inputs

- Search result files (DIA-NN native format or OSW format) containing feature identifications with Q-value scores
- Q-value threshold parameter (e.g., 0.01 for 1% FDR)
- Tool metadata (software identifier, experiment label)

## Outputs

- Filtered list of high-confidence analyte identifications
- Filtered feature identifications with log2 quantifications and coefficient of variation values
- Updated dropdown selection boxes populated only with analytes passing the Q-value threshold

## How to apply

Load search results file paths and tool metadata via ResultsLoader or tool-specific loaders (OSWDataAccess for OpenSwath). Apply Q-value filtering at a specified cutoff threshold (e.g., Q-value ≤ 0.01 for 1% FDR) using the results filtering functionality to select analytes that meet the confidence criterion. The sidebar provides interactive settings to control the Q-value cutoff, allowing users to adjust the threshold on the fly. After filtering, extract feature identifications, log2 quantifications, and coefficient of variation values for the retained analytes. Verify that the dropdown selection boxes now contain only analytes passing the Q-value threshold, ensuring that all downstream plots (identifications bar plot, log2 quantifications violin plot, coefficient of variation violin plot, upset comparisons plot) are computed only over the filtered feature set.

## Related tools

- **ResultsLoader** (Loads search result file paths and tool metadata for each search tool, enabling Q-value filtering to be applied) — https://github.com/Roestlab/massdash
- **OSWDataAccess** (Tool-specific loader for OpenSwath results; enables Q-value filtering on OpenSwath search output) — https://github.com/Roestlab/massdash
- **Streamlit** (Provides the graphical user interface sidebar where Q-value cutoff settings are controlled interactively)
- **MassDash** (Modular Python package implementing the overall filtering workflow and visualization pipeline) — https://github.com/Roestlab/massdash

## Evaluation signals

- Verify that analyte dropdown selection boxes contain only identifications with Q-value ≤ the specified cutoff (e.g., ≤ 0.01).
- Check that the count of retained analytes is less than or equal to the total number of identifications in the unfiltered search result file.
- Confirm that all downstream plots (identifications bar plot, log2 quantifications violin plot, coefficient of variation violin plot) are computed only over the filtered analyte set, with no low-confidence features included.
- Inspect the summary export table to ensure all rows correspond to identifications passing the Q-value threshold.
- Verify that interactive adjustment of the Q-value threshold in the sidebar dynamically updates the dropdown contents and downstream visualizations.

## Limitations

- Q-value filtering assumes that search result files include computed Q-value or FDR scores; raw spectral data without pre-computed statistics cannot be filtered this way.
- The choice of Q-value cutoff (e.g., 1% vs. 5% FDR) is task-dependent; the skill does not automatically select an optimal threshold.
- Filtering may reduce the number of analytes available for comparison if one search tool produces many low-confidence identifications; this can complicate tool-to-tool comparisons on very small filtered analyte sets.

## Evidence

- [other] the analytes populated in the drop down selection boxes are filtered based on the feature Q-value of 1%: "the analytes populated in the drop down selection boxes are filtered based on the feature Q-value of 1%"
- [other] Apply Q-value filtering at the specified cutoff threshold using results filtering at Q-value to select high-confidence identifications.: "Apply Q-value filtering at the specified cutoff threshold using results filtering at Q-value to select high-confidence identifications."
- [other] The sidebar provides settings to control results at a specified Q-value cutoff: "The sidebar provides settings to control results at a specified Q-value cutoff"
- [other] Load search results file paths and tool metadata (software identifier, experiment label) for each search tool via ResultsLoader or tool-specific loaders (e.g., OSWDataAccess for OpenSwath results).: "Load search results file paths and tool metadata (software identifier, experiment label) for each search tool via ResultsLoader or tool-specific loaders (e.g., OSWDataAccess for OpenSwath results)."
