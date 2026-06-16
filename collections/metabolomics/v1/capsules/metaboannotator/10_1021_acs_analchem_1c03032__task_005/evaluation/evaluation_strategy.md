# Evaluation Strategy

## Direct Checks

- verify file_exists for each of: global results file, ranked results file, ranked spectra PDF file, pseudo-MS/MS MGF file in the temporary directory specified as saveAnnotations output
- verify each output file is non-empty (file size > 0 bytes)
- verify file_format_is correct: results files parseable as data frame/table, PDF file contains valid PDF header, MGF file contains valid MGF structure (PEPMASS, TITLE, BEGIN IONS/END IONS blocks)
- verify script_runs: saveAnnotations function executes without error on annotations object with specified temporary directory as output path

## Expert Review

- verify that the content and structure of saved results match the vignette-reported expectations for global results, ranked results, ranked spectra PDFs, and pseudo-MS/MS MGF outputs — requires inspection of vignette documentation for expected field names, row counts, spectrum count, and MGF entry structure
