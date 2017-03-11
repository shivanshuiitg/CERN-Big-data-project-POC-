from IPython.core.display import HTML,display
from string import Template
import json,requests,threading,time,thread
import ipywidgets as widgets
from operator import add
from multiprocessing import Process
from pyspark import SparkContext, SparkConf
sparkHost = "localhost"

css_code=open('css/style.css', 'r').read()
javascript_code=open('js/javascript.js','r').read()
html_code = open('html/monitor-template.html','r').read()


## functions to be used

def get_application_id(sc):
    ## Returns application-id corresponding to SparkContext
    return sc._jsc.sc().applicationId()

def get_all_applications(sc):
    ## Returns JSON String of all applications 
    url = get_base_url(sc)
    result = requests.get(url)
    return json.dumps(result.json())

def get_jobs(app_id,sc):
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
def DisplayHtml():
    ## display the Live data as HTML
    display(HTML(css_code + html_code + javascript_code))

def MainApplication(sc,filename):
	textRDD = sc.textFile(filename)
   	words = textRDD.flatMap(lambda x: x.split(' ')).map(lambda x: (x, 1))
   	wordcount = words.reduceByKey(add).collect()
   	for wc in wordcount:
		print (wc[0],wc[1])
   	textRDD.flatMap(lambda line: line.split()).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a+b)
   	ls = range(100)
   	ls_rdd = sc.parallelize(ls, numSlices=4000)
   	ls_out = ls_rdd.map(lambda x: x+1).collect()
   	print ('output!: ', ls_out)

def StartApplication(sc,filename):
    ## start application and monitoring thread
	thread.start_new_thread(DisplayHtml, ())
	thread.start_new_thread(MainApplication, (sc,filename))

def StopApplication(sc):
    ## stop an Spark Application gracefully
    sc.stop()

def InitSpark():
    ## Initialize Spark Context
    conf = SparkConf()
    conf = conf.setAppName("Sample Application").setMaster("local[*]")
    sc = SparkContext(conf = conf)
    return sc