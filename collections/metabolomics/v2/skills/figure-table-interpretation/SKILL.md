---
name: figure-table-interpretation
description: Use when after running a 3DMolMS model (or similar MS/MS prediction pipeline) that outputs predictions in MGF, CSV, or PKL format, use this skill to verify prediction quality by examining peak intensities, m/z values, precursor ions, and similarity metrics against ground truth or reference spectra.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3630
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3050
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3372
  - http://edamontology.org/topic_3474
  - http://edamontology.org/topic_3169
  - http://edamontology.org/topic_0080
  - http://edamontology.org/topic_3173
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_2258
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_2840
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3314
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_3373
  - http://edamontology.org/topic_3361
  - http://edamontology.org/topic_3365
  - http://edamontology.org/topic_0092
  - http://edamontology.org/topic_3308
  - http://edamontology.org/topic_3577
  - http://edamontology.org/topic_0634
  - http://edamontology.org/topic_0188
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_3297
  - http://edamontology.org/topic_3572
  - http://edamontology.org/topic_3047
  - http://edamontology.org/topic_0601
  - http://edamontology.org/topic_3674
  - http://edamontology.org/topic_3575
  - http://edamontology.org/topic_3307
  - http://edamontology.org/topic_0611
  - http://edamontology.org/topic_3315
  - http://edamontology.org/topic_3489
  - http://edamontology.org/topic_3070
  tools:
  - PyTorch
  - RDKit
  - molnetpack
  - matplotlib
  - Pandas
  - MoNA
  - NIST20
  - mzmine
  - mzmine3
  - JavaFX
  - Java Development Kit (JDK)
  - GitHub
  - AnnoSM
  - pandas
  - scikit-learn
  - train.py
  - predict.py
  - GitLab
  - bigmap-download
  - bigmap-family
  - bigmap-map
  - bigmap-analyse
  - BiG-SCAPE
  - MASH
  - bowtie2
  - Bedtools
  - Samtools
  - BinDiscover
  - SIRIUS
  - CSI:FingerID
  - CANOPUS
  - MSNovelist
  - ChEMBL Structure Curation Pipeline Checker
  - PostgreSQL
  - ZODIAC
  - COSMIC
  - OpenMS
  - CompassXport
  - CycloBranch
  - Snakemake
  - Python 3.10
  - PubChem
  - DIATAGeR
  - netgsa R package
  - ggplot2
  - Cytoscape
  - DNEA
  - igraph
  - pheatmap
  - eicCluster
  - R
  - devtools
  - Bioconductor
  - MassBank
  - eRah
  - KNIME
  - Python
  - pyOpenMS
  - nextflow
  - Galaxy
  - TOPPAS
  - GNPS
  - ProteoSAFe
  - GitHub Actions
  - Uptime Robot
  - GNPS ProteoSAFe
  - CCMS-Integration-Tests
  - GitHub Actions CI/Badge system
  - homologueDiscoverer
  - dplyr
  - IDSL_MINT
  - JDK
  - MZmine
  - seaborn
  - ViMMS
  - Instant Clue
  - PyQt6
  - jmztab-m CLI
  - jmztab-m-io library
  - jmztab-m-validation library
  - jmzTab-m-webapp
  - pymzTab-m
  - rmzTab-m
  - MetDNA2
  - MetDNA2Vis
  - R / rmarkdown
  - Python 3.9.0
  - numpy
  - openpyxl
  - brain-isotopic-distribution
  - scipy
  - PySide6
  - GitHub repository (RaoboXu/Lipidwizard)
  - PyTorch Lightning
  - Ray Tune
  - Weights & Biases
  - uv
  - LipiDex
  - Compound Discoverer
  - mzMine 2
  - Proteowizard MS/MS file converter
  - LiPydomics
  - evaluation_generation.py
  - sample.py
  - MAFFIN
  - R (devtools, base functions)
  - Flask
  - uWSGI
  - Docker Compose
  - Plotly
  - Scikit-learn (DBSCAN, OPTICS)
  - GNPS_MASST
  - MetaboAnalystR 4.0
  - MetaboAnalyst web server
  - MetaboAnalystR
  - Vicuna-13B-v1.5
  - GNN encoder (Snap-stanford-gnn pretrained)
  - CNN image encoder (ImageMol-based)
  - Human Metabolome Database (HMDB)
  - metabolitics-frontend
  - Metabol
  - ReDU web UI
  - GNPS (Global Natural Product Social Molecular Networking Platform)
  - MassIVE repository
  - MetaMOPE
  - Docker
  - MetaPro
  - Redis
  - MongoDB
  - AirdPro
  - MetDIT
  - scikit-learn (Random Forest, SVM)
  - XGBoost
  - LightGBM
  - ComplexHeatmap
  - PCAtools
  - plotly
  - ggrepel
  - R v4.3.3
  - tidymass
  - clusterProfiler
  - mineMS2
  - MINNO
  - MPACT
  - Spyder
  - MRMkit
  - MRMhub
  - GitHub Issues
  - TensorFlow
  - MS2toImg-CNN
  - MS-DIAL
  - .NET Framework 4.7.2, .NET Core 3.1, .NET 6
  - Visual Studio 2022 Community
  - Visual Studio Code
  - MSIght
  - PyPI MSIght package
  - MZmine 2
  - mzmine2
  - mzmine (current)
  - MZmine 3
  - JDK 25
  - JavaFX 24
  - proteowizard
  - mzMine
  - XCMS
  - msconvert
  - NeatMS
  - Jupyter notebook
  - dash
  - jupyter-dash
  - ProteoWizard msconvert
  - result_optimization_and_analysis
  - NetAurHPD_M5
  - Python 3.6
  - ISWSVR
  - NP³ MS Workflow – run command
  - NP³ MS Workflow – pca_plot command
  - NP³ MS Workflow – gnps_result command
  - GNPS2 Library Search (offline)
  - TOPPTools
  - GitHub Issues and Pull Requests
  - TAPPAS
  - PeakDetective
  - GitLab CI/CD
  - Maven
  - Spring Framework
  - Open Babel
  - POMAShiny
  - POMA
  - Shiny
  - PredRet R package
  - Protomix
  - pyicoshift
  - NumPy
  - matplotlib, seaborn, Plotly
  - QC4metabolomics
  - GitHub (repository hosting and commit history)
  - RaMP-DB
  - RaMP-Backend
  - Colab
  - regression_filter (computational-chemical-biology)
  - regression_filter (gsarini fork)
  - Conda
  - SGMNS
  - Spektral
  - UMAP
  - Jupyter Notebook
  - SManalyst
  - Seurat
  - UMAP-kmeans
  - MetaS/MetaS
  - SMolESY-select
  - SpecTUS transformer model
  - Pretrained checkpoint (MS-ML on Hugging Face)
  - Jupyter notebooks in notebooks/ directory
  - Jupyter
  - t-SNE
  - ms2deepscore
  - MZmine3
  - matchms
  - SKYLINE
  - MetaboAnalyst
  - statTarget
  - RGtk2
  - Combat
  - struct
  - structToolbox
  - ProteoWizard
  - HMDB
  - Zenodo
  - limma
derived_from:
- doi: 10.1093/bioinformatics/btad354
  title: 3DMolMS
- doi: 10.1021/acs.jproteome.5c00423
  title: ''
- doi: 10.1021/acs.analchem.3c04946
  title: ''
- doi: 10.1016/j.jece.2025.119962
  title: ''
- doi: 10.1021/acs.analchem.1c05224
  title: ''
- doi: 10.1128/msystems.00937-21
  title: ''
- doi: 10.1186/s13321-023-00734-8
  title: ''
- doi: 10.1021/acs.analchem.8b04698
  title: ''
- doi: 10.1186/s13321-020-00478-9
  title: ''
- doi: 10.1038/s41587-021-01045-9
  title: ''
- doi: 10.1177/14690667231164766
  title: ''
- doi: 10.1101/2024.11.13.623458v1
  title: ''
- doi: 10.1016/j.aca.2025.344698
  title: ''
- doi: 10.1186/s12859-024-05994-1
  title: ''
- doi: 10.1016/j.chroma.2018.09.050
  title: ''
- doi: 10.1021/acs.analchem.6b02927
  title: ''
- doi: 10.1074/mcp.M113.031278
  title: ''
- doi: 10.26434/chemrxiv-2024-1zk33
  title: ''
- doi: 10.1038/s41596-020-0317-5
  title: ''
- doi: 10.1002/imt2.195
  title: ''
- doi: 10.1093/bioinformatics/btac647/6722615
  title: ''
- doi: 10.1186/s13321-024-00804-5
  title: ''
- doi: 10.1038/s41467-021-23953-9
  title: ''
- doi: 10.1021/acs.analchem.0c03895
  title: ''
- doi: 10.1038/s41598-018-31154-6
  title: ''
- doi: 10.1038/s41467-022-34537-6
  title: ''
- doi: 10.1021/acs.analchem.3c04419
  title: ''
- doi: 10.1101/2024.10.07.617094v3
  title: ''
- doi: 10.1016/j.cels.2018.03.011
  title: ''
- doi: 10.1021/acs.analchem.0c02560
  title: ''
- doi: 10.1021/jasms.1c00013
  title: ''
- doi: 10.48550/arxiv.2501.01950
  title: ''
- doi: 10.1093/bioinformatics/btac355/6593484
  title: ''
- doi: 10.1021/acs.analchem.3c03594
  title: ''
- doi: 10.1186/s13321-023-00741-9
  title: ''
- doi: 10.1038/s41587-023-01985-4
  title: ''
- doi: 10.1093/nar/gkae253
  title: ''
- doi: 10.1038/s41467-024-48009-6
  title: ''
- doi: 10.1101/2025.11.07.687008v1
  title: ''
- doi: 10.1101/2025.11.07.687008
  title: ''
- doi: 10.1109/tcbbio.2025.3563807
  title: ''
- doi: 10.1093/bioinformatics/btae373
  title: ''
- doi: 10.1093/bioadv/vbad061/7172446
  title: ''
- doi: 10.1007/s11306-023-02018-6
  title: ''
- doi: 10.1016/j.aca.2018.05.001
  title: ''
- doi: 10.1021/acs.analchem.3c04607
  title: ''
- doi: 10.1111/jipb.13774
  title: ''
- doi: 10.1186/s13321-025-01051-y
  title: ''
- doi: 10.1021/acs.analchem.3c04501
  title: ''
- doi: 10.1021/acs.analchem.2c04632
  title: ''
- doi: 10.1021/acs.analchem.0c03060
  title: ''
- doi: 10.48550/arxiv.2510.09716
  title: ''
- doi: 10.1038/s41467-024-54137-w
  title: ''
- doi: 10.1002/rcm.9253
  title: ''
- doi: 10.1021/acs.jproteome.4c01140
  title: ''
- doi: 10.1186/1471-2105-11-395
  title: ''
- doi: 10.1038/s41587-023-01690-2
  title: ''
- doi: 10.1021/acs.analchem.1c02220
  title: ''
- doi: 10.48550/arxiv.2410.22030
  title: ''
- doi: 10.1021/jasms.4c00467
  title: ''
- doi: 10.1021/acs.analchem.3c05829
  title: ''
- doi: 10.1038/nmeth.3959
  title: ''
- doi: 10.1021/acs.analchem.3c00764
  title: ''
- doi: 10.1007/s11306-022-01899-3
  title: ''
- doi: 10.3390/plants12152880
  title: ''
- doi: 10.1371/journal.pcbi.1009148
  title: ''
- doi: 10.1021/acs.analchem.5b02287
  title: ''
- doi: 10.1093/bioadv/vbae192
  title: ''
- doi: 10.1021/acs.analchem.4c07078
  title: ''
- doi: 10.3390/metabo8010016
  title: ''
- doi: 10.1101/2024.08.07.607073v1
  title: ''
- doi: 10.1021/acs.analchem.3c00849
  title: ''
- doi: 10.1038/s42004-023-00939-w
  title: ''
- doi: 10.1038/s41592-019-0344-8
  title: ''
- doi: 10.3390/biom15111562
  title: ''
- doi: 10.3390/metabo13080941
  title: ''
- doi: 10.1021/acs.analchem.1c00113
  title: ''
- doi: 10.48550/arxiv.2502.05114
  title: ''
- doi: 10.1021/acs.analchem.3c04444
  title: ''
- doi: 10.1016/j.aca.2018.08.002
  title: ''
- doi: 10.1093/bioinformatics/btaa1031
  title: ''
- doi: 10.21105/joss.02694
  title: ''
- doi: 10.1007/s11306-018-1363-7
  title: ''
- doi: 10.1021/acs.jproteome.3c00784
  title: ''
- doi: 10.3390/metabo10100416
  title: ''
- doi: 10.1038/s41467-022-32155-w
  title: ''
- doi: 10.3389/fmolb.2022.952149
  title: ''
- doi: 10.1186/s13321-023-00724-w
  title: ''
- doi: 10.21105/joss.02410
  title: ''
- doi: 10.1038/s43588-025-00923-5
  title: ''
- doi: 10.1021/ac051437y
  title: ''
- doi: 10.1038/s42256-020-00234-6
  title: ''
evidence_spans:
- PyTorch must be installed separately. Check the `official PyTorch website
- '3DMolMS has the following dependencies: * Python 3.8+ * PyTorch * RDKit'
- 'Source: github:gitlab.gwdg.de__joerg.buescher__automrm'
- These are generated using RDKit... We extensively use the ChEMBL structure curation pipeline developed with RDKit to clean the data and curate the database.
- snakemake --configfile config/config_fast.yaml --jobs 1 --dry-run -p
- This entails conversion to molecules using `rdkit`, removing light fragments, neutralizing charges, filtering for valid elements
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_3dmolms_cq
    doi: 10.1093/bioinformatics/btad354
    title: 3DMolMS
  - build: coll_aird_msi_cq
    doi: 10.1021/acs.jproteome.5c00423
    title: Aird-MSI
  - build: coll_annosm_cq
    doi: 10.1021/acs.analchem.3c04946
    title: AnnoSM
  - build: coll_asrtnet_cq
    doi: 10.1016/j.jece.2025.119962
    title: AsRTNet
  - build: coll_automrm_cq
    doi: 10.1021/acs.analchem.1c05224
    title: automRm
  - build: coll_big_map_cq
    doi: 10.1128/msystems.00937-21
    title: BiG-MAP
  - build: coll_bindiscover
    doi: 10.1186/s13321-023-00734-8
    title: bindiscover
  - build: coll_bindiscover_cq
    doi: 10.1186/s13321-023-00734-8
    title: bindiscover
  - build: coll_canopus_2_cq
    doi: 10.1021/acs.analchem.8b04698
    title: CANOPUS
  - build: coll_canopus_cq
    doi: 10.1021/acs.analchem.8b04698
    title: CANOPUS
  - build: coll_coconut_cq
    doi: 10.1186/s13321-020-00478-9
    title: COCONUT
  - build: coll_cosmic_cq
    doi: 10.1038/s41587-021-01045-9
    title: cosmic
  - build: coll_cyclobranch_cq
    doi: 10.1177/14690667231164766
    title: CycloBranch
  - build: coll_deepmet_cq
    doi: 10.1101/2024.11.13.623458v1
    title: DeepMet
  - build: coll_diatage_cq
    doi: 10.1016/j.aca.2025.344698
    title: DIATAGe
  - build: coll_dnea_cq
    doi: 10.1186/s12859-024-05994-1
    title: DNEA
  - build: coll_eiccluster_cq
    doi: 10.1016/j.chroma.2018.09.050
    title: eicCluster
  - build: coll_erah_cq
    doi: 10.1021/acs.analchem.6b02927
    title: eRah
  - build: coll_featurefindermetab
    doi: 10.1074/mcp.M113.031278
    title: featurefindermetab
  - build: coll_featurefindermetab_cq
    doi: 10.1074/mcp.M113.031278
    title: featurefindermetab
  - build: coll_finnee_2024_cq
    doi: 10.26434/chemrxiv-2024-1zk33
    title: Finnee 2024
  - build: coll_gnps_feature_based_molecular_networking__cq
    doi: ''
    title: ''
  - build: coll_gnps_molecular_networking_protocol_cq
    doi: 10.1038/s41596-020-0317-5
    title: GNPS molecular networking protocol
  - build: coll_gutudb_cq
    doi: 10.1002/imt2.195
    title: GutUDB
  - build: coll_homologuediscoverer_cq
    doi: 10.1093/bioinformatics/btac647/6722615
    title: homologueDiscoverer
  - build: coll_idslmint_cq
    doi: 10.1186/s13321-024-00804-5
    title: idslmint
  - build: coll_iimn_cq
    doi: 10.1038/s41467-021-23953-9
    title: iimn
  - build: coll_in_silico_ms_fragmentation_strategy_opti_cq
    doi: 10.1021/acs.analchem.0c03895
    title: ''
  - build: coll_instant_clue_cq
    doi: 10.1038/s41598-018-31154-6
    title: Instant Clue
  - build: coll_jmztab_m_parser_writer_validator_mztab_2_cq
    doi: ''
    title: ''
  - build: coll_knowledge_guided_mn_knowns_unknowns_cq
    doi: 10.1038/s41467-022-34537-6
    title: Knowledge-guided MN (knowns→unknowns)
  - build: coll_lipid_wizard_cq
    doi: 10.1021/acs.analchem.3c04419
    title: Lipid Wizard
  - build: coll_lipidetective_cq
    doi: 10.1101/2024.10.07.617094v3
    title: LipiDetective
  - build: coll_lipidex_cq
    doi: 10.1016/j.cels.2018.03.011
    title: LipiDex
  - build: coll_lipydomics_cq
    doi: 10.1021/acs.analchem.0c02560
    title: LiPydomics
  - build: coll_macroms_cq
    doi: 10.1021/jasms.1c00013
    title: macroMS
  - build: coll_madgen_cq
    doi: 10.48550/arxiv.2501.01950
    title: MADGEN
  - build: coll_maffin_cq
    doi: 10.1093/bioinformatics/btac355/6593484
    title: MAFFIN
  - build: coll_magnetstein_cq
    doi: 10.1021/acs.analchem.3c03594
    title: Magnetstein
  - build: coll_mass_suite_cq
    doi: 10.1186/s13321-023-00741-9
    title: Mass-Suite
  - build: coll_masst_2_cq
    doi: 10.1038/s41587-023-01985-4
    title: MASST
  - build: coll_masst_cq
    doi: 10.1038/s41587-023-01985-4
    title: MASST
  - build: coll_metaboanalyst_6_0_cq
    doi: 10.1093/nar/gkae253
    title: MetaboAnalyst 6.0
  - build: coll_metaboanalystr_cq
    doi: 10.1038/s41467-024-48009-6
    title: metaboanalystr
  - build: coll_metabolitechat_cq
    doi: 10.1101/2025.11.07.687008v1
    title: MetaboliteChat
  - build: coll_metaboliticsdb_cq
    doi: 10.1109/tcbbio.2025.3563807
    title: MetaboliticsDB
  - build: coll_metaboreport_cq
    doi: 10.1093/bioinformatics/btae373
    title: MetaboReport
  - build: coll_metadata_based_source_annotation_redu_st_cq
    doi: ''
    title: ''
  - build: coll_metamope_cq
    doi: 10.1093/bioadv/vbad061/7172446
    title: MetaMOPE
  - build: coll_metapro_cq
    doi: 10.1007/s11306-023-02018-6
    title: MetaPro
  - build: coll_metdit_cq
    doi: 10.1021/acs.analchem.3c04607
    title: MetDIT
  - build: coll_metminer_mdatoolkits_cq
    doi: 10.1111/jipb.13774
    title: MetMiner, MDAtoolkits
  - build: coll_minems2_cq
    doi: 10.1186/s13321-025-01051-y
    title: minems2
  - build: coll_minno_cq
    doi: 10.1021/acs.analchem.3c04501
    title: MINNO
  - build: coll_mpact_cq
    doi: 10.1021/acs.analchem.2c04632
    title: MPACT
  - build: coll_mrmkit_cq
    doi: 10.1021/acs.analchem.0c03060
    title: MRMkit
  - build: coll_ms2toimg_cq
    doi: 10.48550/arxiv.2510.09716
    title: MS2toImg
  - build: coll_ms_dial_5_cq
    doi: 10.1038/s41467-024-54137-w
    title: MS-DIAL 5
  - build: coll_ms_vis_cq
    doi: 10.1002/rcm.9253
    title: MS-VIS
  - build: coll_msight_cq
    doi: 10.1021/acs.jproteome.4c01140
    title: MSIght
  - build: coll_mzmine2
    doi: 10.1186/1471-2105-11-395
    title: mzmine2
  - build: coll_mzmine2_cq
    doi: 10.1186/1471-2105-11-395
    title: mzmine2
  - build: coll_mzmine3_cq
    doi: 10.1038/s41587-023-01690-2
    title: mzmine3
  - build: coll_neatms_cq
    doi: 10.1021/acs.analchem.1c02220
    title: neatms
  - build: coll_netaurhpd_cq
    doi: 10.48550/arxiv.2410.22030
    title: NetAurHPD
  - build: coll_norm_iswsvr_cq
    doi: 10.1021/jasms.4c00467
    title: Norm ISWSVR
  - build: coll_np3_ms_workflow_cq
    doi: 10.1021/acs.analchem.3c05829
    title: NP3 MS Workflow
  - build: coll_openms
    doi: 10.1038/nmeth.3959
    title: OpenMS
  - build: coll_openms_cq
    doi: 10.1038/nmeth.3959
    title: OpenMS
  - build: coll_peakdetective_cq
    doi: 10.1021/acs.analchem.3c00764
    title: PeakDetective
  - build: coll_peakforest_cq
    doi: 10.1007/s11306-022-01899-3
    title: PeakForest
  - build: coll_plantmetsuite_cq
    doi: 10.3390/plants12152880
    title: PlantMetSuite
  - build: coll_pomashiny_cq
    doi: 10.1371/journal.pcbi.1009148
    title: POMAShiny
  - build: coll_predret_cq
    doi: 10.1021/acs.analchem.5b02287
    title: PredRet
  - build: coll_protomix_cq
    doi: 10.1093/bioadv/vbae192
    title: Protomix
  - build: coll_qc4metabolomics_cq
    doi: 10.1021/acs.analchem.4c07078
    title: qc4metabolomics
  - build: coll_ramp_cq
    doi: 10.3390/metabo8010016
    title: RaMP
  - build: coll_regfilter_cq
    doi: 10.1101/2024.08.07.607073v1
    title: RegFilter
  - build: coll_sgmns_cq
    doi: 10.1021/acs.analchem.3c00849
    title: SGMNS
  - build: coll_sigmaccs_cq
    doi: 10.1038/s42004-023-00939-w
    title: SigmaCCS
  - build: coll_sirius
    doi: 10.1038/s41592-019-0344-8
    title: sirius
  - build: coll_sirius_cq
    doi: 10.1038/s41592-019-0344-8
    title: sirius
  - build: coll_smanalyst_cq
    doi: 10.3390/biom15111562
    title: SMAnalyst
  - build: coll_smetas_cq
    doi: 10.3390/metabo13080941
    title: SMetaS
  - build: coll_smolesy_cq
    doi: 10.1021/acs.analchem.1c00113
    title: SMolESY
  - build: coll_spectus_cq
    doi: 10.48550/arxiv.2502.05114
    title: SpecTUS
  - build: coll_specxplore_cq
    doi: 10.1021/acs.analchem.3c04444
    title: specxplore
  - build: coll_stattarget_cq
    doi: 10.1016/j.aca.2018.08.002
    title: statTarget
  - build: coll_struct_cq
    doi: 10.1093/bioinformatics/btaa1031
    title: struct
  - build: coll_submaldi_cq
    doi: 10.21105/joss.02694
    title: subMALDI
  - build: coll_tarmet_cq
    doi: 10.1007/s11306-018-1363-7
    title: TarMet
  - build: coll_tidy_direct_to_ms_cq
    doi: 10.1021/acs.jproteome.3c00784
    title: Tidy-Direct-to-MS
  - build: coll_tidymass_cq
    doi: 10.1038/s41467-022-32155-w
    title: tidyMass
  - build: coll_turboputative_cq
    doi: 10.3389/fmolb.2022.952149
    title: TurboPutative
  - build: coll_umetaflow_cq
    doi: 10.1186/s13321-023-00724-w
    title: UmetaFlow
  - build: coll_viime_cq
    doi: 10.21105/joss.02410
    title: Viime
  - build: coll_viime_path_cq
    doi: 10.21105/joss.02410
    title: Viime
  - build: coll_vinsmoc_cq
    doi: 10.1038/s43588-025-00923-5
    title: VInSMoC
  - build: coll_xcms_2_cq
    doi: 10.1021/ac051437y
    title: XCMS
  - build: coll_zodiac_cq
    doi: 10.1038/s42256-020-00234-6
    title: ZODIAC
  dedup_kept_from: coll_3dmolms_cq
schema_version: 0.2.0
---

# figure_table_interpretation

## Summary

Extract and interpret numerical results, model predictions, and quantitative comparisons from figures, tables, and structured output (MGF, CSV, PKL formats) produced by mass spectrometry prediction workflows. This skill validates that predictions match expected ranges, statistical distributions, and domain constraints (e.g., precursor types, atom counts).

## When to use

After running a 3DMolMS model (or similar MS/MS prediction pipeline) that outputs predictions in MGF, CSV, or PKL format, use this skill to verify prediction quality by examining peak intensities, m/z values, precursor ions, and similarity metrics against ground truth or reference spectra. Triggers include: (1) need to assess whether predicted spectra are chemically plausible; (2) evaluation of model performance via cosine similarity or other metrics; (3) filtering or ranking predictions by confidence; (4) checking whether predicted ions fall within expected instrument-specific mass ranges or precursor type distributions.

## When NOT to use

- Input is already a pre-computed similarity matrix or aggregated summary statistic (e.g., AUC, F1 score already reported); this skill is for extracting and computing per-prediction metrics from raw output files.
- Ground truth spectra are unavailable or incompletely documented; comparison-based interpretation requires reference labeling.
- Molecules violate hard constraints (>300 atoms, unsupported atom types, unsupported precursor types) — these should be filtered out during preprocessing, not interpreted post-hoc.

## Inputs

- predicted_mgf_file (MGF format spectra from molnet_engine.pred_msms)
- ground_truth_spectra (MGF, SDF, or reference library in MoNA/NIST format)
- prediction_dataframe (CSV or PKL output from pred_msms, pred_rt, or pred_ccs)
- test_pkl_file (preprocessed molecule dataset with ground truth labels)
- model_checkpoint (PyTorch .pt file for reproducibility)

## Outputs

- evaluation_results_csv (per-spectrum metrics: cosine similarity, peak accuracy, precursor error)
- similarity_histogram (matplotlib plot of cosine similarity distribution)
- prediction_dataframe_annotated (input predictions + computed metrics + pass/fail flags)
- summary_statistics (mean, std, quantiles of similarity, RT error, CCS error by instrument/precursor type)

## How to apply

Load the predicted spectra (MGF or PKL) and ground truth reference data into a structured format (DataFrame or dictionary). Compute per-spectrum metrics: peak count, intensity distribution, precursor m/z accuracy, and for comparison tasks, cosine similarity or spectral entropy. Filter predictions using constraints extracted from the workflow: atom number ≤300, atom types in {C, O, N, H, P, S, F, Cl, B, Br, I, Na}, and precursor types in {[M+H]+, [M-H]-, [M+H-H2O]+, [M+Na]+}. Plot histograms or scatter plots of similarity scores, retention time residuals, or CCS prediction errors to assess systematic biases. Rationale: The 3DMolMS model learns molecular representations through MS/MS prediction; interpreting its outputs against these domain constraints validates that the learned representations encode chemically and instrumentally meaningful features.

## Related tools

- **molnetpack** (Python package providing MolNet class with pred_msms(), pred_rt(), pred_ccs(), and evaluate() methods to load predictions and ground truth data for interpretation) — https://pypi.org/project/molnetpack/
- **matplotlib** (Visualization library for plotting histograms, scatter plots, and heatmaps of prediction metrics (similarity, error distributions))
- **Pandas** (Data structure library for loading, filtering, and aggregating prediction DataFrames and computing per-spectrum statistics)
- **PyTorch** (Deep learning framework underlying model checkpoints; used to load and reproducibly apply models during prediction interpretation) — https://pytorch.org/get-started/locally/
- **MoNA** (Reference spectral library (MoNA-export-All_LC-MS-MS_QTOF.sdf, MoNA-export-All_LC-MS-MS_Orbitrap.sdf) for ground truth comparison in similarity computation)
- **NIST20** (Reference library (hr_msms_nist.SDF, available under academic license) for evaluating MS/MS prediction accuracy)

## Examples

```
molnet_engine.evaluate(test_pkl="./data/qtof_etkdgv3_test.pkl", pred_mgf="./output_msms.mgf", result_path="./eval_results.csv", plot_path="./eval_similarity_hist.png")
```

## Evaluation signals

- Cosine similarity distribution across test set is unimodal, centered > 0.7, with no unexpected bimodality suggesting model failure on a subset
- Per-spectrum peak count in predicted MGF matches order of magnitude in ground truth (e.g., both have 10–100 peaks for singly-charged ions)
- Precursor m/z values in predictions fall within ±0.01 Da (QTOF) or ±5 ppm (Orbitrap) of input SMILES-derived m/z after accounting for adduct type
- Retention time (RT) and collision cross section (CCS) predictions show residuals with median close to zero and inter-quartile range <2× the training set standard deviation
- Histogram of similarity scores shows no spike at 0 or <0.3 suggesting systematic underperformance on specific subsets (e.g., molecules with unsupported atom types)

## Limitations

- Model predictions are restricted to molecules with ≤300 atoms and atom types in {C, O, N, H, P, S, F, Cl, B, Br, I, Na}; interpretation is undefined for inputs outside these constraints.
- Precursor types supported: [M+H]+, [M-H]−, [M+H-H2O]+, [M+Na]+; predictions on other adducts (e.g., [M+2Na]2+) are not validated.
- Ground truth spectra quality depends on reference library provenance (MoNA, NIST20) and may reflect instrument-specific fragmentation patterns; QTOF and Orbitrap show different spectral distributions and require separate model checkpoints.
- Cosine similarity as a single metric does not capture peak intensity ordering errors or missing low-abundance fragments; supplementary metrics (spectral entropy, peak recall) may be needed for interpretation.

## Evidence

- [readme] 3D Molecular Network for Mass Spectra Prediction (3DMolMS) is a deep neural network model to predict the MS/MS spectra of compounds from their 3D conformations.: "3D Molecular Network for Mass Spectra Prediction (3DMolMS) is a deep neural network model to predict the MS/MS spectra of compounds from their 3D conformations."
- [readme] Predict and save to MGF (checkpoints are downloaded automatically) pred_df = molnet_engine.pred_msms(path_to_results="./output_msms.mgf", instrument="qtof"): "Predict and save to MGF (checkpoints are downloaded automatically) pred_df = molnet_engine.pred_msms(path_to_results="./output_msms.mgf", instrument="qtof")"
- [readme] Evaluate against ground truth results_df = molnet_engine.evaluate(test_pkl="./data/qtof_etkdgv3_test.pkl", pred_mgf="./output_msms.mgf", result_path="./eval_results.csv", plot_path="./eval_similarity_hist.png"): "Evaluate against ground truth results_df = molnet_engine.evaluate(test_pkl="./data/qtof_etkdgv3_test.pkl", pred_mgf="./output_msms.mgf", result_path="./eval_results.csv","
- [methods] Atom types: 'C', 'O', 'N', 'H', 'P', 'S', 'F', 'Cl', 'B', 'Br', 'I', 'Na': "Atom types: 'C', 'O', 'N', 'H', 'P', 'S', 'F', 'Cl', 'B', 'Br', 'I', 'Na'"
- [methods] Precursor types: '[M+H]+', '[M-H]-', '[M+H-H2O]+', '[M+Na]+': "Precursor types: '[M+H]+', '[M-H]-', '[M+H-H2O]+', '[M+Na]+'"
- [readme] This model's molecular representation, learned through MS/MS prediction tasks, can be further applied to enhance performance in other molecular-related tasks, such as predicting retention times (RT) and collision cross sections (CCS).: "This model's molecular representation, learned through MS/MS prediction tasks, can be further applied to enhance performance in other molecular-related tasks, such as predicting retention times (RT)"
