---
name: spectral-network-propagation-analysis
description: Use when after running MetaMiner's Dereplicator stage to identify some RiPPs via direct database matching against a constructed structure database, apply this skill to enlarge the set of identifications by propagating those matches through spectral clusters and visualizing the connected components.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3938
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
  tools:
  - MetaMiner
  - NPDtools 2.5.0
  - GNPS Spectral Networking / Molecular Networking
  - matplotlib
  - networkx
  - Dereplicator
  - ProteoWizard
derived_from:
- doi: 10.1038/s41467-018-06082-8
  title: dereplicator
evidence_spans:
- MetaMiner is a metabologenomic pipeline which integrates metabolomic (tandem mass spectra) and genomic data to identify novel RiPPs
- MetaMiner is a metabologenomic pipeline which integrates metabolomic (tandem mass spectra) and genomic data to identify novel Ribosmally synthesized and Post-translationally modified Peptides (RiPPs)
- The latest version is available in the Natural Product Discovery toolkit (NPDtools) at https://github.com/ablab/npdtools
- Spectral network can be easily run through GNPS. Detailed instructions can be found in the [GNPS documentation]
- For presenting Spectral Network propagation graphs, MetaMiner also requires `matplotlib` and `networkx` Python libraries
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

# spectral-network-propagation-analysis

## Summary

Enlarge and visualize identified RiPP (ribosomally synthesized and post-translationally modified peptide) identifications by propagating spectral networking results through connected clusters of tandem mass spectra. This skill uses molecular networking to extend peptide discovery beyond direct database matches by leveraging spectral similarity relationships.

## When to use

After running MetaMiner's Dereplicator stage to identify some RiPPs via direct database matching against a constructed structure database, apply this skill to enlarge the set of identifications by propagating those matches through spectral clusters and visualizing the connected components of significant PSM (peptide spectrum matches) in the molecular network.

## When NOT to use

- No spectral network has been pre-computed for your mass spectrometry data; you must first run GNPS Spectral Networking on your spectra files.
- Your input spectra are not in a ProteoWizard-supported format (MGF, mzXML, mzML, mzData) and cannot be converted; spectral networking requires standardized centroided MS/MS data.
- You have not yet identified at least some RiPP matches via Dereplicator or direct database search; propagation requires initial seed matches to propagate through the network.

## Inputs

- mzML spectra files (or other ProteoWizard-supported LC-MS/MS formats)
- Unpacked spectral network directory (ProteoSAFe-METABOLOMICS-SNETS-V2 archive structure)
- RiPP precursor peptide FASTA file
- MetaMiner output or pre-computed Dereplicator results

## Outputs

- propagations.pdf (graphical report with one page per connected component of significant PSM)
- propagations_detailed.txt (detailed text report listing all spectra from same cluster and clusters at distance 1 and 2)
- propagations_short.txt (same as detailed but with one representative per cluster)
- spec_nets output folder within MetaMiner output directory

## How to apply

Provide MetaMiner with the unpacked spectral network output directory (generated from GNPS Spectral Networking / Molecular Networking, e.g., ProteoSAFe-METABOLOMICS-SNETS-V2 format) via the --spec-network flag, along with the tandem mass spectrometry files and RiPP precursor sequence FASTA. MetaMiner will propagate initial Dereplicator hits through the spectral network by identifying spectra in the same cluster and clusters at distance 1 and 2 from matched spectra. The propagation reports are generated in three forms: (1) propagations.pdf for graphical visualization with one page per connected component, (2) propagations_detailed.txt listing all spectra per cluster with remote clusters, and (3) propagations_short.txt with one representative per cluster. Ensure matplotlib and networkx Python libraries are installed for PDF graph generation; without them, output is plain text only.

## Related tools

- **MetaMiner** (Orchestrates spectral network propagation; accepts --spec-network flag to point to unpacked spectral network directory and generates propagation reports) — https://github.com/mohimanilab/MetaMiner
- **GNPS Spectral Networking / Molecular Networking** (Pre-computes spectral network (molecular network) structure from tandem mass spectra; output must be unpacked and passed to MetaMiner)
- **Dereplicator** (Identifies initial RiPP matches against structure database; these seed matches are then propagated through the spectral network) — https://github.com/ablab/npdtools
- **matplotlib** (Renders spectral network propagation graphs as PDF visualizations; required for graphical output; falls back to plain text if absent)
- **networkx** (Analyzes and traverses the spectral network graph structure to identify connected components and propagate matches; required for graph rendering)
- **ProteoWizard** (Converts tandem mass spectrometry data to MGF format for spectral networking and MetaMiner analysis)

## Examples

```
python metaminer.py test_data/metaminer/msms/ -s test_data/metaminer/molnet/example_RiPP.fasta --blind --spec-network test_data/metaminer/molnet/ProteoSAFe-METABOLOMICS-SNETS-V2-unpacked -o metaminer_outdir
```

## Evaluation signals

- spec_nets output folder is created within the MetaMiner output directory; its absence indicates the --spec-network flag was not applied or the spectral network path is incorrect
- propagations.pdf contains at least one page per connected component of significant PSM; visual inspection confirms matches are grouped by spectral similarity
- propagations_detailed.txt and propagations_short.txt are non-empty and list representative spectra with consistent cluster identifiers; verify that distance-1 and distance-2 neighbors are populated for each match
- The number of RiPP identifications in the propagation reports exceeds the number of Dereplicator seed matches, confirming that spectral propagation enlarged the identification set
- All spectra listed in propagation reports are present in the input spectral network; cross-check spectrum IDs against the ProteoSAFe-METABOLOMICS-SNETS-V2 metadata

## Limitations

- Spectral network propagation is only as accurate as the GNPS Spectral Networking clustering; poor quality or noisy spectra may produce spurious connections and false propagations
- Propagation relies on initial seed matches from Dereplicator; if few or no RiPPs are initially matched, the propagation set will be small regardless of network quality
- Graph visualization (PDF output) requires matplotlib and networkx; environments without these libraries will only produce plain text reports, limiting interpretability
- The --blind flag used for demonstration purposes may reduce specificity; production runs should use appropriate enzymatic cleavage rules and precursor mass tolerance settings
- Distance-based propagation (clusters at distance 1 and 2) is fixed by the implementation; no user-adjustable distance threshold is exposed to control propagation breadth

## Evidence

- [other] The MetaMiner pipeline includes a spectral networking stage that enlarges the set of identified RiPPs via spectral networking and allows users to visualize the results after identifying some RiPPs.: "spectral networking stage that enlarges the set of identified RiPPs via spectral networking and allows users to visualize the results"
- [other] Execute MetaMiner with the --spec-network option pointing to the unpacked spectral network directory, the example RiPP FASTA file (DATITTVTVTSTSIWASTVSNHC), and the --blind flag for demonstration purposes: python metaminer.py <spectra_files> -s test_data/metaminer/molnet/example_RiPP.fasta --blind --spec-network test_data/metaminer/molnet/ProteoSAFe-METABOLOMICS-SNETS-V2-unpacked -o metaminer_outdir.: "Execute MetaMiner with the --spec-network option pointing to the unpacked spectral network directory"
- [other] Verify that the spec_nets output folder is created within metaminer_outdir containing the three required output files: propagations.pdf (graphical report with one page per connected component of significant PSM), propagations_detailed.txt (detailed text report listing all spectra from same cluster and clusters at distance 1 and 2), and propagations_short.txt (same as detailed but with one representative per cluster).: "propagations.pdf (graphical report with one page per connected component of significant PSM), propagations_detailed.txt (detailed text report listing all spectra from same cluster and clusters at"
- [readme] For presenting Spectral Network propagation graphs, MetaMiner requires `matplotlib` and `networkx` Python libraries. If they are not installed, the propagation will be generated in a plain text format only (see `--spec-network` option).: "MetaMiner requires `matplotlib` and `networkx` Python libraries. If they are not installed, the propagation will be generated in a plain text format only"
- [other] (iv) enlarges the set of described RiPPs via spectral networking: "enlarges the set of described RiPPs via spectral networking"
