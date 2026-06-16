# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] What is the distribution of IOKR scores across all 2966 MIBiG-GNPS BGC-spectrum pairs, and how do validated links rank within this distribution?: 'The MIBiG/GNPS data set consists of sets of associated BGC, metabolite and spectrum... we tested the method on the paired MIBiG/GNPS data by matching each spectrum to the candidate set consisting of'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] IOKR achieves a mean score of 0.0105 for all 2966 BGC-spectrum links and 0.0364 for validated links (p=1.7968 × 10−9), with top-1 accuracy of 0.1208, top-5 accuracy of 0.1708, and AUC of 0.6534 compared to a random baseline AUC of 0.5209.: 'IOKR: 0.0105 (all), 0.0364 (validated), p-value 1.7968 × 10−9... Table 3 shows the top-n performance of IOKR: top-1: 0.1208, top-5: 0.1708, top-10: 0.1870... AUC of 0.6534 compared to 0.5209 for the'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] GNPS library MS2 spectra with structural annotations (4138 spectra): 'we use library MS2 spectra from the public, community-driven GNPS knowledge base [33] as a training set for the IOKR model. We use the same training data set as Brouard and co-workers [26], which'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] MIBiG database entries with structural annotations (SMILES/InChI format): 'Molecular fingerprints are extracted from SMILES strings using the Chemistry Development Kit [29]. The fingerprint vector is composed of three concatenated sets of fingerprints: CDK Substructure,'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] MIBiG-GNPS paired BGC-spectrum dataset (2966 pairs): 'This yields 2966 BGC-spectrum pairs, each with an associated metabolite, which can be used to evaluate the IOKR model proposed in this paper. These pairs include 2069 unique spectra and 242 unique'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] MS2 spectral data from GNPS for evaluation (6246 spectra restricted to those with structure predictions): 'Out of 3316 BGCs in the data set, 2242 could be assigned structure based on similarity to MIBiG entries, and used as candidate set for the 6246 MS2 spectra in the data set'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] IOKR model object with learned mapping from MS2 spectrum kernel space to molecular fingerprint space: 'This mapping, along with the function mapping molecular structures to fingerprints, is then used to project similarities in the input space of spectra and the output space (molecular structures) to'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Ranked list of candidate BGCs for each of 2966 MS2 spectra with IOKR scores: 'For each spectrum, IOKR returns an ordered list of all metabolites in the candidate set'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Top-n accuracy metrics (top-1, top-5, top-10, top-20, top-200) and AUC score for IOKR on MIBiG-GNPS pairs: 'Table 3 shows the top-n performance of IOKR, i.e. how often the 'true' BGC match for a given spectrum is among the top n matches returned by IOKR, for a selection of n'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Distribution histogram of IOKR scores for all 2966 BGC-spectrum pairs with validated links highlighted: 'we can observe the distribution of the scores for the validated links among the scores for all potential links. The upper end of the distribution for the IOKR score contains a relatively high'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Mean IOKR score for all links (0.0105) and for validated links (0.0364) with statistical significance (p-value): 'the mean score of 0.0105 for all links and 0.0364 for validated links (Table 1). Results for other data sets can be found in Table C in S1 Text'

## ev_012

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] GNPS: 'we use library MS2 spectra from the public, community-driven GNPS knowledge base [33] as a training set for the IOKR model'

## ev_013

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] MIBiG: 'Molecular fingerprints are extracted from SMILES strings using the Chemistry Development Kit'

## ev_014

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Chemistry Development Kit (CDK): 'Molecular fingerprints are extracted from SMILES strings using the Chemistry Development Kit [29]'

## ev_015

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Probability Product Kernel (PPK): 'we filter the input spectra to include only the peaks found in the training data, before using the Probability Product Kernel (PPK)'

## ev_016

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] antiSMASH: 'after downloading the strain assemblies and metabolomics data, the genomes were run through antiSMASH v5.0.0 for BGC detection'

## ev_017

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] exact kernel function type (e.g., Probability Product Kernel, polynomial, RBF) and hyperparameter values (bandwidth, degree) used for IOKR model training on GNPS 4138-spectrum set: 'IOKR is also highly dependent on the choice of both kernel function and molecular fingerprints'

## ev_018

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] specific molecular fingerprint type, dimensionality, and construction method (e.g., Morgan fingerprints, MACCS keys, CDK fingerprints, radius/bit-length parameters) used in IOKR scoring: 'IOKR is also highly dependent on the choice of both kernel function and molecular fingerprints'

## ev_019

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[abstract] detailed denoising/filtering procedure applied to spectra before IOKR training and scoring (peak intensity threshold, noise removal method, spectral normalization protocol): 'As a denoising step, to avoid time-consuming computation of fragmentation trees for the spectra'

## ev_020

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[abstract] number of training spectra retained after peak filtering step (spectra with peaks found in training data only) before IOKR model fitting: 'we filter the input spectra to include only the peaks found in the training data, before using the Probability Product Kernel (PPK)'

## ev_021

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] exact cross-validation or train-test split strategy used for IOKR model development on GNPS training set; whether performance metrics in Table 3 are from held-out test set or resubstitution: 'The training set used to build the IOKR model includes metabolites from sources other than microbial'

## ev_022

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] computational resource requirements and runtime for IOKR model training on 4138-spectrum set and scoring 2966 pairs (memory, CPU/GPU time, software version specifics): '[not present in provided section text]'
