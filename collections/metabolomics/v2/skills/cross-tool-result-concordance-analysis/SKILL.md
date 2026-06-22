---
name: cross-tool-result-concordance-analysis
description: Use when you have executed multiple NPDtools database search pipelines (Dereplicator, VarQuest, Dereplicator+, or MetaMiner in different modes) on identical test spectra or RiPP sequence inputs and need to understand their relative sensitivity, specificity, and complementarity.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
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
  - tandem-MS
derived_from:
- doi: 10.1038/s41467-018-06082-8
  title: dereplicator
evidence_spans:
- The latest version is available in the Natural Product Discovery toolkit (NPDtools) at https://github.com/ablab/npdtools
- MetaMiner is a metabologenomic pipeline which integrates metabolomic (tandem mass spectra) and genomic data to identify novel RiPPs
- MetaMiner is a metabologenomic pipeline which integrates metabolomic (tandem mass spectra) and genomic data to identify novel Ribosmally synthesized and Post-translationally modified Peptides (RiPPs)
- matches tandem mass spectra against the constructed post-translationally modified RiPPs structure database using Dereplicator
- MetaMiner natively supports MGF, mzXML, mzData and uses msconvert utility from the ProteoWizard package to convert spectra in other formats to MGF
- uses msconvert utility from the ProteoWizard package to convert spectra in other formats to MGF
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# cross-tool-result-concordance-analysis

## Summary

Compare hit patterns and detection sensitivity across multiple natural product database search pipelines (Dereplicator, VarQuest, Dereplicator+) on the same test spectra to identify tool-specific identifications, common detections, and mode-dependent performance differences. This skill is essential when validating which pipeline best suits a particular RiPP or natural product discovery workflow.

## When to use

You have executed multiple NPDtools database search pipelines (Dereplicator, VarQuest, Dereplicator+, or MetaMiner in different modes) on identical test spectra or RiPP sequence inputs and need to understand their relative sensitivity, specificity, and complementarity. This is particularly valuable when deciding which pipeline to deploy on large discovery sets, or when troubleshooting unexpected detection patterns (e.g., one tool succeeds while another fails on the same input).

## When NOT to use

- You are analyzing spectra from different datasets or acquisition methods — concordance analysis requires identical inputs to be meaningful.
- You have run only a single pipeline on your data; comparison requires at least two independent pipeline executions.
- Your goal is to filter and curate a single best result set rather than understand tool performance — use post-hoc ranking or FDR thresholding instead.

## Inputs

- Test spectra in MGF format (or mzML/mzXML/mzData convertible to MGF via ProteoWizard msconvert)
- RiPP FASTA sequence file (e.g., example_RiPP.fasta)
- RiPP structure database (or natural product chemical structure database for Dereplicator+)
- significant_matches.tsv outputs from Dereplicator, VarQuest, Dereplicator+, and/or MetaMiner executions

## Outputs

- Unified cross-tool comparison table (tabulating scan IDs, candidate identifiers, tool-specific match scores, p-values, FDR by pipeline)
- Tool-specific detection sets (hits unique to each pipeline)
- Common detection set (hits found by multiple pipelines)
- Summary statistics (e.g., sensitivity per tool, concordance matrices, mode-dependent sensitivity deltas)

## How to apply

Execute each database search pipeline independently on the same test spectra (converted to MGF format using ProteoWizard msconvert if necessary) and the same RiPP structure database or sequence file. For MetaMiner, run once with standard parameters (default lantibiotic class) and once with the --blind flag to capture modification-tolerant matches. Parse the significant_matches.tsv outputs from all tools, extracting scan identifiers, match scores, p-values, and false discovery rates. Create a unified table cross-referencing hits by scan ID and candidate identifier. Perform set operations (union, intersection, tool-specific-only) to identify common identifications versus tool-exclusive detections. Compare hit patterns across search modes to quantify sensitivity differences and identify mode-dependent detection bottlenecks.

## Related tools

- **Dereplicator** (Database search pipeline for identification of peptidic natural products through spectral matching against RiPP structure database) — https://github.com/ablab/npdtools
- **VarQuest** (Modification-tolerant database search pipeline for identification of novel variants of peptidic natural products) — https://github.com/ablab/npdtools
- **Dereplicator+** (Metabolite identification pipeline for both peptidic and non-peptidic natural products through database search) — https://github.com/ablab/npdtools
- **MetaMiner** (Metabologenomic pipeline integrating tandem mass spectra with genomic data; executed in standard and --blind modes to compare baseline vs. modification-tolerant detection) — https://github.com/mohimanilab/MetaMiner
- **ProteoWizard msconvert** (Converts spectra from mzML, mzXML, mzData formats to MGF for pipeline compatibility)
- **Python** (Scripting language (2.6–2.7, 3.3+) for parsing, tabulating, and cross-comparing significant_matches.tsv outputs)

## Examples

```
python parse_and_compare.py --dereplicator matches_dereplicator.tsv --varquest matches_varquest.tsv --dereplicator+ matches_dereplicator_plus.tsv --metaminer-standard matches_metaminer_std.tsv --metaminer-blind matches_metaminer_blind.tsv --output concordance_report.tsv
```

## Evaluation signals

- All input spectra files are successfully parsed by each pipeline without format errors or dropped scans.
- Unified cross-tool table has complete row coverage: every scan ID present in at least one pipeline's output is represented.
- Tool-specific and common detection sets are mutually exclusive and exhaustive (union equals total hit count across all pipelines).
- Hit concordance metrics (e.g., percentage of scans with ≥2 pipeline agreement) are reported; concordance >50% suggests strong signal, <20% suggests pipeline-dependent sensitivity.
- Mode-dependent sensitivity deltas (standard vs. --blind MetaMiner) are quantified; --blind mode should increase detection count if modification tolerance is relevant.

## Limitations

- Concordance analysis assumes identical database composition across pipelines; mismatched RiPP structure databases or sequence files will confound tool-vs.-database effects.
- Different pipelines use different scoring schemes (e.g., cosine similarity, p-value, FDR); direct score comparison across tools is not valid; only rank-order or binary detection (hit/no-hit) should be compared.
- Tool agreement does not validate correctness; multiple pipelines may converge on a false positive. Orthogonal validation (e.g., MS/MS fragmentation pattern matching, genomic evidence) is required.
- Performance differences may reflect database index speed rather than search sensitivity; tools with faster indices may fail to report marginal hits due to timeout, not algorithmic limitation.
- Spectral preprocessing (centroiding, deisotoping, parent mass tolerance) is applied before reaching the pipelines; differences in these upstream steps are not captured by this skill and may contribute to apparent tool-specific detections.

## Evidence

- [methods] NPDtools version 2.5.0 includes multiple database search pipelines (Dereplicator, VarQuest, Dereplicator+) within its toolkit for natural product mass spectrometry analysis.: "NPDtools version 2.5.0 includes multiple database search pipelines (Dereplicator, VarQuest, Dereplicator+) within its toolkit"
- [methods] Parse and tabulate significant_matches.tsv outputs from all three tools, recording scan identifiers, match scores, p-values, and false discovery rates.: "Parse and tabulate significant_matches.tsv outputs from all three tools, recording scan identifiers, match scores, p-values, and false discovery rates"
- [methods] Cross-compare hit sets to identify tool-specific detections, common identifications, and mode-dependent sensitivity differences.: "Cross-compare hit sets to identify tool-specific detections, common identifications, and mode-dependent sensitivity differences"
- [readme] Dereplicator — a tool for identification of peptidic natural products (PNPs) through database search of mass spectra: "Dereplicator — a tool for identification of peptidic natural products (PNPs) through database search of mass spectra"
- [readme] VarQuest — a tool for modification-tolerant identification of novel variants of PNPs: "VarQuest — a tool for modification-tolerant identification of novel variants of PNPs"
- [readme] Dereplicator+ — a tool for identification of metabolites (both peptidic and non-peptidic) through database search of mass spectra: "Dereplicator+ — a tool for identification of metabolites (both peptidic and non-peptidic) through database search of mass spectra"
- [readme] MetaMiner natively supports MGF, mzXML, mzData and uses msconvert utility from the ProteoWizard package to convert spectra in other formats to MGF: "MetaMiner natively supports MGF, mzXML, mzData and uses msconvert utility from the ProteoWizard package to convert spectra in other formats to MGF"
- [methods] Execute MetaMiner with standard parameters (default lantibiotic class) on test spectra and RiPP sequences, generate significant_matches.tsv. Execute MetaMiner again with --blind flag enabled to search for arbitrary post-translational modifications.: "Execute MetaMiner with standard parameters (default lantibiotic class) on test spectra and RiPP sequences, generate significant_matches.tsv. Execute MetaMiner again with --blind flag enabled to"
