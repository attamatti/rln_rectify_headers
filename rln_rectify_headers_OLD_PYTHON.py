#!/usr/bin/python

#### remove header lines and data columns from a batch of star files to make them match a model starfile
# skips files that don't contain the specified column
# helpful for combining autopicked and manual picked data 

# back-compatible version for old python (pre 2.x)
# 2017 Matt Iadanza - University of Leeds - Astbury Centre for Structural Molecular Biology
# please acknowledge if you use this script

import sys
import glob
import os

###---------function: read the star file get the header, labels, and data -------------#######
def read_starfile(f):
    alldata = open(f,'r').readlines()
    labelsdic = {}
    data = []
    header = []
    for i in alldata:
        if '#' in i:
            labelsdic[i.split('#')[0]] = int(i.split('#')[1])-1
        if len(i.split()) >= 2 and '#' not in i:
            data.append(i.split())
        if len(i.split()) < 2 or '#' in i:
            header.append(i.strip("\n"))
    return(labelsdic,header,data)
#---------------------------------------------------------------------------------------------#

model_file=raw_input('Name of model file (with correct headers): ')
model_labels,model_header,model_data = read_starfile(model_file)
print('new header format')
for i in model_header:
    if '#' in i:
        print i

if os.path.isdir('rln_head_rec') == False:
    os.system('mkdir rln_head_rec')

files_to_process = glob.glob(raw_input('file search string: '))
for i in files_to_process:
    print(i)
for filename in files_to_process:
    output = open('rln_head_rec/%s'%(filename.split('/')[-1]),'w')
    headerkeys = []
    for i in model_header:
        output.write('%s\n'%(i))
        if '_rln' in i:
            headerkeys.append(i.split('#')[0])
    labels,header,data = read_starfile(filename)
    bad = False
    for i in data:
        if bad == True:
            break
        line = []
        for col in headerkeys:
            try:
                line.append(i[labels[col]])
            except KeyError:
               bad = True
               print("skipping %s because it doesn't contain header column %s" %(filename,col))
        if bad == False:
            line = '\t'.join(line)
            output.write('%s\n'%(line))
    output.close()
