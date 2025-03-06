from Bio import Blast

fasta_string = open("../../data/examples_DBAASP/AMP_sequences_staphylococcus_DBAASP.fasta").read()
result_stream = Blast.qblast("blastp", "pt", fasta_string)

with open("my_blast.xml", "wb") as out_stream:
    out_stream.write(result_stream.read())
result_stream.close()
