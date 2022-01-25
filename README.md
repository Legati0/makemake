# Makemake
## Description
Simple script to generate makefiles, I may change some stuff if something is not working. 

The special thing about this makefile generator is, that it saves the specified compiler, compiler flags, the name of the exe and even how the makefile should be called. No need to always set them when creating a new makefile. For this the params are globally stored in `/path/to/install/makemake.cfg` and locally in your working dir as `.makemake.cfg`. The global config will be used if there is no local config. A local config will only be generated when a var is set locally. If there is no global config, a new one is generated.

## Installation
```bash
$ cd /usr/src/
$ git clone https://github.com/Legati0/makemake.git
$ sudo ln -s /usr/src/makemake/makemake.py /usr/bin/makemake
$ sudo chmod +x /usr/bin/makemake
```
To test if it's working:
```
$ makemake help
```

## Usage
### Creating a makefile
```
$ makemake
```
### Setting a specific compiler
Standard is `g++`. Add `-g` to set it globally.
```
$ makemake -compiler <compilername>
```
### Setting specific compiler flags
Standard are no flags. Add `-g` to set it globally.
```
$ makemake -flags <flag1> <flag2> <flag3> ...
```
To clear compiler flags, just specify no flags
```
$ makemake -flags
```
### Setting name of built executable
Standard is `run`. Add `-g` to set it globally.
```
$ makemake -exe <exe name>
```
### Setting name of generated makefile
Standard is `Makefile`. Add `-g` to set it globally.
```
$ makemake -mfname <makefile name>
```
