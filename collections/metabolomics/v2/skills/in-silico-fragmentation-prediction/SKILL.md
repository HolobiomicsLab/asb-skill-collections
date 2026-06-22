---
name: in-silico-fragmentation-prediction
description: Use when you have candidate metabolite structures (from database lookup or enumeration) and experimental MS/MS spectra (mzML, mzXML format), and need to rank candidates by how well their predicted fragments match observed peaks.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3172
  tools:
  - MAGMa
  - PubChem
derived_from:
- doi: 10.5702/massspectrometry.S0033
  title: magma
evidence_spans:
- MAGMa is a abbreviation for 'Ms Annotation based on in silico Generated Metabolites'.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_magma_cq
    doi: 10.5702/massspectrometry.S0033
    title: magma
  dedup_kept_from: coll_magma_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.5702/massspectrometry.S0033
  all_source_dois:
  - 10.5702/massspectrometry.S0033
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# in-silico-fragmentation-prediction

## Summary

Predict theoretical fragment ion masses and intensities for candidate metabolite structures to enable scoring and ranking of metabolite annotations against experimental tandem MS/MS spectra. This skill bridges chemical structure space with MS/MS data by simulating fragmentation patterns, essential for high-throughput metabolite identification in metabolomics workflows.

## When to use

You have candidate metabolite structures (from database lookup or enumeration) and experimental MS/MS spectra (mzML, mzXML format), and need to rank candidates by how well their predicted fragments match observed peaks. Use this when a molecular formula or parent mass has yielded multiple plausible metabolites and you must discriminate among them via fragment-level evidence.

## When NOT to use

- Input is a single, unambiguous metabolite structure already confirmed by orthogonal methods (NMR, standard reference); fragmentation prediction adds no discriminatory value.
- Experimental MS/MS spectrum is of low quality (low signal-to-noise, missing major fragments) or acquired under non-standard conditions (unusual collision energy, uncommon ionization mode); predicted fragments may not match due to instrumental factors, not poor structure assignment.
- Candidate pool is empty or very small (e.g., one structure); ranking and comparative scoring require multiple plausible alternatives to be meaningful.

## Inputs

- Candidate metabolite structures (SMILES, InChI, or molecular graph format)
- Experimental MS/MS spectrum (mzML, mzXML, or similar format with m/z and intensity pairs)
- Parent mass or molecular formula
- Fragmentation rule set (e.g., bond dissociation energies, neutral loss patterns)

## Outputs

- Ranked list of candidate metabolites with annotation scores
- Match statistics for each candidate (number of matched peaks, cosine similarity or peak-matching score)
- Theoretical fragment ion m/z and intensity for top-ranked candidates
- Confidence metrics for the best-matching metabolite

## How to apply

For each candidate metabolite structure, apply fragmentation rules (bond cleavage, rearrangement, neutral loss) to enumerate all theoretically possible fragment ions and their m/z values. Calculate the intensity or probability of each fragment based on chemical stability and prevalence in similar compounds. Compare the resulting theoretical fragment ion list against the experimental MS/MS spectrum by computing a peak-matching score (e.g., cosine similarity or count of matched peaks within mass tolerance). Rank all candidates by annotation score and output the ranked list with match statistics (number of matched peaks, score magnitude, mass accuracy). The rationale is that true metabolite identities will produce fragment spectra with high overlap to experimental data, whereas false candidates will show poor peak alignment.

## Related tools

- **MAGMa** (Executes in silico metabolite structure generation, fragmentation rule application, and cosine similarity scoring of theoretical vs. experimental MS/MS spectra) — https://github.com/NLeSC/MAGMa
- **PubChem** (Provides candidate metabolite structures and chemical properties used as input to fragmentation prediction)

## Evaluation signals

- Top-ranked candidate metabolite matches a reference standard or is confirmed by orthogonal structural analysis (NMR, HRMS exact mass).
- Cosine similarity or peak-matching score between predicted and experimental MS/MS spectra is ≥ 0.7 for the correct metabolite and < 0.5 for false positives.
- Number of matched fragment peaks (within specified mass tolerance, e.g., ±0.01 m/z or ±5 ppm) is high (>60% of experimental peaks) for the true metabolite and low for decoys.
- Ranked output includes match statistics and fragment assignments that are biologically plausible (e.g., neutral losses match known functional groups in the candidate structure).
- Fragmentation predictions are consistent across independent runs and do not depend on arbitrary parameter choices (e.g., fragmentation energy thresholds).

## Limitations

- Fragmentation rule accuracy depends on the completeness and domain-specificity of the rule set; uncommon or novel fragmentation patterns may not be captured.
- In silico predictions assume standard MS/MS acquisition conditions; non-standard collision energies, ion mobility separation, or unusual ionization modes may produce spectra that deviate from predictions.
- Ranking by cosine similarity or peak-matching alone may fail when multiple structurally similar metabolites (isomers, homologs) produce overlapping fragment patterns.
- Computational cost scales with the number of candidate structures and spectral complexity; large-scale metabolomics studies may require filtering or prioritization before fragmentation prediction.

## Evidence

- [other] Generate in silico metabolite structures using PubChem database lookup or chemical structure enumeration.: "Generate in silico metabolite structures using PubChem database lookup or chemical structure enumeration."
- [other] Calculate theoretical fragment ions for each candidate metabolite via fragmentation rules.: "Calculate theoretical fragment ions for each candidate metabolite via fragmentation rules."
- [other] Score each candidate by comparing experimental MS/MS peaks against theoretical fragments using cosine similarity or peak-matching algorithm.: "Score each candidate by comparing experimental MS/MS peaks against theoretical fragments using cosine similarity or peak-matching algorithm."
- [readme] MAGMa is a abbreviation for 'Ms Annotation based on in silico Generated Metabolites'.: "MAGMa is a abbreviation for 'Ms Annotation based on in silico Generated Metabolites'."
- [readme] The project develops chemo-informatics based methods for metabolite identification and biochemical network reconstruction in an integrative metabolomics data analysis workflow.: "The project develops chemo-informatics based methods for metabolite identification and biochemical network reconstruction in an integrative metabolomics data analysis workflow."
