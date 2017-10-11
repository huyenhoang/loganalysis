#Log Analysis Project

This project is part of Udacity's Full Stack Nanodegree Program. 

The purpose is to use Python and PostgreSQL to build an internal tool to query databases and provide answers to questions about authors, articles, and links of a news website.

#Getting Started

##Prerequisites

Make sure to have the following installed:
1. Vagrant
2. VirtualBox
3. Python 2.7.9 (at least)

##Installing

##Creating Views with PostgreSQL

###View(s) Created for Question 1: 

####View name: articleViewCount

CREATE VIEW articleViewCount AS 
SELECT articles.title, COUNT(log.id) as views
FROM articles, log
WHERE log.path = Concat('/article/', articles.slug)
GROUP BY articles.title
ORDER BY views DESC LIMIT 3;

This view joins the articles and the log table in order to provide a table with the title of articles alongside the total number of views, calculated by counting the id column in the log table. The table selects only the first three rows.

###View(s) Created for Question 2*: 

####View 1 name: articleAuthorName

Create OR REPLACE View articleAuthorName AS
SELECT authors.name, articles.title, articles.slug
FROM authors, articles
WHERE authors.id = articles.author;

This view joins the authors and articles tables to provide a table with a written name for the authors instead of an integer ID alongside the article’s title and slug. This view will be referenced later to answer Question 2.

####View 2 name: slugViews

Create view slugViews as select articles.title, count(log.id) as views from articles, log where log.path = concat('/article/', articles.slug) group by articles.title order by views desc;

This view creates a table with the title of the article and the number of views it received. This view will be referenced later to answer Question 2.

####View 3 name: authorTotalViews

CREATE OR REPLACE VIEW authorTotalViews AS
SELECT articleAuthorName.name, slugViews.Views
FROM articleAuthorName, slugViews
WHERE articleAuthorName.title = slugViews.title
GROUP BY articleAuthorName.name, slugViews.Views
ORDER BY views DESC;

This view reference both the previous two views in order to provide a table with the author’s names and the number of views associated with their name for each article they authored. An SQL query that sum up the views column of this table for each author will result in the total views for each author all time. 

###View(s) Created for Question 3*:

####View 1 name: errorRequests

CREATE OR REPLACE VIEW errorRequests AS
SELECT date(time) AS date, count(*) AS requests
FROM log
WHERE status != '200 OK'
GROUP BY date
ORDER BY date;

This view presents the number of errors for each date.

####View 2 name: allRequests

CREATE OR REPLACE VIEW allRequests AS
SELECT date(time) as date, count(*) as requests
FROM log
Group by date
Order by date;

This view presents the total number of requests for each date, including errors.

####View 3 name: dateError

CREATE OR REPLACE VIEW dateError AS
SELECT errorRequests.date, round(((errorRequests.requests*100.0)/allRequests.requests*1.0), 2) AS percent
FROM errorRequests, allRequests
WHERE errorRequests.date = allRequests.date
GROUP by errorRequests.date, percent
ORDER by percent;

This view uses the previous two views to calculate the number of errors for each date as a percentage of the total requests.

*CREATE OR REPLACE VIEW is used instead of CREATE VIEW because a handful of views were created before the right one was generated that could be used to answer the question.

##Running the Python program




