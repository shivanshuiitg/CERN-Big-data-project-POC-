<script>
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
        $('#main-div').css("height",(number_of_jobs*150 + 120).toString()+"px");
        var count = 0;
        var str = " ";
        for (count = 0;count <number_of_jobs;count++){
         str =  str + '<div class="job-div" id="job-'+count+'"><div class="job-details"><strong style="color:green">Job ID:</strong> <strong><span class="job-id">1<span></strong><br><strong style="color:green">Job Name:</strong> <strong><span class="job-name"><span></strong><br><strong style="color:green">Job Status: </strong><strong><span class="job-status"><span><strong></div><table border="3" class="job-table"><tbody><tr style="height: 23px;"><td style="width: 150px; height: 23px;"><strong>Number of Tasks</strong></td><td style="width: 150px; height: 23px; color: orange;"><strong>Active Tasks</strong></td><td style="width: 150px; height: 23px; color: green;"><strong>Completed Tasks</strong></td><td style="width: 150px; height: 23px; color: blue;"><strong>Skipped Tasks</strong></td><td style="width: 150px; height: 23px; color: red;"><strong>Failed Tasks</strong></td></tr><tr style="height: 23px;"><td style="width: 150px; height: 23px;"><span class="number-of-tasks"><span></td><td style="width: 150px; height: 23px;"><span class="active-tasks"><span></td><td style="width: 150px; height: 23px;"><span class="completed-tasks"><span></td><td style="width: 150px; height: 23px;"><span class="skipped-tasks"><span></td><td style="width: 150px; height: 23px;"><span class="failed-tasks"><span></td></tr></tbody></table><span class="job-progress-span"><div class="progress-slider"><div class="progress-slider-bar" id="progress_slider_bar_"'+count+' ></div><div class="progress-slider-number"></div></div></span></div><br>';
        }
        $("#job-info").html(str)
    }
    function render_live_data(jobs_dict){
        //alert("Number of Jobs : " + jobs_dict.length)
        number_of_jobs = jobs_dict.length
        render_html(number_of_jobs)
        
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
            console.log(percentage_progress);
            $("#job-"+i.toString()).find('.progress-slider-number').text(percentage_progress + " %");
            // TODO
            // width not changing
            //$("#progress_slider_bar_"+i.toString()).css("width":percentage_progress+" %");
            //$("#job-"+i.toString()).find('.progress-slider-number').text(percentage_progress + "%");
    }
    }
    function render_application_data(application_dict){
            $("#application-name").text(application_dict[0]["name"]);
            $("#application-id").text(application_dict[0]["id"]);
            $("#number-of-attempts").text((application_dict[0]["attempts"]).length);
    }

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
        //console.log(res)
        var jobs_json_string = result.substr(1).slice(0, -1);
        //console.log(jobs_json_string)
        var jobs_dict = JSON.parse(jobs_json_string);
        //console.log(jobs_dict);
        //console.log(jobs_dict[0]["status"]);
        render_live_data(jobs_dict);
    }
    function handle_application_data_output(out){
        var result = get_output(out)
        var application_json_string = result.substr(1).slice(0, -1);
        var application_dict = JSON.parse(application_json_string);
        //alert(application_dict["name"])
        render_application_data(application_dict)
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
        var get_application_python_code = "get_all_applications()";
        var kernel_1 = IPython.notebook.kernel;
        var msg_id_1 = kernel_1.execute(get_application_python_code,{ 'iopub' : {'output' : handle_application_data_output}}, {silent:false})
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
