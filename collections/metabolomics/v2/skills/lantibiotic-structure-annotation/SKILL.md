---
name: lantibiotic-structure-annotation
description: Use when you have (1) genomic data from a Streptomyces or other RiPP-producing
  organism in raw FASTA format or annotated GenBank format, (2) high-resolution LC-MS/MS
  spectra in centroided MGF, mzML, mzXML, or mzData format, and (3) a known or predicted
  lantibiotic core peptide sequence you wish to.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3646
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3047
  - http://edamontology.org/topic_0160
  tools:
  - NPDtools 2.5.0
  - MetaMiner
  - Dereplicator
  - ProteoWizard
  - NPDtools
  - joblib
  - SPAdes
  - antiSMASH
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

# lantibiotic-structure-annotation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Annotate lantibiotic structures in RiPP biosynthetic gene clusters by matching tandem mass spectra against computationally constructed post-translationally modified peptide databases using MetaMiner. This skill integrates genomic (FASTA nucleotide sequences) and metabolomic (centroided MS/MS spectra in MGF or mzML/mzData format) data to identify lanthipeptides with characteristic dehydrobutyrine and dehydroalanine modifications.

## When to use

Apply this skill when you have (1) genomic data from a Streptomyces or other RiPP-producing organism in raw FASTA format or annotated GenBank format, (2) high-resolution LC-MS/MS spectra in centroided MGF, mzML, mzXML, or mzData format, and (3) a known or predicted lantibiotic core peptide sequence you wish to detect and characterize. Use it to confirm the presence of lantibiotics by detecting their characteristic mass signatures (dehydration shifts of −18 Da on Ser/Thr residues) and verify that genome mining predictions have corresponding metabolite evidence.

## When NOT to use

- Input genome is in antiSMASH .final.gbk or .gbk format—MetaMiner fails to detect lantibiotics from GenBank-formatted input; use raw contigs.fasta instead.
- Spectra are not centroided or are in non-standard formats without ProteoWizard-compatible conversion options.
- You are searching for non-RiPP natural products (e.g., polyketides, non-ribosomal peptides not post-translationally modified); use Dereplicator+ or database search pipelines instead.

## Inputs

- nucleotide sequence (FASTA format, raw contigs.fasta, not antiSMASH .gbk output)
- centroided LC-MS/MS spectra (MGF, mzML, mzXML, or mzData format)
- lantibiotic core peptide sequence (expected/reference sequence, e.g. TGSQVSLLVCEYSSLSVVLCTP)

## Outputs

- significant_matches.tsv (tab-separated file with FragmentSeq, ModifiedSeq, score, and spectral metadata)
- lantibiotic structure annotations with post-translational modifications (dehydrobutyrine/dehydroalanine positions and mass shifts)
- compound identifications linked to genomic loci

## How to apply

Download and extract NPDtools 2.5.0 binaries for your platform (Linux or macOS), ensuring Python 2.6–3.3+ and joblib are available. Prepare input files: (1) obtain or assemble your organism's genomic sequence as a raw nucleotide FASTA file (avoid antiSMASH .gbk output, which has been shown to fail lantibiotic detection); (2) download or generate centroided MS/MS spectra in MGF format (use ProteoWizard's msconvert if spectra are in other formats). Run MetaMiner via command line with the lantibiotic RiPP class flag and default scoring. Parse the tab-separated significant_matches.tsv output file by searching the FragmentSeq column for your target lantibiotic core sequence (e.g., 'TGSQVSLLVCEYSSLSVVLCTP' for AmfS) and verifying that the ModifiedSeq column displays characteristic dehydration mass shifts (T−18 or S−18, indicating dehydrobutyrine or dehydroalanine residues). Filter results to include only hits with the expected modification pattern and spectral scoring above default thresholds.

## Related tools

- **MetaMiner** (Core metabologenomic pipeline that integrates genome assembly and tandem MS data to identify and annotate RiPP structures with post-translational modifications) — https://github.com/mohimanilab/MetaMiner
- **NPDtools 2.5.0** (Container toolkit providing MetaMiner executable, dependency management, and Dereplicator for RiPP structure database matching) — https://github.com/ablab/npdtools
- **Dereplicator** (Matches tandem mass spectra against post-translationally modified RiPP structure databases constructed by MetaMiner)
- **ProteoWizard** (Provides msconvert utility to convert non-native spectrum formats (mzML, mzData) to MGF for MetaMiner input)
- **SPAdes** (Assembles raw DNA short reads (.fastq) into longer contigs (FASTA) for input to MetaMiner when genome assembly is required)
- **antiSMASH** (Alternative genome mining tool whose output format (.gbk) is NOT recommended for lantibiotic detection; use raw FASTA instead)

## Examples

```
python metaminer.py test_data/metaminer/msms/ -s test_data/metaminer/fasta/ -c lantibiotic -o metaminer_outdir
```

## Evaluation signals

- Verify that FragmentSeq column in significant_matches.tsv contains exact or near-exact match to your target lantibiotic core peptide (e.g., TGSQVSLLVCEYSSLSVVLCTP for AmfS).
- Confirm ModifiedSeq shows characteristic dehydration shifts: mass −18 assigned to Ser (S−18) or Thr (T−18) residues, indicating dehydrobutyrine/dehydroalanine post-translational modifications.
- Check that spectral match score meets or exceeds pipeline defaults and that the compound is ranked above noise/decoy hits in the significant_matches.tsv.
- Cross-reference genomic coordinates of the identified precursor peptide (PrecursorSeq and BGC location) to confirm it lies within a predicted biosynthetic gene cluster containing lantibiotic modification and transport genes.
- Validate that raw contigs.fasta input (not antiSMASH .gbk) was used and that input spectra were centroided (non-centroided spectra will yield low or missing hits).

## Limitations

- MetaMiner successfully detects lantibiotics only from raw nucleotide sequence FASTA files; it fails when using antiSMASH-formatted GenBank output (.final.gbk or .gbk), restricting input flexibility.
- Requires centroided mass spectra; non-centroided spectra will not be matched correctly and must be pre-processed with external tools.
- Detection accuracy depends on the quality and completeness of the genome assembly and the presence of detectable post-translational modifications in the mass spectrum; heavily modified or truncated lantibiotics may be missed.
- MetaMiner requires Python 2.6–3.3+ and joblib for parallel processing; older or newer Python versions are not supported.
- No changelog is provided, limiting visibility into which specific modifications or RiPP classes are handled in version 2.5.0 relative to earlier releases.

## Evidence

- [results] MetaMiner successfully detects AmfS using contigs.fasta genome files, though it fails when using antiSMASH results as input: "MetaMiner successfully detects AmfS using contigs.fasta genome files, though it fails when using antiSMASH results as input, indicating that raw nucleotide sequence format supports lantibiotic"
- [readme] MetaMiner is a metabologenomic pipeline which integrates metabolomic (tandem mass spectra) and genomic data to identify novel RiPPs: "MetaMiner is a metabologenomic pipeline which integrates metabolomic (tandem mass spectra) and genomic data to identify novel RiPPs"
- [readme] matches tandem mass spectra against the constructed post-translationally modified RiPPs structure database using Dereplicator: "matches tandem mass spectra against the constructed post-translationally modified RiPPs structure database using Dereplicator"
- [methods] parse the tab-separated significant_matches.tsv output file to extract compound identifications, verifying presence of AmfS by FragmentSeq column matching 'TGSQVSLLVCEYSSLSVVLCTP' and ModifiedSeq showing dehydrobutyrine/dehydroalanine modifications: "parse the tab-separated significant_matches.tsv output file to extract compound identifications, verifying presence of AmfS by FragmentSeq column matching 'TGSQVSLLVCEYSSLSVVLCTP' and ModifiedSeq"
- [readme] MetaMiner uses either raw nucleotide sequences or specific genome mining tools' output: raw nucleotide sequences `.fasta` format or *antiSMASH*'s `.final.gbk` or `.gbk` file: "MetaMiner uses either raw nucleotide sequences or specific genome mining tools' output: raw nucleotide sequences `.fasta` format or *antiSMASH*'s `.final.gbk` or `.gbk` file"
- [readme] NPDtools natively supports MGF, mzXML, mzData and uses msconvert utility from the ProteoWizard package to convert spectra in other formats to MGF: "NPDtools natively supports MGF, mzXML, mzData and uses msconvert utility from the ProteoWizard package to convert spectra in other formats to MGF"
- [readme] NPDtools requires a 64-bit Linux system or macOS and Python (versions 2.6-2.7, 3.3 and higher are supported): "NPDtools requires a 64-bit Linux system or macOS and Python (versions 2.6-2.7, 3.3 and higher are supported)"
- [readme] For parallel processing of multiple spectra or/and sequence files, MetaMiner requires `joblib` Python library: "For parallel processing of multiple spectra or/and sequence files, MetaMiner requires `joblib` Python library"
