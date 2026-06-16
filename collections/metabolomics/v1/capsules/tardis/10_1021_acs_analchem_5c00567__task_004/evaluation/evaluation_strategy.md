# Evaluation Strategy

## Direct Checks

- verify that vignette mzML files exist in the package repository at documented location
- verify that tardisPeaks() function exists and is callable with mass_range parameter
- verify that EIC output plots are generated as files (format: PDF or PNG) when tardisPeaks() runs without scan-window separation
- verify that sawtooth artefact is visibly present in EIC plots from first run — expert judgment required on visual pattern; no canonical quantitative threshold
- verify that EIC output plots are generated as files (format: PDF or PNG) when tardisPeaks() runs with corrected mass_range argument
- verify that peak profiles in second run show absence of sawtooth artefact — expert judgment required on visual pattern comparison between runs

## Expert Review

- inspect EIC plots from tardisPeaks() without scan-window separation and confirm sawtooth artefact is present and characteristic of incorrect mass_range routing
- inspect EIC plots from tardisPeaks() with corrected mass_range argument and confirm peak profiles are clean and sawtooth pattern is eliminated
- assess whether the visual difference between the two EIC sets adequately demonstrates the effect of scan-window routing on peak profile quality
