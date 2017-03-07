
# coding: utf-8

# In[ ]:

# from IPython.core.display import HTML
from string import Template
import json,requests,threading,time
import ipywidgets as widgets
from pyspark import SparkConf, SparkContext
from operator import add
## Please specify `sparkHost` and `filename`
## `sparkHost` is the server on which you are running the script
sparkHost = "localhost"
## `filename` is path of textfile
filename = '/home/shivanshu/Documents/SPARK/spark-1.2.0-bin-hadoop2.4/textfile.txt'

## Stopping default SparkContext, so that I can specify my Own SparkContext with required configurations
sc.stop()


# In[2]:

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


# In[3]:

## HTML code

html = """
    <div id="main-div" > </div>
"""

## CSS code

css = """
<style> 
#main-div {
    border-radius: 10px;
    border: 2px solid #73AD21;
    padding: 20px; 
    width: 950px;
    height: 150px;    
}
.job-div {
    border-radius : 5px;
    border: 2px solid black;
    padding: 20 px;
    width: 100%;
    height: 150px;
}
.job-table{
    position:relative;
    float:right;
    right:5px;
    top:5px;
}
.job-details{
    position:relative;
    float:left;
    width:140px;
    top:5px;
    left:5px;
    height:120px;
    border: 1px solid black;
    border-radius:1px;
}
.job-progress-span{
    position:relative;
    left: 20px; 
    top: 10px;
}
.progress-slider{
    width:500px;
    height:30px;
    border:1px solid #000;
    border-radius: 3px;
    overflow:hidden;}
.progress-slider-bar{
    width:100%;
    height:30px;
    border-right: 1px solid #000000;
    background: green;}
.progress-slider-number {
    color: #000000;
    font-size: 15px;
    font-style: italic;
    font-weight: bold;
    left: 25px;
    position: relative;
    top: -24px; }
</style>
"""
## Javascript code
javascript = """
<script type="text/Javascript">
var iteration = 1
    function isJSON(str) {
        try {
            JSON.parse(str);
        } catch (e) {
            return false;
        }
        return true;
    }
    function render_html(number_of_jobs){
        $('#main-div').css("height",(number_of_jobs*150 + 60).toString()+"px");
        var count = 0;
        for (count = 0;count <number_of_jobs;count++){
            var str = '<div class="job-div" id="job-'+count+'"><div class="job-details">Job ID: <strong><span class="job-id">1<span></strong><br>Job Name: <strong><span class="job-name">collect:xxc4500<span></strong><br>Job Status: <strong><span class="job-status">Running<span><strong></div><table border="3" class="job-table"><tbody><tr style="height: 23px;"><td style="width: 150px; height: 23px;"><strong>Number of Tasks</strong></td><td style="width: 150px; height: 23px; color: orange;"><strong>Active Tasks</strong></td><td style="width: 150px; height: 23px; color: green;"><strong>Completed Tasks</strong></td><td style="width: 150px; height: 23px; color: blue;"><strong>Skipped Tasks</strong></td><td style="width: 150px; height: 23px; color: red;"><strong>Failed Tasks</strong></td></tr><tr style="height: 23px;"><td style="width: 150px; height: 23px;"><span class="number-of-tasks"><span></td><td style="width: 150px; height: 23px;"><span class="active-tasks"><span></td><td style="width: 150px; height: 23px;"><span class="completed-tasks"><span></td><td style="width: 150px; height: 23px;"><span class="skipped-tasks"><span></td><td style="width: 150px; height: 23px;"><span class="failed-tasks"><span></td></tr></tbody></table><span class="job-progress-span"><div class="progress-slider"><div class="progress-slider-bar"></div><div class="progress-slider-number"></div></div></span></div><br>';
            $("#main-div").append(str);
        }
    }
    function render_live_data(jobs_dict){
        //alert("Number of Jobs : " + jobs_dict.length)
        number_of_jobs = jobs_dict.length
        if (iteration == 1){
            render_html(number_of_jobs);
            iteration = 0
        }
        
        for (var i = 0;i<number_of_jobs;i++){
            var job = jobs_dict[i];
            $("#job-"+i.toString()).find('.number-of-tasks').text(job["numTasks"]);
            $("#job-"+i.toString()).find('.active-tasks').text(job["numActiveTasks"]);
            $("#job-"+i.toString()).find('.completed-tasks').text(job["numCompletedTasks"]);
            $("#job-"+i.toString()).find('.skipped-tasks').text(job["numSkippedTasks"]);
            $("#job-"+i.toString()).find('.failed-tasks').text(job["numFailedTasks"]);
            $("#job-"+i.toString()).find('.job-id').text(job["jobId"]);
            $("#job-"+i.toString()).find('.job-name').text(job["name"]);
            $("#job-"+i.toString()).find('.job-status').text(job["status"]);
            var number_of_tasks = job["numTasks"];
            var processed_tasks = job["numCompletedTasks"] + job["numSkippedTasks"] + job["numFailedTasks"];
            var percentage_progress = Math.round((processed_tasks*100)/number_of_tasks);
            // TODO
            // width not changing
            //alert(percentage_progress)
            //$("#job-"+i.toString()).find('.progress-slider-bar').css("width":percentage_progress.toString()+"%");
            //$("#job-"+i.toString()).find('.progress-slider-number').text(percentage_progress + " %");
    }
    }
    
    function handle_jobs_data_output(out){
        var res = null;
        if(out.msg_type == "stream"){
            res = out.content.text;
        }
        else if(out.msg_type === "pyout"){
            res = out.content.data["text/plain"];
        }
        else if(out.msg_type == "error"){
            res = out.content.ename + ": " + out.content.evalue;
        }
        else if (out.msg_type == "execute_result"){
            res = out.content.data["text/plain"];
        }
        else{
            res = "[out type not implemented]";   
        }
        //console.log(res)
        var jobs_json_string = res.substr(1).slice(0, -1);
        //console.log(jobs_json_string)
        var jobs_dict = JSON.parse(jobs_json_string);
        //console.log(jobs_dict);
        //console.log(jobs_dict[0]["status"]);
        render_live_data(jobs_dict);
    }
    /**
    var application_id = " ";
    function handle_application_id_output(out){
        var res = null;
        if(out.msg_type == "stream"){
            res = out.content.text;
        }
        else if(out.msg_type === "pyout"){
            res = out.content.data["text/plain"];
        }
        else if(out.msg_type == "error"){
            res = out.content.ename + ": " + out.content.evalue;
        }
        else if (out.msg_type == "execute_result"){
            res = out.content.data["text/plain"];
        }
        else{
            res = "[out type not implemented]";   
        }
        application_id = res;
    }
    **/
    function exec_code(){
        var get_jobs_python_code = "get_jobs(get_application_id(sc))";
        var kernel_2 = IPython.notebook.kernel;
        var callbacks = { 'iopub' : {'output' : handle_jobs_data_output}};
        var msg_id_2 = kernel_2.execute(get_jobs_python_code, callbacks, {silent:false});
    }
   exec_code()
setInterval(function(){
    exec_code()
  }, 500);
</script>
"""


# In[4]:

## Combining all three code and displaying it.
HTML(css + html + javascript)


# In[5]:

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


# In[ ]:



