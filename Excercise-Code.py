
# coding: utf-8

# In[ ]:

from IPython.core.display import HTML,display
from string import Template
import json,requests,threading,time,thread
import ipywidgets as widgets
from pyspark import SparkConf, SparkContext
from operator import add
## Please specify `sparkHost` and `filename`
## `sparkHost` is the server on which you are running the script
sparkHost = "localhost"
## `filename` is path of textfile
filename = 'textfile.txt'
## getting css,html and javascript code
css_code=open('css/style.css', 'r').read()
javascript_code=open('js/javascript.js','r').read()
html_code = open('html/monitor-template.html','r').read()
## Stopping default SparkContext, so that I can specify my Own SparkContext with required configurations
sc.stop()

## functions to be used
def get_application_id(sc):
    ## Returns application-id corresponding to SparkContext
    return sc._jsc.sc().applicationId()

def get_all_applications():
    ## Returns JSON String of all applications 
    url = get_base_url(sc)
    result = requests.get(url)
    return json.dumps(result.json())

def get_jobs(app_id):
    ## Returns JSON String of all jobs associated with app_id
    url = "{base_url}/{app_id}/jobs".format(base_url=get_base_url(sc),app_id=app_id)
    result = requests.get(url)
    return json.dumps(result.json())

def get_base_url(sc):
    ## Get the port on which UI for this application is running and return base url for querying Spark API
    for x in range(4040,4060):
        link = "http://"+sparkHost+":"+str(x)+"/environment/"
        result = requests.get(link)
        if ( result.status_code == 200 and sc.applicationId in str(result.content)):
            return "http://{spark_host}:{ui_port}/api/v1/applications".format(spark_host=sparkHost,ui_port=x)
def show_html():
    ## display the Live data as HTML
    display(HTML(css_code + html_code + javascript_code))


# In[ ]:

thread.start_new_thread(show_html, ())
## Calculates the word count of the given file.

## Constants
APP_NAME = "Simple Application"

def main(sc,filename):
   textRDD = sc.textFile(filename)
   words = textRDD.flatMap(lambda x: x.split(' ')).map(lambda x: (x, 1))
   wordcount = words.reduceByKey(add).collect()
   for wc in wordcount:
      print(wc[0],wc[1])
   textRDD.flatMap(lambda line: line.split()).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a+b)

if __name__ == "__main__":
   # Configure Spark
   conf = SparkConf().setAppName(APP_NAME)
   conf = conf.setMaster("local[*]")
   sc   = SparkContext(conf=conf)
   # Execute Main functionality
   main(sc, filename)
   ls = range(100)
   ls_rdd = sc.parallelize(ls, numSlices=1000)
   ls_out = ls_rdd.map(lambda x: x+1).collect()
   print ('output!: ', ls_out)

