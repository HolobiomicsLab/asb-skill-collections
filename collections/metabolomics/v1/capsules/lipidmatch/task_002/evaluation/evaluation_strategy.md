# Evaluation Strategy

## Direct Checks

- verify that inputs include a peaklist file in a supported format (mzML, mzXML, or CSV with m/z and intensity columns) from Q-Exactive or Q-TOF instrument
- verify that inputs include at least one in-silico library .csv file from the LipidMatch repository or a user-generated library with required columns (lipid name, adduct, theoretical m/z)
- verify that the matching output table file exists and is in CSV or tabular format
- verify that output table contains at least the following named columns: matched lipid identifier, experimental m/z, theoretical m/z, m/z error (ppm or Da), matched fragment count, confidence score or ranking
- verify that all rows in output table have non-null values in the m/z error field and that error values are numeric and within a biologically plausible range (typically ≤ 5–10 ppm for high-resolution instruments)
- verify that the LipidMatch matching script runs without fatal errors when executed with the provided peaklist and library files
- verify that row count of output table is greater than zero (at least one lipid matched)
- byte-for-byte match of output against a reference result file (if a reference matched-identifications table from a published validation is deposited) or expert review of match quality

## Expert Review

- assess whether matched lipid identifications are chemically and biochemically plausible given the sample type and ionization mode
- assess whether m/z error distribution across all matched fragments is reasonable and consistent with instrument calibration and resolution
- assess whether the number of matched lipids and their relative abundances are consistent with expected lipidome composition for the sample type
- verify that the matching logic correctly applies mass tolerance thresholds and fragment matching rules as documented in the LipidMatch method
- assess whether any false-positive or false-negative matches are evident by comparing against independent lipid annotations (if available from the same sample)
