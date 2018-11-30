from flask import Flask,session
from database import db, User, Todos
import config
from apis.userapi import user
from apis.indexapi import index
from apis.analysisapi import analysis
from apis.noteapi import note
from apis.crawlapi import crawl
from celery import Celery
from celery import platforms  # 如果你不是linux的root用户，这两行没必要
from toolbox import analysis_new_mission_gaodemapscene_tagged, analysis_new_mission_commonparameters_tagged_contains, \
    analysis_new_mission_commonparameters_tagged_100, analysis_new_mission_commonparameters_tagged_100_200, \
    downloadcsvanalysis, downloadcsvanalysis_gaode

app = Flask(__name__)
app.config.from_object(config)


platforms.C_FORCE_ROOT = True  # 允许root权限运行celery

app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'


celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'],backend=app.config['CELERY_RESULT_BACKEND'])
celery.conf.update(app.config)


db.init_app(app)
app.register_blueprint(blueprint=user)
app.register_blueprint(blueprint=index)
app.register_blueprint(blueprint=crawl)
app.register_blueprint(blueprint=analysis)
app.register_blueprint(blueprint=note)

@app.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()

        if user:
            return {'user':user}
    return {}


@celery.task()
def data_operation(city,_city):

    # print('场景与小区关联')
    analysis_new_mission_gaodemapscene_tagged(city)
    # print('小区与场景关联')
    # 点在面内‘1’
    analysis_new_mission_commonparameters_tagged_contains(city)
    # 100米范围内‘2’
    analysis_new_mission_commonparameters_tagged_100(city)
    # 100-200米范围内‘3’
    analysis_new_mission_commonparameters_tagged_100_200(city)

    downloadcsvanalysis(city)

    downloadcsvanalysis_gaode(_city)

    return '任务完成'


if __name__ == '__main__':
    app.run(debug=True)