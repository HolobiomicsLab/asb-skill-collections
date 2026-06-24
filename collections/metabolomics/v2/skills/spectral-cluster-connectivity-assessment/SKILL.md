---
name: spectral-cluster-connectivity-assessment
description: Use when after running spectral networking on tandem MS data and obtaining
  a network graph, when you need to assess which spectra cluster together, determine
  cluster representatives, and propagate RiPP identifications across clusters at distance
  1 or 2 to enlarge the set of identified RiPPs beyond.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0226
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0202
  tools:
  - MetaMiner
  - NPDtools 2.5.0
  - GNPS Spectral Networking / Molecular Networking
  - matplotlib
  - networkx
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1038/s41467-018-06082-8
  title: dereplicator
evidence_spans:
- MetaMiner is a metabologenomic pipeline which integrates metabolomic (tandem mass
  spectra) and genomic data to identify novel RiPPs
- MetaMiner is a metabologenomic pipeline which integrates metabolomic (tandem mass
  spectra) and genomic data to identify novel Ribosmally synthesized and Post-translationally
  modified Peptides (RiPPs)
- The latest version is available in the Natural Product Discovery toolkit (NPDtools)
  at https://github.com/ablab/npdtools
- Spectral network can be easily run through GNPS. Detailed instructions can be found
  in the [GNPS documentation]
- For presenting Spectral Network propagation graphs, MetaMiner also requires `matplotlib`
  and `networkx` Python libraries
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

# spectral-cluster-connectivity-assessment

## Summary

Assessment and visualization of spectral cluster connectivity in molecular networking to identify related natural product identifications and propagate RiPP assignments across spectra in the same cluster or adjacent clusters. This skill evaluates how spectral networking enlarges the set of identified metabolites by linking related mass spectra and reporting cluster-level and inter-cluster relationships.

## When to use

Apply this skill after running spectral networking on tandem MS data and obtaining a network graph, when you need to assess which spectra cluster together, determine cluster representatives, and propagate RiPP identifications across clusters at distance 1 or 2 to enlarge the set of identified RiPPs beyond initial dereplication results.

## When NOT to use

- Spectral networking has not been run or the ProteoSAFe network output archive is unavailable; use raw spectra for spectral networking first.
- Input spectra are not centroided or are in unsupported formats (not mzML, mzXML, mzData, or MGF); convert using ProteoWizard msconvert first.
- No RiPP FASTA sequences are available or the FASTA file is empty; dereplication and cluster connectivity assessment require valid precursor sequences.

## Inputs

- mzML spectra files (centroided tandem MS data)
- Unpacked spectral network directory from GNPS ProteoSAFe-METABOLOMICS-SNETS-V2 archive
- Example RiPP FASTA file with precursor peptide sequences
- MetaMiner command-line parameters (--spec-network, --blind flags)

## Outputs

- propagations.pdf (graphical report with connected components and significant PSM clusters)
- propagations_detailed.txt (text report listing all spectra per cluster and distance-1/distance-2 neighboring clusters)
- propagations_short.txt (condensed text report with one representative per cluster)
- spec_nets output folder (directory containing the three report files)

## How to apply

Execute MetaMiner with the --spec-network flag, providing the unpacked spectral network directory (e.g., ProteoSAFe-METABOLOMICS-SNETS-V2 output), an example RiPP FASTA file (such as DATITTVTVTSTSIWASTVSNHC), and the --blind flag for demonstration. MetaMiner will construct a spectral network graph and generate three complementary outputs: propagations.pdf (graphical report with one page per connected component showing significant PSM clusters), propagations_detailed.txt (text listing all spectra per cluster and clusters at distance 1 and 2), and propagations_short.txt (same information with one representative per cluster). Use matplotlib and networkx libraries to render the graphical report; if unavailable, outputs are generated in plain text format only. Verify that the spec_nets output folder exists and contains all three files to confirm successful propagation assessment.

## Related tools

- **MetaMiner** (Metabologenomic pipeline that integrates spectral networking results and propagates RiPP identifications across connected spectra using spectral clustering) — https://github.com/mohimanilab/MetaMiner
- **GNPS Spectral Networking / Molecular Networking** (Generates the spectral network graph (ProteoSAFe-METABOLOMICS-SNETS-V2 output) that clusters related mass spectra for input to MetaMiner)
- **matplotlib** (Renders graphical propagation report (propagations.pdf) showing connected components and cluster relationships)
- **networkx** (Constructs and analyzes the spectral network graph to identify clusters and inter-cluster distances)
- **NPDtools 2.5.0** (Toolkit containing MetaMiner and associated utilities for metabologenomic pipeline execution) — https://github.com/ablab/npdtools

## Examples

```
python metaminer.py test_data/metaminer/msms/ -s test_data/metaminer/molnet/example_RiPP.fasta --blind --spec-network test_data/metaminer/molnet/ProteoSAFe-METABOLOMICS-SNETS-V2-unpacked -o metaminer_outdir
```

## Evaluation signals

- The spec_nets output folder is created within the MetaMiner output directory and contains all three required files (propagations.pdf, propagations_detailed.txt, propagations_short.txt).
- propagations.pdf contains one page per connected component of significant PSM clusters, with visible network graph representations.
- propagations_detailed.txt lists all spectra from the same cluster and includes clusters at distance 1 and 2, demonstrating cluster connectivity assessment.
- propagations_short.txt contains the same information as the detailed report but with exactly one representative spectrum per cluster, indicating successful cluster summarization.
- RiPP identifications are propagated across clusters, enlarging the set of identified RiPPs beyond initial dereplication results (verify by comparing pre- and post-spectral-networking RiPP counts).

## Limitations

- Graphical propagation reports (propagations.pdf) require matplotlib and networkx Python libraries; if unavailable, propagation is generated in plain text format only, limiting visual assessment of network topology.
- The skill depends on the quality and completeness of the input spectral network from GNPS; sparse or incomplete networks may result in suboptimal cluster connectivity and reduced RiPP propagation.
- Spectral clustering and distance-based propagation (distance 1 and 2) are sensitive to the parameters used in the original GNPS spectral networking run; parameter mismatches may affect cluster membership and connectivity assessment.

## Evidence

- [methods] The MetaMiner pipeline includes a spectral networking stage that enlarges the set of identified RiPPs via spectral networking and allows users to visualize the results after identifying some RiPPs.: "The MetaMiner pipeline includes a spectral networking stage that enlarges the set of identified RiPPs via spectral networking and allows users to visualize the results after identifying some RiPPs."
- [methods] Verify that the spec_nets output folder is created within metaminer_outdir containing the three required output files: propagations.pdf (graphical report with one page per connected component of significant PSM), propagations_detailed.txt (detailed text report listing all spectra from same cluster and clusters at distance 1 and 2), and propagations_short.txt (same as detailed but with one representative per cluster).: "Verify that the spec_nets output folder is created within metaminer_outdir containing the three required output files: propagations.pdf (graphical report with one page per connected component of"
- [readme] For presenting Spectral Network propagation graphs, MetaMiner requires `matplotlib` and `networkx` Python libraries. If they are not installed, the propagation will be generated in a plain text format only (see `--spec-network` option).: "For presenting Spectral Network propagation graphs, MetaMiner requires `matplotlib` and `networkx` Python libraries. If they are not installed, the propagation will be generated in a plain text"
- [methods] Execute MetaMiner with the --spec-network option pointing to the unpacked spectral network directory: "Execute MetaMiner with the --spec-network option pointing to the unpacked spectral network directory, the example RiPP FASTA file (DATITTVTVTSTSIWASTVSNHC), and the --blind flag"
