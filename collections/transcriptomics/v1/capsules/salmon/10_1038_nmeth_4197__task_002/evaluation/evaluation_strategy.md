# Evaluation Strategy

## Direct Checks

- File exists: yeast ERR458493 dataset (SRA accession ERR458493) retrievable from ENA or SRA
- File exists: Ensembl R64-1-1 S. cerevisiae cDNA reference (6,612 transcripts) retrievable from Ensembl FTP or GitHub release artifact
- Script runs: salmon 1.11.4 (C++ pre-fix version) executable or container image obtainable from COMBINE-lab/salmon cpp branch or conda salmon-cpp package
- Script runs: salmon 1.12.0 (C++ post-fix version) executable or container image obtainable from COMBINE-lab/salmon cpp branch or conda salmon-cpp package
- Script runs: salmon 2.0.0 (Rust port) executable obtainable from GitHub release, cargo, or conda
- Script runs: pufferfish commit 5dce7f4 (with SSHash orientation fix) retrievable and compilable or pinned in salmon 1.12.0
- File exists: salmon index built from Ensembl R64-1-1 cDNA using salmon 1.11.4 (C++ pre-fix), salmon 1.12.0 (C++ post-fix), and salmon 2.0.0 (Rust)
- File exists: salmon quant output (quant.sf) for ERR458493 using each of the three configurations above
- Value in range: C++ salmon 1.11.4 (pre-fix) mapping rate on ERR458493 equals 83.48% (byte-for-byte or within ±0.01 percentage points)
- Value in range: C++ salmon 1.12.0 (post-fix) mapping rate on ERR458493 equals 85.55% (byte-for-byte or within ±0.01 percentage points)
- Value in range: salmon 2.0.0 (Rust) mapping rate on ERR458493 equals 85.55% (byte-for-byte or within ±0.01 percentage points)
- Value in range: NumReads Pearson correlation between C++ 1.12.0 and Rust 2.0.0 quant.sf output ≈ 0.99 (robust to rounding; acceptable range 0.985–0.995)
- Value in range: EffectiveLength Pearson correlation between C++ 1.12.0 and Rust 2.0.0 quant.sf output equals 0.9996 (robust to minor floating-point precision differences; acceptable range 0.999–1.0)
- Output matches reference: byte-identical index (same k-length, same transcripts, same reference) used across all three quantifications to control for index format differences

## Expert Review

- Verify that the ~2% improvement from C++ 1.11.4 to 1.12.0 (83.48% → 85.55%) is causally attributable to the pufferfish SSHash streaming-orientation bug fix (commit 5dce7f4) and not to other changes in salmon 1.11.4 → 1.12.0; cross-check pufferfish changelog and salmon 1.12.0 release notes for confounding fixes
- Verify that the Rust port mapping rate (85.55%) matches C++ post-fix (85.55%) within 1 read as claimed; inspect raw SAM/PAF alignment outputs and count total mapped reads for both to confirm 'within 1 read' statement is accurate
- Verify that the 62,812 reads mapped by Rust but not C++, and the 154 reads mapped by C++ but not Rust, are reproducible and that the documented chain-sub-optimality threshold difference (orphanChainSubThresh = 0.95 in C++, default off in Rust) and benign tie-breaks account for ~80% of this asymmetry as claimed
- Confirm that no score-threshold bug or correctness bug is present in either implementation by spot-checking a random sample of the 62,812 Rust-only and 154 C++-only alignments for alignment correctness, score consistency, and tie-break handling
