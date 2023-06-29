# DVC Data Registry

I have reused the data processing steps from previous module's DVC pipeline
to create the data registry in a separate [repository](https://github.com/alex-fedorenk0/dvc-registry.git).

Two versions of dataset with corresponding git tags were created:

|Tag|Description|Train dataset|Test dataset|
|-|-|-|-|
|`v1_train-01-2023_test-02-2023_clean`|Dataset after feature selection and engineering|2023-01|2023-02
|`v2_train-01-2023_test-02-2023_clean_no_outliers`|Cleaned outliers for trip duration, distance and avg speed|2023-01|2023-02|

To create any additional version of train/test datasets:

- clone this repo
- use `dvc pull` command to get latest data version from remote
- change the corresponding params in `params.yaml` file,
- execute pipeline with `dvc repro`
- run `dvc push` to push changes to remote
- push changes to git
- set a new git tag with short changes description and push it to git remote


To pull any of the versions from data registry use `dvc get` or `dvc import` 
commands or `dvc.api` calls such as:
```
dvc.api.get_url(
    path='data/processed/train.feather',
    repo='https://github.com/alex-fedorenk0/dvc-registry.git',
    rev='v2_train-01-2023_test-02-2023_clean_no_outliers')
```
