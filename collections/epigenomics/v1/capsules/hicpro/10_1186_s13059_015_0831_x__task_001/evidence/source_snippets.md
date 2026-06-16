# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] What post-processing operations does HiC-Pro apply to SAM/BAM files output from the alignment stage?: 'An optimized and flexible pipeline for Hi-C data processing'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] HiC-Pro implements SAM processing using samtools (>=1.9), which is automatically installed if not detected in the system.: 'A couple of tools such as `bowtie2` and `samtools` (>=1.9) can be automatically installed if not detected.'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] HiC-Pro installation source directory containing config-install.txt template and Makefile: '1 - Edit the config-install.txt file and set the paths. If not set, the dependencies will be sought in the $PATH'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] samtools binary (version >=1.9) installed on system or available in PATH: 'A couple of tools such as `bowtie2` and `samtools` (>=1.9) can be automatically installed if not detected.'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] config-system.txt file containing resolved full path to samtools binary and all other HiC-Pro dependencies: 'The installation process will generate a config-system.txt file which defines all paths to HiC-Pro dependencies.'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] samtools (>=1.9): 'A couple of tools such as `bowtie2` and `samtools` (>=1.9) can be automatically installed if not detected.'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] bowtie2: 'A couple of tools such as `bowtie2` and `samtools` (>=1.9) can be automatically installed if not detected.'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog documenting SAM processing stage updates, parameter changes, or version history: 'No changelog found.'
