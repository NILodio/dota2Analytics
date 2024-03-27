Dota2Analytics
==============================

## 🚨 Warning: This project is currently undergoing restructuring. 😎 

Please avoid using it at the moment and patiently await further updates.

Anticipated completion in the next couple of months. 😎 🚀


--------


### Setup

1. First, yo need to create a virtual environment by running `make create_environment` on the root directory of this project please make sure you have `make` installed on your machine before running this command
2. Then, you need to install the dependecies by running `make requirements` on the same directory where `requirements.txt` located
3. Create `.env` file at the root directory of this project/repo or copy the `.env.example` and rename it to `.env`
4. Dota Key is required to run this project. You can get the key by registering at [OpenDota](https://www.opendota.com/) and get the key from the profile page.

> [!IMPORTANT]  
> Crucial please add the make coomand when you create a new command. It will help you to understand the command that you want to run. For example, if you want to get data process you can run `make data`



### How to Use this Tool After Doing Setup?
all this project is create with Makefile. Thus, you can run the command by using `make` command. Here are the list of command that you can use:


1. `make data` : This command will run the scrapping process. It will scrap the job data from JobStreet website and store the result to CSV

2. `make requirements` : This command will install all the dependencies that listed at `requirements.txt`

3. `make create_environment` : This command will create a virtual environment for this project

4. `make clean` : This command will remove the virtual environment and all the dependencies that installed on the virtual environment

> [!IMPORTANT]  
> Crucial please add the make coomand when you create a new command. It will help you to understand the command that you want to run. For example, if you want to get data process you can run `make data`


Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>