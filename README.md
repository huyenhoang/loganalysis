# Log Analysis Project

This project is part of Udacity's Full Stack Nanodegree Program. 

The purpose is to use Python and PostgreSQL to build an internal tool to query databases and provide answers to questions about authors, articles, and links of a news website.

Objectives: Given three tables with author, articles, and request informations, provide answers to the following 3 questions using one (1) query to the databases:
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

# Getting Started

## Prerequisites

Make sure to have the following installed:
1. Python 2.7.0 (at least)
2. VirtualBox
3. Vagrant

## Installations

### Python

#### On Mac
To determine if you have Python 2.7, open the Terminal application, type the following, and press Return:

`python -V`

This command will report the version of Python:

`Python 2.7.9`

Any version between 2.7.0 and 2.7.10 is fine.

#### On Windows 7

To get to the command line, open the Windows menu and type “command” in the search bar. Select Command Prompt from the search results. In the Command Prompt window, type the following and press Enter.

`python`

If Python is installed and in your path, then this command will run python.exe and show you the version number.

`Python 2.7.9 (default, Dec 10 2014, 12:24:55) [MSC v.1500 32 bit (Intel)] on win32
Type "help", "copyright", "credits" or "license" for more information.`

Otherwise, you will see:

`'python' is not recognized as an internal or external command, operable program or batch file.`

#### On Linux

Open a shell and type

`which python`

If Python is installed, you will get back its location, which may or may not include the version number. If the location does not include a version number, then ask for it:

`python -V`

This command returns the version

`Python 2.7.9`

### VirtualBox
Can be downloaded here: (https://www.virtualbox.org/wiki/Downloads)

### Vagrant
Download Vagrant hre: https://www.vagrantup.com/downloads.html

To check if you've successfully installed, vagrant, type:
`vagrant --version`

The vagrant configuration file, named vagrantfile, can be forked from this Udacity respository: https://github.com/udacity/fullstack-nanodegree-vm

To launch the virtual VM, change directory to where the vagrantfile is and use the following command:

`vagrant up`

To log into the virtual machine:
`vagrant ssh`

Before loading the data, `cd` into the `vagrant` directory.

## The Data
The SQL data file is not provided with this repository (too big). But let's pretend it is. The file is called newsdata.sql. Put this file into the vagrant directory, which is shared with your virtual machine.

Note that PostgreSQL comes with the Vagrant machine you installed. To load the data, `cd` into the `vagrant` directory and use the command `psql -d news -f newsdata.sql`.

Here's what this command does:

* `psql` — the PostgreSQL command line program
* `-d news` — connect to the database named news which has been set up already
* `-f newsdata.sql` — run the SQL statements in the file newsdata.sql

## Creating Views with PostgreSQL

To access the data and create the views necessary to solve the 3 objectives, use `psql news`.

### View(s) Created for Question 1: 

#### View name: `articleViewCount`

```
CREATE VIEW articleViewCount AS 
SELECT articles.title, COUNT(log.id) AS views
FROM articles, log
WHERE log.path = Concat('/article/', articles.slug)
GROUP BY articles.title
ORDER BY views DESC LIMIT 3;
```

This view joins the articles and the log table in order to provide a table with the title of articles alongside the total number of views, calculated by counting the id column in the log table. The table selects only the first three rows.

### View(s) Created for Question 2*: 

#### View 1 name: `articleAuthorName`

```
CREATE OR REPLACE VIEW articleAuthorName AS
SELECT authors.name, articles.title, articles.slug
FROM authors, articles
WHERE authors.id = articles.author;
```

This view joins the authors and articles tables to provide a table with a written name for the authors instead of an integer ID alongside the article’s title and slug. This view will be referenced later to answer Question 2.

#### View 2 name: `slugViews`

```
CREATE VIEW slugViews AS 
SELECT articles.title, COUNT(log.id) AS views 
FROM articles, log 
WHERE log.path = CONCAT('/article/', articles.slug) 
GROUP BY articles.title 
ORDER BY views DESC;
```

This view creates a table with the title of the article and the number of views it received. This view will be referenced later to answer Question 2.

#### View 3 name: `authorTotalViews`

```
CREATE OR REPLACE VIEW authorTotalViews AS
SELECT articleAuthorName.name, slugViews.Views
FROM articleAuthorName, slugViews
WHERE articleAuthorName.title = slugViews.title
GROUP BY articleAuthorName.name, slugViews.Views
ORDER BY views DESC;
```

This view reference both the previous two views in order to provide a table with the author’s names and the number of views associated with their name for each article they authored. An SQL query that sum up the views column of this table for each author will result in the total views for each author all time. 

### View(s) Created for Question 3*:

#### View 1 name: `errorRequests`

```
CREATE OR REPLACE VIEW errorRequests AS
SELECT date(time) AS date, count(*) AS requests
FROM log
WHERE status != '200 OK'
GROUP BY date
ORDER BY date;
```

This view presents the number of errors for each date.

#### View 2 name: `allRequests`

```
CREATE OR REPLACE VIEW allRequests AS
SELECT date(time) AS date, count(*) AS requests
FROM log
GROUP BY date
ORDER BY date;
```

This view presents the total number of requests for each date, including errors.

#### View 3 name: `dateError`

```
CREATE OR REPLACE VIEW dateError AS
SELECT errorRequests.date, round(((errorRequests.requests*100.0)/allRequests.requests*1.0), 2) AS percent
FROM errorRequests, allRequests
WHERE errorRequests.date = allRequests.date
GROUP BY errorRequests.date, percent
ORDER BY percent;
```

This view uses the previous two views to calculate the number of errors for each date as a percentage of the total requests.

*`CREATE OR REPLACE VIEW` is used instead of `CREATE VIEW` because multiple views with the same names were created.

## Running the Python program

From the command line, type `python log-analysis.py` to run the module. 

The `answerQuestions` method in the python module and print out the results, which are recorded in the text file `printedResults.txt`


