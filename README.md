# Cluster Evaluation Survey Application

**CIPHE is a survey platform for collecting human interpretation data of document clusters. It is built on Django and contain metrics for calculating cluster precision and participant agreement. It can be hosted on a server to collect data from experts or crowdsourcing workers to gather data for human evaluation of document clusters.**


## Paper
This is the repository connected to the paper "CIPHE: A Framework for Cluster Interpretation and Precision from Human Exploration" presented at NLP4DH 2024. It is currently undergoing updates for new research projects and is very user-unfriendly. It will become much more flexible and user-friendly with the next publication. Meanwhile, I am happy to assist anyone who wants to use the framework or wants an explanation on how it was used in the CIPHE paper.


## Setup
1. `Create venv with requirements.txt`
2. `./manage.py makemigrations`
3. `./manage.py migrate`
4. `./manage.py createsuperuser`
5. `./manage.py import_data data/data.json`
6. `./manage.py runserver`
7. Copy hooks/precommit to .git

A document in `data.json` should contain the fields `title`, `text` and `label`, where the label corresponds to cluster id.

## Usage
#### Survey
A User object is created for each user id string that is submitted on the welcome page. If a user already exists, their data is loaded. The user will be shown one cluster at a time from the survey. The survey/models.py holds the database models that make up the survey platform. In the django admin view, the imported documents should be showing up under Articles. Each Article is connected to a Cluster. The users taking the survey are connected to clusters through the Page object. The page also links to the objects that contain survey answers for a user such as `LikertScaleQuestion`, `UFQuestion`, and `TaxonomyQuestion`.

#### Analysis
The data is stored in db.sqlite3. To get the CIPHE metrics for a survey and e.g. users 1, 2, and 42, run `./manage ciphe_metrics 1 2 42`.
The functions for plotting can be found in `survey/plotting/`.


### Linting
Please lint your code using "ruff"
* Install ruff: pip install ruff
* Format: ruff format survey
* Lint: ruff check survey --fix


#### Cite
Citing information found at:
[CIPHE: A Framework for Document Cluster Interpretation and Precision from Human Exploration](https://aclanthology.org/2024.nlp4dh-1.52) (Eklund et al., NLP4DH 2024)