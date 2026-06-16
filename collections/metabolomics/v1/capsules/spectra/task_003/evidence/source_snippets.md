# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Does the mz<- replacement method for MsBackendTest correctly validate that m/z values are increasingly sorted within each spectrum, and does it use an efficient vectorised is.unsorted() implementation on NumericList objects rather than vapply?: 'm/z values within each spectrum need to be increasingly ordered. We thus also check that this is the case for the provided m/z values. We take here the advantage that a efficient `is.unsorted()`'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] The mz<- replacement method uses the efficient is.unsorted() implementation for NumericList rather than vapply, and raises a stop error when any spectrum has unsorted m/z values: 'if (any(is.unsorted(value))) stop("m/z values need to be increasingly sorted within each spectrum")': 'if (any(is.unsorted(value)))
        stop("m/z values need to be increasingly sorted within each spectrum")'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] MsBackendTest source code from Spectra package (RforMassSpectrometry/Spectra repository): 'https://github.com/RforMassSpectrometry/Spectra/workflows/R-CMD-check-bioc'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Validation report documenting mz<- method correctness: confirmation of vectorised is.unsorted() usage, successful assignment of sorted m/z values, and error raised on unsorted input: 'm/z values within each spectrum are expected to be sorted increasingly.'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Spectra: 'The *Spectra* package defines an efficient infrastructure for storing and handling mass spectrometry spectra'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] R: 'library(Spectra)
library(IRanges)'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] S4Vectors: 'return the **full** spectra data within a backend as a `DataFrame` object (defined in the `r Biocpkg("S4Vectors")`'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog documenting the mz<- method implementation or changes to MsBackendTest: '_No changelog found._'
