# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] How does the genFragEntry function process an experimental MS/MS spectrum to generate a metabolite library entry by applying peak-picking thresholds and occurrence scoring?: 'This function will attribute occurrence scores to the peaks above *mpeaksThres* threshold ("marker peaks") and above the noise level.'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] genFragEntry converts an MS/MS spectrum into a library entry by identifying marker peaks above the mpeaksThres threshold (0.1 default) and noise level (0.005 default), attributing occurrence scores to these peaks, with parameters including mpeaksScore=0.9, mzTol=0.01, and requires explicit definition of metabolite name, adduct notation, accurate adduct m/z, and output filename.: 'This function will attribute occurrence scores to the peaks above *mpeaksThres* threshold ("marker peaks") and above the noise level. Note that metabolite name, adduct name, accurate adduct m/z and'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] D-Pantothenic Acid MS/MS spectrum from MassBank accession MSBNK-RIKEN-PR100295: 'MS/MS spectrum of D-Pantothenic Acid [M+H]+ adduct from MassBank, accession code: MSBNK-RIKEN-PR100295'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] CSV library entry containing annotated fragments with mass-to-charge, intensity, and fragment match scores: 'MetaboAnnotatoR is designed to perform metabolite annotation of features from LC-MS All-ion fragmentation (AIF) datasets, using ion fragment databases'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] MetaboAnnotatoR: 'MetaboAnnotatoR is designed to perform metabolite annotation of features from LC-MS All-ion fragmentation (AIF) datasets'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] R: 'To install this package, start R (version "4.5.0" or higher)'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog found: 'No changelog found.'
