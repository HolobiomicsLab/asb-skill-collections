---
name: biotransformation-prediction-across-microbiota-contexts
description: Use when you have one or more small-molecule chemical structures (as SMILES, MOL, or SDF) and need to systematically explore their fate across mammalian biotransformation, human gut microbial degradation, or environmental (soil/aquatic) microbial degradation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
  tools:
  - BioTransformer
derived_from:
- doi: 10.1186/s13321-019-0375-2
  title: BioTransformer 1.0
evidence_spans:
- This is version 3.0.0 of BioTransformer. BioTransformer is a software tool that predicts small molecule metabolism
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_biotransformer_1_0_cq
    doi: 10.1186/s13321-019-0375-2
    title: BioTransformer 1.0
  dedup_kept_from: coll_biotransformer_1_0_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-019-0375-2
  all_source_dois:
  - 10.1186/s13321-019-0375-2
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# biotransformation-prediction-across-microbiota-contexts

## Summary

Predict small-molecule metabolism across three distinct biological compartments—mammalian, gut microbiota, and soil/aquatic microbiota—using BioTransformer 3.0.0 to generate metabolite structures, reaction types, and metabolic pathway information. This skill enables computational metabolite identification and pathway elucidation when characterizing how xenobiotics or natural products are transformed across different microenvironments.

## When to use

Apply this skill when you have one or more small-molecule chemical structures (as SMILES, MOL, or SDF) and need to systematically explore their fate across mammalian biotransformation, human gut microbial degradation, or environmental (soil/aquatic) microbial degradation. Use it to generate predicted metabolite profiles before or alongside experimental metabolomics, to support metabolite identification in LC-MS data, or to assess xenobiotic persistence across microbiota contexts.

## When NOT to use

- Input is a protein or macromolecule; BioTransformer predicts small-molecule biotransformation only.
- You require real experimental metabolite data (LC-MS/MS); BioTransformer produces in silico predictions and must be validated against observed metabolomics.
- Your molecule is not representable as a single SMILES, MOL, or SDF structure (e.g., protein adducts, non-standard covalent complexes).

## Inputs

- small-molecule SMILES string (quoted or in file)
- MOL-format input file
- SDF-format input file containing one or more small molecules

## Outputs

- SDF file containing predicted metabolite structures, reaction types, and metadata
- CSV file containing predicted metabolite tabular results
- metabolite identification results with pathway annotation (when -k cid is used)
- PubChem CID and synonym annotations (when -a flag is used)

## How to apply

Prepare your input molecule(s) in SMILES, MOL, or SDF format. Execute BioTransformer 3.0.0 with the -k pred flag (prediction task) and select the appropriate biotransformer module via the -b flag: 'cyp450' and 'phaseII' for human metabolism, 'hgut' for human gut microbiota, or 'envimicro' for soil/aquatic microbiota. Specify the number of transformation steps using -s (default 1); for multi-step sequential transformations, use -q to define an ordered sequence (e.g., 'cyp450:2; phaseII:1'). Optionally annotate predicted metabolites with PubChem CIDs and synonyms using -a. Output results in SDF or CSV format. Evaluate success by verifying that metabolite structures are chemically plausible, reaction types are classified appropriately, and pathway depth matches your -s or -q specification.

## Related tools

- **BioTransformer** (Java-based executable that predicts small-molecule metabolism across mammalian, gut microbiota, and environmental microbiota compartments via EC-based, CYP450, Phase II, and microbial degradation reaction rules.) — https://github.com/Wishartlab-openscience/Biotransformer

## Examples

```
java -jar biotransformer-3.0.0.jar -k pred -b allHuman -ismi "CC(C)C1=CC=C(C)C=C1O" -ocsv output.csv -s 2 -cm 3
```

## Evaluation signals

- Predicted metabolites have valid molecular structures (parseable by cheminformatics tools; no valence errors).
- Output depth (number of biotransformation steps) matches the specified -s parameter or -q sequence.
- Reaction type annotations (e.g., oxidation, conjugation, deconjugation) are consistent with the biotransformer module selected (-b cyp450, -b phaseII, -b hgut, or -b envimicro).
- Metabolite mass shifts are chemically rational for the reported reaction types (e.g., oxidation typically adds 16 Da; conjugation adds expected group masses).
- When -a annotation flag is used, PubChem CID and synonym fields are populated where the predicted metabolite has a PubChem record.

## Limitations

- Predictions are computational and must be experimentally validated; BioTransformer does not account for tissue distribution, bioavailability, or kinetic barriers that affect in vivo biotransformation rates.
- Environmental microbial predictions include both aerobic and anaerobic reactions, which may not reflect the actual redox conditions of a specific soil or aquatic habitat.
- The environmental microbial degradation module (envimicro) uses data from EAWAG's Biodegradation and Biocatalysis Database licensed under CC-BY-NC-SA 4.0; commercial use requires an explicit commercial license from EnviPath.
- Rule-based prediction may miss novel or non-canonical biotransformation pathways not captured in the EC-based or CYP450 reaction rule sets.
- Accuracy and coverage vary by molecule class; aromatic compounds and xenobiotics with well-characterized human metabolism are typically better predicted than rare or highly novel chemical scaffolds.

## Evidence

- [readme] BioTransformer predicts small molecule metabolism in mammals, their gut microbiota, as well as the soil/aquatic microbiota.: "BioTransformer is a software tool that predicts small molecule metabolism in mammals, their gut microbiota, as well as the soil/aquatic microbiota"
- [readme] BioTransformer assists scientists in metabolite identification based on metabolism prediction.: "BioTransformer also assists scientists in metabolite identification, based on the metabolism prediction"
- [readme] Supported input formats are SMILES, MOL, and SDF.: "Please make sure to download the folders database and supportfiles, and save them in the same folder as the .jar file"
- [readme] The environmental microbial degradation module uses EAWAG's database and is restricted for commercial use.: "BioTransformer's environmental microbial degradation module uses data from the EAWAG's Biodegradation and Biocatalysis Database, which is licensed by EnviPath under the Creative Commons"
- [readme] Biotransformer module options include EC-based, CYP450, Phase II, human gut microbial, and environmental microbial.: "The type of biotransformer - EC-based (ecbased), CYP450 (cyp450), Phase II (phaseII), Human gut microbial (hgut), human super transformer** (superbio, or allHuman), Environmental microbial (envimicro)"
- [readme] The -s parameter specifies the number of biotransformation steps; the -q parameter defines an ordered sequence of transformation steps.: "The number of steps for the prediction. This option can be set by the user for the EC-based, CYP450, Phase II, and Environmental microbial biotransformers. The default value is 1"
- [readme] Outputs can be saved in SDF or CSV format; annotation with PubChem data is optional.: "Save the results into the specified CSV file"
