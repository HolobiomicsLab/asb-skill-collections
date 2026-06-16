# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] How does NPLinker orchestrate the integration of antiSMASH/BiG-SCAPE genomic outputs and GNPS metabolomic outputs to create and rank hypothetical BGC-metabolite links?: 'NPLinker accepts genomic outputs from antiSMASH and BiG-SCAPE (including reference BGCs from the MIBiG database [32]), and metabolomic output from the public, community-driven Global Natural Products'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] NPLinker creates objects for spectra, MFs, BGCs and GCFs from input data while maintaining hierarchical relationships and strain associations, then generates hypothetical links between metabolomic and genomic objects that can be evaluated using various scoring functions (both built-in and custom) and sorted, filtered, and visualized in tabular format.: 'NPLinker creates objects for spectra, MFs, BGCs and GCFs in the data set, maintaining the hierarchical relationship between them, and keeps track of strain ID or IDs associated with each object.'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] antiSMASH v5.0.0 BGC predictions (JSON or GenBank format) from microbial genome assemblies: 'after downloading the strain assemblies and metabolomics data, the genomes were run through antiSMASH v5.0.0 for BGC detection'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] GNPS metabolomic data: MS2 spectra with strain annotations and molecular families from spectral clustering: 'metabolomic output from the public, community-driven Global Natural Products Social (GNPS) knowledge base [33]'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] MIBiG database reference BGCs with structural annotations for homology scoring: 'BGCs from the relevant strains show significant homology to the MIBiG BGC. Because both of them belong to the product class'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Ranked hypothetical link table (CSV or TSV) with GCF ID, MF ID, standardised strain correlation score, IOKR score, combined ℓ₁/₂ score, and metadata (strain count, BGC size, product type) sorted by combined score: 'links can be sorted, inspected and filtered by various scoring functions or combinations thereof, and visualised as tables'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] NPLinker link objects and metadata structure (JSON or Python pickle) persisting GCF–MF and BGC–spectrum relationships with associated scores: 'NPLinker creates objects for spectra, MFs, BGCs and GCFs in the data set, maintaining the hierarchical relationship between them'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Filtering and ranking statistics: count of links scoring above 90th percentile for each scoring function and their intersections: 'links scoring above the 90th percentile for raw correlation, standardised correlation and IOKR scores'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] antiSMASH: 'the genomes were run through antiSMASH v5.0.0 for BGC detection'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] BiG-SCAPE: 'and BiG-SCAPE v1.0.0 to cluster the BGCs into GCFs'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] NPLinker: 'NPLinker creates objects for spectra, MFs, BGCs and GCFs in the data set'

## ev_012

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] GNPS: 'metabolomic output from the public, community-driven Global Natural Products Social (GNPS) knowledge base'

## ev_013

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] MIBiG: 'MIBiG database [32] most of which have structural annotations'

## ev_014

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] Specific file format and schema for antiSMASH output ingested by NPLinker (GenBank, JSON, or other): 'By pairing the MIBiG and GNPS databases, and using the Paired omics Data Platform, we introduced data sets to test the efficiency of the scoring methods'

## ev_015

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] Specific file format and schema for BiG-SCAPE output ingested by NPLinker (cluster assignment table or other): 'By pairing the MIBiG and GNPS databases, and using the Paired omics Data Platform, we introduced data sets to test the efficiency of the scoring methods'

## ev_016

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] Specific file format and schema for GNPS metabolomic data ingested by NPLinker (spectrum library metadata, MS/MS spectra in mzXML/mzML or other): 'By pairing the MIBiG and GNPS databases, and using the Paired omics Data Platform, we introduced data sets to test the efficiency of the scoring methods'

## ev_017

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] Details on how NPLinker resolves the 'antiSMASH mapping the same ID to multiple GCFs' edge case during orchestration: 'antiSMASH mapping the same ID to multiple GCFs, as discussed earlier'

## ev_018

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] Computational time complexity and memory requirements for the NPLinker orchestration loop (BGC-spectrum enumeration, strain correlation computation, IOKR scoring): 'As a denoising step, to avoid time-consuming computation of fragmentation trees for the spectra'

## ev_019

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] Quantitative measure of homology threshold used to assign MIBiG structures to BGCs for IOKR candidate set filtering: 'restricts its use to those BGCs which show considerable homology with MIBiG entries'

## ev_020

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] Specific kernel function (PPK parameters, bandwidth, or other hyperparameters) used in the IOKR component of NPLinker: 'IOKR is also highly dependent on the choice of both kernel function and molecular fingerprints'

## ev_021

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] Specific molecular fingerprint algorithm and parameters used in the IOKR component of NPLinker: 'IOKR is also highly dependent on the choice of both kernel function and molecular fingerprints'

## ev_022

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] Documented validation workflow or test suite for verifying NPLinker orchestration correctness on known positive and negative link sets: 'As an additional level of validation, we tested some high scoring links by exploring whether it was possible to manually match peaks in the MS2 spectra to the chemical structures'
