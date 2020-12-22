import sys
import os
# from zipfile import  ZipFile
import zipfile
import shutil


def ziprocess(filename):
    currentdir = os.getcwd()
    with zipfile.ZipFile(filename, 'r') as zip:
        filename = filename.split('/')[-1]
        if not os.path.exists('vortodata'):
            os.mkdir('vortodata')
        if not os.path.exists('vortodata/' + filename.rstrip('.zip')):
            os.mkdir('vortodata/' + filename.rstrip('.zip'))
        if (len(os.listdir(currentdir + '/vortodata/' + filename.rstrip('.zip'))) == 0):
            zip.extractall(currentdir + '/vortodata/' + filename.rstrip('.zip'))
    return currentdir + '/vortodata/' + filename.rstrip('.zip')


def processinfomodel(fileaccess, filename):
    file = open(fileaccess + '/' + filename, "r")
    functionblockfiles = []
    namespace = ""
    infomodel = ""
    for line in file:
        if (line.__contains__("namespace")):
            namespace = line.split(" ")[1].rstrip("\n")
        if (line.__contains__("infomodel")):
            infomodel = line.split(" ")[1].rstrip("\n")
        if (line.__contains__("using")):
            print(line)
            splittedline = line.split(" ")
            functionblock = splittedline[1].rstrip(';')
            splittedline[2] = splittedline[2].rstrip("\n")
            parts = functionblock.split(".")

            functionblock = ""
            for i in range(len(parts)):
                if (i == len(parts) - 1):
                    functionblock = functionblock + parts[i]
                elif (i == len(parts) - 2):
                    functionblock = functionblock + parts[i] + ":"
                else:
                    functionblock = functionblock + parts[i] + "."

            functionblockfile = functionblock + ":" + splittedline[2] + ".fbmodel"
            functionblockfiles.append(functionblockfile)

    for funcfile in functionblockfiles:
        try:
            open(fileaccess + "/" + funcfile, 'r')
        except IOError:
            print("There is no such file: " + funcfile)

    fblocks = False
    featurenames = {}
    file = open(fileaccess + '/' + filename, "r")
    for line in file:
        if (fblocks):
            if (line.__contains__('\t')):
                featurename = line.lstrip("\t").lstrip()
            else:
                featurename = line.lstrip()
            featurename = featurename.rstrip('\n')
            featurename = featurename.split(" ")
            if (len(featurename) >= 2):
                for funcfile in functionblockfiles:
                    if (funcfile.__contains__(featurename[2])):
                        featurenames[featurename[0]] = funcfile
        if (line.__contains__("functionblocks")):
            fblocks = True;
        if (line.__contains__("}")):
            fblocks = False;
    processfunctionblocks(fileaccess, featurenames,namespace,infomodel)


def processfunctionblocks(fileaccess, funcbdict, ns, imodel):
    alldicts = {}
    alloperations = []
    namespaces = []

    for key in funcbdict.keys():
        featurename = key
        alldicts[featurename] = {}
        featurefilename = fileaccess + '/' + funcbdict[key]
        status = False
        configuration = False
        operation = False
        datadict = {}
        operationarray = []
        with open(featurefilename, 'r') as f:
            for line in f:
                if (line.__contains__("vortolang")):
                    continue
                if (line.__contains__("namespace")):
                    namespace = line.split(" ")[1].rstrip('\n')
                    namespaces.append(namespace)
                    continue
                if (line.__contains__("version")):
                    continue
                if (line.__contains__("displayname")):
                    continue
                if (line.__contains__("description")):
                    continue
                if (line.__contains__("functionblock")):
                    continue
                if (line.__contains__("status")):
                    status = True
                    continue
                if (line.__contains__("configuration")):
                    configuration = True
                    continue
                if (line.__contains__("operation")):
                    operation = True
                    continue
                if (line.__contains__("}")):
                    status = False
                    configuration = False
                    operation = False
                if (status | configuration):
                    line = line.lstrip()
                    line = line.rstrip('\n')
                    dataarray = line.split(" ")
                    if (line.__contains__("mandatory") | line.__contains__("optional")):
                        datadict[dataarray[1]] = dataarray[3]
                    else:
                        datadict[dataarray[0]] = dataarray[2]
                if (operation):
                    line = line.lstrip()
                    line = line.rstrip('\n')
                    op = line.split("(")[0]
                    operationarray.append(op)

        alldicts[featurename] = datadict
        alloperations.append(operationarray)
    print("[NAMESPACE]")
    print(ns)
    print("[IMODEL]")
    print(imodel)
    print("[DATA]")
    for key in alldicts.keys():
        print("Functionblock " + key)
        for otherkey in alldicts[key].keys():
            print(otherkey + " " + alldicts[key][otherkey])
    print("[OPERATIONS]")
    for operations in alloperations:
        for operation in operations:
            print(operation)


def prepocess():
    if (len(sys.argv) > 1):
        path = sys.argv[1]
        file = path.split('/')[-1]
    if len(sys.argv) < 2:
        print("Zip file is missing")
    elif not zipfile.is_zipfile(path):
        print("Given file's format is not zip")
    else:
        fileaccess = ziprocess(path)
        for filename in os.listdir(fileaccess):
            if (filename.endswith(".infomodel")):
                processinfomodel(fileaccess, filename)


prepocess()
