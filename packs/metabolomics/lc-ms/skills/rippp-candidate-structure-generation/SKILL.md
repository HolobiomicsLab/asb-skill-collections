---
name: rippp-candidate-structure-generation
description: Use when after identifying precursor peptides from genome assemblies via BGC mining, when you need to enumerate the chemical space of PTM variants (lantibiotic, lassopeptide, cyanobactin, or other RiPP classes) before matching tandem mass spectra against a constructed database using Dereplicator or.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3778
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0219
  tools:
  - MetaMiner
  - NPDtools 2.5.0
  - Dereplicator
  - antiSMASH
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# RiPP Candidate Structure Generation

## Summary

Generate putative post-translationally modified (PTM) variants of identified RiPP precursor peptides according to class-specific modification rules, producing a structured database of candidate structures for downstream spectral matching. This skill bridges genome-mined precursor sequences to mass spectrometry-queryable structure space.

## When to use

After identifying precursor peptides from genome assemblies via BGC mining, when you need to enumerate the chemical space of PTM variants (lantibiotic, lassopeptide, cyanobactin, or other RiPP classes) before matching tandem mass spectra against a constructed database using Dereplicator or similar tools.

## When NOT to use

- Input is raw genomic DNA without prior BGC or precursor peptide identification — use MetaMiner's BGC identifier module first.
- Mass spectra are already matched to known RiPP databases — this skill is only needed when building new candidate databases for novel or uncharacterized precursors.
- RiPP class is unknown or not supported by the available modification rule sets (e.g., bacteriocins are not yet integrated into MetaMiner v2.5.0).

## Inputs

- Precursor peptide sequences (FASTA or extracted from annotated genome assemblies)
- RiPP class label (e.g., 'lantibiotic', 'lassopeptide', 'cyanobactin')
- Class-specific modification rule set (implicit in MetaMiner's BGC identifier output)

## Outputs

- Per-class RiPP structure database (TSV or equivalent structured file)
- Enumerated candidate structures with PTM annotation
- Precursor–structure mapping metadata (BGC ID, gene coordinates, modification patterns)

## How to apply

For each precursor peptide identified by MetaMiner's BGC identifier module, apply the RiPP Structure Database Builder to enumerate putative PTM variants according to the target RiPP class's modification rules (specified via the --class parameter). The builder generates all combinatorially possible modifications (e.g., cyclization, dehydration, oxidation patterns for lanthipeptides) for each precursor. Aggregate all per-class candidate structures into a single TSV or structured file, preserving precursor sequence metadata (BGC ID, gene coordinates, RiPP class). The output file serves as the searchable database for Dereplicator's spectral matching step.

## Related tools

- **MetaMiner** (BGC identifier and RiPP Structure Database Builder — identifies precursor peptides and enumerates PTM variants by RiPP class) — https://github.com/mohimanilab/MetaMiner
- **NPDtools 2.5.0** (Toolkit containing MetaMiner and Dereplicator; provides end-to-end metabologenomic and spectral matching workflows) — https://github.com/ablab/npdtools
- **Dereplicator** (Spectral database search tool — matches tandem mass spectra against the constructed RiPP structure database) — https://github.com/ablab/npdtools
- **antiSMASH** (Optional upstream genome mining tool; outputs can be provided to MetaMiner as an alternative to raw FASTA)

## Examples

```
python metaminer.py test_data/metaminer/msms/ -s test_data/metaminer/fasta/ --class lantibiotic -o metaminer_outdir
```

## Evaluation signals

- Output TSV contains one row per candidate structure with columns for precursor ID, BGC coordinates, modification pattern, and predicted m/z or molecular formula
- Number of candidate structures per precursor is within the expected combinatorial range for the RiPP class (verify no explosion of redundant variants or missing modifications)
- Precursor sequences match those extracted from the input genome assembly; no truncation or sequence corruption
- All candidates conform to the specified RiPP class rules (e.g., lantipeptides contain only cyclic thioether and dehydrated residues, no other PTMs)
- Database is consumable by downstream Dereplicator spectral matching without schema or format errors

## Limitations

- MetaMiner's BGC identifier may fail to detect some precursor peptides when using antiSMASH-generated output (e.g., .final.gbk files); raw contig FASTA is more reliable for detection.
- Only RiPP classes explicitly supported by MetaMiner (lantibiotic, lassopeptide, cyanobactin, and a few others) can be enumerated; bacteriocins and other natural product classes are not yet integrated.
- Combinatorial enumeration can produce very large databases for precursors with many possible modification sites; no filtering or scoring at this stage to rank likely variants by biological plausibility or spectral likelihood.
- Modification rule sets are hardcoded by class and version; variant discovery for novel PTM patterns requires manual rule extension or integration of updated databases.

## Evidence

- [methods] For each identified precursor peptide, apply the RiPP Structure Database Builder to enumerate putative post-translationally modified variants according to class-specific modification rules.: "For each identified precursor peptide, apply the RiPP Structure Database Builder to enumerate putative post-translationally modified variants according to class-specific modification rules."
- [other] MetaMiner operates in a multi-stage workflow where it first identifies putative BGCs and corresponding precursor peptides from genome assemblies, then constructs putative RiPP structure databases, before matching spectra against the constructed database.: "MetaMiner operates in a multi-stage workflow where it first identifies putative BGCs and corresponding precursor peptides from genome assemblies, then constructs putative RiPP structure databases,"
- [other] Aggregate all generated candidate structures into a per-class RiPP structure database. Output the intermediate candidate database as a structured file (TSV or equivalent) ready for downstream spectral matching by Dereplicator.: "Aggregate all generated candidate structures into a per-class RiPP structure database. Output the intermediate candidate database as a structured file (TSV or equivalent) ready for downstream"
- [methods] While `MetaMiner` successfully detect AmfS using the `contigs.fasta` file, it fails with antiSMASH result as input: "While `MetaMiner` successfully detect AmfS using the `contigs.fasta` file, it fails with antiSMASH result as input"
- [readme] MetaMiner (former *RiPPquest*, *MetaRiPPquest*) — a tool implementing metabologenomics approach for the discovery of ribosomally synthesized and post-translationally modified peptides (RiPPs): "MetaMiner (former *RiPPquest*, *MetaRiPPquest*) — a tool implementing metabologenomics approach for the discovery of ribosomally synthesized and post-translationally modified peptides (RiPPs)"
