# rln_rectify_headers
Fix relion headers between different versions

When you switch to different versions of relion sometimes the headers don't match up for the manual picking files.
this script fixes that problem... 

It would also probably work for merging autopick and manual pick files - although the coordinate files would have to be re-imported and possibly renamed

copy the script into the relion working directory and run with:
python rln_rectify_headers.py

It will prompt for an example file: if you have two header types this should be the shorter of the two:
To see all of the files and their header lengths run this in the directory with the star files:

for x in *.star; do echo $x; grep _rln $x | wc -l; done 

After entering the example file the program asks for the file search string: this is a unix-like search string that will find all of the manual pick star files. (EG: ManualPick/job001/Micrographs/*.star)

The script will then write a new directory called rln_head_rec with the corrected starfiles (all with the same names) re-import them into relion as coordinate files and run the extraction.

BOOM!
