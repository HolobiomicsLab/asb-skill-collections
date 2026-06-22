---
name: ribosomally-synthesized-peptide-identification
description: Use when you have LC-MS/MS spectral data (in MGF, mzXML, mzML, or mzData format) and corresponding genomic sequence data (raw FASTA nucleotide sequences or genome mining tool outputs like antiSMASH .final.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3646
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0080
  tools:
  - NPDtools 2.5.0
  - MetaMiner
  - Dereplicator
  - ProteoWizard
  - NPDtools
  - joblib
  - antiSMASH
  - SPAdes
  techniques:
  - LC-MS
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

# ribosomally-synthesized-peptide-identification

## Summary

Identify ribosomally synthesized and post-translationally modified peptides (RiPPs) by integrating metabolomic tandem mass spectra with genomic sequence data using MetaMiner, a metabologenomic pipeline that constructs putative RiPP structure databases and matches them against experimental spectra.

## When to use

You have LC-MS/MS spectral data (in MGF, mzXML, mzML, or mzData format) and corresponding genomic sequence data (raw FASTA nucleotide sequences or genome mining tool outputs like antiSMASH .final.gbk files), and you want to discover novel RiPPs or verify the presence of known RiPP compounds (e.g., lantibiotics, thiopeptides, linear azol(in)e-containing peptides) by matching spectra against computationally predicted post-translationally modified peptide structures derived from biosynthetic gene clusters.

## When NOT to use

- Your spectra are not centroided — MetaMiner requires centroided data; raw profile-mode spectra will produce incorrect or no matches.
- You lack corresponding genomic data or only have protein sequence databases — MetaMiner is a metabologenomic pipeline and requires nucleotide sequences to identify biosynthetic gene clusters and predict precursor peptides.
- You are working with non-peptidic natural products or small molecules — MetaMiner is specialized for RiPPs; use Dereplicator+ instead for broader metabolite identification.

## Inputs

- LC-MS/MS spectral data in centroided MGF, mzXML, mzML, or mzData format
- Raw nucleotide sequence file in FASTA format (.fasta)
- Optional: antiSMASH genome mining output (.final.gbk or .gbk file)

## Outputs

- significant_matches.tsv (tab-separated file with compound identifications)
- Identified RiPP structures with predicted core peptide sequences (FragmentSeq)
- Modified peptide sequences (ModifiedSeq) showing post-translational modifications
- Spectral network graphs (if matplotlib and networkx are installed) or plain text propagation results

## How to apply

Download and extract NPDtools 2.5.0 binaries for your platform (Linux or macOS), ensuring Python 2.6–3.3+ and the joblib library are available. Prepare input files: obtain your centroided spectra in MGF format (or convert via ProteoWizard's msconvert if in mzXML/mzML/mzData format) and your genomic sequence as a raw nucleotide FASTA file (preferred over antiSMASH outputs, which may fail to detect some RiPPs). Run MetaMiner with the command: `python metaminer.py <spectra_directory_or_files> -s <path_to_genome.fasta> -c <ripp_class> -o <output_directory>`, specifying the RiPP class (e.g., 'lantibiotic', 'thiopeptide', 'lanthipeptide') appropriate to your discovery target. Parse the tab-separated output file (significant_matches.tsv) to extract compound identifications, verifying the presence of your target RiPP by matching the FragmentSeq column against the expected core peptide sequence and confirming ModifiedSeq shows expected post-translational modifications (e.g., dehydrobutyrine/dehydroalanine mass shifts for lantibiotics).

## Related tools

- **MetaMiner** (Core metabologenomic pipeline that integrates tandem mass spectra and genomic data to identify RiPPs; constructs predicted RiPP structure databases from identified biosynthetic gene clusters and matches experimental spectra against them) — https://github.com/mohimanilab/MetaMiner
- **Dereplicator** (Matches tandem mass spectra against constructed post-translationally modified RiPP structure database within the MetaMiner workflow) — https://github.com/ablab/npdtools
- **antiSMASH** (Optional genome mining tool whose output (.final.gbk or .gbk files) can be used as alternative input to raw FASTA sequences, though raw nucleotide FASTA is preferred for lantibiotic discovery)
- **SPAdes** (Assembles raw DNA short reads (.fastq or .fastq.gz) into nucleotide contigs that can then be used as input to MetaMiner)
- **ProteoWizard** (Provides msconvert utility to convert spectra from mzXML, mzML, mzData formats to MGF for MetaMiner compatibility)
- **NPDtools 2.5.0** (Toolkit containing MetaMiner and all supporting binaries and libraries for RiPP identification) — https://github.com/ablab/npdtools

## Examples

```
python metaminer.py test_data/metaminer/msms/ -s test_data/metaminer/fasta/ -c lantibiotic -o metaminer_outdir
```

## Evaluation signals

- Presence of significant_matches.tsv output file with non-empty results rows containing target RiPP identifications
- FragmentSeq column matches the expected core peptide sequence (e.g., 'TGSQVSLLVCEYSSLSVVLCTP' for AmfS lantibiotic)
- ModifiedSeq shows expected post-translational modification mass shifts (e.g., T-18 and S-18 shifts for dehydrobutyrine and dehydroalanine in lantibiotics)
- Match score or significance metric in output meets or exceeds default threshold (verify against significant_matches.tsv header documentation)
- Spectra can be traced back to genomic locations via biosynthetic gene cluster annotations in output

## Limitations

- MetaMiner fails to detect some RiPPs (e.g., AmfS) when using antiSMASH genome mining tool outputs (.final.gbk files) as input; raw nucleotide FASTA sequences are required for reliable lantibiotic discovery.
- Spectra must be centroided; raw profile-mode data is not supported.
- Requires 64-bit Linux or macOS system; Windows is not natively supported.
- RiPP class must be specified a priori (e.g., lantibiotic, thiopeptide); blind discovery across all RiPP classes is not explicitly documented.
- Spectral network visualization requires matplotlib and networkx Python libraries; without them, results are output in plain text only.
- No changelog is available for version 2.5.0, limiting visibility into bug fixes or improvements relative to prior versions.

## Evidence

- [other] MetaMiner successfully detects AmfS using contigs.fasta genome files, though it fails when using antiSMASH results as input, indicating that raw nucleotide sequence format supports lantibiotic discovery.: "While `MetaMiner` successfully detect AmfS using the `contigs.fasta` file, it fails with antiSMASH result as input"
- [readme] MetaMiner integrates metabolomic and genomic data to identify RiPPs by identifying putative biosynthetic gene clusters, constructing RiPP structure databases, matching spectra against them, and enlarging the RiPP set via spectral networking.: "MetaMiner (i) identifies putative BGCs and the corresponding precursor peptides (ii) constructs putative RiPP structure databases (iii) matches tandem mass spectra against the constructed"
- [readme] MetaMiner accepts raw nucleotide FASTA sequences or genome mining tool outputs (antiSMASH .final.gbk or .gbk, BOA .annotated.txt files) as input.: "MetaMiner uses either raw nucleotide sequences or specific genome mining tools' output: raw nucleotide sequences `.fasta` format or *antiSMASH*'s `.final.gbk` or `.gbk` file"
- [readme] Spectra files must be centroided and in open formats; MetaMiner natively supports MGF, mzXML, and mzData, and can convert other formats via ProteoWizard.: "Spectra files must be centroided and be in an open spectrum format (**MGF**, **mzXML**, **mzML** or **mzData**). NPDtools natively supports MGF and mzXML/mzData (our parser is based on"
- [readme] MetaMiner requires Python 2.6–3.3+ and the joblib library for parallel processing on 64-bit Linux or macOS systems.: "NPDtools requires a 64-bit Linux system or macOS and Python2 or Python3 to be pre-installed on it (versions 2.6-2.7, 3.3 and higher are supported). For parallel processing of multiple spectra files,"
- [other] Verification of identified RiPPs involves checking the FragmentSeq column for matching the expected core peptide sequence and confirming ModifiedSeq shows expected post-translational modifications.: "verifying presence of AmfS by FragmentSeq column matching 'TGSQVSLLVCEYSSLSVVLCTP' and ModifiedSeq showing dehydrobutyrine/dehydroalanine modifications (T-18 and S-18 mass shifts)"
