## CERN-Big-data-project
This is a proof of concept of how 'Big data tools for Physics Analysis' can be implemented in GSoC-2017.

 - This project has been made and tested on Spark-1.6.3
 - Go to directory, where you cloned this repositry.
 - Execute command from terminal, ```jupyter notebook```


Environment Variable settings:-

Add these lines (with directory name changed as per your system) to your .bashrc file.
```
export SPARK_HOME="/home/shivanshu/Documents/SPARK-1/spark-1.6.3-bin-hadoop2.6"
export PATH=$PATH:$SPARK_HOME/bin
export PYTHONPATH=$SPARK_HOME/python/:$PYTHONPATH
export PYTHONPATH=$SPARK_HOME/python/lib/py4j-0.9-src.zip:$PYTHONPATH
```
