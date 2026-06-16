# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] How do the four samples (test1, test2, ctrl1, ctrl2) cluster based on methylation similarity, and what are their relationships in principal component space?: 'We can cluster the samples based on the similarity of their methylation profiles. The following function will cluster the samples and draw a dendrogram.'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] clusterSamples() produces a dendrogram showing sample clustering by correlation distance with Ward linkage, and PCASamples() generates a scree plot and PC1/PC2 scatter plot revealing methylation profile relationships among the four samples.: 'clusterSamples(meth, dist="correlation", method="ward", plot=TRUE)
```

Setting the `plot=FALSE` will return a dendrogram object which can be
manipulated by users or fed in to other user functions'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] methylBase object from unite() on example CpG files: 'From the united methylBase object produced by unite() on the example CpG files'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Dendrogram object showing hierarchical clustering of samples: 'run clusterSamples() to obtain a dendrogram'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Scree plot showing variance explained by each principal component (PNG or PDF): 'PCASamples() to obtain a scree plot'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] PC1/PC2 scatter plot visualization (PNG or PDF): 'PC1/PC2 scatter'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] methylKit: 'title: "methylKit: User Guide'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] R: 'packageVersion('methylKit')'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] knitr: '%\VignetteEngine{knitr::rmarkdown}'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog found.: '_No changelog found._'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] No detailed methods section content provided; only vignette header and setup code present.: 'Document contains only vignette header and setup code, no methods section text'
