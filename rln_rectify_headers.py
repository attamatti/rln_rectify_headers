#!/usr/bin/python

#### remove header lines and data columns from a batch of star files to make them match a model starfile
# skips files that don't contain the specified column
# helpful for combining autopicked and manual picked data 

# 2017 Matt Iadanza - University of Leeds - Astbury Centre for Structural Molecular Biology
# please acknowlegde if you use this script


import sys
import glob
import os

###---------function: read the star file get the header, labels, and data -------------#######
def read_starfile(f):
    inhead = True
    alldata = open(f,'r').readlines()
    labelsdic = {}
    data = []
    header = []
    count = 0
    labcount = 0
    for i in alldata:
        if '_rln' in i and '#' in i:
            labelsdic[i.split('#')[0]] = labcount
            labcount+=1
        if inhead == True:
            header.append(i.strip("\n"))
            if '_rln' in i and '#' in i and  '_rln' not in alldata[count+1] and '#' not in alldata[count+1]:
                inhead = False
        elif len(i.split())>=1:
            data.append(i.split())
        count +=1
    
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
    output = open('rln_head_rec/{0}'.format(filename.split('/')[-1]),'w')
    headerkeys = []
    for i in model_header:
        output.write('{0}\n'.format(i))
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
               print("skipping {0} because it doesn't contain header column {1}".format(filename,col))
        if bad == False:
            line = '\t'.join(line)
            output.write('{0}\n'.format(line))
    output.close()
