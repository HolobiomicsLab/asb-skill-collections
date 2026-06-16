# Evaluation Strategy

## Direct Checks

- verify that the MetaMiner BGC Identifier stage can be isolated and executed independently on a genome FASTA file (input: test_data/metaminer/fasta/ or equivalent FASTA files from github:ablab__npdtools) without requiring prior spectral data or Dereplicator matching
- verify that intermediate per-class RiPP candidate database files are produced and exist in the output directory after BGC Identifier and RiPP Structure Database Builder stages complete (file_exists check for output files with naming pattern matching RiPP class assignments)
- verify that the fixed-architecture pipeline stages (BGC identification and structure database construction) complete without errors when run on Streptomyces griseus ATCC 12648 test contigs.fasta (script_runs check: MetaMiner BGC/structure stages execute to completion with zero non-zero exit codes)
- verify that candidate database output is produced before any spectral matching occurs (file_format_is check: output files must be in intermediate format prior to Dereplicator matching phase, robust to parameter choices in BGC detection sensitivity)

## Expert Review

- assess whether the intermediate RiPP candidate structure databases are chemically and biosynthetically coherent (i.e., whether predicted post-translational modifications and structure class assignments reflect known RiPP biology)
- evaluate whether BGC boundaries identified by the fixed-architecture stage align with expert expectations for Streptomyces griseus precursor peptides and biosynthetic gene organization
