from sys import *

ordered = int(argv[1])
n = int(argv[2])
parts = int(argv[3])
blocks = int(argv[4])
assert(blocks <= parts)

for i in range(0,parts,blocks):
    j = min(parts,i+blocks)
    prefix = "_main_"+str(ordered)+"_"+str(n)+"_"+str(parts)+"_"+str(i)+"-"+str(j)
    with open(prefix+".job","w") as f:     
        f.write("#!/bin/sh\n")
        f.write("#$ -cwd\n")
        f.write("#$ -N "+prefix+"\n")
        f.write("#$ -o "+prefix+".out\n")
        f.write("#$ -e "+prefix+".err\n")
        f.write("#$ -j n\n")
        f.write("#$ -pe mp "+str(blocks)+"\n")
        f.write("#$ -l h_rt=720000\n")
        f.write("#$ -m abe\n")
        f.write("#$ -M scheuch@math.tu-berlin.de\n")
        f.write("./main "+str(ordered)+" "+str(n)+" "+str(parts)+" "+str(i)+" "+str(j)+"\n")

