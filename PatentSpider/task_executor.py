'''
Meta-Task:
Execute and coordinate Spider and Parser

這是啟動任務的關鍵中介，程式啟動時會從這裡開始
task_executor的主要功能是將任務及任務所需的資料(如url)交給spider去執行
spider 完成後自己會交棒給parser,這一部分就不需要task_executor 來了
'''
import time
import subprocess
import traceback

from mrq.task import Task
from mrq.job import queue_job
from mrq.context import connections, log

import sys
import os
sys.path.insert(0, os.path.abspath(os.getcwd()+'../../../'))
sys.path.insert(1, os.path.abspath(os.getcwd()+'../../../../'))


class Execute_Crawl(Task):
    '''
    Execution of two tasks: crawl and parse
    '''

    def __init__(self):
        super(Execute_Crawl, self).__init__()

    def exec_push_work(self, url):
        # import subprocess
        # modify arguments
        # 這些是會傳下去給spider的函數 除了spider需要用的之外，還包括所有栈名以及其任務的路徑
        # 如果有更改栈名請於此更改
        args = {
            'url': url,
            'spiderTask': 'spider.spider.USPTOSpider',
            'spiderqueue': 'crawl_patents',
            'parseTask': 'parser.parse_posts.USPTOParser',
            'parsequeue': 'parse_patents'
        }
        # task = ['spider.spider_crawl.LcSpider']
        # command = ['mrq-run'] + task + args
        # '--queue', 'crawl_posts'
        # subprocess.Popen(command)
        queue_job(args['spiderTask'], args, queue=args['spiderqueue'])

    def run(self, params):
        '''
        Enqueue spider jobs
        '''
        # 我們在這裡開始分發任務
        # assign the CPC classification here
        # classification = "H01L"
        start_pages = 1001
        end_pages = 2000  # get first 1000 pages of patents
        for page in range(start_pages, end_pages+1):
            url = f"http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&u=%2Fnetahtml%2FPTO%2Fsearch-adv.htm&r=0&f=S&l=50&d=PTXT&OS=CPCL%2FH01L&RS=CPCL%2FH01L&Query=CPCL%2FH01L&TD=439972&Srch1=H01L.CPCL.&NextList{page}=Next+50+Hits"
            self.exec_push_work(url)

    def run_wrapped(self, params):
        """
        Wrap all calls to tasks in init & safety code.
        這是保險，如果執行task_executor有意外這裡會重新啟動
        """
        try:
            return self.run(params)
        except Exception as e:
            traceback.print_exc()
            self.requeue_job(
                params, fpath='task_executor.Execute_Crawl', nqueue='taskexecutor')
            print(e)

    def requeue_job(self, params, fpath=None, nqueue=None):
        '''
        requeue an unfinished job
        run_wrapped的helper function
        '''
        log.warning('Job Failed, re-queue...%s' % params['url'])
        queue_job(fpath, params, queue=nqueue)
