---
name: metabologenomic-database-construction
description: Use when you have genome FASTA or annotated genome files (antiSMASH .gbk, BOA .annotated.txt) and wish to discover ribosomally synthesized and post-translationally modified peptides (RiPPs) by integrating genomic and mass spectrometry data.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3349
  edam_topics:
  - http://edamontology.org/topic_0621
  - http://edamontology.org/topic_0622
  - http://edamontology.org/topic_3520
  tools:
  - MetaMiner
  - NPDtools 2.5.0
  - antiSMASH
  - BOA
  - SPAdes / metaSPAdes
  - Dereplicator
  - NPDtools
derived_from:
- doi: 10.1038/s41467-018-06082-8
  title: dereplicator
evidence_spans:
- MetaMiner is a metabologenomic pipeline which integrates metabolomic (tandem mass spectra) and genomic data to identify novel RiPPs
- MetaMiner is a metabologenomic pipeline which integrates metabolomic (tandem mass spectra) and genomic data to identify novel Ribosmally synthesized and Post-translationally modified Peptides (RiPPs)
- The latest version is available in the Natural Product Discovery toolkit (NPDtools) at https://github.com/ablab/npdtools
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

# metabologenomic-database-construction

## Summary

Construct a searchable RiPP structure database by identifying putative biosynthetic gene clusters (BGCs) and precursor peptides from genome assemblies, then enumerating post-translationally modified variants according to class-specific rules. This intermediate database enables downstream matching of tandem mass spectra against predicted peptide structures.

## When to use

You have genome FASTA or annotated genome files (antiSMASH .gbk, BOA .annotated.txt) and wish to discover ribosomally synthesized and post-translationally modified peptides (RiPPs) by integrating genomic and mass spectrometry data. Apply this skill when you need to generate candidate RiPP structures for a specific RiPP class (lantibiotic, lassopeptide, cyanobactin, or other) before spectral matching.

## When NOT to use

- Input is non-genomic (mass spectra only, without genome sequence data) — use database search pipelines (Dereplicator, VarQuest) instead.
- Genome assembly is incomplete or highly fragmented (e.g., many short contigs <5 kb) — BGC identifier may fail to detect multi-gene clusters; consider assembly improvement or alternative tools.
- antiSMASH .gbk output is used when raw contigs.fasta is available — documented failure mode where antiSMASH output misses some precursor peptides (AmfS example) while raw FASTA succeeds.

## Inputs

- genome FASTA file (nucleotide sequences)
- antiSMASH .final.gbk or .gbk output (alternative to raw FASTA)
- BOA .annotated.txt file (alternative to raw FASTA)
- RiPP class identifier (e.g., lantibiotic, lassopeptide, cyanobactin)

## Outputs

- per-class RiPP structure database (TSV or structured file format)
- precursor peptide sequence list with BGC coordinates
- enumerated post-translationally modified candidate structures

## How to apply

Load a genome assembly (FASTA format or genome mining tool output) into MetaMiner's BGC identifier module, which scans for putative biosynthetic gene clusters and extracts precursor peptide sequences matching your target RiPP class via the --class parameter. For each identified precursor peptide, apply the RiPP Structure Database Builder to enumerate all putative post-translationally modified variants according to class-specific modification rules (e.g., cyclization, dehydration, lanthionine formation for lantibiotics). Aggregate all generated candidate structures into a per-class TSV or structured output file ready for downstream spectral matching by Dereplicator. The rationale is that exhaustive enumeration of modifications before spectral matching increases sensitivity for novel RiPP discovery while maintaining a defined search space.

## Related tools

- **MetaMiner** (main tool that executes BGC identification and RiPP structure database construction; integrates genomic data with metabolomic spectra) — https://github.com/mohimanilab/MetaMiner
- **antiSMASH** (optional input source: genome mining tool producing .final.gbk or .gbk files that MetaMiner can ingest instead of raw FASTA)
- **BOA** (optional input source: bacteriocin/RiPP prediction tool producing .annotated.txt files that MetaMiner can ingest) — https://github.com/idoerg/BOA
- **SPAdes / metaSPAdes** (upstream genome assembly: converts raw short reads (.fastq) to contigs/scaffolds (.fasta) before MetaMiner processing)
- **Dereplicator** (downstream spectral matching: searches constructed RiPP structure database against tandem mass spectra)
- **NPDtools** (packaging framework containing MetaMiner and all dependent tools) — https://github.com/ablab/npdtools

## Examples

```
python metaminer.py test_data/metaminer/msms/ -s test_data/metaminer/fasta/ --class lantibiotic -o metaminer_outdir
```

## Evaluation signals

- Output TSV or structure file is non-empty and contains expected number of precursor peptide sequences matching the target RiPP class.
- Each precursor peptide row includes BGC coordinates, genomic context, and class-specific modification variants (e.g., count of enumerated lantibiotics per precursor matches expected combinatorial expansion).
- Downstream spectral matching (Dereplicator) against the constructed database successfully identifies at least one known RiPP from a positive control dataset (e.g., MSV000080102 for validation runs).
- For raw FASTA inputs, verify detection of expected precursors; compare against antiSMASH .gbk output where available — raw FASTA should detect at least as many precursors as .gbk (due to documented antiSMASH filtering issues).
- Database size and diversity scale appropriately with input genome size and RiPP class diversity; verify no systematic truncation or missing modification variants in output.

## Limitations

- antiSMASH .final.gbk output may fail to detect some precursor peptides (documented failure with AmfS) compared to raw contigs.fasta; prefer raw FASTA input when available.
- Exhaustive enumeration of post-translationally modified variants grows combinatorially with precursor length and class-specific modification rules; very large precursors or complex modification patterns may generate computationally expensive databases.
- Database construction assumes the RiPP class is known a priori (--class parameter); misspecification of class will miss relevant modifications and reduce spectral matching sensitivity.
- Performance depends on quality of input genome assembly; fragmented or low-coverage assemblies may produce incomplete or incorrect BGC predictions.

## Evidence

- [other] MetaMiner operates in a multi-stage workflow where it first identifies putative BGCs and corresponding precursor peptides from genome assemblies, then constructs putative RiPP structure databases, before matching spectra against the constructed database.: "MetaMiner operates in a multi-stage workflow where it first identifies putative BGCs and corresponding precursor peptides from genome assemblies, then constructs putative RiPP structure databases,"
- [other] Execute MetaMiner's BGC identifier module to scan for putative biosynthetic gene clusters and extract precursor peptide sequences matching the target RiPP class (lantibiotic, lassopeptide, cyanobactin, or specified class via --class parameter).: "Execute MetaMiner's BGC identifier module to scan for putative biosynthetic gene clusters and extract precursor peptide sequences matching the target RiPP class (lantibiotic, lassopeptide,"
- [other] For each identified precursor peptide, apply the RiPP Structure Database Builder to enumerate putative post-translationally modified variants according to class-specific modification rules.: "For each identified precursor peptide, apply the RiPP Structure Database Builder to enumerate putative post-translationally modified variants according to class-specific modification rules."
- [other] Aggregate all generated candidate structures into a per-class RiPP structure database. Output the intermediate candidate database as a structured file (TSV or equivalent) ready for downstream spectral matching by Dereplicator.: "Aggregate all generated candidate structures into a per-class RiPP structure database. Output the intermediate candidate database as a structured file (TSV or equivalent) ready for downstream"
- [readme] MetaMiner uses either raw nucleotide sequences or specific genome mining tools' output: raw nucleotide sequences `.fasta` format or *antiSMASH*'s `.final.gbk` or `.gbk` file: "MetaMiner uses either raw nucleotide sequences or specific genome mining tools' output: raw nucleotide sequences `.fasta` format or *antiSMASH*'s `.final.gbk` or `.gbk` file"
- [methods] While `MetaMiner` successfully detect AmfS using the `contigs.fasta` file, it fails with antiSMASH result as input: "While `MetaMiner` successfully detect AmfS using the `contigs.fasta` file, it fails with antiSMASH result as input"
- [readme] MetaMiner is a metabologenomic pipeline which integrates metabolomic (tandem mass spectra) and genomic data to identify novel RiPPs: "MetaMiner is a metabologenomic pipeline which integrates metabolomic (tandem mass spectra) and genomic data to identify novel RiPPs"
- [readme] Starting from the genome assemblies, MetaMiner (i) identifies putative BGCs and the corresponding precursor peptides (ii) constructs putative RiPP structure databases (iii) matches tandem mass spectra against the constructed post-translationally modified RiPPs structure database using Dereplicator: "Starting from the genome assemblies, MetaMiner (i) identifies putative BGCs and the corresponding precursor peptides (ii) constructs putative RiPP structure databases (iii) matches tandem mass"
