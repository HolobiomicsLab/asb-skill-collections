# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Does pre-populating the @spectraVars data frame with all core spectra variable columns consume more memory than adding missing columns on-the-fly during spectraData() calls?: 'As an alternative, we could also initialize the `@spectraVars` data frame within the `backendInitialize()` method adding columns for spectra variables that are not provided by the user and require'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Pre-populating @spectraVars with all core spectra variables increases memory footprint because all variables, including those with only missing values, must be stored in the object, whereas on-the-fly initialization via fillCoreSpectraVariables() avoids storing empty columns but may be less efficient for data extraction.: 'the backend class would also have a larger memory footprint because even spectra variables with only missing values for all spectra need to be stored within the object.'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] MsBackendTest class definition with S4 slots for spectraVars (data.frame), mz (NumericList), and intensity (NumericList): 'slots = c(
             spectraVars = "data.frame",
             mz = "NumericList",
             intensity = "NumericList"
         )'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Numeric comparison table with columns: backend_variant, initial_object_size_bytes, post_spectraData_size_bytes, memory_increase_bytes, spectraData_execution_time_seconds: 'The `spectraData()` method should return the **full** spectra data within a backend as a `DataFrame` object'

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

[discussion] No changelog or version history provided: '_No changelog found._'
