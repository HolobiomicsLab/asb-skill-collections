# Evaluation Strategy

## Direct Checks

- verify file exists at github:kbseah__mass2adduct containing pointsAdducts() function implementation
- script_runs: execute pointsAdducts(d, d.diff.annot.cor.Na, which="adduct", signif=TRUE, pch=20, cex=0.5, col="red") on a correlation-filtered massdiff object subset to Na adduct matches without error
- output_matches_reference: generated scatter plot contains red-colored points representing adduct ions and blue-colored points representing parent ions, with overlapping regions visible (robust to exact pixel coordinates, parameter-sensitive to point size and transparency settings)
- file_format_is: output figure in standard graphics format (PNG, PDF, or R graphics object)

## Expert Review

- visual assessment that red/blue overlap pattern in scatter plot is consistent with reported paper findings regarding adduct-parent ion co-localization
- confirmation that pointsAdducts() correctly interprets the which="adduct" parameter to distinguish adduct from parent ion populations
- assessment that signif=TRUE filtering parameter appropriately restricts display to statistically significant correlation pairs
