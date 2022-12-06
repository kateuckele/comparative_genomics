# comparative_genomics
## Tools to aid comparative genomic analyses

### Satsuma2Circos.py
This script converts [Satsuma](https://satsuma.sourceforge.net/) output into a format that is compatible with [Circos](http://circos.ca/). 

The Satsuma output can be generated with the following Satsuma script:

`./BlockDisplaySatsuma -i satsuma_summary_file -t target_fasta_file -q query_fasta_file`

Based on the BlockDisplay output, `Satsuma2Circos.py` generates two karyotype files and a links file that can be used with Circos. 
