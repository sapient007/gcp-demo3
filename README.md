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

You may run the workflow from the provided Jupyter Notebook in notebooks/gcpdemo3.ipynb or feel
free to use the source code methods as you see fit.

### Using Google Cloud Storage (GCS) Python Client
Please follow directions to the detailed doc to set up client library [GCS Client Lib](https://cloud.google.com/storage/docs/reference/libraries#client-libraries-install-python).

You will need to set up authentication for a service account to interact with files inside the GCS buckets. Additional information on service account setup is located in [GCP Authentication](https://cloud.google.com/docs/authentication/production).

### Whitepaper
Additional information regarding the process of creating this demo can be found at the following location:

https://docs.google.com/document/d/1HWdXoEKdzVJw-AFGLrBUHB68xa0vapUIoersgKzP4Rw/edit?usp=sharing

