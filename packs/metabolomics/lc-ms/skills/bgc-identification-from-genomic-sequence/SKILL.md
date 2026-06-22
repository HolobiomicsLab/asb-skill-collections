---
name: bgc-identification-from-genomic-sequence
description: Use when you have assembled genome sequences (contigs or scaffolds in FASTA format) and want to identify putative BGCs and their precursor peptides before constructing a RiPP structure database for spectral matching.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0436
  edam_topics:
  - http://edamontology.org/topic_0621
  - http://edamontology.org/topic_0080
  - http://edamontology.org/topic_0202
  tools:
  - MetaMiner
  - NPDtools 2.5.0
  - SPAdes
  - antiSMASH
  - BOA
  techniques:
  - LC-MS
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# bgc-identification-from-genomic-sequence

## Summary

Scan genome assemblies in FASTA format using MetaMiner's BGC identifier module to locate putative biosynthetic gene clusters and extract corresponding precursor peptide sequences for a specified RiPP class (lantibiotic, lassopeptide, cyanobactin, or others). This is the first stage of the metabologenomic workflow to identify novel ribosomally synthesized and post-translationally modified peptides.

## When to use

Apply this skill when you have assembled genome sequences (contigs or scaffolds in FASTA format) and want to identify putative BGCs and their precursor peptides before constructing a RiPP structure database for spectral matching. Use this step to bridge genomic and metabolomic data in a metabologenomic discovery pipeline targeting specific RiPP classes.

## When NOT to use

- Input is already a set of annotated precursor peptides or known RiPP sequences — skip directly to RiPP structure database construction.
- Working with antiSMASH-processed .final.gbk output that has failed to detect the target precursor in preliminary testing — use raw FASTA contigs instead.
- RiPP class is not among the supported classes (lantibiotic, lassopeptide, cyanobactin) and no MetaMiner module exists for that class.

## Inputs

- Genome assembly in FASTA format (contigs or scaffolds)
- RiPP class identifier (lantibiotic, lassopeptide, cyanobactin, or class via --class parameter)

## Outputs

- List of identified putative biosynthetic gene clusters with genomic coordinates
- Precursor peptide sequences extracted from identified BGCs
- Structured intermediate file (TSV or equivalent) of precursor peptides per RiPP class

## How to apply

Load genome assembly in FASTA format and parse nucleotide sequences. Execute MetaMiner's BGC identifier module, specifying the target RiPP class via the --class parameter (lantibiotic, lassopeptide, cyanobactin, or equivalent). The module scans for putative biosynthetic gene clusters and extracts matching precursor peptide sequences according to class-specific sequence features. Aggregate the identified precursor peptides as intermediate output. Note that raw FASTA contigs may succeed where antiSMASH-preprocessed .final.gbk files fail to detect certain precursors (e.g., AmfS), so prefer native FASTA input when available.

## Related tools

- **MetaMiner** (BGC identifier module that scans genome FASTA files and extracts precursor peptide sequences matching a specified RiPP class) — https://github.com/mohimanilab/MetaMiner
- **NPDtools 2.5.0** (Container toolkit providing MetaMiner as a metabologenomic pipeline component for natural product discovery) — https://github.com/ablab/npdtools
- **SPAdes** (Assembles DNA short reads (.fastq) into nucleotide sequences (contigs or scaffolds) to generate FASTA input for BGC identification)
- **antiSMASH** (Alternative genome mining tool whose .final.gbk or .gbk output can be used as MetaMiner input (though raw FASTA may be more sensitive))
- **BOA** (Genome mining tool whose .annotated.txt output is accepted as an alternative input format by MetaMiner) — https://github.com/idoerg/BOA

## Examples

```
python metaminer.py test_data/metaminer/msms/ -s test_data/metaminer/fasta/ -o metaminer_outdir
```

## Evaluation signals

- Precursor peptide sequences are extracted and match expected sequence motifs for the specified RiPP class (e.g., leader peptide followed by core peptide for lantibiotics).
- Output TSV or structured file contains one row per identified precursor, with BGC coordinates, precursor ID, and extracted sequence.
- Number and specificity of identified BGCs are consistent with known genomic content and literature expectations for the organism queried.
- Raw FASTA input successfully identifies precursor peptides that antiSMASH-preprocessed inputs fail to detect, confirming input format sensitivity.
- Downstream RiPP structure database construction and spectral matching steps proceed without errors or schema mismatches on the extracted precursor output.

## Limitations

- MetaMiner BGC identifier may fail to detect certain precursor peptides when input is antiSMASH-preprocessed .final.gbk rather than raw FASTA contigs; raw nucleotide sequences are preferred.
- BGC identification is limited to the RiPP classes implemented in MetaMiner (lantibiotic, lassopeptide, cyanobactin); other natural product classes or RiPP types are not supported.
- Putative BGCs and precursor peptides are predictions and require downstream validation via mass spectrometry matching and spectral networking to confirm biological relevance.
- Performance depends on quality and completeness of genome assembly; fragmented contigs or gaps may reduce BGC detection sensitivity.

## Evidence

- [methods] Load genome assembly in FASTA format and parse nucleotide sequences. 2. Execute MetaMiner's BGC identifier module to scan for putative biosynthetic gene clusters and extract precursor peptide sequences matching the target RiPP class: "Load genome assembly in FASTA format and parse nucleotide sequences. 2. Execute MetaMiner's BGC identifier module to scan for putative biosynthetic gene clusters and extract precursor peptide"
- [methods] Starting from the genome assemblies, MetaMiner (i) identifies putative BGCs and the corresponding precursor peptides: "Starting from the genome assemblies, MetaMiner (i) identifies putative BGCs and the corresponding precursor peptides"
- [methods] While `MetaMiner` successfully detect AmfS using the `contigs.fasta` file, it fails with antiSMASH result as input: "While `MetaMiner` successfully detect AmfS using the `contigs.fasta` file, it fails with antiSMASH result as input"
- [methods] MetaMiner is a metabologenomic pipeline which integrates metabolomic (tandem mass spectra) and genomic data to identify novel RiPPs: "MetaMiner is a metabologenomic pipeline which integrates metabolomic (tandem mass spectra) and genomic data to identify novel RiPPs"
- [methods] Aggregate all generated candidate structures into a per-class RiPP structure database. 5. Output the intermediate candidate database as a structured file (TSV or equivalent): "Aggregate all generated candidate structures into a per-class RiPP structure database. 5. Output the intermediate candidate database as a structured file (TSV or equivalent) ready for downstream"
