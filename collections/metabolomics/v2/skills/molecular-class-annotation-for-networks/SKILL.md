---
name: molecular-class-annotation-for-networks
description: Use when after molecular formulas have been assigned to detected peaks (via CoreMS, Formularity, or equivalent) and you are constructing biochemical transformation networks where node interpretation requires understanding what chemical classes are being transformed.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0599
  tools:
  - MetaboDirect
  - Python (NumPy, pandas)
  - R (vegan package)
  - Cytoscape
  - CoreMS
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1186/s40168-023-01476-3
  title: MetaboDirect
evidence_spans:
- Molecular transformation networks for each sample (mass difference network-based approach) are generated in this step
- The MetaboDirect pipeline consists of 6 major steps/categories (Fig. 1)
- The MetaboDirect pipeline was developed in Python 3.8 and requires the Python dependencies NumPy, pandas
- developed in Python 3.8 [38] and R 4.0.2 [39]
- Networks are then constructed using Cytoscape and colored based on their molecular class
- Networks are then constructed using Cytoscape [79] and colored based on their molecular class.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metabodirect_cq
    doi: 10.1186/s40168-023-01476-3
    title: MetaboDirect
  dedup_kept_from: coll_metabodirect_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s40168-023-01476-3
  all_source_dois:
  - 10.1186/s40168-023-01476-3
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# molecular-class-annotation-for-networks

## Summary

Assign molecular class labels (e.g., lipids, proteins, carbohydrates, lignin) to detected masses in FT-ICR MS samples based on their elemental composition, enabling chemical interpretation of biochemical transformation networks. This annotation step bridges raw mass assignments to biologically meaningful compound categories within network nodes.

## When to use

After molecular formulas have been assigned to detected peaks (via CoreMS, Formularity, or equivalent) and you are constructing biochemical transformation networks where node interpretation requires understanding what chemical classes are being transformed. Use this skill when your goal is to label network nodes with compound class information for visualization, hub identification, or pathway interpretation in Cytoscape.

## When NOT to use

- Input peaks lack assigned molecular formulas or have formula assignment error > 0.5 ppm; annotation requires confident elemental composition.
- Your goal is to identify *unknown* compounds without reference class definitions; this skill applies only to classification against known compound classes.
- Data are already in a high-level aggregated form (e.g., pathway or gene expression) where mass-based molecular class inference is not appropriate.

## Inputs

- Pre-processed CSV containing peak m/z values, detected in a single sample
- Molecular formula assignments for each peak (C, H, N, O, S elemental counts)
- Molecular class reference key (mapping elemental composition to classes)

## Outputs

- Node table (CSV) with columns: peak m/z, molecular formula, molecular class
- Annotated network nodes ready for import into Cytoscape with class labels

## How to apply

For each filtered peak in the sample, extract its assigned molecular formula (C, H, N, O, S counts). Apply a classification algorithm that maps elemental composition ratios (e.g., O/C, H/C, N/C) and known structural thresholds to predefined molecular classes (lipids, sugars, amino acids, lignin, etc.). The MetaboDirect pipeline determines compound classes based on the assigned molecular formula according to reference criteria; these classifications are then propagated to the node table exported for network visualization. Store the class assignment in a node attribute table (CSV) with columns: peak m/z, molecular formula, and molecular class. This allows downstream tools like Cytoscape to color or filter network nodes by class, revealing which chemical families dominate transformations or serve as network hubs.

## Related tools

- **MetaboDirect** (Automates molecular class determination from assigned molecular formulas during pipeline preprocessing; generates node tables with class annotations for network export.) — https://github.com/Coayala/MetaboDirect
- **CoreMS** (Upstream tool that provides the molecular formula assignments consumed by the classification step; open-source framework for signal processing and formula assignment.)
- **Cytoscape** (Visualization and analysis platform that imports the annotated node table and uses molecular class attributes for node coloring, filtering, and visual interpretation of transformation networks.)

## Evaluation signals

- Every peak in the node table has a non-null molecular class assignment; no peaks remain unclassified.
- Assigned classes are confined to the predefined reference set (lipids, sugars, amino acids, lignin, etc.); no spurious or out-of-vocabulary classes appear.
- Elemental composition distributions by class align with known biochemical expectations (e.g., lipids have low O/C ratios, carbohydrates have O/C ~ 1).
- Network hubs identified by degree show consistent class profiles (e.g., if a lipid class dominates hub nodes, this aligns with sample biology).
- Node table imports cleanly into Cytoscape without schema errors; class attribute is available for visual encoding (e.g., node color mapping).

## Limitations

- FT-ICR MS cannot distinguish chemical isomers; multiple isomers with identical molecular formulas receive the same class assignment, potentially masking structural diversity within a class.
- Classification relies on reference keys; novel or unannotated molecular structures will be misclassified or left unclassified if not covered by the reference.
- Ion suppression or enhancement effects can bias detected peak distributions toward certain chemical classes, leading to biased class abundance estimates in the network.
- Ambiguous elemental compositions (e.g., mixtures of isobars at the mass resolution limit) may result in incorrect formula and thus incorrect class assignment.

## Evidence

- [methods] Compound classes of each of the filtered peaks are then determined based on the assigned molecular formula: "Compound classes of each of the filtered peaks are then determined based on the assigned molecular formula"
- [other] Generate node table (CSV) with all peaks present in the sample and their molecular class assignments.: "Generate node table (CSV) with all peaks present in the sample and their molecular class assignments"
- [intro] can detect a wide range of compounds (e.g., lipids, sugars, amino acids, or lignin): "can detect a wide range of compounds (e.g., lipids, sugars, amino acids, or lignin)"
- [other] Export edge and node tables formatted for import into Cytoscape: "Export edge and node tables formatted for import into Cytoscape"
