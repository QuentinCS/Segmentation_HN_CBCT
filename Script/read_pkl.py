# Scrit to read and print .pkl files as dictionnary 

import pickle
import sys

if len(sys.argv) <= 1:
    print("Error: Argument missing. Need one argument to name task \n")
    exit()

with open(sys.argv[1], 'rb') as f:
    data = pickle.load(f)


for i in data.items():
    print(i)
