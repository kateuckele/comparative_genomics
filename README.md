# comparative_genomics
## Tools to aid comparative genomic analyses

### SatsumaBlockDisplay2Circos.py
This script converts [Satsuma](https://satsuma.sourceforge.net/) output into a format that is compatible with [Circos](http://circos.ca/). 

The Satsuma output can be generated with the following Satsuma script:

`./BlockDisplaySatsuma -i satsuma_summary_file -t target_fasta_file -q query_fasta_file`

Based on the BlockDisplay output, `BlockDisplay` generates two karyotype files and a links file that can be used with Circos. 

To run the `SatsumaBlockDisplay2Circos.py` script, specify the BlockDisplay input file:

`python SatsumaBlockDisplay2Circos.py --input block_display_input_file`

Additional `SatsumaBlockDisplay2Circos.py` arguments can be viewed by calling for help:

`python SatsumaBlockDisplay2Circos.py --help`
