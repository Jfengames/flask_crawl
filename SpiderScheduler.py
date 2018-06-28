# coding=utf-8
"""
@Date: 6/21/18

@Authro: henry
"""
import time
import sys
spider_path = '/home/henry/proj/MapCrawler/'
sys.path.append(spider_path)
from MapCrawler.spider_interface import custom_and_run


from multiprocessing import Process,Pool
from database import Scrape_Missions,db

from config import MAX_PROCESS



class SpiderScheduler():
    """
    爬虫调度器，从数据库中获取任务，并根据任务情况调度爬虫任务
    method:
        update:调度器更新，在添加新爬虫任务会调用，通知调度器更新任务，返回值为“running”或者”pending“，表示开始执行，或者挂起了
        start_a_spider: 启动一个新进程，调度一个任务


    """

    def __init__(self):
        """
        获取数据库中所有未完成的任务，并开始
        """
        self.pool = Pool(processes=MAX_PROCESS)
        self.missions_running = 0


    def update(self,mission = None):
        """
        指定一个mission，更新任务队列。如为None，则从数据库中找一个没完成的任务
        :param mission:
        :return:
        """
        if not mission:
            # 没有指定
            mission = Scrape_Missions.query.filter(Scrape_Missions.status=='not start yet').first()

        status = self._update(mission,db)


        # 看看有没有其他没有执行完的任务
        other_missions = Scrape_Missions.query.filter(Scrape_Missions.status=='not start yet').all()
        for one in other_missions:
            self._update(one,db)

        return status



    def _update(self,mission,db):

        running_missions = Scrape_Missions.query.filter(Scrape_Missions.adsl_server_url==mission.adsl_server_url)\
                                .filter(Scrape_Missions.status=='running').all()

        if len(running_missions)>=1:
            # 该ADSL服务器已被使用
            # 需要暂停直到ADSL资源释放
            return '该ASDL正在使用，请改天再试'

        else:
            self.start_a_spider(mission,db)
            return '开始爬取'


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
                 'LOG_LEVEL':'INFO',
                 # 'LOG_FILE':mission.city_adcode+'-'+mission.type_code+'.log'
                 }
        # proc = Process(target=custom_and_run,args=(paras,spider_path))
        self.pool.apply_async(func=custom_and_run,args=(paras,spider_path))
        print('已调度新进程:%s-%s'%(paras['city_adcode'],paras['type_code']))
        mission.status = 'running'
        db.session.commit()




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
