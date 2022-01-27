#!/bin/python3
import sys
import os

def getPath(_global: bool) -> str:
	if _global:
		return os.path.join(sys.path[0], "makemake.cfg")
	else:
		return ".makemake.cfg"


def parseF(fname: str) -> dict:
	d = {}
	with open(fname, "r") as f:
		for l in f.readlines():
			if l.startswith("GXX"):
				d["GXX"] = l.split("=")[1].strip()
			if l.startswith("CFLAGS"):
				d["CFLAGS"] = l.split("=")[1].strip()
			if l.startswith("EXE"):
				d["EXE"] = l.split("=")[1].strip()
			if l.startswith("MFILE"):
				d["MFILE"] = l.split("=")[1].strip()
	return d

def parseConfig():
	# if local cfg, get local it, else get global cfg 
	lPath = getPath(False)
	if os.path.isfile(lPath):
		return parseF(lPath)
	return parseF(getPath(True))


def writeConfig(d: dict, _global: bool):
	with open(getPath(_global), "w") as f:
		f.write("GXX = {}\n".format(d["GXX"]))
		f.write("CFLAGS = {}\n".format(d["CFLAGS"]))
		f.write("EXE = {}\n".format(d["EXE"]))
		f.write("MFILE = {}\n".format(d["MFILE"]))


def setCompiler(compiler: str, _global: bool):
	cfg = parseConfig()
	cfg["GXX"] = compiler
	writeConfig(cfg, _global)


def setFlags(flags: list, _global: bool):
	cfg = parseConfig()
	cfg["CFLAGS"] = " ".join(flags)
	writeConfig(cfg, _global)


def setExeName(exe: str, _global: bool):
	cfg = parseConfig()
	cfg["EXE"] = exe
	writeConfig(cfg, _global)


def setMfileName(mfile: str, _global: bool):
	cfg = parseConfig()
	cfg["MFILE"] = mfile
	writeConfig(cfg, _global)


def getIncludes(fname):
	includes = []
	isMain = False
	with open(fname, "r") as f:
		for l in f.readlines():
			if l.startswith("#include \""):
				first = l.find("\"") + 1
				includes.append(l[ first : l.find("\"", first)])
			if l.startswith("int main("):
				isMain = True
	return includes, isMain


def getDependencies():
	ls = []
	for fname in os.listdir():
		if not (fname.endswith(".cpp") or fname.endswith(".cc")):
			continue
		includes, isMain = getIncludes(fname)
		obj = fname.rsplit(".", 1)[0] + ".o"
		tup = [fname, obj, includes]
		if isMain:
			ls.insert(0, tup)
		else:
			ls.append(tup)
	return ls

def generateMakefile():
	deps = getDependencies()
	cfg = parseConfig()
	with open(cfg["MFILE"], "w") as f:
		f.write("GXX = {}\n".format(cfg["GXX"]))
		f.write("CFLAGS = {}\n".format(cfg["CFLAGS"]))
		f.write("{}: ".format(cfg["EXE"]) + " ".join(tup[1] for tup in deps) + "\n")
		f.write("\t$(GXX) $(CFLAGS) -o {} ".format(cfg["EXE"]) + " ".join(tup[1] for tup in deps) + "\n")
		f.write("\n")
		for dep in deps:
			f.write(dep[1] + ": " + dep[0] + " " + " ".join(dep[2]) + "\n")
			f.write("\t$(GXX) $(CFLAGS) -c " + dep[0] + "\n")
			f.write("\n")
		f.write("clean:\n")
		f.write("\trm *.o {}\n".format(cfg["EXE"]))


if __name__ == "__main__":
	argv = sys.argv	# one shouldn't modify sys.argv
	argv.pop(0)	# pop of file path

	# write global cfg, if it doesn't exist
	if not os.path.isfile(getPath(True)):
		writeConfig({"GXX": "g++", "CFLAGS": "", "EXE": "run", "MFILE": "Makefile"}, True)
	
	# check if should be global
	if "-g" in argv:
		_global = True
		argv.remove("-g")
	else:
		_global = False
	
	# no args -> generate makefile
	if not argv:	
		generateMakefile()
		exit(0)
	
	# pop of first arg
	fArg = argv.pop(0)	
	if fArg == "-compiler":
		if not argv:	# no args left
			print("err: expected string specifying compiler")
			exit(1)
		setCompiler(argv[0], _global)
	elif fArg == "-exe":
		if not argv:	# no args left
			print("err: expected string specifying name of exe")
			exit(1)
		setExeName(argv[0], _global)
	elif fArg == "-mfname":
		if not argv:	# no args left
			print("err: expected string specifying name of makefile (should be 'makefile' or 'Makefile')")
			exit(1)
		setMfileName(argv[0], _global)
	elif fArg == "-flags":
		setFlags(argv, _global)
	elif fArg == "help":
		print("makemake\t- generates a makefile")
		print("makemake -compiler <name> (-g)\t- sets used compiler to <name>")
		print("makemake -exe <name> (-g)\t- sets name of built execultable to <name>")
		print("makemake -mfname <name> (-g)\t- sets name of created makefile to <name>, should be 'makefile' or 'Makefile', but I won't stop you")
		print("makemake -flags <name1> <name2> ... (-g)\t- sets used flags to all names that follow")
		print("makemake help\t- prints help")
	else:
		print("err: unkown command")
		print("\tuse 'makemake help' to get help about usage")