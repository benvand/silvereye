![test.yml](https://github.com/spendnetwork/cove-ocds/workflows/Test%20suite/badge.svg)

- [Silvereye](#silvereye)
  * [Installation](#installation)
    + [Running locally (with Vagrant)](#running-locally-with-vagrant)
    + [Running locally (without Vagrant)](#running-locally-without-vagrant)
    + [Deployment to Heroku](#deployment-to-heroku)
      - [Enable S3 storage on Heroku](#enable-s3-storage-on-heroku)
  * [Data loading](#data-loading)
  * [Loading data from Contracts Finder](#loading-data-from-contracts-finder)
    + [Updating Publisher metadata](#updating-publisher-metadata)
    + [Preparing Publisher metrics](#preparing-publisher-metrics)
  * [Using Silvereye](#using-silvereye)
    + [Publishers](#publishers)
      - [Django Admin](#django-admin)


# Silvereye

Silvereye is a web-based tool to help create and store procurement notices in the Open Contracting Data Standard (OCDS).

The code is based on a modified fork of the Open Contracting GitHub repository `cove-ocds` (OCDS Data Review Tool) 
available here: https://github.com/open-contracting/cove-ocds

Cove-ocds is a web application that allows you to review Open Contracting data, validate it against the Open 
Contracting Data Standard, and review it for errors or places for improvement. You can also use it to covert data 
between JSON and Excel spreadsheet formats.

The original tool runs at https://standard.open-contracting.org/review/

Documentation for the original tool is at https://ocds-data-review-tool.readthedocs.io/en/latest/

Silvereye also makes use of code from an OCDS Django alpha project, `bluetail`, that prototypes linking of OCDS data 
with beneficial ownership (BODS) data. More info can be found at https://github.com/mysociety/bluetail

An example deployment of Silvereye runs at https://ocds-silvereye.herokuapp.com

Documentation for Silvereye is in this README.md https://github.com/spendnetwork/cove-ocds/.

Further technical documentation about Silvereye can be found in the `docs` directory. [technical_docs.md](silvereye/docs/silvereye_development.md)


## Installation

Clone the repository

```
git clone git@github.com:spendnetwork/cove-ocds.git silvereye
cd silvereye
```

### Running locally (with Vagrant)

A Vagrantfile is included for local development. Assuming you have [Vagrant](https://www.vagrantup.com/) installed, 
you can create a Vagrant VM with:

```
vagrant up
```

Then SSH into the VM, and run the server script:

```
vagrant ssh
script/server
```

The site will be visible at <http://localhost:8000>.


### Running locally (without Vagrant)

You’ll need:

* Python 3.6
* A local PostgreSQL server (10+)

As above, make sure you’ve cloned the repo.

Open up a Postgres shell (eg: `psql`) and create a user and database matching the details in `.env.template`:

```
CREATE USER silvereye SUPERUSER CREATEDB PASSWORD 'silvereye'
CREATE DATABASE silvereye
```

Create a Python virtual environment at a location of your choosing, activate it, and install the required packages:

```
python3 -m venv ./venv
. ./venv/bin/activate
pip3 install --requirement requirements_dev.txt
```

Copy the `.env.template` file to `.env` and set the variable `SECRET_KEY` to a unique string. 
https://docs.djangoproject.com/en/2.2/ref/settings/#secret-key

With the virtual environment still activated, run the Django migrations, to set up the database:

```
script/migrate
```

If you want to setup (or reset) the database and load the example data, run:

```
script/setup
```

To run the server

```
script/server
```

### Deployment to Heroku

Heroku has good documentation for deploying using git. https://devcenter.heroku.com/articles/git

These environment variables must be set on the Heroku app before deployment.

    DJANGO_SETTINGS_MODULE=cove_project.settings_heroku
    DATABASE_URL="postgres://..."
    SECRET_KEY=

If you have forked the GitHub Repository you can connect your GitHub fork to a Heroku app and deploy using the Heroku 
dashboard:

https://devcenter.heroku.com/articles/github-integration

Or else you can push your git clone directly to your Heroku app. This is easiest done using the Heroku CLI tools. 
https://devcenter.heroku.com/articles/heroku-cli

1. Log in to Heroku CLI (https://devcenter.heroku.com/articles/heroku-cli#getting-started)
2. Add the Heroku app git remote to your git clone

    Execute this command in your silvereye clone root directory

        heroku git:remote --app your_heroku_appname

3. Push your branch to the Heroku remote `master` branch.

        git push heroku master

    Note you can push any local branch, but it must be pushed to the Heroku remote `master` branch to deploy.

        git push heroku [local_branch_to_push]:master

    If there are issues/errors from the Heroku git repo it can be reset first using 
    https://github.com/heroku/heroku-repo

        heroku plugins:install heroku-repo
        heroku repo:reset -a ocds-silvereye

4. Run the setup script to setup and prepare the Heroku database with the sample data.

        heroku run "script/setup"

    4. Or else simply run migrate for a clean database.

            heroku run "python manage.py migrate"
 

#### Enable S3 storage on Heroku

Using Silvereye on heroku will also require enabling S3 storage for the submitted files as the Heroku local storage is 
ephemeral. This is made possible by the Django package: `django-storages`

To use an AWS bucket, first create an S3 bucket with your desired name and permissions, then set the following environment 
variables:

    STORE_OCDS_IN_S3="TRUE"
    AWS_ACCESS_KEY_ID=""
    AWS_SECRET_ACCESS_KEY=""
    AWS_STORAGE_BUCKET_NAME=""

See [docs/s3-storage.md](silvereye/docs/s3-storage.md) for more details


## Data loading
 
To insert the sample data from Contracts Finder run 
 
    script/insert_cf_data
 
## Loading data from Contracts Finder
 
There is a management command to insert data from the UK Contracts Finder API. 
https://www.contractsfinder.service.gov.uk/apidocumentation/Notices/1/GET-Harvester-Notices-Data-CSV
 
This can point to a local file or provide arguments to retrieve files from the API directly in a date range

The command takes additional arguments:

- --publisher_submissions

    Combines the daily data into weekly CSVs grouped by buyers returned by the `get_publisher_names()` function to 
    simulate typical upload behaviour.   

- --load_data

        Inserts the generated CSVs into the database 

Insert local sample CSV file as weekly publisher submissions

    python manage.py get_cf_data --file_path silvereye/data/cf_daily_csv/export-2020-08-05.csv --load_data --publisher_submissions
    
Insert local CSVs from a zip file 

    python manage.py get_cf_data --file_path silvereye/data/cf_daily_csv/cf_files_2019-06-01_to_2020-09-06.zip --start_date 2019-06-01 --end_date 2020-09-06 --load_data --publisher_submissions

Download Contracts Finder releases in a date range from their API and insert as weekly publisher submissions

    python manage.py get_cf_data --start_date 2020-07-01 --end_date 2020-10-01 --load_data --publisher_submissions

### Updating Publisher metadata

This command updates the contact details from the latest submitted file for each publisher

    python manage.py update_publisher_data

### Preparing Publisher metrics

This management command will update the metric data for the Silvereye Publisher pages

    python manage.py update_publisher_metrics
          
          
## Using Silvereye

Silvereye facilitates building a database of OCDS data by uploading CSV files using simple user-friendly templates.
These are split into separate templates for tenders, awards, and spend data, which can be downloaded, filled in with 
data and then uploaded again. Upon uploading, the file is validated and converted to OCDS  
[release packages](https://standard.open-contracting.org/latest/en/schema/release_package/). If it passes validation the
OCDS data is stored in the database. 

### Publishers

To submit data to Silvereye, publisher information must first be entered into the database to be available for selection 
on the upload page. This can be done in the django admin page:

http://localhost:8000/admin/silvereye/publisher/
 
#### Django Admin

The Django admin can be used to view or update various data in Silvereye.

http://localhost:8000/admin/

Default login credentials are

- Username: admin
- Password: admin
