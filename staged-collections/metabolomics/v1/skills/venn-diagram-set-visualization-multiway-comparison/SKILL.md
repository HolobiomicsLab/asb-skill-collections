---
name: venn-diagram-set-visualization-multiway-comparison
description: Use when analyzing metabolomics data through Venn diagram visualization to compare three-way sets of in vitro S9-incubated metabolites, BioTransformer in silico predictions, and literature-reported metabolites.
when_to_use_negative:
- Input metabolites are not yet standardized to a common identifier (molecular formula, InChI, SMILES) — first normalize the representation across sources.
- You have fewer than two reference knowledge sources (e.g., only in vitro and literature, no predictions, or only predictions) — use pairwise or single-source visualizations instead.
- The three sets originate from different chemical spaces or parent compounds — ensure all three are derived from the same set of parent compounds (22 pesticides in this study).
edam_operation: http://edamontology.org/operation_3695
edam_topics:
- http://edamontology.org/topic_0154
- http://edamontology.org/topic_2269
- http://edamontology.org/topic_3370
tools:
- name: BioTransformer
  role: In silico prediction of phase I metabolite structures and molecular formulas using rule-based and machine-learning approaches with CYP450 transformation type selection
- name: R v 3.6.1
  role: Data analysis and set comparison operations for Venn diagram generation and overlap calculation
  repo: https://github.com/chufz/incubatoR
- name: GenForm
  role: Molecular formula calculation from MS1 and MS2 spectra to standardize experimental metabolite representation for set matching
provenance:
  source_task_ids:
  - task_005
  source_papers:
  - doi: 10.1021/acs.analchem.1c00972
    title: Improving the Screening Analysis of Pesticide Metabolites in Human Biomonitoring by Combining High-Throughput <i>In Vitro</i> Incubation and Automated LC–HRMS Data Processing
schema_version: 0.2.0
metadata:
  merge_audit:
    n_source_runs: 2
    source_files:
    - outputs/pesticide_full_2026-05-10_v2/skills/venn-diagram-set-visualization-multiway-comparison/SKILL.md
    - outputs/pesticide_full_2026-05-10_v2/skills/venn-diagram-set-visualization-multiway-comparison/skill.md
    merged_at: '2026-05-25T07:15:31.006580+00:00'
    merge_kind: slug_match_union
  iri: https://w3id.org/holobiomicslab/asb-skill/venn-diagram-set-visualization-multiway-comparison@sha256:957a96c23918e618294443bd3cdc23729b98e07603741af438d5a349fd2b54b2
  related_workflows:
  - benchmark/tasks/audit_haffner_v2/workflow.smk
  - benchmark/tasks/audit_jeong_full/workflow.smk
  - benchmark/tasks/article_878_full_2026-05-10_v5/workflow.smk
  - benchmark/tasks/pesticide_full_2026-05-10_v2/workflow.smk
  - benchmark/tasks/audit_s41592_full/workflow.smk
derived_from:
- doi: 10.1021/acs.analchem.1c00972
---

# venn-diagram-set-visualization-multiway-comparison

## Summary

Venn diagram visualization for three-way set comparison showing overlap and exclusive membership among in vitro S9-incubated metabolites, BioTransformer in silico predictions, and literature-reported metabolites. This skill evaluates metabolite discovery completeness and prediction algorithm performance.

## When to use

When you have identified experimental metabolites (e.g., from LC–HRMS metabolite feature prioritization) and want to compare them against two reference knowledge sources: (1) in silico predictions from rule-based or machine-learning metabolite generators (e.g., BioTransformer with CYP450 transformation type), and (2) published literature or registration dossier records. This comparison is particularly valuable when assessing whether your in vitro incubation or biomonitoring assay has recovered known or predicted metabolites and identifying gaps in coverage.

## When NOT to use

- Input metabolites are not yet standardized to a common identifier (molecular formula, InChI, SMILES) — first normalize the representation across sources.
- You have fewer than two reference knowledge sources (e.g., only in vitro and literature, no predictions, or only predictions) — use pairwise or single-source visualizations instead.
- The three sets originate from different chemical spaces or parent compounds — ensure all three are derived from the same set of parent compounds (22 pesticides in this study).

## Inputs

- Experimental molecular formula set from prioritized LC–HRMS metabolite features (91 unambiguous formulas for 22 pesticides)
- BioTransformer-predicted phase I metabolite molecular formulas (CYP450 transformation rules)
- Literature or registration dossier metabolite records (e.g., EFSA pesticide dossiers, MassBank)

## Outputs

- Three-way Venn diagram visualization (mass@rt or molecular formula membership)
- Overlap statistics (percentage/count in each region: all three, pairwise intersections, unique to each source)
- Membership categories (metabolites unique to in vitro, unique to prediction, unique to literature, or shared)

## How to apply

Extract molecular formulas or metabolite identifiers from three independent sources: (1) experimental in vitro S9-incubated samples (91 unambiguous molecular formulas assigned to 82 features in ESI+ and 39 in ESI− mode in this study); (2) BioTransformer predictions for the same parent compounds using CYP450 transformation type selection; (3) literature metabolites from registration dossiers or published metabolism studies. Standardize formula/identifier representation across all three sets. Compute set intersection (metabolites found in all three), pairwise intersections, and exclusive elements (in vitro only, predicted only, literature only). Generate a three-way Venn diagram showing counts or percentages in each region. Report the overlap percentage (e.g., "about two-thirds") as a metric of prediction accuracy and in vitro assay completeness. Use the diagram to identify reaction types or metabolites missing from predictions or in vitro detection.

## Related tools

- **BioTransformer** (In silico prediction of phase I metabolite structures and molecular formulas using rule-based and machine-learning approaches with CYP450 transformation type selection)
- **R v 3.6.1** (Data analysis and set comparison operations for Venn diagram generation and overlap calculation) — https://github.com/chufz/incubatoR
- **GenForm** (Molecular formula calculation from MS1 and MS2 spectra to standardize experimental metabolite representation for set matching)

## Evaluation signals

- All three sets contain the same parent compound identifiers and are derived from identical or comparable study cohorts (e.g., 22 pesticides across all sources).
- Overlap percentage matches literature or prior expectation for the biological or chemical system (e.g., ~66–67% of in vitro metabolites matched to literature or BioTransformer predictions in this study).
- Exclusive or low-overlap metabolites can be explained by known biological or analytical limitations (e.g., weak bond breaking, consecutive hydroxylations, or reduction reactions not covered by CYP450 rules; undetected metabolites due to low ionization efficiency or losses during extraction).
- Venn diagram regions are labeled with counts or percentages and include both numeric and categorical information (e.g., 'n=X (% of total)') for transparency.
- Special cases (e.g., compounds with zero or complete overlap, such as isoproturon and triazines vs. metazachlor) are documented alongside the diagram to explain deviation from overall trend.

## Limitations

- In vitro S9 liver microsome incubation does not cover all potential or existing metabolites; some phase II conjugation or gut microbiome metabolites may be missed. For metazachlor, only 3 of 12 mammalian metabolites in the registration dossier were observed in vitro.
- BioTransformer CYP450-focused predictions may miss in vitro metabolites formed by reduction reactions (dehydrogenation), consecutive hydroxylations, or breaking of weak bonds not explicitly represented in rule sets.
- Detected metabolites may not appear in the experimental dataset due to low ionization efficiency in LC–HRMS, especially for hydrophilic compounds, or losses during sample extraction and cleanup; conversely, some predicted metabolites may not ionize well in ESI+ or ESI− mode.
- Literature data and registration dossiers may contain only mammalian (rat, mouse, rabbit) metabolism data and may not reflect human biotransformation patterns; fipronil case showed 6 rat metabolites but only fipronil-sulfone as a biomarker in human serum.
- Overlap interpretation is sensitive to molecular formula standardization and ionization mode (ESI+ vs. ESI−); formulas assigned with ambiguity or adduct differences may artificially inflate or deflate overlap counts.

## Evidence

- [methods] About two-thirds of the in vitro-metabolites were reported in the literature or predicted: "About two-thirds of the in vitro-metabolites were reported in the literature or predicted"
- [methods] By applying the data processing workflow, we could assign in total 91 unambiguous molecular formulas to a number of 82 prioritized features in ESI+ and 39 in ESI− for the 22 pesticides.: "By applying the data processing workflow, we could assign in total 91 unambiguous molecular formulas to a number of 82 prioritized features in ESI+ and 39 in ESI− for the 22 pesticides."
- [methods] Metabolites were predicted using BioTransformer, which combines a rule-based approach and a machine learning approach.: "Metabolites were predicted using BioTransformer, which combines a rule-based approach and a machine learning approach."
- [discussion] A comparison with the literature data and metabolization prediction showed that the S9 incubation does not cover all potential or existing metabolites.: "A comparison with the literature data and metabolization prediction showed that the S9 incubation does not cover all potential or existing metabolites."
- [discussion] For metazachlor, 12 mammalian metabolites are described in the registration dossier, but we only observed three in the incubation experiment.: "For metazachlor, 12 mammalian metabolites are described in the registration dossier, but we only observed three in the incubation experiment."
- [discussion] In vitro metabolites, which were not predicted, were mainly formed by reduction reactions (dehydrogenation), two consecutive hydroxylations or the breaking of a weak bond in the molecule: "In vitro metabolites, which were not predicted, were mainly formed by reduction reactions (dehydrogenation), two consecutive hydroxylations or the breaking of a weak bond in the molecule"
- [readme] Main task is to identify metabolic transformation products in a LC-HRMS2 dataset of in-parallel incubated xenobiotic compounds by applying statistical tools as well as mass defect filtering and extraction of the respective mass spectra for spectal library generation.: "Main task is to identify metabolic transformation products in a LC-HRMS2 dataset of in-parallel incubated xenobiotic compounds by applying statistical tools as well as mass defect filtering and"
