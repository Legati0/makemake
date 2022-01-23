# Makemake
## Description
Simple script to generate makefiles, I may change some stuff if something is not working. 

The special thing about this makefile generator is, that it saves the specified compiler and compiler flags, no need to always set them when creating a new makefile. For this the compiler and compiler flags are stored in `/installdir/makemake.cfg`.
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
Standard is `g++`.
```
makemake -compiler <compilername>
```
### Setting specific compiler flags
Standard are no flags.
```
makemake -flags <flag1> <flag2> <flag3> ...
```
To clear compiler flags, just specify no flags
```
makemake -flags
```
