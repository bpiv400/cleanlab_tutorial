# Cleanlab Tutorial

## Ceate the dataset
1. Download the cats and dogs dataset from kaggle (https://www.kaggle.com/chetankv/dogs-cats-images) and unzip to a well-known location
1. Clean the dataset directory, so that it only contains training_set and test_set from the original dataset
1. Ensure you have conda installed
1. Overwrite the environment variable `DATA_DIR` in the conda yaml to point to the directory containing the dataset directories (i.e. the parent directory of `training_set` and `test_set`)
1. Create the conda environment with `conda env create --file envname.yml`
1. Run `dataset.py` to subset the data and introduce noise to the labels:
```
python dataset.py --noise [double] --shrink [double]
```
* `--noise`: sets the fraction of labels to swap
* `-shrink`: sets the fraction of the dataset to retain

This will output a new dataset directory and a zipped copy of the dataset next to the parent directory of the original dataset. 
