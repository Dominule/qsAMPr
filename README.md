# AMP Prediction
This is a bachelor project for prediction of potencial AMPs against a specific target bacteria (focused on Staphylococcus aureus) using ML and data from publicly available databases (DBAASP, AMPSphere, ...).

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

For data visualization see [General visualisation.](src/visualize_data/general_visualization.ipynb)

Datasets were generated using scripts in this folder: [create_datasets](src/create_descriptors_datasets). Descriptors were computed using all available descriptors in `peptides` package.

## Usage
To get started, first create a virtual environment to isolate the project dependencies.

*On Windows:*
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

*On macOS and Linux:*
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
This will create a virtual environment named venv, activate it, install all the necessary packages listed in requirements.txt.

In src/classification/run_all_models.py choose the dataset you want to use for training by setting variable `dst` to value '01'/'02'/'03' (see section Datasets).

Train the models:
```
python src/classification/run_all_models.py
```

Your models and graphs will be stored in `data/outputs/dataset0x/evaluation_all`. (0x - chosen dataset)

## Running on a different dataset
To run on a different (balanced) dataset change the path to your dataset by setting variables `df_pos` (positive dataset) and `df_neg` (negative dataset) in `src/classification/run_all_models.py`.

The dataset should contain columns 'SEQUENCE', 'ACTIVITY' and computed descritors.


## Backstory
In a beautiful world where no evil was present, suddenly a big wicked antibiotic resistance came. The world changed and there was no savior...

Until a little peptide appeared. And not just one but quite a few came to fight with the Resistance. These antimicrobial peptides (AMPs) and other antimicrobial substances, invisible for human eyes, shine in the darkness and need our help.
Only together we can defeat the Resistance and make the world better again.

## Name
The name of this repository, qsAMPr, stands for Quantitative Structure-Activity Mapping & Peptide Research. It combines QSAR and AMPs, which is very clever.

## Inspiration
I was inspired by an [article][1] about recently published database [AMPSphere][2].

[1]: https://wikipedia.org](https://www.cell.com/cell/fulltext/S0092-8674(24)00522-1#relatedArticles            "Article"
[2]: https://ampsphere.big-data-biology.org/home  "AMPSphere"
