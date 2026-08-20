---
name: molecular-fingerprint-extraction-and-vectorization
description: Use when you have annotated metabolite structures (with SMILES strings) from a reference library (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0292
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3373
  - http://edamontology.org/topic_3172
  tools:
  - GNPS
  - MIBiG
  - Chemistry Development Kit (CDK)
  - antiSMASH
  - NPLinker
  techniques:
  - LC-MS
derived_from:
- doi: 10.1101/2024.10.11.617756
  title: NPLinker
- doi: 10.1371/journal.pcbi.1008920
  title: ''
evidence_spans:
- the metabolomics data, the genomes were run through antiSMASH v5.0.0 for BGC detection and BiG-SCAPE v1.0.0 to cluster the BGCs into GCFs
- we use library MS2 spectra from the public, community-driven GNPS knowledge base [33] as a training set for the IOKR model
- To assign one or more molecular structures to BGCs, according to how many high-scoring matches are found in MIBiG
- Molecular fingerprints are extracted from SMILES strings using the Chemistry Development Kit
- Molecular fingerprints are extracted from SMILES strings using the Chemistry Development Kit [29]
- after downloading the strain assemblies and metabolomics data, the genomes were run through antiSMASH v5.0.0 for BGC detection
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_nplinker
    doi: 10.1101/2024.10.11.617756
    title: NPLinker
  dedup_kept_from: coll_nplinker
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2024.10.11.617756
  all_source_dois:
  - 10.1101/2024.10.11.617756
  - 10.1371/journal.pcbi.1008920
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# molecular-fingerprint-extraction-and-vectorization

## Summary

Extract and vectorize molecular fingerprints from chemical structures (SMILES strings) using multiple fingerprint encodings (CDK Substructure, PubChem Substructure, Klekota-Roth) to create a feature space for training kernel regression models that link spectra to molecular structures. This skill enables encoding of metabolite chemical diversity in a format compatible with spectrum-to-fingerprint regression tasks.

## When to use

You have annotated metabolite structures (with SMILES strings) from a reference library (e.g. GNPS training set with ~4138 spectra and structural annotations) and need to prepare them as training targets for a regression model that will predict chemical fingerprints from experimental MS2 spectra. Use this skill when you are constructing Input-Output Kernel Regression (IOKR) or similar kernel methods that require a vectorized molecular feature space to map spectrum kernels to fingerprint space.

## When NOT to use

- Input metabolite structures lack SMILES or InChI representations; fingerprints require parseable chemical structure notation.
- Training set size is too small (<100 metabolites with both spectra and SMILES); insufficient diversity for learning generalizable fingerprint-spectrum mappings.
- You are predicting molecular fingerprints directly from BGCs without intermediate spectrum data; IOKR requires spectrum kernels as the input space, not genomic sequences.

## Inputs

- SMILES strings (string format molecular structures)
- Annotated metabolite library with structural assignments (e.g. GNPS library with ~4138 spectra and SMILES annotations)
- Metabolite-to-spectrum pairing metadata

## Outputs

- CDK Substructure fingerprint vectors (binary/bit vectors)
- PubChem Substructure fingerprint vectors (binary/bit vectors)
- Klekota-Roth fingerprint vectors (binary/bit vectors)
- Composite multi-fingerprint feature matrix (F) ready for kernel regression training

## How to apply

For each annotated metabolite in the training library, parse the SMILES string and compute three complementary molecular fingerprint encodings using Chemistry Development Kit (CDK): CDK Substructure, PubChem Substructure, and Klekota-Roth fingerprints. Concatenate or stack these three fingerprint vectors to form a composite molecular feature representation for each metabolite. This multi-fingerprint approach provides redundancy and captures different aspects of chemical structure (functional groups, pharmacophoric features, fragment patterns), improving robustness of the downstream kernel regression model. Store these vectorized fingerprints as the target space F in the IOKR training formulation, paired with their corresponding spectrum kernel representations. The choice of multiple fingerprint types is motivated by their complementarity and is essential for the operator-valued kernel regression framework.

## Related tools

- **Chemistry Development Kit (CDK)** (Parsing SMILES strings and computing three complementary molecular fingerprint encodings (Substructure, PubChem Substructure, Klekota-Roth) from chemical structures)
- **GNPS** (Source of training library with ~4138 spectra and structural annotations (SMILES) for fingerprint extraction) — https://gnps.ucsd.edu
- **NPLinker** (Framework integrating fingerprint extraction with IOKR model training and BGC-spectrum linking) — https://github.com/NPLinker/nplinker

## Evaluation signals

- All SMILES strings parse successfully without errors in CDK and produce valid bit-vector fingerprints for all three encoding types.
- Composite fingerprint matrix has dimensionality consistent with concatenation of three CDK fingerprint types (verify row count = metabolite count, column count = 3× single fingerprint dimension).
- Fingerprint vectors are binary (0/1 values) or integer-valued as expected for bit-vector and fragment-count representations.
- Paired spectrum-fingerprint training set contains no missing values and matches the reported training set size (~4138 spectra with valid SMILES and fingerprints).
- Downstream IOKR model trained on these fingerprints achieves reported performance metrics: IOKR mean score 0.0364 for validated links vs 0.0105 for all links (p=1.7968 × 10−9), top-1 accuracy 0.1208, AUC 0.6534.

## Limitations

- IOKR fingerprint prediction is highly dependent on the choice of fingerprint types (CDK Substructure, PubChem Substructure, Klekota-Roth); different fingerprint encodings may yield substantially different performance.
- Fingerprint extraction relies on valid, unambiguous SMILES strings; incomplete or non-standard chemical notation will cause parsing failures or incorrect vectorization.
- IOKR performance is restricted to BGCs showing considerable homology with MIBiG entries (only 2242 of 3316 BGCs in the test set could be assigned structures based on MIBiG similarity), limiting applicability to novel or distant natural product classes.
- Training set includes metabolites from sources other than microbial organisms; performance on purely microbial metabolites may differ.
- The kernels used on MS2 spectra can be further optimized, suggesting that fingerprint-spectrum kernel pairing choices are not yet optimal and may benefit from alternative spectrum kernel designs.

## Evidence

- [full_text] Extract molecular fingerprints (CDK Substructure, PubChem Substructure, Klekota-Roth) from SMILES strings: "extract molecular fingerprints (CDK Substructure, PubChem Substructure, Klekota-Roth) from SMILES strings for each annotated metabolite"
- [full_text] GNPS library training set used for fingerprint source: "Load the GNPS library training set (4138 spectra with structural annotations) and extract molecular fingerprints"
- [full_text] Fingerprints as target space F in IOKR framework: "learning a mapping from the spectrum kernel space (X, with kernel K_x) to the molecular fingerprint space (F) using the training pairs"
- [abstract] Multiple fingerprint complementarity rationale: "does not directly depend on natural product compound class"
- [results] IOKR performance achieved with fingerprints: "IOKR achieves a mean score of 0.0105 for all 2966 BGC-spectrum links and 0.0364 for validated links"
- [discussion] Fingerprint dependency issue: "IOKR is also highly dependent on the choice of both kernel function and molecular fingerprints"
- [readme] README installation for chemical processing: "It requires <span style="color:red;">**~4.5GB**</span> of disk space to install all the dependencies"
