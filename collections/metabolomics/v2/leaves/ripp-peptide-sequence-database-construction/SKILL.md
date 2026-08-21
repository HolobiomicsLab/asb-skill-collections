---
name: ripp-peptide-sequence-database-construction
description: Use when when you have genomic sequences (assembled contigs or antiSMASH/BOA
  mining results) and want to match experimental tandem mass spectra against predicted
  RiPP structures.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0361
  edam_topics:
  - http://edamontology.org/topic_0102
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - NPDtools 2.5.0
  - MetaMiner
  - Dereplicator
  - ProteoWizard
  - Python
  - antiSMASH
  - BOA
  - SPAdes / metaSPAdes
  - VarQuest
  - Dereplicator+
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
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

# RiPP peptide sequence database construction

## Summary

Construct a post-translationally modified RiPP structure database from genome-derived precursor peptides and predicted biosynthetic modifications. This database serves as the search target for tandem mass spectra in natural product dereplication workflows.

## When to use

When you have genomic sequences (assembled contigs or antiSMASH/BOA mining results) and want to match experimental tandem mass spectra against predicted RiPP structures. Apply this skill before executing database search pipelines (Dereplicator, VarQuest, Dereplicator+) that require a curated RiPP structure database as input.

## When NOT to use

- Input is already a validated RiPP structure database or chemical structure library (skip to direct spectrum matching).
- You lack genomic data or genome mining results; only have mass spectra without sequence information (use blind spectral search instead).
- The organism is not a known RiPP producer or the target natural product class is unknown (consider using Dereplicator+ or blind PTM search instead of class-specific prediction).

## Inputs

- Assembled DNA contigs (.fasta format)
- antiSMASH genome mining output (.final.gbk or .gbk file)
- BOA genome mining output (.annotated.txt file)
- Raw nucleotide sequences (.fasta format)

## Outputs

- RiPP structure database (formatted for Dereplicator, VarQuest, or Dereplicator+ input)
- Precursor peptide sequences and predicted post-translational modifications
- BGC annotations with coordinates and associated peptide sequences

## How to apply

Starting from assembled genome sequences or genome mining tool output (antiSMASH .final.gbk/.gbk, BOA .annotated.txt, or raw .fasta contigs), use MetaMiner to identify putative biosynthetic gene clusters (BGCs) and extract corresponding precursor peptides. MetaMiner then constructs putative RiPP structure databases by predicting post-translational modifications (PTMs) characteristic of the RiPP class of interest (e.g., lantibiotic modifications for the default class, or arbitrary PTMs when run with the --blind flag). The resulting structure database is formatted for direct input to downstream database search tools. Key decision points: choose input source (antiSMASH output works with some limitations; raw contig FASTA is more reliable); specify RiPP class or use --blind mode for modification-agnostic discovery.

## Related tools

- **MetaMiner** (Primary tool for identifying BGCs, extracting precursor peptides, and constructing post-translationally modified RiPP structure databases from genomic sequences) — https://github.com/mohimanilab/MetaMiner
- **antiSMASH** (Upstream genome mining tool whose output (.final.gbk or .gbk files) can be ingested by MetaMiner to identify biosynthetic gene clusters)
- **BOA** (Upstream genome mining tool whose .annotated.txt output can be used by MetaMiner for BGC and precursor peptide identification) — https://github.com/idoerg/BOA
- **SPAdes / metaSPAdes** (Upstream genome assembly tool to generate contigs (.fasta) from raw DNA short reads before RiPP database construction)
- **Dereplicator** (Downstream database search pipeline that accepts the constructed RiPP structure database to match against tandem mass spectra) — https://github.com/ablab/npdtools
- **VarQuest** (Downstream modification-tolerant database search tool that accepts the RiPP structure database for variant detection) — https://github.com/ablab/npdtools
- **Dereplicator+** (Downstream database search pipeline for both peptidic and non-peptidic metabolites that uses the constructed database) — https://github.com/ablab/npdtools

## Examples

```
python metaminer.py test_data/metaminer/msms/ -s test_data/metaminer/fasta/ -o metaminer_outdir
```

## Evaluation signals

- RiPP structure database file is generated and formatted correctly for downstream Dereplicator/VarQuest/Dereplicator+ input.
- Precursor peptides are extracted from identified BGCs with correct start and stop coordinates in genomic sequences.
- Post-translational modifications are predicted for the specified RiPP class (e.g., lantibiotic PTMs are present for default lantibiotic-class predictions).
- When run on the same input, MetaMiner successfully detects known RiPP precursors (e.g., AmfS when using contigs.fasta, though antiSMASH .final.gbk output may fail for some BGCs).
- Resulting database yields match hits with reported scan identifiers, match scores, p-values, and false discovery rates when queried by downstream search tools.

## Limitations

- antiSMASH output (.final.gbk) fails to detect some BGCs (e.g., AmfS) while the raw contig FASTA file succeeds, indicating input format dependency.
- RiPP class specification (default lantibiotic) may miss novel or uncharacterized RiPP types; --blind flag enables discovery but increases computation.
- Requires functional genome assembly and gene annotation upstream; poor-quality contigs or assembly gaps lead to missed or truncated precursor peptides.
- No changelog available in repository; version-specific behavior changes and bug fixes may not be documented.

## Evidence

- [methods] identifies putative BGCs and the corresponding precursor peptides: "Starting from the genome assemblies, MetaMiner (i) identifies putative BGCs and the corresponding precursor peptides"
- [methods] constructs putative RiPP structure databases: "(ii) constructs putative RiPP structure databases"
- [readme] NPDtools natively supports MGF, mzXML, mzData and uses msconvert utility from the ProteoWizard package to convert spectra in other formats to MGF: "MetaMiner natively supports MGF, mzXML, mzData and uses msconvert utility from the ProteoWizard package to convert spectra in other formats to MGF"
- [readme] raw nucleotide sequences or output of specific genome mining tools: "The metabologenomic pipelines (currently MetaMiner only) require either raw genome nucleotide sequences or output of specific genome mining tools."
- [methods] antiSMASH result fails to detect AmfS using contigs.fasta succeeds: "While `MetaMiner` successfully detect AmfS using the `contigs.fasta` file, it fails with antiSMASH result as input"
- [methods] matches tandem mass spectra against the constructed post-translationally modified RiPPs structure database using Dereplicator: "(iii) matches tandem mass spectra against the constructed post-translationally modified RiPPs structure database using Dereplicator"
