from random import randint
import csv
def get_peptides_ids():
    negative_ids = []
    positive_ids = []

    # fill positive_ids
    with open("../../data/examples_DBAASP/raw_dbaasp_staphylococcus_without_modifications.csv") as file:
        reader = csv.reader(file, delimiter=",")
        for row in reader:
            if row[0] == "ID":
                continue
            positive_ids.append(int(row[0]))
        positive_ids.sort()
        print("done with positives, len:\t" + str(len(positive_ids)))


    # fill negative_ids
    # get 450 random ids from range(10, 8000)
    random_id = randint(10, 8000)
    for i in range(450):
        # if the number is in the positive_ids, drop and generate other
        while random_id in positive_ids:
            while random_id in negative_ids:
                print("random_id in negative_ids:" + str(random_id) + "\t\tid:" + str(i))
                random_id = randint(10, 8000)
            print("random_id in positive_ids:" + str(random_id) + "\t\tid:" + str(i))
            random_id = randint(10, 8000)
        negative_ids.append(random_id)
        random_id = randint(10, 8000)
    print("done with negatives")
    negative_ids.sort()
    print("negatives:\t")
    print(negative_ids[:12])

    print("positives:\t")
    print(positive_ids[:12])

    return negative_ids


get_peptides_ids()
print("done with everything")

