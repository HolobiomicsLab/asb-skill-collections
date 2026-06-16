# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] What is the final count of feature groups after applying EIC similarity-based refinement with a correlation threshold of 0.7 on the top 2 samples, and how do the extracted ion chromatograms visually differ between sub-groups within feature groups FG.013.001 and FG.045.001?: 'The grouping based on EIC correlation on the pre-defined feature groups from the previous sections grouped the `r nrow(featureDefinitions(xmse))` features into `r length(unique(featureGroups(xmse)))`'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] After EIC similarity analysis with threshold 0.7 and n=2, features within feature groups FG.013.001 and FG.045.001 were subdivided into separate sub-groups, with one feature in FG.013.001 showing a shifted retention time in EIC plots that distinguished it from co-eluting features, and FG.045.001 being grouped into two distinct sub-groups based on EIC correlation patterns.: 'One of the features (highlighted in red in the plots above) within the original feature group was separated from the other two because of a low similarity of their EICs. In fact, the feature's EIC is'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Abundance-correlation-refined feature groups (output from AbundanceSimilarityParam refinement): 'AbundanceSimilarityParam: perform a feature grouping based on correlation of feature abundances (values) across samples.'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Final count of feature groups after EIC similarity refinement: 'EicSimilarityParam: perform a feature grouping based on correlation of EICs.'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Overlay EIC plot for feature group FG.013.001: 'plotFeatureGroups function which shows all features in the m/z - retention time space with grouped features being connected with a line.'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Overlay EIC plot for feature group FG.045.001: 'plotFeatureGroups function which shows all features in the m/z - retention time space with grouped features being connected with a line.'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] xcms: 'The *xcms* R package provides functionality to efficiently preprocess LC-MS'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] MsFeatures: 'General MS feature grouping functionality if defined by the `r Biocpkg("MsFeatures")` package'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog documenting recent changes or versions of the xcms package is available: '_No changelog found._'
