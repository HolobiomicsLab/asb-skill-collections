# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Does champ.SVD() correctly limit the number of reported principal components to a maximum of 20 when Random Matrix Theory detects more than 20 latent components in the data?: 'In champ.SVD() we used Random Matrix Theory from isva package to detect numbers of latent variables. If our method detected more than 20 components, we would select only top 20.'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] champ.SVD() implements a component capping mechanism that selects only the top 20 components when Random Matrix Theory detects more than 20 latent variables in the methylation dataset.: 'If our method detected more than 20 components, we would select only top 20.'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Normalized beta matrix from HumanMethylation450 test dataset or GSE40279: 'The 450k lung tumor data set contains only 8 samples, 4 lung tumor samples (T) and 4 control samples (C)'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] SVD analysis report with latent component count capped at 20: 'The singular value decomposition (SVD) method allows an in-depth look at batch effects'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] ChAMP: 'ChAMP package is designed for conduct DNA methylation array analysis, providing service from data loading, to final gene set enrichment analysis'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] No methods section content describing champ.SVD() implementation, Random Matrix Theory detection parameters, or component-capping logic is provided in the document.: 'Document contains only title metadata and introduction; no methods section present'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog or version-specific documentation found that would indicate when the 20-component cap was introduced or modified.: 'No changelog found.'
