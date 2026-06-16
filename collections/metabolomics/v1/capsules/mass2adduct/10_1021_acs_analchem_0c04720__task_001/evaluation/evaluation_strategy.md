# Evaluation Strategy

## Direct Checks

- verify that mass2adduct package is installable from github:kbseah__mass2adduct
- verify that built-in datasets 'adducts' and 'adducts2' are accessible via data(adducts) and data(adducts2)
- verify file_exists: extdata/msi.csv is present in package
- script_runs: msimat() successfully loads the CSV file and returns an object of class msimat
- script_runs: massdiff() function executes on msimat object and returns object with classes data.frame and massdiff
- script_runs: hist() method executes on massdiff object and returns object with classes histogram and massdiffhist
- script_runs: adductMatch() function executes on histogram object to annotate known adducts
- script_runs: topAdducts() function executes and produces ranked table of mass differences with adduct matches in descending order by occurrence, robust to dataset size variations
- file_format_is: topAdducts() output is a structured table with at least columns for mass difference values, occurrence counts, and adduct annotations
- value_in_range: all computed mass difference values are positive numbers (masses cannot be negative)
- output_matches_reference: topAdducts() table rows are sorted in descending order by occurrence count

## Expert Review

- chemical plausibility of matched adducts: verify that adductMatch() correctly identifies biologically-relevant adducts from the built-in datasets for the test dataset
- appropriateness of mass difference histogram binning: confirm that histogram resolution is adequate to resolve distinct adduct types without over- or under-binning
- correctness of massdiff calculation: verify that pairwise mass differences are computed exhaustively and accurately from the input mass list
