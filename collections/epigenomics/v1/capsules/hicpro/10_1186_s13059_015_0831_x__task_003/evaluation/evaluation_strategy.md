# Evaluation Strategy

## Direct Checks

- verify file config-system.txt exists in package after installation step
- verify config-system.txt contains field for bowtie2 binary path (key-value pair or structured format)
- verify config-system.txt contains field for samtools binary path (key-value pair or structured format)
- verify script that generates config-system.txt runs without error when bowtie2 and samtools are available in PATH or specified in inputs
- verify config-system.txt format matches the documented structure (exact format robust to whitespace normalization)
- verify output file is valid text or INI format (file_format_is text or INI)
- verify bowtie2 path value in config-system.txt points to existing executable or matches reference path from inputs

## Expert Review

- assess whether detected bowtie2 and samtools versions satisfy documented minimum version requirements (bowtie2 any version, samtools >=1.9)
- evaluate whether environment variable substitution and PATH fallback logic are correctly implemented in config-system.txt generation
- review whether config-system.txt encoding is compatible with downstream runtime pipeline consumption
