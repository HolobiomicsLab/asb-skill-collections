---
name: phase-i-transformation-biotransformation-pathways
description: "Predict and validate phase I metabolite structures and molecular formulas for xenobiotic compounds (pesticides) using rule-based and machine-learning biotransformation prediction, then compare predictions against experimentally detected metabolites from LC–HRMS analysis of in vitro S9 liver microsome incubations. This skill bridges computational metabolite prediction with high-throughput experimental screening to identify which phase I transformations are physiologically relevant."
when_to_use_negative: |
  - "Input features already labeled with phase II or conjugation modifications (e.g., glucuronides, sulfates); phase I prediction is orthogonal to these."
  - "Parent compounds are already Phase I metabolites (secondary substrates); prediction is most reliable for intact parent structures."
  - "Experimental dataset lacks sufficient molecular formula assignments or has >20% ambiguous features; low-confidence formula sets will inflat false-negative and false-positive rates."
edam_operation: "http://edamontology.org/operation_3802"
edam_topics: |
  - "http://edamontology.org/topic_0602"
  - "http://edamontology.org/topic_3172"
  - "http://edamontology.org/topic_3375"
tools: |
  - name: "BioTransformer"
  role: "Predict phase I metabolite structures and molecular formulas from parent xenobiotic structures using rule-based and machine-learning biotransformation rules"
  - name: "XCMS version 3.8"
  role: "Feature detection, alignment, and retention time correction on raw LC–HRMS data prior to formula assignment"
  - name: "CAMERA"
  role: "Componentize detected features to group isotopes and adducts, improving feature-level annotation accuracy"
  - name: "GenForm"
  role: "Calculate molecular formulas from MS1 and MS2 spectra for experimental features"
  - name: "ProteoWizard v3.0.18265"
  role: "Convert raw vendor mass spectra to mzML format and centroid; prerequisite for XCMS feature detection"
  - name: "Sirius version 4.4.27"
  role: "Structure elucidation via in silico fragmentation and molecular fingerprint prediction for confirmed metabolites (post-overlap analysis)"
  - name: "R v 3.6.1 (incubatoR package)"
  role: "Automated workflow orchestration for feature filtering, statistical comparison, mass defect filtering, EIC extraction, MSMS processing, and overlap analysis"
  repo: "https://github.com/chufz/incubatoR"
provenance: |
  source_task_ids:
  - task_005
  source_papers:
  - doi: "10.1021/acs.analchem.1c00972"
  title: "Improving the Screening Analysis of Pesticide Metabolites in Human Biomonitoring by Combining High-Throughput <i>In Vitro</i> Incubation and Automated LC–HRMS Data Processing"
schema_version: "0.2.0"
metadata:
  iri: https://w3id.org/holobiomicslab/asb-skill/phase-i-transformation-biotransformation-pathways@sha256:58b13e2c6e9728ade1f22d406faa887492668583e5394066c3c7cda21ed9f5d0
---

# phase-i-transformation-biotransformation-pathways

## Summary

Predict and validate phase I metabolite structures and molecular formulas for xenobiotic compounds (pesticides) using rule-based and machine-learning biotransformation prediction, then compare predictions against experimentally detected metabolites from LC–HRMS analysis of in vitro S9 liver microsome incubations. This skill bridges computational metabolite prediction with high-throughput experimental screening to identify which phase I transformations are physiologically relevant.

## When to use

Apply this skill when you have (1) a set of parent xenobiotic structures (e.g., pesticides, drugs), (2) experimental LC–HRMS metabolite data from in vitro S9 incubation assays with assigned molecular formulas, and (3) a goal to identify which predicted phase I metabolites actually occur in vitro or are reported in literature. Use it to prioritize detected features as true metabolites versus artifacts, and to assess coverage of in vitro systems (e.g., 'does 3 h S9 incubation detect all expected mammalian metabolites?').

## When NOT to use

- Input features already labeled with phase II or conjugation modifications (e.g., glucuronides, sulfates); phase I prediction is orthogonal to these.
- Parent compounds are already Phase I metabolites (secondary substrates); prediction is most reliable for intact parent structures.
- Experimental dataset lacks sufficient molecular formula assignments or has >20% ambiguous features; low-confidence formula sets will inflat false-negative and false-positive rates.

## Inputs

- Parent compound structures (SMILES, InChI, or structure files for xenobiotics)
- BioTransformer-generated phase I metabolite structures and molecular formulas
- Experimentally assigned molecular formulas from LC–HRMS feature detection (91 unambiguous formulas assigned to 82 ESI+ and 39 ESI− features)
- Mass spectrometry metadata: parent m/z, retention time, fold-change and replication info
- Literature metabolite records (registration dossiers, peer-reviewed data)

## Outputs

- Set of predicted phase I metabolite molecular formulas (from BioTransformer)
- Set of experimentally detected metabolite molecular formulas (from filtered feature list)
- Intersection, union, and exclusive sets (predicted-only, experimental-only, literature-only, overlap)
- Overlap quantification: percentage match (e.g., ~67% of in vitro metabolites in predictions or literature)
- Venn diagram or tabular classification of each feature (structure ID if available, molecular formula, MS level, identification level [** or *], phase I modification type, source: S9/Pred/Lit)
- List of false negatives (predicted but not detected; possible reasons: low ionization, hydrophilicity, extraction loss)
- List of false positives (detected but not predicted; e.g., unexpected reaction pathways)

## How to apply

First, execute BioTransformer with CYP450 (phase I) transformation rules on the parent structures to generate predicted metabolite structures and their corresponding molecular formulas. Second, extract and standardize molecular formulas from both BioTransformer output and your experimental feature list (after applying mass difference filtering: e.g., reject features m/z > parent + 50 u, which correspond to conjugation products outside phase I scope). Third, perform set intersection and union of predicted formulas versus experimental formulas to quantify overlap. Fourth, cross-reference unmatched experimental metabolites and undetected predictions against literature (e.g., EFSA registration dossiers, peer-reviewed studies) to classify each feature as 'literature-supported', 'BioTransformer-predicted', 'in vitro-only', or 'false positive'. Use a Venn diagram to visualize three-way overlap (S9 metabolites, predictions, literature). Rationale: phase I reactions (hydroxylation, N-oxidation, dehydrogenation, ester cleavage) follow predictable rules, but in vitro systems (S9) do not always express all CYP450 isoforms or may lose highly hydrophilic or volatile products; comparing predictions to experiments reveals system gaps and confirms metabolic relevance.

## Related tools

- **BioTransformer** (Predict phase I metabolite structures and molecular formulas from parent xenobiotic structures using rule-based and machine-learning biotransformation rules)
- **XCMS version 3.8** (Feature detection, alignment, and retention time correction on raw LC–HRMS data prior to formula assignment)
- **CAMERA** (Componentize detected features to group isotopes and adducts, improving feature-level annotation accuracy)
- **GenForm** (Calculate molecular formulas from MS1 and MS2 spectra for experimental features)
- **ProteoWizard v3.0.18265** (Convert raw vendor mass spectra to mzML format and centroid; prerequisite for XCMS feature detection)
- **Sirius version 4.4.27** (Structure elucidation via in silico fragmentation and molecular fingerprint prediction for confirmed metabolites (post-overlap analysis))
- **R v 3.6.1 (incubatoR package)** (Automated workflow orchestration for feature filtering, statistical comparison, mass defect filtering, EIC extraction, MSMS processing, and overlap analysis) — https://github.com/chufz/incubatoR

## Evaluation signals

- Overlap percentage matches literature values: ~67% of in vitro-detected metabolites should be reported in literature or predicted by BioTransformer (as reported for 22 pesticides in this study).
- False-negative classification is documented: features predicted by BioTransformer but not detected should be traceable to known limitations (e.g., low ionization efficiency, hydrophilicity, extraction loss, missing CYP450 isoforms in S9).
- Mass difference filter applied correctly: all experimental features with m/z > parent + 50 u are excluded (these correspond to phase II conjugation, not phase I).
- Molecular formula sets are unambiguous: 91 unambiguous formulas assigned (no multiply-matched features); formulas should satisfy GenForm acceptance thresholds (MS1 ≤8 ppm, MS2 fragments within ±8 ppm or ±15 rejection).
- Three-way Venn diagram is reproducible and consistent: expected pattern shows partial overlap (complete overlap only observed for isoproturon and triazines; metazachlor shows 3 of 12 registered metabolites; fipronil shows 1 of 6 rat urine metabolites).

## Limitations

- S9 liver microsome incubation does not cover all potential or existing metabolites; some predicted transformations require specific CYP450 isoforms absent or under-expressed in S9 (e.g., CYP2D6, CYP3A4 variants).
- Predicted metabolites may not be detected due to low ionization efficiencies (especially for very hydrophilic or large conjugates), losses during sample extraction and cleanup, or rapid further metabolism (secondary phase I/II).
- Incomplete metabolite detection for some compounds: metazachlor shows only 3 of 12 mammalian metabolites described in EFSA registration dossier; fipronil shows only fipronil-sulfone despite six metabolites reported in rat urine—in vitro assay coverage is incomplete.
- In vitro metabolites not predicted by BioTransformer include reduction reactions (dehydrogenation), consecutive hydroxylations, and weak bond breakage; rule-based prediction may miss these less common phase I pathways.
- Molecular formula alone does not assign structure: identification is only at formula level (*) unless MS/MS fragmentation pattern matches reference library or in silico prediction (Sirius); multiple isomers may share the same formula.
- Standard impurities from pesticide reference materials can contaminate the metabolite feature list; must compare incubated sample features to pure standard measured at same concentration to remove impurities and adducts.

## Evidence

- [methods] About two-thirds of the in vitro-metabolites were reported in the literature or predicted: "About two-thirds of the in vitro-metabolites were reported in the literature or predicted"
- [methods] By applying the data processing workflow, we could assign in total 91 unambiguous molecular formulas to a number of 82 prioritized features in ESI+ and 39 in ESI−: "By applying the data processing workflow, we could assign in total 91 unambiguous molecular formulas to a number of 82 prioritized features in ESI+ and 39 in ESI−"
- [methods] Metabolites were predicted using BioTransformer, which combines a rule-based approach and a machine learning approach.: "Metabolites were predicted using BioTransformer, which combines a rule-based approach and a machine learning approach."
- [methods] Features with an m/z value >+50 mu to the parent pesticide were removed since they are more likely to occur from conjugation: "Features with an m/z value >+50 mu to the parent pesticide were removed since they are more likely to occur from conjugation"
- [discussion] A comparison with the literature data and metabolization prediction showed that the S9 incubation does not cover all potential or existing metabolites.: "A comparison with the literature data and metabolization prediction showed that the S9 incubation does not cover all potential or existing metabolites."
- [discussion] For metazachlor, 12 mammalian metabolites are described in the registration dossier, but we only observed three in the incubation experiment.: "For metazachlor, 12 mammalian metabolites are described in the registration dossier, but we only observed three in the incubation experiment."
- [discussion] Some might have been formed but could not have been detected due to low ionization efficiencies...Also, losses during the sample extraction and cleanup procedure are possible: "Some might have been formed but could not have been detected due to low ionization efficiencies...Also, losses during the sample extraction and cleanup procedure are possible"
- [discussion] In vitro metabolites, which were not predicted, were mainly formed by reduction reactions (dehydrogenation), two consecutive hydroxylations or the breaking of a weak bond in the molecule: "In vitro metabolites, which were not predicted, were mainly formed by reduction reactions (dehydrogenation), two consecutive hydroxylations or the breaking of a weak bond in the molecule"
- [readme] Main task is to identify metabolic transformation products in a LC-HRMS2 dataset of in-parallel incubated xenobiotic compounds by applying statistical tools as well as mass defect filtering: "Main task is to identify metabolic transformation products in a LC-HRMS2 dataset of in-parallel incubated xenobiotic compounds by applying statistical tools as well as mass defect filtering"
- [discussion] The individual filtering steps provided in this workflow can be adapted for a more or less strict prioritization of features: "The individual filtering steps provided in this workflow can be adapted for a more or less strict prioritization of features"
