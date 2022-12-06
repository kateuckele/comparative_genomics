#!/usr/bin/python

# This script takes the Satsuma block display output file (the output of ./BlockDisplaySatsuma) and makes it Circos compatible
# Satsuma whole-genome synteny alignment program: https://satsuma.sourceforge.net/
# Circos software package for visualizing data and information in a circular layout: http://circos.ca/

# usage: python SatsumaBlockDisplay2Circos.py --input inputfile 
# for a description of additional arguments: python SatsumaBlockDisplay2Circos.py --help

import argparse
from argparse import RawTextHelpFormatter
import sys
import numpy as np

####### Arguments and help ###########
parser = argparse.ArgumentParser(description="\
  Modify Satsuma block display output into a format that can be plotted with Circos\n\
  Written by Kathryn Uckele (https://github.com/kateuckele)\
", formatter_class=RawTextHelpFormatter)

parser.add_argument("-i", "--input", help="block display input file, required", type=str)
parser.add_argument("-o", "--output", help="output prefix for links file", type=str)
parser.add_argument("-t", "--target", help="name of target genome for karyotypes file", type=str, default = "target")
parser.add_argument("-q", "--query", help="name of query genome for karyotypes file", type=str, default = "query")
parser.add_argument("-c", "--color", help="target or query; determines whether colors should be applied to target or query chromosomes", type=str, default = "target")
parser.parse_args()
args = parser.parse_args()

infile = args.input
if (infile is None): 
  sys.exit("error: the following arguments are required: --input")

target_name = args.target
query_name = args.query
color = args.color

if (args.output is None):
  links_output = "links.txt"
else: 
  links_output = args.output + ".links.txt"

karyotype_outfile_target = "karyotype." + target_name + ".txt"
karyotype_outfile_query = "karyotype." + query_name + ".txt"

######################################
## Make links file

# Select subset columns from the block display input file
links = []
with open(infile) as f_in:
    for line in f_in:
        line = np.array(line.split())
        # only proceed if the line has 10 entries
        if len(line) == 10:
            indices = [0, 1, 2, 4, 5, 6]
            links.append(" ".join(line[indices]))

# Initialize variable containing Circos colors
values = ["chr0", "chr1", "chr2", "chr3", "chr4", "chr5", "chr6", "chr7",
"chr8", "chr9", "chr10", "chr11", "chr12", "chr13", "chr14", "chr15", "chr16",
"chr17", "chr18", "chr19", "chr20", "chr21", "chr22", "chr23", "chr24", "lgreen",
"vlgreen", "vlorange", "black", "optyellow", "dorange", "vlyellow", "stalk", "lred"]

# Determine whether target (default) or query chromosomes should be colored
if color == "target":
  x = 0
  y = 3
else: 
  x = 3
  y = 0

# Initialize directory of unique chromosome names from first genome
for link in links:
  lis = [link.split()[x] for link in links]
  unique_lis = np.unique(lis)
  my_dict1 = dict(zip(unique_lis, values[0:len(unique_lis)]))
 
# Initialize directory of unique chromosome names from second genome
for link in links:
  lis = [link.split()[y] for link in links]
  unique_lis = np.unique(lis)
  my_dict2 = dict(zip(unique_lis, ["black"]*len(unique_lis)))
  
# Consolidate directories into one
my_dict = my_dict1 | my_dict2

# Make links file
lines = []
for link in links:
  chrom = link.split()[x]
  color = "color=" + my_dict[chrom] + "\n"
  line = link.strip() # remove newline character
  line = "%s %s" % (line, color)
  lines.append(line)

with open(links_output, 'w') as f_out:
    for line in lines:
        f_out.write(line)
f_out.close()
    
############################
## Make karyotype files

# Generate two lists that include the target and query chromosome lengths, respectively
target_list = []
query_list = []
with open(infile) as f_in:
    lines = (line.rstrip() for line in f_in) # All lines including the blank ones
    lines = (line for line in lines if line) # Non-blank lines
    for line in lines:
      # only proceed if the line begines with "chromosomes"
      if line.split()[0] == "chromosomes":
        n_chrom = int(line.split()[1])
        if bool(target_list) == False:
          for i in range(n_chrom):
            target_list.append(next(lines))
        else:
          for i in range(n_chrom):
            query_list.append(next(lines))
f_in.close()

# Make karyotype file for target genome
counter = 1
lines = []
with open(karyotype_outfile_target, 'w') as f_out:
  for line in target_list:
    first_element = line.split('\t')[0]
    second_element = line.split('\t')[1]
    line = 'chr - ' + first_element + " " + str(counter) + " 0 " + second_element + " " + my_dict[first_element] + '\n'
    lines.append(line)
    counter +=1
        
with open(karyotype_outfile_target, 'w') as f_out:
    for line in lines:
        f_out.write(line)

# Make karyotype file for query genome
counter = 1
lines = []
with open(karyotype_outfile_query, 'w') as f_out:
      for line in query_list:
        first_element = line.split('\t')[0]
        second_element = line.split('\t')[1]
        line = "chr - " + first_element + " " + str(counter) + " 0 " + second_element + " " + my_dict[first_element] + '\n'
        lines.append(line)
        counter +=1

with open(karyotype_outfile_query, 'w') as f_out:
    for line in lines:
        f_out.write(line)