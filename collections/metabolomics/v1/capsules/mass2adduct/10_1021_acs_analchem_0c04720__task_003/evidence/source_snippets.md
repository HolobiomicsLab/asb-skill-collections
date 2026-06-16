# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] How can sodium adduct ions be visually distinguished from their parent ions in mass spectrometry imaging data?: 'pointsAdducts(d, d.diff.annot.cor.Na, which="adduct", signif=TRUE, pch=20, cex=0.5, col="red")'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] The pointsAdducts() function generates a scatter plot that highlights adduct ions in red and parent ions in contrasting colors, enabling visual identification of the red/blue overlap pattern between sodium adducts and their corresponding parent ions.: 'pointsAdducts(d, d.diff.annot.cor.Na, which="adduct", signif=TRUE, pch=20, cex=0.5, col="red")'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] msimat object: preprocessed MSI data matrix with intensity values for each mass peak across all pixels: 'd <- msimat(system.file("extdata","msi.csv",package="mass2adduct"),sep=";")'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] massdiff object annotated with adductMatch() and filtered by corrPairsMSI() for spatial correlation significance: 'd.diff.annot <- adductMatch(d.diff,add=adducts2)'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] correlation-tested massdiff object with Estimate, P.value, and Significance columns from corrPairsMSI(): 'd.diff.annot.cor <- corrPairsMSI(d,d.diff.annot)'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Annotated mass spectrum plot with parent ions marked as blue circle outlines and adduct ions marked as red filled points, showing overlap indicating ions with dual roles: 'You can annotate the original mass spectrum using a massdiff object, to mark peaks corresponding to parent ions and adduct ions in different colors.'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] mass2adduct: 'library(mass2adduct)'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] R: 'library(mass2adduct)'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog documenting version history, breaking changes, or function signature stability for pointsAdducts() across releases: '_No changelog found._'
