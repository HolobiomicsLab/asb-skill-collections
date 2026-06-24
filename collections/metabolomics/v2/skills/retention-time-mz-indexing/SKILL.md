---
name: retention-time-mz-indexing
description: Use when when you have parsed .mzML or Thermo .raw LC-MS data and need
  to support interactive or programmatic queries by retention time (RT) and mass-to-charge
  ratio (m/z) without re-scanning the entire file.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3644
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - lcmsWorld
  - RawFileReader (Thermo)
  - mzML parser
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1021/acs.jproteome.0c00618
  title: lcmsWorld
evidence_spans:
- lcmsWorld is a 3d viewer for LC-MS data
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lcmsworld_cq
    doi: 10.1021/acs.jproteome.0c00618
    title: lcmsWorld
  dedup_kept_from: coll_lcmsworld_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.0c00618
  all_source_dois:
  - 10.1021/acs.jproteome.0c00618
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# retention-time-mz-indexing

## Summary

Construction of an in-memory indexed data structure for LC-MS spectral data keyed by retention time and m/z values, enabling rapid random-access queries during 3D visualization and analysis of mass spectrometry datasets. This skill is essential for interactive exploration of large LC-MS files where sequential scanning would be prohibitively slow.

## When to use

When you have parsed .mzML or Thermo .raw LC-MS data and need to support interactive or programmatic queries by retention time (RT) and mass-to-charge ratio (m/z) without re-scanning the entire file. Typical triggers include: (1) the user requests 3D visualization with rotation/zoom on a large dataset; (2) you need to extract a chromatogram for a specific m/z window; (3) you are matching identification results (peptides with assigned m/z and RT) against raw spectral data; (4) memory constraints permit caching but disk I/O is the bottleneck.

## When NOT to use

- Input is a pre-computed feature table or peak list (m/z and RT already aggregated); use direct annotation matching instead.
- File is small (<100 MB) and fits entirely in RAM; sequential in-memory search may be faster than index construction overhead.
- You need only a single chromatogram or mass spectrum extraction; a full index is unnecessary for one-off queries.

## Inputs

- Parsed LC-MS spectral data structure (containing scans with retention time, m/z array, intensity array, scan number, and MS level)
- File metadata (total scan count, RT range, m/z range)

## Outputs

- Indexed spectral data structure with random-access capability by (retention_time, m/z)
- Validation report confirming index completeness (scan count, index hit rate)

## How to apply

After extracting key spectral metadata (retention time, m/z values, intensities, scan number, MS level) from the parsed file, construct a hierarchical or multi-keyed in-memory index. The most common approach is a two-level index: first partition scans by retention time (or retention time bin) to support RT-range queries; second, within each RT partition, index m/z values (often as a sorted array or tree) to enable rapid m/z lookups. Validate that the index is complete by confirming that every extracted scan has entries in both indices and that the number of indexed scans matches the file's scan count. For large files (>1–2 GB), consider pre-allocating data structures and using memory-mapped I/O to avoid loading the entire dataset into RAM at once. During viewer operation, use the index to fetch only the scans needed for the current 3D viewport, then render them directly without re-parsing.

## Related tools

- **lcmsWorld** (3D LC-MS viewer that loads and indexes .mzML or Thermo .raw files to enable interactive spatial navigation and real-time filtering by retention time and m/z) — https://github.com/PGB-LIV/lcmsWorld
- **RawFileReader (Thermo)** (Parser for proprietary Thermo .raw binary format; outputs spectral metadata (RT, m/z, intensity, scan number) consumed by the indexing step)
- **mzML parser** (Parser for XML-based .mzML spectral data format; extracts retention time, m/z values, intensities, and scan-level metadata for indexing)

## Evaluation signals

- Index cardinality: total number of scans in the index equals the file's declared scan count (no missing or duplicate scans).
- RT range coverage: min and max retention times in the index span the file's documented RT range with no gaps.
- m/z lookup latency: random queries by (RT, m/z) return results in <10 ms (wall-clock time), confirming index efficiency.
- Scan retrieval completeness: for each indexed scan, all four metadata fields (retention time, m/z array, intensity array, scan number) are present and non-null.
- Indexed spectral intensity distribution: histogram of indexed scan intensities matches the original file (no systematic loss or corruption during indexing).

## Limitations

- Memory consumption scales with spectral complexity and file size; the README notes that .lcms file size is roughly equivalent to the source .raw or .mzml, requiring 'roughly the same amount of hard disk space.' For very large files (>10 GB), indexing may exceed available RAM even on high-end workstations.
- Index construction is one-time only and stored in the .lcms derivative file; rebuilding the index (if file format changes or corruption is suspected) requires re-parsing the entire source file, which is time-consuming.
- The README states that RawFileReader (used for .raw parsing) is '64-bit only .NET application' and requires '.NET Framework 4.7 on Windows,' limiting portability to Windows; Linux and MacOS users must compile from source.
- No changelog or version history is documented, so reproducibility and index format stability across lcmsWorld releases are unclear.

## Evidence

- [other] Extract key spectral metadata (retention time, m/z values, intensities, scan number, MS level). Construct an in-memory spectral data structure with indexed access to scans.: "Extract key spectral metadata (retention time, m/z values, intensities, scan number, MS level). Construct an in-memory spectral data structure with indexed access to scans."
- [readme] Roughly the same amount of hard disk space as the .raw, .mzml being viewed. For large files, preferably loaded from fast hard disk - the viewable .lcms file is created on the same disk, and data is streamed from it during use.: "Roughly the same amount of hard disk space as the .raw, .mzml being viewed. For large files, preferably loaded from fast hard disk"
- [readme] The first time you load a file, lcmsWorld automatically converts this file and creates a corresponding .lcms file. In future, you can load this .lcms file to start viewing instantly.: "lcmsWorld automatically converts this file and creates a corresponding .lcms file. In future, you can load this .lcms file to start viewing instantly."
- [readme] RawFileReader from Thermo is used to load .raw files. This is a 64-bit only .NET application. You may need to install .NET Framework 4.7 on Windows to use this.: "RawFileReader from Thermo is used to load .raw files. This is a 64-bit only .NET application."
- [readme] lcmsWorld is a 3d viewer for LC-MS data (it can load .mzml or Thermo .raw format files): "lcmsWorld is a 3d viewer for LC-MS data (it can load .mzml or Thermo .raw format files)"
