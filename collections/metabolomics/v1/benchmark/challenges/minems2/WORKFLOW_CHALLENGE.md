# Workflow Challenge: `coll_minems2_workflow`


> mineMS2 couples frequent fragmentation pattern mining with GNPS molecular networks to identify and interpret m/z difference patterns that explain network components in MS/MS spectral libraries.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 1-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

The mineMS2 package enables discovery of frequent patterns in MS/MS spectra by mining fragmentation graphs, where each pattern is a graph of ion peaks connected by m/z differences. When applied to the Penicillium nordicum dataset (51 MS/MS spectra), the workflow extracted nine network components from a precomputed GNPS molecular network and identified explaining patterns for each component using precision, recall, and F1-score metrics. For component 8 (a high-similarity pair with precursor m/z 370.1283 and 404.0891), pattern P70 achieved an F1-score of 1, meaning it explained all component spectra without explaining any spectra outside the component, while other top-5 candidate patterns maintained recall of 1 but showed lower precision. The method identified that 19 of 21 spectra in the largest component shared an m/z difference of 99.0683 (consistent with valine loss in tetrapeptides), and discovered that an m/z difference of 186.079 (possibly tryptophan loss) appeared across seven spectra not all directly linked in the molecular network, revealing new similarities independent of network thresholds.

## Research questions

- When findPatternsExplainingComponents is applied to component 8 (a high-similarity pair of spectra with precursor m/z values 370.1283 and 404.0891) using recall-precision-size metrics and top=5, does pattern P70 achieve perfect F1-score while other top-5 patterns maintain recall=1 but exhibit lower precision?

## Methods overview

Load pre-processed Penicillium nordicum ms2Lib object with discretized m/z differences and extracted closed subgraph patterns. Load GNPS molecular network as igraph object and extract connected components, cliques, and high-similarity node pairs. Execute findPatternsExplainingComponents algorithm with metric=c('recall','precision','size') and top=5 to rank patterns by their explanatory power. Compute F1-scores for each pattern–component pair as the harmonic mean of recall and precision. Extract and tabulate results for component 8 (m/z 370.1283 and 404.0891), verifying P70 achieves F1=1.0 and all competing top-5 patterns have recall=1.0 but lower precision. Validation: Output must contain verifiable metric values showing P70 with F1-score=1.0 and all other top-5 patterns with recall=1.0 and 0<precision<1.0 for component 8.

**Domain:** metabolomics

**Techniques:** database-annotation, dereplication, molecular-networking, spectral-library-matching, substructure-mining, tandem-ms

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** mineMS2 patterns are graphs with ion peaks as nodes and m/z differences as edges. _[grounded: SYS_MINEMS2]_
- **(finding)** mineMS2 m/z differences include not only neutral losses but also m/z differences between ions that belong to distinct fragmentation paths. _[grounded: SYS_MINEMS2]_
- **(finding)** The mineMS2 method is independent of external spectral databases and knowledge of the molecular formula of precursor ions. _[grounded: SYS_MINEMS2]_
- **(hypothesis)** mineMS2 patterns are complementary to MS2LDA patterns because they consist of exact graphs rather than probabilistic lists. _[grounded: SYS_MINEMS2]_
- **(finding)** The dataset contains 51 MS/MS spectra from secondary metabolites of Penicillium nordicum. _[grounded: TOOL_INSTRUMENT]_
- **(finding)** The Penicillium nordicum spectra were acquired on a Luna C18 column using HPLC coupled to an LTQ Orbitrap XL hybrid mass spectrometer. _[grounded: TOOL_INSTRUMENT]_
- **(finding)** The Penicillium nordicum spectra were acquired in positive ionization mode at HCD20 collision energy with a resolution of 7,500. _[grounded: COMP_PENICILLIUM_NORDICUM]_
- **(finding)** The molecular network was precomputed on the GNPS website and extracted in GraphML format. _[grounded: SYS_MINEMS2]_
- **(finding)** mineMS2 can be coupled to GNPS MS/MS molecular networking to focus on patterns that best explain components of the network. _[grounded: SYS_MINEMS2]_
- **(finding)** It is recommended to compute the patterns and the GNPS network using the same .mgf input file to avoid matching issues. _[grounded: TOOL_GNPS]_
- **(finding)** The ms2Lib class is used throughout the workflow to store the spectra data and metadata, the m/z differences, the fragmentation graphs, and the patterns. _[grounded: COMP_MS2LIB]_
- **(finding)** The ms2Lib constructor function can take the collection of MS/MS spectra as input as a single mgf file, a vector of individual mgf file names, the name of a directory containing individual spectra as mgf files, or a list of Spectrum2 objects. _[grounded: COMP_MS2LIB]_
- **(finding)** Supplementary metadata about the spectra can be provided as a tsv tabular file.
- **(finding)** The metadata are not used in the computations of m/z differences, fragmentation graphs, or frequent patterns but can be displayed in plot titles.
- **(finding)** Two columns mz.precursor and file are automatically inserted at the beginning of the metadata table stored in the ms2Lib object. _[grounded: COMP_MS2LIB]_
- **(finding)** The discretizeMzDifferences method computes the m/z differences between the peaks in each spectrum and discretizes them for the whole spectra collection. _[grounded: SYS_MINEMS2]_
- **(finding)** The m/z differences computed by discretizeMzDifferences include not only neutral losses but also differences between ions that belong to distinct fragmentation paths of the precursor. _[grounded: COMP_DISCRETIZE]_
- **(finding)** The default value of the ppm parameter in discretizeMzDifferences is 15. _[grounded: COMP_DISCRETIZE]_
- **(finding)** The default value of the dmz parameter in discretizeMzDifferences is 0.007 Da. _[grounded: COMP_DISCRETIZE]_
- **(finding)** The default value of the count parameter in discretizeMzDifferences is 2. _[grounded: COMP_DISCRETIZE]_
- **(finding)** The default value of the maxFrags parameter in discretizeMzDifferences is 15. _[grounded: COMP_DISCRETIZE]_
- **(finding)** The default value of the limMzFormula parameter in discretizeMzDifferences is c(14.5, 200). _[grounded: COMP_DISCRETIZE]_
- **(finding)** The mineClosedSubgraphs method extracts frequent subgraphs among the fragmentation graphs. _[grounded: COMP_MINESUBGRAPHS]_
- **(finding)** The default value of the count parameter in mineClosedSubgraphs is 2. _[grounded: COMP_MINESUBGRAPHS]_
- **(finding)** The default value of the sizeMin parameter in mineClosedSubgraphs is 1. _[grounded: COMP_MINESUBGRAPHS]_
- **(finding)** When the number of frequent m/z differences is above 600 and sizeMin is set to 1, the sizeMin value will be automatically increased to 2.
- **(finding)** The findGNPSComponents function extracts connected components from the molecular network. _[grounded: COMP_FINDGNPS]_
- **(finding)** The findGNPSComponents function can extract cliques from the molecular network. _[grounded: COMP_FINDGNPS]_
- **(finding)** The findGNPSComponents function selects a set of disjoint cliques by decreasing order of size. _[grounded: SYS_MINEMS2]_
- **(finding)** The findGNPSComponents function can extract high similarity pairs of nodes from the molecular network. _[grounded: COMP_FINDGNPS]_
- **(finding)** The minSize parameter of findGNPSComponents specifies the minimum size of detected cliques. _[grounded: COMP_FINDGNPS]_
- **(finding)** The pairThreshold parameter of findGNPSComponents specifies the threshold of the cosine score for high similarity pairs of nodes. _[grounded: COMP_FINDGNPS]_
- **(finding)** Nine components were selected from the Penicillium nordicum GNPS molecular network. _[grounded: TOOL_GNPS]_
- **(finding)** Components 6, 7, 8 and 9 are the connected components of the Penicillium nordicum network. _[grounded: COMP_PENICILLIUM_NORDICUM]_
- **(finding)** Components 1, 3, and 4 are disjoint cliques from component 6 (the larger cluster).
- **(finding)** Components 2 and 5 are disjoint cliques from component 7 (the smaller cluster).
- **(finding)** The recall metric measures the proportion of explained spectra among the component spectra.
- **(finding)** The precision metric measures the proportion of component spectra among the explained spectra.
- **(finding)** The F1-score is the harmonic mean of precision and recall.
- **(finding)** For the pair of spectra with precursor m/z values of 370.1283 and 404.0891 (component 8), the best explaining pattern P70 has an F1-score of 1.
- **(finding)** The largest component in the Penicillium nordicum GNPS network consists of 21 spectra. _[grounded: TOOL_GNPS]_
- **(finding)** The m/z difference of 99.0683 is shared by 19 out of 21 fragmentation spectra in the largest component.
- **(finding)** The m/z difference of 99.0683 has a precision of 1, indicating it is not present in any other spectra of the dataset.
- **(finding)** The m/z difference of 186.079 has a possible formula of C11H10ON2. _[grounded: COMP_TRYPTOPHAN]_
- **(hypothesis)** A total of multiple patterns include the m/z difference of 186.079. _[grounded: COMP_P179]_
- **(finding)** A pattern including the m/z difference 186.079 is found in 7 spectra. _[grounded: TOOL_GNPS]_
- **(hypothesis)** mineMS2 discovers new similarities between spectra that are not all linked together in the GNPS network. _[grounded: SYS_MINEMS2]_
- **(finding)** The default ppm tolerance in mineMS2 is 15 ppm. _[grounded: SYS_MINEMS2]_
- **(finding)** When ppm tolerance was set to 7 ppm on the LIMS-DB dataset, the average F1-score decreased to 0.47.
- **(finding)** With the default ppm tolerance of 15 ppm on the LIMS-DB dataset, the average F1-score is 0.53.
- **(finding)** At 7 ppm tolerance, patterns explaining ChemOnt concepts contained 5.2 m/z differences on average.
- **(finding)** At 15 ppm tolerance, patterns explaining ChemOnt concepts contained 6.8 m/z differences on average.
- **(finding)** The default maximum number of fragments in discretizeMzDifferences is set to 15. _[grounded: COMP_DISCRETIZE]_
- **(finding)** Mining the LIMS-DB dataset with maxFrags of 20 increased running time to 1.5 hours.
- **(finding)** The default maxFrags of 15 requires 20 minutes to mine the LIMS-DB dataset.
- **(finding)** The GNPS network for Penicillium nordicum contains 2 clusters of sizes 21 and 11, in addition to 2 pairs. _[grounded: TOOL_GNPS]_

## Sanctioned method substitutions
Using any of these instead of the source method is **not penalized**:
- MetGem can be used instead of GNPS for molecular network generation, with different node and edge attribute names

## Invariants (must not change)
Changing any of these **is** a failure regardless of openness:
- Patterns and GNPS network should be computed using the same .mgf input file to avoid matching issues

## Steps

### Step `task_001`
- Title: Reproduce the count of GNPS components extracted from the Penicillium nordicum molecular network
- Task kind: `reproduction`
- Task: Run findPatternsExplainingComponents on the Penicillium nordicum ms2Lib object and extracted GNPS components using metric=c('recall','precision','size') and top=5, then verify that pattern P70 achieves F1-score=1.0 for component 8 while all other top-5 patterns have recall=1.0 but lower precision.
- Inputs:
  - Penicillium nordicum ms2Lib object with 51 MS/MS spectra, discretized m/z differences, and extracted fragmentation patterns
  - GNPS molecular network in GraphML format with connected components, cliques, and high-similarity node pairs
- Expected outputs:
  - Table or data frame with pattern identifiers, recall, precision, F1-score, and size metrics for top-5 patterns per component, confirming P70 achieves F1=1.0 for component 8
  - Verification report confirming pattern P70 F1-score=1.0 and all other top-5 patterns have recall=1.0 with precision<1.0
- Tools: mineMS2, igraph, R
- Landmark output files: ms2lib_patterns_discretized.rds, gnps_components_extracted.rds, findPatternsExplainingComponents_output.csv
- Primary expected artifact: `pattern_metrics_component8.csv`

## Final expected outputs

- `Table or data frame with pattern identifiers, recall, precision, F1-score, and size metrics for top-5 patterns per component, confirming P70 achieves F1=1.0 for component 8` (type: file, tolerance: hash)
- `Verification report confirming pattern P70 F1-score=1.0 and all other top-5 patterns have recall=1.0 with precision<1.0` (type: file, tolerance: hash)

## How your attempt will be scored

ASB defines seven rubrics in `workflow_rubric.py` (STEP_ORDERING, INTERMEDIATE_FIDELITY, END_TO_END_OUTPUT, TOOL_SELECTION, EFFICIENCY, CLAIM_VALIDATION, ADVERSARIAL_TRAP_AVOIDANCE). Which of them bind for *this* challenge depends on the tier and openness below.

### Tier evaluation profile

**Evaluator:** automated — filesystem presence + type-port resolution; END_TO_END_OUTPUT with declared per-output tolerance.
**Binding rubrics:** STEP_ORDERING, END_TO_END_OUTPUT (typed/tolerance), TOOL_SELECTION, CLAIM_VALIDATION.

### Openness stance

**Openness: mixed — per-step.** Closed steps must reproduce (rubrics above bind on them); open steps are judged by **SCIENTIFIC_VALIDITY** (below). Invariants bind everywhere; different is not wrong on the open steps.

## SCIENTIFIC_VALIDITY (binding for open / mixed tasks)
Open/mixed steps are graded at **EvalTier** granularity by the shared card judge (`runner_checks` llm_judge), not by exact match. The judge assigns one of `reproduced` / `replicated` / `re_analyzed` / `consistent` / `improved`; `consistent` and `re_analyzed` earn partial credit per the tier multipliers (0.60 / 0.75), so a scientifically sound but different result is credited rather than failed. Exact-match rubrics (INTERMEDIATE_FIDELITY, END_TO_END_OUTPUT) are **informational** for these tasks. Three axes the judge weighs:

1. **Addresses the research question** — does the attempt answer it?
2. **Defensible method** — sound, and respects the *Invariants* above?
3. **Results validity** — consistent with the claims, or a valid, evidenced extension? New supported claims earn credit, not penalty.

## Workflow characterisation

_Suter et al. 2025 (DOI 10.1016/j.future.2025.107974)._

- **Coupling:** tight

- **Composition modularity:** hierarchical

- **Abstraction level:** concrete

- **Orchestration planning:** static

- **Data transport:** in_memory

- **Characterisation confidence:** inferred


## Submission

Produce two artifacts in your output directory:

1. The output files at the paths declared under **Final expected outputs**.
2. An `attempt.json` matching the schema below.
3. _(Optional)_ `attempt_metrics.json` with `wall_time_s`, `total_tokens`, `cost_usd` for the EFFICIENCY rubric.

### `attempt.json` schema

```json
{
  "workflow_id": "coll_minems2_workflow",
  "agent_order": [
    "task_001"
  ],
  "intermediate_outputs": {
    "task_001": {
      "<output_name>": "<locator>"
    }
  },
  "final_outputs": {
    "Table or data frame with pattern identifiers, recall, precision, F1-score, and size metrics for top-5 patterns per component, confirming P70 achieves F1=1.0 for component 8": "<locator>",
    "Verification report confirming pattern P70 F1-score=1.0 and all other top-5 patterns have recall=1.0 with precision<1.0": "<locator>"
  },
  "chosen_tools": {
    "task_001": "<tool_name>"
  }
}
```

---
_Generated by `asb workflow-challenge` (see ASB docs/superpowers/specs/2026-05-12-workflow-evaluation-and-reviewer-ui-design.md)._
