#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import re
infiles = ["genTemplates22.py_20110113_18_15_18.sh.o4296909.1,genTemplates22.py_20110113_18_15_18.sh.o4296941.33,genTemplates22.py_20110113_18_15_18.sh.o4296910.2, genTemplates22.py_20110113_18_15_18.sh.o4296942.34,genTemplates22.py_20110113_18_15_18.sh.o4296911.3, genTemplates22.py_20110113_18_15_18.sh.o4296943.35,genTemplates22.py_20110113_18_15_18.sh.o4296912.4,   genTemplates22.py_20110113_18_15_18.sh.o4296944.36,genTemplates22.py_20110113_18_15_18.sh.o4296913.5,   genTemplates22.py_20110113_18_15_18.sh.o4296945.37,genTemplates22.py_20110113_18_15_18.sh.o4296914.6,   genTemplates22.py_20110113_18_15_18.sh.o4296946.38,genTemplates22.py_20110113_18_15_18.sh.o4296915.7,   genTemplates22.py_20110113_18_15_18.sh.o4296947.39,genTemplates22.py_20110113_18_15_18.sh.o4296916.8,   genTemplates22.py_20110113_18_15_18.sh.o4296948.40,genTemplates22.py_20110113_18_15_18.sh.o4296917.9,   genTemplates22.py_20110113_18_15_18.sh.o4296949.41,genTemplates22.py_20110113_18_15_18.sh.o4296918.10,  genTemplates22.py_20110113_18_15_18.sh.o4296950.42,genTemplates22.py_20110113_18_15_18.sh.o4296919.11,  genTemplates22.py_20110113_18_15_18.sh.o4296951.43,genTemplates22.py_20110113_18_15_18.sh.o4296920.12,  genTemplates22.py_20110113_18_15_18.sh.o4296952.44,genTemplates22.py_20110113_18_15_18.sh.o4296921.13,  genTemplates22.py_20110113_18_15_18.sh.o4296953.45,genTemplates22.py_20110113_18_15_18.sh.o4296922.14,  genTemplates22.py_20110113_18_15_18.sh.o4296954.46,genTemplates22.py_20110113_18_15_18.sh.o4296923.15,  genTemplates22.py_20110113_18_15_18.sh.o4296955.47,genTemplates22.py_20110113_18_15_18.sh.o4296924.16,  genTemplates22.py_20110113_18_15_18.sh.o4296956.48,genTemplates22.py_20110113_18_15_18.sh.o4296925.17,  genTemplates22.py_20110113_18_15_18.sh.o4296957.49,genTemplates22.py_20110113_18_15_18.sh.o4296926.18,  genTemplates22.py_20110113_18_15_18.sh.o4296958.50,genTemplates22.py_20110113_18_15_18.sh.o4296927.19,  genTemplates22.py_20110113_18_15_18.sh.o4296959.51,genTemplates22.py_20110113_18_15_18.sh.o4296928.20,  genTemplates22.py_20110113_18_15_18.sh.o4296960.52,genTemplates22.py_20110113_18_15_18.sh.o4296929.21,  genTemplates22.py_20110113_18_15_18.sh.o4296961.53,genTemplates22.py_20110113_18_15_18.sh.o4296930.22,  genTemplates22.py_20110113_18_15_18.sh.o4296962.54,genTemplates22.py_20110113_18_15_18.sh.o4296931.23,  genTemplates22.py_20110113_18_15_18.sh.o4296963.55,genTemplates22.py_20110113_18_15_18.sh.o4296932.24,  genTemplates22.py_20110113_18_15_18.sh.o4296964.56,genTemplates22.py_20110113_18_15_18.sh.o4296933.25,  genTemplates22.py_20110113_18_15_18.sh.o4296965.57,genTemplates22.py_20110113_18_15_18.sh.o4296934.26,  genTemplates22.py_20110113_18_15_18.sh.o4296966.58,genTemplates22.py_20110113_18_15_18.sh.o4296935.27,  genTemplates22.py_20110113_18_15_18.sh.o4296967.59,genTemplates22.py_20110113_18_15_18.sh.o4296936.28,  genTemplates22.py_20110113_18_15_18.sh.o4296968.60,genTemplates22.py_20110113_18_15_18.sh.o4296937.29,  genTemplates22.py_20110113_18_15_18.sh.o4296969.61,genTemplates22.py_20110113_18_15_18.sh.o4296938.30,  genTemplates22.py_20110113_18_15_18.sh.o4296970.62,genTemplates22.py_20110113_18_15_18.sh.o4296939.31,  genTemplates22.py_20110113_18_15_18.sh.o4296971.63,genTemplates22.py_20110113_18_15_18.sh.o4296940.32,  genTemplates22.py_20110113_18_15_18.sh.o4296972.64"]
outfile = "output.txt"

outpt = open(outfile, 'w')

data = re.compile('(RUN=)\d{4,6}\s(LUMIS=)\d{1,6}\s(EVENT=)\d{1,12}\s(PT=)\d{1,6}\.\d{1,12}')
wspace = re.compile('\s+')

for infile in infiles :
  inpt = open(infile, 'r')
  temp = inpt.read()
  lines = data.findall(temp)
  for line in lines :
    outpt.write(line)
  inpt.close()
outpt.close()
