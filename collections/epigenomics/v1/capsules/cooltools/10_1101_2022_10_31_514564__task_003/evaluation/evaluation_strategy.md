# Evaluation Strategy

## Direct Checks

- verify that input cooler file exists and is readable in cooler format
- verify output insulation score table file exists
- verify output BED file exists
- file_format_is: insulation score table is TSV or CSV with numeric columns
- file_format_is: BED file conforms to standard BED format (tab-delimited, chrom, chromStart, chromEnd, and optional fields)
- field_present: insulation score table contains per-bin score column
- field_present: BED file contains boundary call coordinates
- value_in_range: insulation scores are numeric and within expected range (no NaN values in output, or NaN handling is documented)
- row_count_equals: number of rows in insulation score table matches number of bins in input cooler file
- script_runs: cooltools.insulation function executes without error on the input cooler file

## Expert Review

- insulation score values are biologically plausible for Hi-C contact matrices (expert judgment required on typical insulation score distribution for this data type)
- boundary calls in BED file correspond to expected topologically associating domain (TAD) boundaries or domain insulation patterns
- parameter choices (window size, distance threshold) are appropriate for the resolution and scale of the input cooler file
