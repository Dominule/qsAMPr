# AMP Prediction
This is a bachelor project for prediction of potencial AMPs using ML and data from publicly available databases (DBAASP, AMPSphere, ...).

## Quick description
In folder [inputs](data/inputs) are stored datasets with aminoacid sequences, their activities and computed descriptors.
In folder [outputs](data/outputs) are stored trained models and results. For example: [evaluation for dataset 02](data/outputs/dataset02/evaluation_all).

Interface for models: [skeleton](src/skeleton.py).
Setup for classification models: [classification](src/classification/models.py).
Setup for regression models: [regression](src/regression/models.py).

Script to run all classification models: [run all](src/classification/run_all_models.py).

Clustering and visualized descriptors: [clustering](src/cluster_stuff/better_clustering.ipynb).

## Datasets
One positive dataset of sequences active against styphylococcus aureus, three negative datasets:

-01- staphylococcus inactive + gram negative bacteria active peptides* (DBAASP)

-02- random real sequences (UniProt from AntiTbPred)

-03- random generated sequences (with the same amino acid distribution as the positive dataset)

[General visualisation.](src/visualize_data/general_visualization.ipynb)

Datasets were generated using scripts in this folder: [create_datasets](src/create_descriptors_datasets).

## Usage
To be added.

## Backstory
In a beautiful world where no evil was present, suddenly a big wicked antibiotic resistance came. The world changed and there was no savior...

Until a little peptide appeared. And not just one but quite a few came to fight with the Resistance. These antimicrobial peptides (AMPs), invisible for human eyes, shine in the darkness and need our help.
Only together we can defeat the Resistance and make the world better again.


## Inspiration
I was inspired by an [article][1] about recently published database [AMPSphere][2].

[1]: https://wikipedia.org](https://www.cell.com/cell/fulltext/S0092-8674(24)00522-1#relatedArticles            "Article"
[2]: https://ampsphere.big-data-biology.org/home  "AMPSphere"
