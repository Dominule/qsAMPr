from Bio.Blast import NCBIXML

"""
Open xml with blast results and do sth with it...
"""

result_handle = open("my_blast.xml", 'r')
blast_records = NCBIXML.parse(result_handle)
for blast_record in blast_records:
    print(blast_record.database_sequences)
    # Do something with blast_record