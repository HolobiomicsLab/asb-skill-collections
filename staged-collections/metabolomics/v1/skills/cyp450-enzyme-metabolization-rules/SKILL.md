---
name: cyp450-enzyme-metabolization-rules
description: Use when metabolomics involves LC-MS or GC-MS techniques to apply computational prediction of Phase I CYP450-mediated metabolite structures and molecular formulas using BioTransformer, and compare these predictions against experimentally detected metabolite formulas from LC–HRMS data.
when_to_use_negative:
- Input parent structures are missing or incomplete—BioTransformer requires valid chemical structure input.
- Experimental metabolite dataset has not been filtered for false positives (blank contamination, isotopes, adducts not removed)—apply abundance filters (>4-fold), mass defect (−100 to +50 mmu), and mass difference (<+50 u) filtering before comparison.
- Study objective is to identify phase II metabolites (conjugation, glucuronidation) rather than phase I CYP450 oxidative transformations—BioTransformer CYP450 mode is not designed for conjugation prediction.
edam_operation: http://edamontology.org/operation_3762
edam_topics:
- http://edamontology.org/topic_0154
- http://edamontology.org/topic_3172
- http://edamontology.org/topic_3407
tools:
- name: BioTransformer
  role: Predicts phase I CYP450-mediated metabolite structures and molecular formulas from parent xenobiotic structures using combined rule-based and machine learning approaches
- name: XCMS version 3.8
  role: Detects, aligns, and corrects retention time of LC–HRMS features prior to metabolite filtering and formula assignment
- name: CAMERA
  role: Componentizes features to remove isotopes and adducts, reducing false positive features before metabolite prioritization
- name: GenForm
  role: Calculates molecular formulas from MS1 accurate mass and MS2 fragmentation spectra for experimental metabolite annotation
- name: incubatoR
  role: R-based automated LC–HRMS data processing workflow integrating XCMS, CAMERA, statistical filtering, mass defect/difference filtering, and GenForm to generate prioritized experimental metabolite list for comparison with BioTransformer predictions
  repo: https://github.com/chufz/incubatoR
- name: R v 3.6.1
  role: Implements set operations (intersection, union) and visualization (Venn diagram) for predicted vs. experimental metabolite comparison
provenance:
  source_task_ids:
  - task_005
  source_papers:
  - doi: 10.1021/acs.analchem.1c00972
    title: Improving the Screening Analysis of Pesticide Metabolites in Human Biomonitoring by Combining High-Throughput <i>In Vitro</i> Incubation and Automated LC–HRMS Data Processing
schema_version: 0.2.0
derived_from:
- doi: 10.1021/acs.analchem.1c00972
metadata:
  iri: https://w3id.org/holobiomicslab/asb-skill/cyp450-enzyme-metabolization-rules@sha256:507def0dc7fae4c16a3e48f54f25bd7d7c617843830f5874cff4c6e50eee4fd3
---

# cyp450-enzyme-metabolization-rules

## Summary

Apply computational prediction of Phase I CYP450-mediated metabolite structures and molecular formulas using BioTransformer, then compare predicted metabolites against experimentally detected metabolite formulas from LC–HRMS data to validate in vitro metabolic transformation coverage and identify unmapped transformation pathways.

## When to use

When you have: (1) parent pesticide or xenobiotic structures; (2) experimentally detected metabolite molecular formulas from in vitro S9 liver microsome incubations analyzed by LC–HRMS; and (3) a need to assess whether observed metabolites match known CYP450 phase I transformations or to prioritize features for further structural elucidation by flagging predicted but undetected metabolites or experimentally detected but unpredicted metabolites (e.g., reduction, consecutive hydroxylation, or weak bond-breaking reactions).

## When NOT to use

- Input parent structures are missing or incomplete—BioTransformer requires valid chemical structure input.
- Experimental metabolite dataset has not been filtered for false positives (blank contamination, isotopes, adducts not removed)—apply abundance filters (>4-fold), mass defect (−100 to +50 mmu), and mass difference (<+50 u) filtering before comparison.
- Study objective is to identify phase II metabolites (conjugation, glucuronidation) rather than phase I CYP450 oxidative transformations—BioTransformer CYP450 mode is not designed for conjugation prediction.

## Inputs

- Parent pesticide or xenobiotic structures (SMILES or structure file)
- Experimentally detected metabolite molecular formulas from in vitro S9 incubation LC–HRMS analysis (post-filtering: abundance >4-fold, ≥2/3 replicates, mass defect −100 to +50 mmu, mass difference <+50 u)

## Outputs

- Set of predicted phase I metabolite molecular formulas from BioTransformer
- Categorized metabolite list: [in vitro & predicted], [in vitro & unpredicted], [predicted & undetected]
- Overlap percentage (e.g., ~67% overlap for these 22 pesticides)
- Venn diagram visualization of three-way metabolite comparison
- Prioritized feature list for further structural elucidation (unmapped metabolites)

## How to apply

First, input parent pesticide structures (e.g., 2,4-dichlorophenoxyacetic acid, atrazine, imidacloprid—22 compounds in this study) into BioTransformer configured with the CYP450 transformation type selector to generate predicted phase I metabolite structures and their molecular formulas. Extract and standardize the predicted molecular formula list. In parallel, obtain the experimentally assigned molecular formula dataset (e.g., 91 unambiguous formulas assigned to 82 prioritized features in ESI+ and 39 in ESI− after applying abundance filters [fold change >4, detection in ≥2 of 3 replicates], mass defect filtering [−100 to +50 mmu], and mass difference filtering [m/z <+50 u relative to parent, excluding conjugations]). Compare the two formula sets using set intersection and union operations to calculate the overlap percentage and categorize metabolites into: (a) in vitro-detected & BioTransformer-predicted (high confidence, likely phase I CYP450 transformations); (b) in vitro-detected but unpredicted (novel transformations—reduction, consecutive hydroxylations, weak bond cleavage); and (c) predicted but undetected (possible low ionization efficiency or extraction loss). Generate a Venn diagram visualization to summarize the three-way relationship (in vitro S9 metabolites, BioTransformer predictions, literature reference metabolites). Use variable filtering strictness to adapt sensitivity based on your prioritization strategy.

## Related tools

- **BioTransformer** (Predicts phase I CYP450-mediated metabolite structures and molecular formulas from parent xenobiotic structures using combined rule-based and machine learning approaches)
- **XCMS version 3.8** (Detects, aligns, and corrects retention time of LC–HRMS features prior to metabolite filtering and formula assignment)
- **CAMERA** (Componentizes features to remove isotopes and adducts, reducing false positive features before metabolite prioritization)
- **GenForm** (Calculates molecular formulas from MS1 accurate mass and MS2 fragmentation spectra for experimental metabolite annotation)
- **incubatoR** (R-based automated LC–HRMS data processing workflow integrating XCMS, CAMERA, statistical filtering, mass defect/difference filtering, and GenForm to generate prioritized experimental metabolite list for comparison with BioTransformer predictions) — https://github.com/chufz/incubatoR
- **R v 3.6.1** (Implements set operations (intersection, union) and visualization (Venn diagram) for predicted vs. experimental metabolite comparison)

## Evaluation signals

- Overlap percentage is calculated and documented (e.g., ~67% of in vitro metabolites were reported in literature or predicted by BioTransformer in this study)
- Venn diagram correctly displays three non-overlapping regions: in vitro S9 metabolites, BioTransformer predictions, and literature-reported metabolites
- Unmapped experimental metabolites are characterized by type of reaction (reduction, consecutive hydroxylation, weak bond cleavage) rather than standard CYP450 phase I pathways
- For each pesticide, the predicted formula list and experimental formula list have consistent precision and recall relative to literature reference metabolites (e.g., metazachlor: 3 of 12 literature metabolites observed in vitro; detection completeness documented)
- Mass difference filter correctly excludes features with m/z >+50 u to parent (conjugation signatures); mass defect filter correctly excludes features with defect shift <−100 or >+50 mmu

## Limitations

- In vitro S9 liver microsome incubation does not cover all potential or existing metabolites—some predicted metabolites may not form under assay conditions, and some in vivo metabolites formed by other tissue-specific enzymes or gut microbiota are missed.
- Some predicted metabolites could not be detected due to low ionization efficiencies in ESI+/ESI− modes or losses during sample extraction and cleanup; metabolite detection is ESI-ionization-mode dependent and not exhaustive.
- BioTransformer's rule-based and machine learning approaches do not predict all observed in vitro transformations—reduction reactions (dehydrogenation), consecutive hydroxylations, and weak bond breaking are underrepresented in predictions and require manual pathway annotation.
- Mass difference filtering at +50 u cutoff may exclude some oxidative metabolites or metabolites with minor additions (e.g., +O, +2O); threshold can be adjusted but involves manual validation.
- Metabolite comparison relies on molecular formula matching, not structural isomer discrimination—multiple isomers with the same formula cannot be distinguished by this workflow alone; MS2 fragmentation and library matching (e.g., via Sirius, MassBank) are required for structure confirmation.

## Evidence

- [methods] BioTransformer prediction method: "Metabolites were predicted using BioTransformer, which combines a rule-based approach and a machine learning approach."
- [methods] Overlap finding—two-thirds of in vitro metabolites: "About two-thirds of the in vitro-metabolites were reported in the literature or predicted"
- [methods] Experimental metabolite dataset size and filtering: "By applying the data processing workflow, we could assign in total 91 unambiguous molecular formulas to a number of 82 prioritized features in ESI+ and 39 in ESI− for the 22 pesticides."
- [methods] Mass difference filter cutoff rationale: "all features with a mass difference higher than +50 u to the parent compound, corresponding to an addition of three O atoms, were also not further evaluated."
- [discussion] Types of unpredicted metabolites: "In vitro metabolites, which were not predicted, were mainly formed by reduction reactions (dehydrogenation), two consecutive hydroxylations or the breaking of a weak bond in the molecule"
- [discussion] Incomplete detection for specific compounds: "For metazachlor, 12 mammalian metabolites are described in the registration dossier, but we only observed three in the incubation experiment."
- [discussion] Possible detection loss mechanisms: "Some might have been formed but could not have been detected due to low ionization efficiencies. Also, losses during the sample extraction and cleanup procedure are possible"
- [readme] Workflow purpose—incubatoR README: "Main task is to identify metabolic transformation products in a LC-HRMS2 dataset of in-parallel incubated xenobiotic compounds by applying statistical tools as well as mass defect filtering"
- [methods] Abundance and replication filter parameters: "We used a generic cutoff value of >4 for the fold change and kept only the features that were detected in at least two of three replicates"
- [methods] Mass defect filter parameters: "For mass defect filtering, features with a mass defect shift of <−100 and >+50 mmu were removed."
