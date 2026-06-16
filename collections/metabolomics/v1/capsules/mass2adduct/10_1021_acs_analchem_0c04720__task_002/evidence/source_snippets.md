# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] How does the corrPairsMSI() function compute pairwise correlations between ion pairs in mass spectrometry imaging data with statistical correction?: 'This performs a correlation test (by default two-tailed with Pearson's method) on each pair of peaks in the massdiff object.'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] The corrPairsMSI() function performs a two-tailed Pearson correlation test on each pair of peaks in the massdiff object to assess spatial correlation between parent and adduct ions.: 'This performs a correlation test (by default two-tailed with Pearson's method) on each pair of peaks in the massdiff object.'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Example MSI data matrix (msi.csv) with m/z values as column names, pixels as rows, and intensity values as entries: 'You can find an example CSV file in the folder `inst/extdata` in the source package. The columns represent mass peaks, with m/z values as column names, and rows represent pixels'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Built-in adducts reference dataset (adducts2) listing chemical species names, formulas, and mass values: 'There are two built-in data sets `adducts` and `adducts2` (shorter), which list biologically-relevant chemical species that might occur in biological samples'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Annotated massdiff data frame with columns A (parent ion m/z), B (adduct ion m/z), diff (mass difference), matches (adduct name), Estimate (Pearson correlation coefficient), P.value (uncorrected), and Significance (Bonferroni-corrected boolean): 'The correlation tests results will be added to the massdiff object, with three values reported: `Estimate` (correlation coefficient), `P.value`, and `Significance` (whether or not p-value is below'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] mass2adduct: 'library(mass2adduct)'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] R: 'library(mass2adduct)'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog or version history is documented.: '_No changelog found._'
