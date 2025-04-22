from Bio import Blast

"""
Blastp against peptides in fasta file
"""

fasta_string = open("../data_old/sequences_staphylococcus_DBAASP.fasta").read()
result_stream = Blast.qblast("blastp", "pt", fasta_string)

# save to file
with open("my_blast.xml", "wb") as out_stream:
    out_stream.write(result_stream.read())
result_stream.close()
