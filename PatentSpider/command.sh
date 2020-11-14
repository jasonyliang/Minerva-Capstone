#!/bin/bash
# this is the sh file that activates the crawler
#  make and activate virtual environments
python3 -m virtualenv venv
source venv/bin/activate
pip install -r requirements.txt

# Que the task-exectutor to set up the first sets of tasks
mrq-run --queue taskexecutor task_executor.Execute_Crawl

# Activate mrq workers
# these workers will start executing tasks 
# we assign workers for different tasks: task executor, crawler, and parser
# each worker would then work on those tasks when they become available
mrq-worker taskexecutor --greenlet 1 & mrq-worker crawl_patents --greenlet 3 & mrq-worker parse_patents --greenlet 5 &
# last worker works on the default queue, in charge of taking care of extraneous tasks on the dashboard