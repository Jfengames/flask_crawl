# coding=utf-8
"""
@Date: 6/21/18

@Authro: henry
"""
import time
import sys
spider_path = 'C:/Users/X1Carbon/MapCrawler_test/MapCrawler/'
sys.path.append(spider_path)
from MapCrawler.spider_interface import custom_and_run
import os

from multiprocessing import Process
from models import Dataoperation
from exts import db


def crawler(mission,db):
    """
    爬虫模拟
    :param mission:
    :param db:
    :return:
    """
    print('mission:%s start using process id:%s'%(str(mission),os.getpid()))
    time.sleep(60*2)
    print('mission:%s finished. process id:%s'%(str(mission),os.getpid()))

    mission.status = 'pass test'
    db.session.commit()


class SpiderScheduler():
    """
    爬虫调度器，从数据库中获取任务，并根据任务情况调度爬虫任务
    method:
        update:调度器更新，在添加新爬虫任务会调用，通知调度器更新任务，返回值为“running”或者”pending“，表示开始执行，或者挂起了
        start_a_spider: 启动一个新进程，调度一个任务
        after_close: 爬虫结束，更新数据库的状态
        schedule: 根据队列情况，调度任务


    """
    MAX_PROCESS = 2

    def __init__(self):
        """
        获取数据库中所有未完成的任务，并开始
        """
        # self.missions = CrawlerMission.query.filter(CrawlerMission.status!='finished').all()
        # self.scheduling = True
        # self.schedule()
        self.missions_running = 0


    def update(self,mission = None):
        """
        指定一个mission，更新任务队列。如为None，则从数据库中找一个没完成的任务
        :param mission:
        :return:
        """
        if not mission:
            # 没有指定
            mission = Dataoperation.query.filter(Dataoperation.status!='finished').first()

        if self.missions_running < self.MAX_PROCESS:
            # 有可用进程
            self._update(mission,db)
            status = 'running'
        else:
            status = 'pending'

        # # 如果有可用资源，则把剩下的资源都用尽
        # num = self.MAX_PROCESS - self.missions_running
        # if num >0:
        #     missions = CrawlerMission.query.filter(CrawlerMission.status not in ['finished','running']).limit(num).all()
        #     for m in missions:
        #         self._update(m,db)

        # 指定的任务状态
        return status


    def _update(self,mission,db):
        mission.status = 'running'
        db.session.commit()
        self.start_a_spider(mission,db)
        self.missions_running += 1



    def start_a_spider(self,mission,db):
        """
        开启新进程，爬取任务

        :param mission:任务对象
        :param db: 数据库对象
        :return:
        """
        paras = {'email':mission.email,
                 'city_adcode':mission.city_adcode,
                 'type_code':mission.type_code,
                 'keys':mission.keys.split(','),
                 'adsl_server_url':mission.adsl_server_url,
                 'adsl_auth':tuple(mission.adsl_auth.split(',')),
                 'final_grid':mission.final_grid,
                 'status':mission.status,
                 'resolution':mission.resolution,
                 'LOG_LEVEL':'DEBUG',
                 'LOG_FILE':mission.city_adcode+'-'+mission.type_code+'.log'
                 }
        proc = Process(target=custom_and_run,args=(paras,spider_path))
        proc.start()
        print('已调度新进程%s'%proc.pid)



    def after_close(self,mission,status,grid):
        """
        爬虫结束，根据结束原因更新数据库状态，并再更细
        :param mission: 任务对象
        :param status： 状态
        :return:
        """
        self.missions_running -= 1
        assert self.missions_running >=0, 'mission_running只应该大于0'

        # 更新数据库状态
        # 数据库状态由爬虫自行更改
        # mission.status = status
        # mission.final_grid = grid
        # db.session.commit()

    # def schedule(self):
    #     """
    #     根据队列情况，调度任务
    #
    #     :return:
    #     """
    #     while True:
    #         if self.missions_running < self.MAX_PROCESS:
    #             # 有可用进程
    #             try:
    #                 m = self.missions.pop()
    #                 self.start_a_spider(m)
    #                 self.missions_running+=1
    #             except IndexError:
    #                 # 队列中已无数据
    #                 break
    #
    #     self.scheduling = False

if __name__ == '__main__':
    sc = SpiderScheduler()
    # mission = CrawlerMission()
    # mission.email = 'test@SpiderScheduler.py'
    # mission.status = 'not start yet'
    # mission.final_grid =0
    # mission.adsl_server_ip = 'http://teset'
    # mission.adsl_auth = 'fasdf'
    # mission.keys = 'keys'
    # mission.type_code = '120000'
    # mission.city_adcode = '123333'
    #
    # db.session.add(mission)
    # db.session.commit()

    sc.update()
