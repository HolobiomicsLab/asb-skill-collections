# Evaluation Strategy

## Direct Checks

- verify file EPICSimData is loadable via R command data(EPICSimData) within the ChAMP package environment
- verify champ.DMR() function exists and is callable in the loaded ChAMP package
- verify script_runs: R script executing data(EPICSimData); dmr_result <- champ.DMR(EPICSimData, method='bumphunter') completes without error
- verify output_matches_reference: the number of detected DMRs returned by champ.DMR() with bumphunter method falls in the range of approximately 4700 or higher, as reported for bumphunter-based simulation (exact boundary parameter-sensitive; multiple defensible thresholds near 4700 defensible)
- verify the dmr_result object contains a structured field or slot reporting total DMR count as a single numeric value

## Expert Review

- expert review of whether the DMR detection result is biologically plausible and consistent with stated bumphunter simulation benchmark
- expert review of whether champ.DMR() with method='bumphunter' on EPICSimData produces output structure and semantics expected for DMR detection (regions properly defined, statistical support present)
