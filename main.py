#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# enable debugging
import cgi
import cgitb
import mysql.connector
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

cgitb.enable()
print("Content-Type: text/plain;charset=utf-8\n")
fields = cgi.FieldStorage()

def contains(a, el):
    for e in a:
        if e == el:
            return True
    return False

if 'description' in fields:
    desc = (fields['description']).value

    connection = mysql.connector.connect(host='localhost',
                                         port='8889',
                                         database='youtube_data',
                                         user='root',
                                         password='root')

    cursor = connection.cursor()
    query = "SELECT title, description FROM y"
    cursor.execute(query)

    results = cursor.fetchall()

    titles = [i[0] for i in results]
    descriptions = [i[1] for i in results]

    descriptions.append(desc)

    for (title, description) in cursor:
        print(title.encode('utf-8') + " " + description.encode('utf-8'))

    tfidf_v = TfidfVectorizer()
    tfidf_m = tfidf_v.fit_transform(descriptions)

    for i in range(tfidf_m.shape[0]):
       sim_arr = cosine_similarity(tfidf_m[i], tfidf_m)[0]
       sim_arr_sorted = sorted(sim_arr, reverse=True)

       indices = []
       for b in range(len(sim_arr)):
           for a in range(len(sim_arr)):
               if sim_arr[a] == sim_arr_sorted[b] and not contains(indices, b):
                   indices.append(a)
                   break

       print(descriptions[index] for index in range(5))

    cursor.close()
    connection.close()

