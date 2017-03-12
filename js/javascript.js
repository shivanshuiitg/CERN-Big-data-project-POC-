<script>
// indicator variable for all jobs completion
var isComplete = 0;
var iteration = 1;
var isStopped = 0;
// template html string for Job
var job_html_template_string = '<div class="job-details">\
<strong style="color:green">Job ID:</strong><span class="job-id"></span><br>\
<strong style="color:green">Job Name:</strong><span class="job-name"></span><br>\
<strong style="color:green">Job Status: </strong><span class="job-status"></span>\
</div>\
<table border="3" class="job-table">\
<tbody>\
<tr style="height: 23px;">\
<td style="width: 150px; height: 23px;"><strong>Number of Tasks</strong></td>\
<td style="width: 150px; height: 23px; color: orange;"><strong>Active Tasks</strong></td>\
<td style="width: 150px; height: 23px; color: green;"><strong>Completed Tasks</strong></td>\
<td style="width: 150px; height: 23px; color: blue;"><strong>Skipped Tasks</strong></td>\
<td style="width: 150px; height: 23px; color: red;"><strong>Failed Tasks</strong></td>\
</tr>\
<tr style="height: 23px;">\
<td style="width: 150px; height: 23px;"><span class="number-of-tasks"><span></td>\
<td style="width: 150px; height: 23px;"><span class="active-tasks"><span></td>\
<td style="width: 150px; height: 23px;"><span class="completed-tasks"><span></td>\
<td style="width: 150px; height: 23px;"><span class="skipped-tasks"><span></td>\
<td style="width: 150px; height: 23px;"><span class="failed-tasks"><span></td>\
</tr></tbody></table>\
<span class="job-progress-span">\
<div class="progress-slider">\
<div class="progress-slider-bar"></div>\
<div class="progress-slider-number"></div>\
</div>\
</span>\
<span class="job_submission">\
<span style="color:green;font-weight:bold;">Job Submission : </span>\
<span class="job_submission_time"></span>\
</span>\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\
<span class="job_completion" style="display:none;">\
<span style="color:green;font-weight:bold;">Job Completion : </span>\
<span class="job_completion_time"></span>\
</span>';

// function to determine if JSON string is valid or not
function isJSON(str) {
    try {
        JSON.parse(str);
    } catch (e) {
        return false;
    }
    return true;
}

// function to render the HTML on Jupyter notebook
function render_html(number_of_jobs){
    $('#main-div').css("height",(number_of_jobs*180 + 70).toString()+"px");
    var count = 0;
    var str = " ";
    for (count = 0;count <number_of_jobs;count++){
        str =  str + '<div class="job-div" id="job-'+count+'"> ' + job_html_template_string + '</div><br>';
    }
    $("#job-info").html(str)
}

// function to render the live data on Jupyter notebook
function render_live_data(jobs_dict){
    number_of_jobs = jobs_dict.length
    render_html(number_of_jobs)
    var jobs_complete = 0;
    for (var i = 0;i<number_of_jobs;i++){
        var job = jobs_dict[i];
        var number_of_tasks = job["numTasks"];
        var processed_tasks = job["numCompletedTasks"] + job["numSkippedTasks"] + job["numFailedTasks"];
        var percentage_progress = Math.round((processed_tasks*100)/number_of_tasks);
        var width = percentage_progress+"%";
        var submission_time = job["submissionTime"];
        var completion_time = " ";
        $("#job-"+i.toString()).find('.number-of-tasks').text(job["numTasks"]);
        $("#job-"+i.toString()).find('.active-tasks').text(job["numActiveTasks"]);
        $("#job-"+i.toString()).find('.completed-tasks').text(job["numCompletedTasks"]);
        $("#job-"+i.toString()).find('.skipped-tasks').text(job["numSkippedTasks"]);
        $("#job-"+i.toString()).find('.failed-tasks').text(job["numFailedTasks"]);
        $("#job-"+i.toString()).find('.job-id').text(job["jobId"]);
        $("#job-"+i.toString()).find('.job-name').text(job["name"]);
        $("#job-"+i.toString()).find('.job-status').text(job["status"]);
        $("#job-"+i.toString()).find('.progress-slider-number').text(percentage_progress + " %");
        $("#job-"+i.toString()).find('.progress-slider-bar').css("width",width);
        if(job["status"]== "SUCCEEDED"){
            jobs_complete = jobs_complete + 1;
            $("#job-"+i.toString()).find('.stop_job_button').prop('disabled', true);
        }
        $("#job-"+i.toString()).find('.job_submission_time').text(submission_time);
        if ("completionTime" in job){
            completion_time = job["completionTime"];
            $("#job-"+i.toString()).find('.job_completion').css("display","");
            $("#job-"+i.toString()).find('.job_completion_time').text(completion_time);
        }
    }
    if (jobs_complete == number_of_jobs){
            isComplete = 1;
            $("#stop_application_button").attr("disabled","disabled");
    }
}

// render Application data on Jupyter notebook
function render_application_data(application_dict){
    $("#application-name").text(application_dict[0]["name"]);
    $("#application-id").text(application_dict[0]["id"]);
    $("#number-of-attempts").text((application_dict[0]["attempts"]).length);
}

// get the output from python kernel
function get_output(out){
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
    return res;
}

function handle_jobs_data_output(out){
    var result = get_output(out);
    var jobs_json_string = result.substr(1).slice(0, -1);
    var jobs_dict = JSON.parse(jobs_json_string);
    render_live_data(jobs_dict);
}

function handle_application_data_output(out){
    var result = get_output(out)
    var application_json_string = result.substr(1).slice(0, -1);
    var application_dict = JSON.parse(application_json_string);
    render_application_data(application_dict)
}

function handle_stop_application_output(out){
    var output  = get_output(out);
}

function stop_application(){
    var get_stop_application_python_code = "fc.StopApplication(sc)";
    var kernel = IPython.notebook.kernel;
    var msg_id = kernel.execute(get_stop_application_python_code,{ 'iopub' : {'output' : handle_stop_application_output}}, {silent:false});
}

function exec_code(){
    if (iteration==1){
        var get_application_python_code = "fc.get_all_applications(sc)";
        var kernel_1 = IPython.notebook.kernel;
        var msg_id_1 = kernel_1.execute(get_application_python_code,{ 'iopub' : {'output' : handle_application_data_output}}, {silent:false})
        iteration = iteration + 1;
    }
    var get_jobs_python_code = "fc.get_jobs(fc.get_application_id(sc),sc)";
    var kernel_2 = IPython.notebook.kernel;
    var callbacks = { 'iopub' : {'output' : handle_jobs_data_output}};
    var msg_id_2 = kernel_2.execute(get_jobs_python_code, callbacks, {silent:false});
}

function application_stop_indication(){
    $(".job-status").html("<strong style='color:red'>Application Killed</strong>");
    $("#stop_application_button").attr("disabled","disabled");
    $('.progress-slider-bar').css('background','#FF4C4C');
}
$("#stop_application_button").click(function(){
    isStopped = 1;
    stop_application();
    setTimeout(application_stop_indication, 800);
});

exec_code()
setInterval(function(){
    // if all jobs are not completed then keep polling
    if (isComplete==0 && isStopped==0){
        exec_code();
    }
}, 500);
</script>