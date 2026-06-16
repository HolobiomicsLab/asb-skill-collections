# Evaluation Strategy

## Direct Checks

- verify package 'tima' installs successfully from https://taxonomicallyinformedannotation.r-universe.dev/tima using install.packages('tima', repos='https://taxonomicallyinformedannotation.r-universe.dev')
- verify package loads without errors by executing library('tima') in R session
- verify R CMD check passes by confirming CI badge in repository README indicates passing status or by running R CMD check locally on package source

## Expert Review

- confirm that any warnings or notes reported by R CMD check are acceptable (e.g., expected non-fatal notes) and do not indicate functional defects in the package
