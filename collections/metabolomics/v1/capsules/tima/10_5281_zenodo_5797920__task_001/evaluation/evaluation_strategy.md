# Evaluation Strategy

## Direct Checks

- verify that the tima R package can be installed from github:taxonomicallyinformedannotation__tima or from CRAN
- verify that a Docker image is available and can be pulled for the tima workflow
- verify that a publicly deposited example dataset exists and is accessible (check Zenodo, GitHub, or package-bundled data)
- verify that the canonical workflow from the README executes without error when run against the example dataset
- verify that the workflow produces named output artifacts (annotated table, structured record, or report file) as documented in the README
- verify file_exists: the workflow README documents the complete end-to-end pipeline steps
- verify contains_substring: the README or package documentation includes worked example with input and output specification

## Expert Review

- assess whether the executed workflow faithfully reproduces the taxonomically informed annotation architecture as illustrated in the paper
- assess whether all intermediate and final outputs match the expected data structure and biological/taxonomic content quality reported in the associated publication
- assess whether the workflow is reproducible across different execution environments (native R vs. Docker) with byte-for-byte or semantically equivalent outputs
