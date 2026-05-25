---
name: metabolite-structure-prediction-biotransformer
description: "Use BioTransformer to generate predicted phase I metabolite structures and molecular formulas for parent xenobiotics, then compare predicted formulas against experimentally detected molecular formulas from LC–HRMS data to assess metabolic coverage and identify experimentally detected metabolites supported by in silico prediction."
when_to_use_negative: |
  - "Input experimental metabolites have not yet been assigned unambiguous molecular formulas (e.g., formulas are ambiguous or missing); formula assignment must precede prediction comparison."
  - "Parent compound structures are unavailable or poorly defined; BioTransformer requires valid chemical structures as input."
  - "The analysis goal is to identify phase II metabolites (e.g., conjugation products with glutathione or glucuronic acid) without modification of BioTransformer parameters; the default CYP450 setting targets phase I oxidative transformations and may not fully capture subsequent phase II modifications."
edam_operation: "http://edamontology.org/operation_3802"
edam_topics: |
  - "http://edamontology.org/topic_0625"
  - "http://edamontology.org/topic_3407"
tools: |
  - name: "BioTransformer"
  role: "Predicts phase I metabolite structures and molecular formulas from parent xenobiotic structures using rule-based and machine learning approaches; serves as the reference prediction set for comparison against experimental detections."
  - name: "GenForm"
  role: "Calculates molecular formulas from MS1 and MS2 spectra; generates the experimental formula dataset used for comparison against BioTransformer predictions."
  - name: "XCMS version 3.8"
  role: "Performs feature detection, alignment, and retention time correction on LC–HRMS data; upstream step that produces the feature list requiring formula assignment."
  - name: "CAMERA"
  role: "Componentizes all features (isotopes, adducts) after XCMS processing; refines the feature list before molecular formula calculation and metabolite filtering."
  - name: "R v 3.6.1"
  role: "Scripting environment (incubatoR workflow) for set-based comparison of predicted and experimental formula sets, visualization of Venn diagrams, and statistical analysis of metabolite overlap."
  repo: "https://github.com/chufz/incubatoR"
provenance: |
  source_task_ids:
  - task_005
  source_papers:
  - doi: "10.1021/acs.analchem.1c00972"
  title: "Improving the Screening Analysis of Pesticide Metabolites in Human Biomonitoring by Combining High-Throughput <i>In Vitro</i> Incubation and Automated LC–HRMS Data Processing"
schema_version: "0.2.0"
metadata:
  iri: https://w3id.org/holobiomicslab/asb-skill/metabolite-structure-prediction-biotransformer@sha256:e9ca45bfa5a2633eb7f766f1d08def85adad336c9067a36890024f5f62ada448
---

# metabolite-structure-prediction-biotransformer

## Summary

Use BioTransformer to generate predicted phase I metabolite structures and molecular formulas for parent xenobiotics, then compare predicted formulas against experimentally detected molecular formulas from LC–HRMS data to assess metabolic coverage and identify experimentally detected metabolites supported by in silico prediction.

## When to use

After experimental detection and molecular formula assignment of metabolites from LC–HRMS incubation studies (e.g., from S9 liver enzyme assays), when you need to validate which detected metabolites are plausible according to known metabolic biotransformation rules, or to identify gaps between experimental detection and predicted metabolic pathways for xenobiotic compounds such as pesticides.

## When NOT to use

- Input experimental metabolites have not yet been assigned unambiguous molecular formulas (e.g., formulas are ambiguous or missing); formula assignment must precede prediction comparison.
- Parent compound structures are unavailable or poorly defined; BioTransformer requires valid chemical structures as input.
- The analysis goal is to identify phase II metabolites (e.g., conjugation products with glutathione or glucuronic acid) without modification of BioTransformer parameters; the default CYP450 setting targets phase I oxidative transformations and may not fully capture subsequent phase II modifications.

## Inputs

- Parent pesticide structures (SMILES, InChI, or molecular structure format)
- Experimental molecular formula dataset (molecular formulas assigned to detected features from LC–HRMS, prioritized using mass defect filtering and abundance thresholds)
- Feature metadata including m/z values, retention times, and fold-change statistics relative to blanks

## Outputs

- BioTransformer predicted metabolite structures and molecular formulas
- Set-based comparison results (overlap percentage, membership categories)
- Venn diagram or table showing three-way intersection of in vitro, predicted, and literature metabolites
- List of observed metabolites not predicted by BioTransformer (e.g., those arising from reduction, consecutive hydroxylation, or weak bond breaking)
- List of predicted metabolites not experimentally detected

## How to apply

First, obtain parent pesticide structures (SMILES or InChI) for the 22 or more compounds under study. Execute BioTransformer with CYP450 transformation type selection to generate predicted phase I metabolite structures and their corresponding molecular formulas. Extract and standardize the predicted molecular formulas into a set-based format. Load the experimental molecular formula dataset (e.g., 91 unambiguous formulas assigned to 82 prioritized features in ESI+ and 39 in ESI− from your LC–HRMS processing workflow). Compare the two formula sets using set intersection, union, and exclusive element analysis to calculate the percentage overlap and categorize each detected metabolite as: (1) observed and predicted, (2) observed but not predicted, or (3) predicted but not observed. Generate a Venn diagram or membership table showing the three-way relationship between in vitro S9-incubated metabolites, BioTransformer predictions, and (optionally) literature metabolites from EFSA registration dossiers.

## Related tools

- **BioTransformer** (Predicts phase I metabolite structures and molecular formulas from parent xenobiotic structures using rule-based and machine learning approaches; serves as the reference prediction set for comparison against experimental detections.)
- **GenForm** (Calculates molecular formulas from MS1 and MS2 spectra; generates the experimental formula dataset used for comparison against BioTransformer predictions.)
- **XCMS version 3.8** (Performs feature detection, alignment, and retention time correction on LC–HRMS data; upstream step that produces the feature list requiring formula assignment.)
- **CAMERA** (Componentizes all features (isotopes, adducts) after XCMS processing; refines the feature list before molecular formula calculation and metabolite filtering.)
- **R v 3.6.1** (Scripting environment (incubatoR workflow) for set-based comparison of predicted and experimental formula sets, visualization of Venn diagrams, and statistical analysis of metabolite overlap.) — https://github.com/chufz/incubatoR

## Evaluation signals

- Approximately two-thirds or higher of in vitro-detected metabolites should be explained by either BioTransformer predictions or literature reports; lower overlap suggests incomplete metabolite detection or prediction limitations.
- Venn diagram membership categories should be balanced: verify that the number of observed-and-predicted metabolites is substantially greater than the number of observed-but-not-predicted or predicted-but-not-observed metabolites, indicating reasonable model performance.
- Detected metabolites not predicted by BioTransformer should be manually reviewed for metabolic plausibility; common unexplained pathways include reduction reactions (dehydrogenation), consecutive hydroxylations, or weak bond breaking.
- Compare the overlap for different compound classes (e.g., triazines vs. neonicotinoids); complete prediction overlap should be rare except for well-characterized compounds like isoproturon and triazines.
- Cross-reference observed metabolites against EFSA registration dossiers or peer-reviewed literature; for compounds with known mammalian metabolites (e.g., fipronil, metazachlor), verify that the proportion of literature metabolites detected in the S9 incubation is consistent with reported bioavailability and ionization efficiency.

## Limitations

- In vitro S9 incubation does not cover all potential or existing metabolites; some predicted metabolites may be formed but not detected due to low ionization efficiencies or losses during sample extraction and cleanup.
- BioTransformer does not predict all metabolic transformations observed in vitro, particularly reduction reactions, consecutive hydroxylations, and weak bond breaking; these pathways require manual curation or custom rule addition.
- For some pesticides (e.g., metazachlor), only a fraction of registered mammalian metabolites are detected in the S9 assay (3 of 12 observed); this reflects limitations of the in vitro model, not necessarily the prediction tool.
- Molecular formula alone does not establish metabolite identity; multiple isomers may share the same formula, and structure elucidation requires additional MS/MS fragmentation data and comparison to reference standards or spectral databases.
- Complete overlap between S9-incubated metabolites and BioTransformer predictions is found only for a subset of compounds (e.g., isoproturon, triazines); generalization of predictive performance across diverse pesticide classes is limited.

## Evidence

- [methods] Metabolites were predicted using BioTransformer, which combines a rule-based approach and a machine learning approach.: "Metabolites were predicted using BioTransformer,35 which combines a rule-based approach and a machine learning approach."
- [methods] About two-thirds of the in vitro-metabolites were reported in the literature or predicted by BioTransformer.: "About two-thirds of the in vitro-metabolites were reported in the literature or predicted"
- [methods] By applying the data processing workflow, we could assign in total 91 unambiguous molecular formulas to a number of 82 prioritized features in ESI+ and 39 in ESI− for the 22 pesticides.: "By applying the data processing workflow, we could assign in total 91 unambiguous molecular formulas to a number of 82 prioritized features in ESI+ and 39 in ESI− for the 22 pesticides."
- [discussion] A comparison with the literature data and metabolization prediction showed that the S9 incubation does not cover all potential or existing metabolites.: "A comparison with the literature data and metabolization prediction showed that the S9 incubation does not cover all potential or existing metabolites."
- [discussion] In vitro metabolites, which were not predicted, were mainly formed by reduction reactions (dehydrogenation), two consecutive hydroxylations or the breaking of a weak bond in the molecule: "In vitro metabolites, which were not predicted, were mainly formed by reduction reactions (dehydrogenation), two consecutive hydroxylations or the breaking of a weak bond in the molecule"
- [discussion] For metazachlor, 12 mammalian metabolites are described in the registration dossier, but we only observed three in the incubation experiment.: "For metazachlor, 12 mammalian metabolites are described in the registration dossier, but we only observed three in the incubation experiment."
- [methods] The corresponding molecular formula was calculated using the GenForm33 command line tool.: "The corresponding molecular formula was calculated using the GenForm33 command line tool."
