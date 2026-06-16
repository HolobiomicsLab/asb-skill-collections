# Evaluation Strategy

## Direct Checks

- verify that ENCODE-DCC/hic-pipeline repository is accessible and contains executable pipeline code
- verify that a public Hi-C FASTQ accession (SRA/GEO format) can be retrieved and loaded
- verify that pipeline execution completes without fatal errors on the selected accession
- verify that output Hi-C map file exists in expected format (e.g., .hic or standard matrix format)
- verify that output checksum or file hash can be computed and compared against documented ENCODE reference checksum (if reference checksum is available in repository or documentation)

## Expert Review

- assess whether the computed Hi-C map reflects expected contact frequency patterns and chromosome structure characteristic of valid Hi-C data
- review whether pipeline parameter settings align with ENCODE uniform processing standards
- evaluate whether any deviations from reference output (if detected) are attributable to software versions, reference genome builds, or acceptable preprocessing variations rather than pipeline failure
