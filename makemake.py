#!/bin/python3
import sys
import os


def parseConfig():
	gxx = ""
	cflags = ""
	with open("makemake.cfg", "r") as f:
		for l in f.readlines():
			if l.startswith("GXX"):
				gxx = l.split("=")[1].strip()
			if l.startswith("CFLAGS"):
				cflags = l.split("=")[1].strip()
	return gxx, cflags


def writeConfig(gxx, cflags):
	with open("makemake.cfg", "w") as f:
		f.write("GXX = {}\n".format(gxx))
		f.write("CFLAGS = {}\n".format(cflags))


def setCompiler(compiler):
	gxx, cflags = parseConfig()
	writeConfig(compiler, cflags)


def setFlags(flags):
	gxx, cflags = parseConfig()
	writeConfig(gxx, " ".join(flags))


def getIncludes(fname):
	includes = []
	isMain = False
	with open(fname, "r") as f:
		for l in f.readlines():
			#if fname == "3_4.cpp":
			#	print(l)
			#	print(l.startswith("#include \""))
			if l.startswith("#include \""):
				first = l.find("\"") + 1
				includes.append(l[ first : l.find("\"", first)])
			if l.startswith("int main("):
				isMain = True
	#print(includes)
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
	gxx, cflags = parseConfig()
	with open("Makefile", "w") as f:
		f.write("GXX = {}\n".format(gxx))
		f.write("CFLAGS = {}\n".format(cflags))
		f.write("main: " + " ".join(tup[1] for tup in deps) + "\n")
		f.write("\t$(GXX) $(CFLAGS) -o run " + " ".join(tup[1] for tup in deps) + "\n")
		f.write("\n")
		for dep in deps:
			f.write(dep[1] + ": " + dep[0] + " " + " ".join(dep[2]) + "\n")
			f.write("\t$(GXX) $(CFLAGS) -c " + dep[0] + "\n")
			f.write("\n")
		f.write("clean:\n")
		f.write("\trm *.o run\n")


if __name__ == "__main__":
	if not os.path.isfile("makemake.cfg"):
		writeConfig("g++", "")

	if len(sys.argv) == 1:
		generateMakefile()
	elif sys.argv[1] == "-compiler":
		if len(sys.argv) < 3:
			print("err: expected string specifying compiler")
			exit(1)
		setCompiler(sys.argv[2])
	elif sys.argv[1] == "-flags":
		setFlags(sys.argv[2 : ] if len(sys.argv) > 2 else [])
	elif sys.argv[1] == "help":
		print("makemake\t- generates a makefile")
		print("makemake -compiler <name>\t- sets used compiler to <name>")
		print("makemake -flags <name1> <name2> ...\t- sets used flags to all names that follow")
		print("makemake help\t- prints help")
	else:
		print("err: unkown command")
		print("\tuse 'makemake help' to get help about usage")