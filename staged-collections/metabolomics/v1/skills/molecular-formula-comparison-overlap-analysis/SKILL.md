---
name: molecular-formula-comparison-overlap-analysis
description: Compare predicted metabolite molecular formulas (from in silico tools like BioTransformer) against experimentally detected molecular formulas (from LC–HRMS data processing) to quantify overlap, identify agreement with literature data, and visualize membership in three-way sets (in vitro, prediction, literature). This skill evaluates the completeness and accuracy of metabolite discovery workflows.
when_to_use_negative:
- Input experimental dataset contains unassigned features or ambiguous molecular formulas; first resolve formula ambiguity via isotope/adduct removal, MS2 fragmentation analysis, or stricter GenForm cutoffs.
- BioTransformer predictions are limited to a single biotransformation type (e.g., only Phase II conjugation); this skill is designed for Phase I phase I metabolite prediction; adjust workflow if predicting Phase II or III metabolites.
- Mass difference filter threshold (+50 u) is inappropriate for the study design; e.g., if phase II conjugation (glucuronidation, sulfation) or species-specific metabolism is the research focus, adjust or disable the filter.
edam_operation: http://edamontology.org/operation_3695
edam_topics:
- http://edamontology.org/topic_0102
- http://edamontology.org/topic_3172
- http://edamontology.org/topic_3407
tools:
- name: BioTransformer
  role: Predicts phase I metabolite structures and molecular formulas from parent xenobiotic compounds using rule-based and machine learning approaches
- name: GenForm
  role: Calculates molecular formulas from high-resolution MS1 and MS2 spectra with configurable mass accuracy (±8 ppm in this example) and odd-electron ion detection
- name: XCMS version 3.8
  role: Performs feature detection, alignment, and retention time correction on centroided LC–HRMS data, generating the peaklist input for molecular formula assignment
- name: CAMERA
  role: Componentizes features (isotopes, adducts, in-source fragments) before statistical filtering and formula assignment
- name: R v 3.6.1
  role: Orchestrates automated workflow including set operations for overlap analysis, Venn diagram visualization, and membership categorization
  repo: https://github.com/chufz/incubatoR
- name: ProteoWizard v3.0.18265
  role: Converts raw vendor mass spectra to mzML format and performs centroiding before XCMS feature detection
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
    - outputs/pesticide_full_2026-05-10_v2/skills/molecular-formula-comparison-overlap-analysis/SKILL.md
    - outputs/pesticide_full_2026-05-10_v2/skills/molecular-formula-comparison-overlap-analysis/skill.md
    merged_at: '2026-05-25T07:15:30.994375+00:00'
    merge_kind: slug_match_union
  iri: https://w3id.org/holobiomicslab/asb-skill/molecular-formula-comparison-overlap-analysis@sha256:7b9bf664bb66f08b22235d782f20ea6e1a065d171ddc4983bae72590e68705ff
  related_workflows:
  - benchmark/tasks/audit_haffner_v2/workflow.smk
  - benchmark/tasks/audit_jeong_full/workflow.smk
  - benchmark/tasks/article_878_full_2026-05-10_v5/workflow.smk
  - benchmark/tasks/pesticide_full_2026-05-10_v2/workflow.smk
  - benchmark/tasks/audit_s41592_full/workflow.smk
derived_from:
- doi: 10.1021/acs.analchem.1c00972
---

# molecular-formula-comparison-overlap-analysis

## Summary

Compare predicted metabolite molecular formulas (from in silico tools like BioTransformer) against experimentally detected molecular formulas (from LC–HRMS data processing) to quantify overlap, identify agreement with literature data, and visualize membership in three-way sets (in vitro, prediction, literature). This skill evaluates the completeness and accuracy of metabolite discovery workflows.

## When to use

After automated LC–HRMS peak detection and molecular formula assignment (via GenForm and MS1/MS2 spectra) have yielded a prioritized list of experimental formulas, AND after running an in silico metabolite predictor (e.g., BioTransformer with CYP450 settings) on parent compound structures. Apply this skill to assess how many detected metabolites align with predictions and published reference data, especially when evaluating the adequacy of in vitro incubation models (e.g., S9 liver enzyme assays) for capturing biologically relevant metabolites.

## When NOT to use

- Input experimental dataset contains unassigned features or ambiguous molecular formulas; first resolve formula ambiguity via isotope/adduct removal, MS2 fragmentation analysis, or stricter GenForm cutoffs.
- BioTransformer predictions are limited to a single biotransformation type (e.g., only Phase II conjugation); this skill is designed for Phase I phase I metabolite prediction; adjust workflow if predicting Phase II or III metabolites.
- Mass difference filter threshold (+50 u) is inappropriate for the study design; e.g., if phase II conjugation (glucuronidation, sulfation) or species-specific metabolism is the research focus, adjust or disable the filter.

## Inputs

- Parent pesticide structures (SMILES, SDF, or chemical name)
- BioTransformer-predicted metabolite molecular formulas (text list or structured output)
- Experimental molecular formula dataset (from LC–HRMS processing: GenForm output, 91 formulas in this example)
- Literature metabolite reference set (EFSA registration dossiers, MassBank, or published studies)
- Feature metadata (m/z, retention time, abundance, ESI mode, replicates)

## Outputs

- Overlap statistics (percentage agreement between predicted and experimental; counts of shared, unique, and missing formulas)
- Membership category assignments (formulas in: in vitro only, prediction only, literature only, in vitro + prediction, in vitro + literature, all three)
- Venn diagram visualization (three-way set comparison)
- Filtered metabolite list (formulas passing mass difference filter: Δm/z ≤ +50 u to parent)
- Gap analysis report (predicted formulas not detected; in vitro formulas not predicted)

## How to apply

Obtain parent pesticide structures and execute BioTransformer with CYP450 transformation type to generate predicted phase I metabolite molecular formulas. Extract and standardize molecular formulas from BioTransformer output (e.g., using R or a formula parser). Load the experimental molecular formula dataset (91 unambiguous formulas from LC–HRMS workflow, assigned to 82 ESI+ and 39 ESI− features in this example). Perform set operations (intersection, union, exclusive members) to calculate overlap percentage and membership categories. Apply mass difference filtering to exclude formulas with m/z > parent + 50 u, which indicates conjugation or unlikely phase I products. Generate a Venn diagram showing three-way comparison: in vitro S9 metabolites, BioTransformer predictions, and literature metabolites (from EFSA registration dossiers or published sources). Document the proportion of overlap (e.g., "two-thirds of in vitro metabolites were predicted or literature-reported") and identify metabolites unique to each category to guide further investigation of unmatched predictions or undetected in vitro signals.

## Related tools

- **BioTransformer** (Predicts phase I metabolite structures and molecular formulas from parent xenobiotic compounds using rule-based and machine learning approaches)
- **GenForm** (Calculates molecular formulas from high-resolution MS1 and MS2 spectra with configurable mass accuracy (±8 ppm in this example) and odd-electron ion detection)
- **XCMS version 3.8** (Performs feature detection, alignment, and retention time correction on centroided LC–HRMS data, generating the peaklist input for molecular formula assignment)
- **CAMERA** (Componentizes features (isotopes, adducts, in-source fragments) before statistical filtering and formula assignment)
- **R v 3.6.1** (Orchestrates automated workflow including set operations for overlap analysis, Venn diagram visualization, and membership categorization) — https://github.com/chufz/incubatoR
- **ProteoWizard v3.0.18265** (Converts raw vendor mass spectra to mzML format and performs centroiding before XCMS feature detection)

## Evaluation signals

- Overlap percentage matches expected biological/chemical ratios; in this study, approximately two-thirds of in vitro metabolites should align with BioTransformer predictions or literature data.
- Mass difference filter correctly removes formulas with Δm/z > +50 u to parent; verify no valid phase I products (e.g., hydroxylation, N-oxidation, deamination) are excluded.
- Venn diagram three-way set contains non-empty exclusive regions; significant numbers of 'prediction-only' or 'literature-only' metabolites indicate gaps in in vitro incubation (e.g., missing CYP450 isoforms, insufficient incubation time, low ionization efficiency, or extraction losses).
- Literature cross-reference: metabolites from EFSA registration dossiers or MassBank should be recoverable in the 'literature' or 'literature + in vitro' categories; unexpectedly low counts suggest incomplete literature search or sample extraction artifacts.
- Individual compound coverage: at least 20 of 22 parent pesticides should yield ≥1 detected metabolite after 3-hour S9 incubation (observed in this study); lower coverage triggers investigation of compound-specific issues (e.g., poor substrate for CYP450, rapid clearance, or poor recovery).

## Limitations

- S9 liver enzyme incubation does not cover all potential or existing metabolites in vivo; some predicted metabolites may not form under in vitro conditions (e.g., tissue-specific isoforms, cofactor depletion, or competing pathways).
- Undetected predicted metabolites may result from low ionization efficiencies (especially for very hydrophilic compounds) or losses during sample extraction/cleanup, not necessarily from absent metabolic formation.
- In vitro metabolites undetected by BioTransformer tend to involve reduction reactions (dehydrogenation), consecutive hydroxylations, or weak bond breaking—processes not well-represented in machine learning training sets.
- Complete metabolite coverage between S9 incubation and BioTransformer prediction was observed only for isoproturon and triazines in this study; heterocyclic pesticides and complex structures show substantial disagreement.
- Mass difference filter (+50 u threshold) assumes phase I-only metabolism; phase II conjugation (e.g., glutathione, glucose, sulfate) will exceed this threshold and be excluded from analysis.
- Molecular formula ambiguity: multiple isomeric structures may correspond to the same molecular formula (e.g., hydroxylated regioisomers), limiting identification to formula level (*) rather than structure level (**).

## Evidence

- [methods] Overlap analysis (set intersection/union/exclusive membership) and Venn diagram visualization: "Compare predicted and experimental formula sets using set intersection, union, and exclusive elements to calculate overlap percentage and generate membership categories. Create Venn diagram"
- [methods] Experimental formula input: 91 formulas from LC–HRMS data processing: "By applying the data processing workflow, we could assign in total 91 unambiguous molecular formulas to a number of 82 prioritized features in ESI+ and 39 in ESI− for the 22 pesticides."
- [methods] Mass difference filtering to exclude formulas > parent + 50 u: "all features with a mass difference higher than +50 u to the parent compound, corresponding to an addition of three O atoms, were also not further evaluated."
- [methods] BioTransformer prediction with CYP450 transformation type: "Metabolites were predicted using BioTransformer, which combines a rule-based approach and a machine learning approach."
- [methods] Key finding: two-thirds overlap between in vitro and prediction/literature: "About two-thirds of the in vitro-metabolites were reported in the literature or predicted"
- [discussion] Incomplete metabolite coverage example: metazachlor: "For metazachlor, 12 mammalian metabolites are described in the registration dossier, but we only observed three in the incubation experiment."
- [discussion] Types of undetected predicted metabolites: "In vitro metabolites, which were not predicted, were mainly formed by reduction reactions (dehydrogenation), two consecutive hydroxylations or the breaking of a weak bond in the molecule"
- [discussion] Incomplete S9 incubation coverage vs. BioTransformer prediction: "For the other compounds, a complete overlap of metabolites in S9 incubation and prediction was only found for isoproturon and triazines."
- [readme] incubatoR workflow overview: metabolite filtering and formula annotation: "Main task is to identify metabolic transformation products in a LC-HRMS2 dataset of in-parallel incubated xenobiotic compounds by applying statistical tools as well as mass defect filtering and"
