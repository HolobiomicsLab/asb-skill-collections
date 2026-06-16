# Evaluation Strategy

## Direct Checks

- verify file exists at path specified in dbpath slot of methylRawListDB object
- file_format_is: tabix-compressed (bgzip) for all methylation data files referenced in dbpath
- verify tabix index file (.tbi) exists for each bgzipped file in dbpath
- contains_substring: tabix header contains 'methylKit' metadata marker
- contains_substring: tabix header contains version string matching pattern 'version[\s=]+(\d+\.\d+\.\d+)' with version >= 1.13.1

## Expert Review

- verify that methylRawListDB object structure and slot organization conform to methylKit ≥1.13.1 dbtype='tabix' specification
- confirm tabix header metadata format matches methylKit's documented tabix serialization schema for version ≥1.13.1
- assess whether example CpG input files are compatible with methRead() tabix mode and produce valid methylation records
