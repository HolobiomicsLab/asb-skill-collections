# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] What is the measured throughput of rawrr::readSpectrum in spectra per second when benchmarked on the sample raw file provided with the package?: '`rawrr:::.benchmark using rawrr::readSpectrum` spectra per second.'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] The benchmark experiment using rawrr::readSpectrum demonstrates throughput measured in spectra per second across multiple runs with varying numbers of randomly generated scan IDs, with overall runtime totaling approximately 0.5 seconds.: 'boxplot(count / runTimeInSec ~ count, data = S, log ='y', sub = paste0("Overall runtime took ", round(sum(S$runTimeInSec), 3), " seconds."))'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] 20181113_010_autoQC01.raw – example Thermo Fisher Q Exactive HF raw file with centroided, lock-mass-corrected FTMS and HCD MS2 spectra: 'The example file `20181113_010_autoQC01.raw` used throughout this manuscript contains Fourier-transformed Orbitrap spectra (FTMS) recorded on a Thermo Fisher Scientific Q Exactive HF in positive mode'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] rawrr R package with pre-compiled .NET 8.0 executable bundled including RawFileReader dynamic link library: '.NET 8.0 [@dotnet] precompiled wrapper methods are bundled, including the runtime, in the `r BiocStyle::Biocpkg('rawrr')` executable file'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Benchmark report with measured spectra-per-second throughput value from readSpectrum function execution: 'rawrr:::.benchmark using rawrr::readSpectrum'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] rawrr: 'Our .NET 8.0 [@dotnet] precompiled wrapper methods are bundled, including the runtime, in the `r BiocStyle::Biocpkg('rawrr')` executable file'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] RawFileReader: 'ThermoFisher.CommonCore dlls can be obtained through: https://github.com/thermofisherlsms/RawFileReader'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] .NET 8.0: 'In case you prefer to compile `rawrr.exe` from C# source code, please install the .NET 8.0'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No explicit reference to a published or archived benchmark result (table, figure, or deposit) containing the expected 'spectra-per-second' throughput figure is provided in the discussion section.: 'Our R package `r BiocStyle::Biocpkg('rawrr')` provides direct access to spectral data... ease-of-use does not impair performance.'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] The discussion section does not specify hardware configuration (CPU model, RAM, OS, .NET runtime version) under which the benchmark throughput should be reproduced.: 'By using vendor API methods whenever possible, we nevertheless made sure that ease-of-use does not impair performance.'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No sample raw file or instructions for obtaining it are documented in the FAQ or acknowledgements section; rawrr::sampleFilePath() is referenced but its behavior and return value are not explicitly defined.: 'f <- rawrr::sampleFilePath()'
