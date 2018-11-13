import psycopg2, bleach
import collections
from collections import OrderedDict
import time


DBNAME = "news"
db = psycopg2.connect(database=DBNAME)
c = db.cursor()
query = ""

def getTopThreeArticles():
  articleDictionary = {}
  topThree = {}
  query = "select distinct substring(path,10) from log where path like '/article/%'"
  c.execute(query)
  logArticles = c.fetchall()
  
  for article in logArticles:
    query = "select count(path) from log where path like '%" + ''.join(article) + "%'"
    c.execute(query)
    articleCount = c.fetchone()
    temp = {''.join(article): int(articleCount[0])}
    articleDictionary.update(temp)
   
  while(len(topThree) < 3):
    maxKey = max(articleDictionary.keys(), key=(lambda k: articleDictionary[k]))    
    maxValue = articleDictionary[maxKey]
    topThree.update({maxKey: maxValue})
    articleDictionary.pop(maxKey)

  topThree = OrderedDict(sorted(topThree.items(), key=lambda x: x[0], reverse = True))
  print(topThree)
  with open('output.txt', 'w') as f:
    for name,views in topThree.items():
      print("'" + name.replace('-', ' ').capitalize() + "' has " + str(views) + " views")
      print("'" + name.replace('-', ' ').capitalize() + "' has " + str(views) + " views", file=f)
 
  db.close()
if __name__ == '__main__':
  start_time = time.time()
  while True:
    print ("""
      1.Retrieve top 3 articles
      2.Retrieve most popular authors of all time
      3.Retrieve which days experienced more than 1% of errors on requests
      4.Exit/Quit
    """)
    ans= input("What would you like to do? ") 
    if ans=="1": 
      getTopThreeArticles
    elif ans=="2":
      print("getTopAuthors()")
    elif ans=="3":
      print("getBadDays()") 
    elif ans=="4":
      print("\n Goodbye") 
      exit()
    elif ans !="":
      print("\n Not Valid Choice Try again") 
  print(time.time() - start_time)