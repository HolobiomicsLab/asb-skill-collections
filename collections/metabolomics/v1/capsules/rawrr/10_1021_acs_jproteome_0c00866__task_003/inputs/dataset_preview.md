### `figures/rawRcolor.png`
_binary file, 333788 bytes_

### `figures/rawRcolor10%.png`
_binary file, 39607 bytes_

### `figures/rawrr_logo.png`
_binary file, 28609 bytes_

### `paper.md`
```
# fgcz__rawrr

## Introduction

[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)
[![JPR](https://img.shields.io/badge/JPR-10.1021%2Facs.jproteome.0c00866-brightgreen)](http://dx.doi.org/10.1021/acs.jproteome.0c00866)
[![codecov](https://codecov.io/gh/fgcz/rawrr/branch/master/graph/badge.svg?token=OO4Y7G4UUX)](https://codecov.io/gh/fgcz/rawrr)
[![bioc-check](https://bioconductor.org/shields/build/devel/bioc/rawrr.svg)](http://bioconductor.org/checkResults/devel/bioc-LATEST/rawrr/)
![Downloads](https://img.shields.io/github/downloads/fgcz/rawrr/total)

![rawrrHexSticker](rawrr_logo.png)

# rawrr

The package provides access to proprietary Thermo Fisher Scientific Orbitrap instrument data as a stand-alone R package or serves as [MsRawFileReaderBackend](https://github.com/cpanse/MsBackendRawFileReader) for the Bioconductor [Spectra](https://bioconductor.org/packages/Spectra/) package.
rawrr wraps the functionality of the [RawFileReader](https://github.com/thermofisherlsms/RawFileReader) [.NET assembly](https://www.mono-project.com/docs/advanced/assemblies-and-the-gac/). 
Test files are provided by the [tartare](https://bioconductor.org/packages/tartare/) ExperimentData package.


## Methods

# System requirements

The `rawrr` executable will run out of the box. 

I you want to build on your own follow the text below.

## Compile and Link yourself

In case you prefer to compile `rawrr.exe` from C# source code, please install
the .NET 8.0

### Linux (debian:10/ubuntu:20.04) (debian:12/ubuntu:24)


```{sh}
## DEPRECIATED: sudo apt-get install mono-mcs mono-xbuild
sudo apt-get install dotnet-sdk-8.0
```

### macOS (Catalina/BigSur/.../Sequoia)

https://dotnet.microsoft.com/en-us/download

### Microsoft Windows

https://dotnet.microsoft.com/en-us/download

## Install the .NET assemblies 

assemblies aka Common Intermediate Lang
…[truncated]
```
