# Evaluation Strategy

## Direct Checks

- Verify file exists: locate MsBackendTest class definition in github:rformassspectrometry__Spectra repository
- Verify file_format_is: confirm MsBackendTest is an R S4 class definition
- Verify contains_substring: search MsBackendTest source code for 'mz<-' replacement method definition
- Verify contains_substring: confirm mz<- method implementation calls is.unsorted() on NumericList input
- Verify contains_substring: confirm is.unsorted() is used instead of vapply() for vectorised unsorted check
- Verify script_runs: execute MsBackendTest mz<- replacement with unsorted m/z values and confirm error is raised, exact error message and class must match implementation intent

## Expert Review

- Assess whether is.unsorted() vectorisation approach on NumericList is appropriate and efficient compared to vapply alternative
- Evaluate whether error message raised for unsorted m/z values is informative and aligns with Spectra package design expectations
- Review whether mz<- method correctly enforces the constraint that 'm/z values within each spectrum are expected to be sorted increasingly'
