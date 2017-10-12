#! /usr/bin/env python3

import psycopg2


def answerQuestions():
    db = psycopg2.connect("dbname=news")
    cursor = db.cursor()
# to answer "What are the most popular three articles of all time?"
    queryTopArticles = """
        SELECT * FROM articleViewCount;"""
    cursor.execute(queryTopArticles)
    results = cursor.fetchall()
    print("The top 3 most popular articles all time are:")
    for (title, views) in results:
        print("{} --- {} total views".format(title, views))
    print("")
# to answer "Who are the most popular articles authors of all time?"
    queryTopAuthors = """
        SELECT name, sum(views) AS views
        FROM authorTotalViews
        GROUP BY name
        ORDER BY views DESC;"""
    cursor.execute(queryTopAuthors)
    results = cursor.fetchall()
    print("The most popular authors of all time are:")
    for (name, views) in results:
        print("{} --- {} total views".format(name, views))
    print("")
# to answer "On which days did more than  1% of requests leads to errors?"
    queryDayError = """
        SELECT date, percent
        FROM dateError
        WHERE percent > 1.00
        GROUP BY date, percent
        ORDER BY percent DESC;"""
    cursor.execute(queryDayError)
    results = cursor.fetchall()
    print "On the following date(s) more than 1% of requests leads to errors:"
    for (date, percent) in results:
        print("{} --- {} % error".format(date, percent))
    print("")
    db.close()

if __name__ == "__main__":
    answerQuestions()

