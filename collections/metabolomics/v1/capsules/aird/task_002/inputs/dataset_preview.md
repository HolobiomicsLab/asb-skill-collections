### `figures/AIR.png`
_binary file, 35011 bytes_

### `figures/AIR_01.png`
_binary file, 13260 bytes_

### `figures/AirdManager.png`
_binary file, 3586 bytes_

### `figures/AirdPro.png`
_binary file, 23266 bytes_

### `figures/AirdProLogo.png`
_binary file, 7449 bytes_

### `figures/AirdProTrans.png`
_binary file, 24669 bytes_

### `figures/AirdPro_ 2.png`
_binary file, 24669 bytes_

### `figures/AirdPro_ 3.png`
_binary file, 23266 bytes_

### `figures/Arrows.png`
_binary file, 280 bytes_

### `figures/CleanErrors.png`
_binary file, 3497 bytes_

### `figures/CleanFinished.png`
_binary file, 3499 bytes_

### `figures/Computation.png`
_binary file, 749 bytes_

### `figures/Connected.png`
_binary file, 5209 bytes_

### `figures/Conversion.png`
_binary file, 6594 bytes_

### `figures/ConversionCenter.png`
_binary file, 3485 bytes_

### `figures/Help.png`
_binary file, 9553 bytes_

### `figures/MetaboLights.jpg`
_binary file, 8552 bytes_

### `figures/Proteomexchange.png`
_binary file, 6695 bytes_

### `figures/SearchEngine.png`
_binary file, 395 bytes_

### `paper.md`
```
# CSi-Studio__AirdPro

## Introduction

AirdPro V5 is now available at 2023.7

AirdPro V6 is now available at 2024.4

# AirdPro
AirdPro is a GUI client for conversion from vendor files to Aird files. AirdPro is written in C# and is based on pwiz_bindings_cli.dll from the ProteoWizard project.
AirdPro is opensource under the MulanPSL2 license


## Methods

# AirdPro Docker Deployment Guide (macOS + Wine)

## Project Overview

AirdPro is a Windows desktop application based on .NET Framework 4.8, featuring both GUI interface and command-line functionality. Since macOS does not natively support .NET Framework, this project enables AirdPro to run on macOS through Docker + Wine technology.

**Important Note**: This solution uses Wine to run Windows applications in Linux containers. Performance may not match native Windows environments, and the first run requires longer initialization time.

## Prerequisites

### macOS Environment Requirements
- macOS 10.15+ (Catalina or later)
- Docker Desktop for Mac (version 20.10+)
- XQuartz (for GUI display support)
- Minimum 8GB available RAM (16GB recommended)
- Stable internet connection (required for downloading Wine and .NET Framework on first run)

### Hardware Requirements
- Intel or Apple Silicon Mac
- Minimum 20GB available disk space
- CPU with virtualization support

## Quick Start

### 1. Install Dependencies

#### Install Docker Desktop
```bash
# Download and install Docker Desktop for Mac
# Download URL: https://www.docker.com/products/docker-desktop

# Start Docker Desktop after installation
open -a "Docker Desktop"
```

#### Install XQuartz (Required for GUI version)
```bash
# Install XQuartz using Homebrew
brew install --cask xquartz

# Start XQuartz
open -a XQuartz

# Configure XQuartz (required for first run)
# 1. Open XQuartz Preferences
# 2. Check "Allow connections from network clients" in Security tab
# 3. Restart XQuartz
```

### 2. Build Docker Images

```bash
# Build all images (first build may take longer)
.
…[truncated]
```
