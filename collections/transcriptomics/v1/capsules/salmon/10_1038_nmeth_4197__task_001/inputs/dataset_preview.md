### `paper.md`
```
# COMBINE-lab__salmon

## Introduction

# salmon

[![CI](https://github.com/COMBINE-lab/salmon/actions/workflows/ci.yml/badge.svg?branch=rust-rewrite)](https://github.com/COMBINE-lab/salmon/actions/workflows/ci.yml)
[![install with bioconda](https://img.shields.io/badge/install%20with-bioconda-brightgreen.svg?style=flat-square)](http://bioconda.github.io/recipes/salmon/README.html)

> [!IMPORTANT]
> **This is salmon 2.0 — a from-scratch Rust rewrite of salmon.** It keeps the
> same workflow (`salmon index` → `salmon quant` → `quant.sf`) and the same
> output formats downstream tools read, but it is a new major version with some
> breaking changes. The most important one: **the index format changed, so you
> must rebuild your index.** See **[MIGRATION.md](MIGRATION.md)** for the full
> list of changed/removed/new options.
>
> The final **C++** release (salmon `1.12.0`) lives on the [`cpp`](https://github.com/COMBINE-lab/salmon/tree/cpp)
> branch and remains installable as the `salmon-cpp` conda package.
>
> Single-cell quantification moved to the [alevin-fry](https://github.com/COMBINE-lab/alevin-fry)
> ecosystem (`salmon alevin` is removed).


## Methods

## Contributing code

Any code that you contribute will be licensed under the GPLv3-license adopted by `salmon`. However, by contributing
code to this project, you also extend permission for your contribution to be re-licensed under the BSD 3-clause 
license (under which we anticipate Salmon will be released once existing GPL code can be removed).

Code contributions should be made via pull requests.  Please make all PRs to the _develop_ branch 
of the repository.  PRs made to the _master_ branch may be rejected if they cannot be cleanly rebased 
on _develop_.  Before you make a PR, please check that:

 * Your PR describes the purpose of your commit. Is it fixing a bug, adding functionality, etc.?
 * Commit messages have been made using [*conventional commits*](https://www.conventionalcommits.org/en/v1.0.0/) — plea
…[truncated]
```
