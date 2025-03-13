from random import randint
import csv

"""
Get positive or negative ids from DBAASP data
"""

def get_positive_ids():
    positive_ids = []
    with open("../../data/samples_DBAASP/raw_dbaasp_staphylococcus_without_modifications.csv") as file:
        reader = csv.reader(file, delimiter=",")
        for row in reader:
            if row[0] == "ID":
                continue
            positive_ids.append(int(row[0]))
        positive_ids.sort()
        print("done with positives, len:\t" + str(len(positive_ids)))
    return positive_ids


def get_random_ids():
    negative_ids = []
    positive_ids = get_positive_ids()


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


def get_raw(path):
    ids = []
    with open(path) as file:
        reader = csv.reader(file, delimiter=",")
        for row in reader:
            if row[0] == "ID":
                continue
            ids.append(int(row[0]))
        ids.sort()
    return ids


def get_gram_negative_ids():
    # return difference between gram negative and gram positive lists
    gram_negative_list = get_raw("../../old/data_old/ids_gram_negative_bacteria.csv")
    gram_positive_list = get_raw("../../old/data_old/ids_gram_positive_bacteria.csv")

    for id in gram_positive_list:
        if id in gram_negative_list:
            gram_negative_list.remove(id)
    return gram_negative_list
