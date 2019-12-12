# Demo 3 - GCP ML Specialization Certification

This code package leverages GCP tools including AutoML to create a model
capable of predicting whether text is of native english origin, translated
by a professional into english, or translated by a machine into english

## Directory Structure
- notebooks -> Directory containing Jupyter Notebook with a walkthrough of the Demo 3 workflow
- src -> Python source code module for running ETL and prediction
- gcpdemo3.yml -> yml file to create necessary conda environment

## Setup

### Requirements
Python 3.7.4
Package Manager - Anaconda3
### Install Anaconda
[Anaconda Distribution](https://docs.anaconda.com/anaconda/install/)

### Setup Environment
```
conda env create -f gcpdemo3.yml
```

Activate the virtual environment
```
source activate gcpdemo3
```
or in some shells
```
conda activate gcpdemo3
```
You can deactivate with
```
source deactivate
```
or in some shells
```
conda deactivate
```
### Building Source Code
```
cd src
python setup.py bdist_wheel sdist
cd dist
pip install -U <filename.whl>
```
### Installing Google SDK
Please use this link to install the [GCloud SDK](https://cloud.google.com/sdk/docs/quickstarts).
Authentication will be made with the provided service account.
```
gcloud auth activate-service-account --key-file=/path/to/credentials.json
```

### Python Authentication to GCP
Set GOOGLE_APPLICATION_CREDENTIALS environment variable to the path to the SA credentials provided.

Windows -
```
set GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json
```
Linux -
```
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json
```

You may run the workflow from the provided Jupyter Notebook in notebooks/gcpdemo3.ipynb or feel
free to use the source code methods as you see fit.

### Whitepaper
Additional information regarding the process of creating this demo can be found at the following location:

https://docs.google.com/document/d/1HWdXoEKdzVJw-AFGLrBUHB68xa0vapUIoersgKzP4Rw/edit?usp=sharing

