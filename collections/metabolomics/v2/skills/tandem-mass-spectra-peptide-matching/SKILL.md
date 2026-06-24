---
name: tandem-mass-spectra-peptide-matching
description: Use when you have centroided LC-MS/MS spectra (in MGF, mzXML, mzML, or
  mzData format) and wish to identify peptidic natural products or ribosomally synthesized
  and post-translationally modified peptides (RiPPs) against a known structure database
  or custom RiPP structure database.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3631
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - NPDtools 2.5.0
  - MetaMiner
  - Dereplicator
  - ProteoWizard
  - Python
  - VarQuest
  - Dereplicator+
  - ProteoWizard msconvert
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1038/s41467-018-06082-8
  title: dereplicator
evidence_spans:
- The latest version is available in the Natural Product Discovery toolkit (NPDtools)
  at https://github.com/ablab/npdtools
- MetaMiner is a metabologenomic pipeline which integrates metabolomic (tandem mass
  spectra) and genomic data to identify novel RiPPs
- MetaMiner is a metabologenomic pipeline which integrates metabolomic (tandem mass
  spectra) and genomic data to identify novel Ribosmally synthesized and Post-translationally
  modified Peptides (RiPPs)
- matches tandem mass spectra against the constructed post-translationally modified
  RiPPs structure database using Dereplicator
- MetaMiner natively supports MGF, mzXML, mzData and uses msconvert utility from the
  ProteoWizard package to convert spectra in other formats to MGF
- uses msconvert utility from the ProteoWizard package to convert spectra in other
  formats to MGF
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_dereplicator
    doi: 10.1038/s41467-018-06082-8
    title: dereplicator
  dedup_kept_from: coll_dereplicator
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-018-06082-8
  all_source_dois:
  - 10.1038/s41467-018-06082-8
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# tandem-mass-spectra-peptide-matching

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Match centroided tandem mass spectra (MS/MS) against peptidic natural product (PNP) structure databases using Dereplicator, VarQuest, or Dereplicator+ to identify known or novel peptidic metabolites with quantified confidence scores and false discovery rates. This skill enables dereplication and variant detection across multiple search modes.

## When to use

You have centroided LC-MS/MS spectra (in MGF, mzXML, mzML, or mzData format) and wish to identify peptidic natural products or ribosomally synthesized and post-translationally modified peptides (RiPPs) against a known structure database or custom RiPP structure database. Use this skill when you need to compare hit patterns across multiple database search pipelines, detect modification-tolerant variants, or generate significant_matches.tsv outputs with scan identifiers, match scores, and p-values for downstream cross-validation.

## When NOT to use

- Input spectra are not centroided or are in unsupported binary formats without conversion capability
- Your goal is to identify non-peptidic metabolites and you do not have access to Dereplicator+ (use Dereplicator+ instead of Dereplicator or VarQuest alone)
- You lack a suitable structure database or RiPP reference set tailored to your organism/sample type

## Inputs

- centroided LC-MS/MS spectra files (MGF, mzXML, mzML, or mzData format)
- chemical structure database of known natural products (for Dereplicator, VarQuest, Dereplicator+)
- RiPP structure database (for MetaMiner)
- optional: RiPP sequence file (FASTA format) for MetaMiner

## Outputs

- significant_matches.tsv (tab-separated file with scan identifiers, match scores, p-values, and false discovery rates)
- match results including tool-specific hit sets and common identifications
- spectral networking graphs (optional, for RiPP propagation visualization)

## How to apply

Prepare centroided spectra in MGF format (convert non-native formats using ProteoWizard msconvert if needed). Select the appropriate NPDtools pipeline: Dereplicator for standard PNP database search, VarQuest for modification-tolerant variant detection, or Dereplicator+ for non-peptidic metabolite identification. Execute the chosen pipeline with the spectra and structure database as inputs, using standard parameters (or --blind flag for arbitrary post-translational modification search in MetaMiner). Parse the resulting significant_matches.tsv output to extract scan identifiers, match scores, p-values, and false discovery rates. For comparative analysis, run all three pipelines on identical test spectra and cross-tabulate results to identify tool-specific detections, common hits, and mode-dependent sensitivity differences.

## Related tools

- **Dereplicator** (database search pipeline for identification of peptidic natural products through tandem mass spectra matching against known PNP structures) — https://github.com/ablab/npdtools
- **VarQuest** (modification-tolerant database search pipeline for identification of novel variants of PNPs with PTM tolerance) — https://github.com/ablab/npdtools
- **Dereplicator+** (extended database search pipeline for identification of both peptidic and non-peptidic metabolites through tandem mass spectra matching) — https://github.com/ablab/npdtools
- **MetaMiner** (metabologenomic pipeline that integrates tandem mass spectra matching with genomic data to identify RiPPs; executes Dereplicator internally with optional --blind flag for arbitrary PTM search) — https://github.com/mohimanilab/MetaMiner
- **ProteoWizard msconvert** (format conversion utility to convert non-native spectrum formats (e.g., .mzML) to MGF for NPDtools compatibility)

## Examples

```
python dereplicator.py test_spectra.mgf -d RiPP_structure_db.txt -o dereplicator_output/ && python varquest.py test_spectra.mgf -d RiPP_structure_db.txt -o varquest_output/
```

## Evaluation signals

- significant_matches.tsv contains non-empty rows with valid scan identifiers, numeric match scores, and p-values within expected ranges (e.g., p < 0.05 for significant matches)
- false discovery rate (FDR) values are computed and reported for each match, indicating statistical significance filtering was applied
- cross-pipeline comparison identifies expected overlaps and tool-specific detections; Dereplicator+ should detect at least as many hits as Dereplicator alone on the same inputs
- spectral network output (if generated) shows connected components with appropriate cosine similarity thresholds, validating propagation-based RiPP enlargement
- no parsing errors or missing columns in significant_matches.tsv; all spectra from input files are represented in output with no truncation

## Limitations

- Requires spectra to be centroided; profile mode spectra must be preprocessed or conversion may fail or produce unreliable results
- antiSMASH output (.final.gbk) may fail to detect certain biosynthetic gene clusters (e.g., AmfS) where raw contig.fasta succeeds; genome input format selection affects MetaMiner sensitivity
- No changelog available in NPDtools 2.5.0 documentation; version-specific behavior changes between releases are not formally documented
- Spectral network visualization requires matplotlib and networkx Python libraries; plain-text output only if these dependencies are absent
- VarQuest and MetaMiner --blind flag increase computational cost and may reduce specificity due to expanded PTM search space

## Evidence

- [other] NPDtools version 2.5.0 includes multiple database search pipelines (Dereplicator, VarQuest, Dereplicator+) within its toolkit for natural product mass spectrometry analysis.: "NPDtools version 2.5.0 includes multiple database search pipelines (Dereplicator, VarQuest, Dereplicator+) within its toolkit"
- [readme] Spectra files must be centroided and be in an open spectrum format (MGF, mzXML, mzML or mzData). NPDtools natively supports MGF and mzXML/mzData and uses msconvert utility from ProteoWizard to convert spectra in other formats to MGF.: "Spectra files must be centroided and be in an open spectrum format (**MGF**, **mzXML**, **mzML** or **mzData**). NPDtools natively supports MGF"
- [other] Execute Dereplicator pipeline on the same test spectra and RiPP structure database, output match results. Execute VarQuest pipeline on the same inputs with standard parameters. Parse and tabulate significant_matches.tsv outputs from all three tools, recording scan identifiers, match scores, p-values, and false discovery rates.: "Parse and tabulate significant_matches.tsv outputs from all three tools, recording scan identifiers, match scores, p-values, and false discovery rates."
- [other] Cross-compare hit sets to identify tool-specific detections, common identifications, and mode-dependent sensitivity differences.: "Cross-compare hit sets to identify tool-specific detections, common identifications, and mode-dependent sensitivity differences."
- [readme] MetaMiner is a metabologenomic pipeline which integrates metabolomic (tandem mass spectra) and genomic data to identify novel RiPPs: "MetaMiner is a metabologenomic pipeline which integrates metabolomic (tandem mass spectra) and genomic data to identify novel RiPPs"
- [other] While `MetaMiner` successfully detect AmfS using the `contigs.fasta` file, it fails with antiSMASH result as input: "While `MetaMiner` successfully detect AmfS using the `contigs.fasta` file, it fails with antiSMASH result as input"
