# This file contains skeleton code provided by Professor Sohn.
# Refer to skeleton.py for the provided skeleton code. I take NO credit for it.
# Refer to README.md for more information.
#!/user/bin/python
import sys
import os
import commands
import re
import sys

import MySQLdb
import mysql.connector

from xml.dom.minidom import parse, parseString

# for converting dict to xml 
from cStringIO import StringIO
from xml.parsers import expat

def get_elms_for_atr_val(tag,atr,val):
   lst=[]
   #tag = "title"
   elms = dom.getElementsByTagName(tag)
   # ............
   #print("elms are = ", elms[0].childNodes)
   return elms

# get all text recursively to the bottom
def get_text(e):
   lst=[]
   # ............
   if e.nodeType in (3,4):
       lst.append(e.data)
   else:
       for y in e.childNodes:
           lst = lst + get_text(y)
   return lst

# replace whitespace chars
def replace_white_space(str):
   p = re.compile(r'\s+')
   new = p.sub(' ',str)   # a lot of \n\t\t\t\t\t\t
   return new.strip()

# replace but these chars including ':'
def replace_non_alpha_numeric(s):
   p = re.compile(r'[^a-zA-Z0-9:-]+')
   #   p = re.compile(r'\W+') # replace whitespace chars
   new = p.sub(' ',s)
   return new.strip()

# convert to xhtml
# use: java -jar tagsoup-1.2.jar --files html_file
def html_to_xml(fn):
   # ............
   cmd = "java -jar tagsoup-1.2.1.jar --files " + fn
   os.system(cmd)
   xhtml_file = fn.replace('.html', '.xhtml')
   return xhtml_file

def extract_values(dm, tag):
   lst = []
   l = get_elms_for_atr_val(tag,'class','most_actives')
   #print("l = ", l)
   lst = map(lambda x : get_text(x),l)
   # ............
   #    get_text(e)
   # ............
   return lst

# mysql> describe most_active;
def insert_to_db(l,tbl):
    # ............
    mydb = mysql.connector.connect(host="localhost", user="root", password="root", database="dbtest1")
    mycursor = mydb.cursor()
    mycursor.execute("CREATE TABLE IF NOT EXISTS `stocks` (`Symbol` VARCHAR(255), `Name` VARCHAR(255), `Price` VARCHAR(255), `Change` VARCHAR(255), `percentChange` VARCHAR(255), `Volumn` VARCHAR(255), `AvgVolumn` VARCHAR(255), `MarketCap` VARCHAR(255), `peRatio` VARCHAR(255))")
    sql = "INSERT INTO `stocks` (`Symbol`, `Name`, `Price`, `Change`, `percentChange`, `Volumn`, `AvgVolumn`, `MarketCap`, `peRatio`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (l[0], l[1], l[2], l[3], l[4], l[5], l[6], l[7], l[8])
    mycursor.execute(sql, val)
    mydb.commit()
    #mydb.close()
    return mycursor

def select_from_db(cursor, fn):
    mydb = mysql.connector.connect(host="localhost", user="root", password="root", database="dbtest1")
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM stocks")
    res = mycursor.fetchall()
   # mydb.close()
    return res

def convert_to_dict(keys, vals):
    d = dict(map(lambda i : (tuple(keys[i]), tuple(vals[i])), range(len(keys))))
    return d


# show databases;
# show tables;
def main():
   print("MADE IT TO MAIN")
   html_fn = sys.argv[1]
   fn = html_fn.replace('.html','') #default is .html
   xhtml_fn = html_to_xml(html_fn)
   #print("fn is = ", fn)
   #print("xhtml=== ", xhtml_fn)
   global dom
   dom = parse(xhtml_fn)
   #dom = parse("books.xml")
   #print(dom.nodeType)
   
   keys = extract_values(dom, 'tr')
   #print("keys=", keys)
   vals = extract_values(dom, 'td')
   # refer to video from july 16th if i need to take keys and values and make a dictionary
   #print("vals=",vals[0])
   #print("keyyy=", keys[0])
   #print("keyy=", keys[1])
   d = convert_to_dict(keys, vals)
   #print(d)
   # make sure your mysql server is up and running
   #print("----------------------")
   lst = keys
   cursor = None
   for item in lst:
       cursor = insert_to_db(item,fn)
   #cursor = insert_to_db(lst,fn) # fn = table name for mysql

   l = select_from_db(cursor,fn) # display the table on the screen

   print(l)

   # make sure the Apache web server is up and running
   # write a PHP script to display the table(s) on your browser

   return 0 #xml
# end of main()

if __name__ == "__main__":
    main()
