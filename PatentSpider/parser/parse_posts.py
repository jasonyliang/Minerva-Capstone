'''
Task 2: Parsing
'''
from mrq.task import Task
from mrq.job import queue_job
from mrq.context import connections, log

import requests
from lxml import etree
from lxml.html.clean import clean_html
from fake_useragent import UserAgent
import traceback
from datetime import datetime

from _dber.pg_orm import Content
from _dber.config import session

import os
import sys

sys.path.insert(0, os.path.abspath(os.getcwd()+'../'))
sys.path.insert(1, os.path.abspath(os.getcwd()+'../../'))
sys.path.insert(2, os.path.abspath(os.getcwd()+'../../../'))
sys.path.insert(3, os.path.abspath(os.getcwd()+'../../../../'))


class USPTOParser(Task):  # make sure you give it a name :) 記得給parser一個名字呦
    def run(self, params):
        '''
        Run parser
        parser任務主要是負責解析spider爬下來的源碼，並將其存入數據庫
        '''
        url = params['patent_url']
        # retrieve info
        info = self.retrieve_info(url)
        for cnt in info:
            inserted = self.insertData(cnt)

            if not inserted:
                queue_job(params['parseTask'],
                          params,
                          queue=params['parsequeue'])
        return True

    def run_wrapped(self, params):
        """ 
        Wrap all calls to tasks in init & safety code. 
        """
        try:
            return self.run(params)
        except Exception as e:
            traceback.print_exc()
            self.requeue_job(
                params, fpath=params['parseTask'], nqueue=params['parsequeue'])
            print(e)

    def retrieve_info(self, url):
        '''
        Parser job based on the source
        Output should be a database object
        在這裡，為了以防再次訪問網站，我們已在spider階段將源碼存入數據庫的pagesource表
        現在，我們只需要將源碼從數據庫中拿出來進行解析就好
        這個函數是parser 的核心，進行主要的解析工作
        '''
        ua = UserAgent()
        headers = {
            "user-agent": ua.random
        }
        res = requests.get(url, headers=headers)
        source = clean_html(res.content.decode(res.encoding))
        tree = etree.HTML(source)
        text_path = "//body//br | //body//hr | //body//center//b//i | //body//center//b | //body//p"
        text_nodes = tree.xpath(text_path)
        # grab text from br that contains claims, start from "Claim" and end at "Description"
        claims = []
        abstract = ""
        description = ""
        start = False
        for i, br_hr in enumerate(text_nodes):
            if br_hr.text == "Abstract":
                start = True  # next one
            if start and br_hr.tag == "p":
                abstract = br_hr.text.strip()
                break
        start = False
        for i, br_hr in enumerate(text_nodes):
            if br_hr.text == "Claims":
                start = True  # there is one horizontal line after Claims
                text_nodes.pop(i + 1)  # remove that hrs
                text_nodes.pop(i + 2)  # remove the "what is claimed" string
            elif start and br_hr.tail:
                claims.append(br_hr.tail.strip())
                # if we get a horizontal line we terminate
                if br_hr.tag == 'hr':
                    break
        # collect descriptions
        start = False
        for i, br_hr in enumerate(text_nodes[i+1:]):
            if br_hr.text == "Description":
                start = True
                text_nodes.pop(i + 1)  # remove that hrs
            elif start and br_hr.tail:
                description += br_hr.tail
        cnt_lst = []
        for c in claims:
            cnt = Content(
                url=url,
                write_date=str(datetime.now()),
                claims=c,
                abstract=abstract,
                description=description
            )
            cnt_lst.append(cnt)
        return cnt_lst

    def insertData(self, cnt):
        '''
        Store result to database
        將解析好的內容存入數據庫
        '''
        try:
            sess = session()
            sess.add(cnt)
            sess.commit()
            return True
        except Exception as e:
            sess.rollback()
            traceback.print_exc()
            print(e)
            return False
        finally:
            sess.close()

    def requeue_job(self, params, fpath=None, nqueue=None):
        '''
        requeue an unfinished job
        '''
        log.warning('Job Failed, re-queue...%s' % params['url'])
        queue_job(fpath, params, queue=nqueue)
