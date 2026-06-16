# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] What is the complete computational workflow for detecting and ranking molecular adducts in mass spectrometry imaging data using the mass2adduct package?: 'This package presents tools for counting and identifying possible adducts in MS data'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] The mass2adduct package implements a pipeline that computes mass difference objects, builds histograms of those differences, matches them to known adducts using adductMatch(), and ranks results with topAdducts() to identify the most abundant adducts.: 'd.diff <- massdiff(d) # Returns object of classes data.frame and massdiff; d.diff.hist <- hist(d.diff); The following function looks for known adducts by finding the closest-matching bin in the mass'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Preprocessed MSI data matrix in CSV format with m/z values as column headers and pixel intensities as entries: 'This should be exported as plain-text CSV files from standard MSI software such as SCiLS or MSiReader.'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Built-in adducts reference dataset listing biologically-relevant chemical species (name, formula, mass columns): 'There are two built-in data sets `adducts` and `adducts2` (shorter), which list biologically-relevant chemical species that might occur in biological samples.'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Mass difference histogram object (massdiffhist class) showing distribution of pairwise m/z differences with labeled peaks for known adducts: 'd.diff.hist <- hist(d.diff) # Object of classes histogram and massdiffhist'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Table of top-ranked mass differences with occurrence counts, quantiles, and matches to known adducts from adductMatch() output: 'The following function looks for known adducts by finding the closest-matching bin in the mass difference histogram produced above. It reports the number of counts (i.e. how many pairs of MS peaks'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Annotated massdiff object with added 'matches' column indicating closest-matching adduct for each ion pair: 'We can match massdiffs to specific adduct types using the same function `adductMatch` that we applied to the histogram above. This adds an additional column to the `massdiff` object called `matches`,'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] mass2adduct: 'This package presents tools for counting and identifying possible adducts in MS data'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] R: 'library(mass2adduct)'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog or version history documented: '_No changelog found._'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] Specific package version or commit hash for reproducibility: 'Source: github:kbseah__mass2adduct'
