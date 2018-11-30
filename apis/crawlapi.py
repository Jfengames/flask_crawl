from flask import render_template, request, session, Blueprint
from database import User,Adcode,Scenecode,ScrapeMissions,db
from decorators import login_required
from config import KEYS
crawl = Blueprint('crawl',__name__)


@crawl.route('/crawl/',methods=['GET', 'POST'])
@login_required
def spider():

    if request.method == 'GET':
        return render_template('crawl.html')
    else:
        user = User.query.filter(User.id == session.get('user_id')).first()
        username = user.username
        email = user.email
        city = request.form.get('city')
        global adcode
        adcode = Adcode.query.filter(Adcode.city == city).first().adcode
        scene = request.form.get('scene')
        global scenecode
        scenecode = Scenecode.query.filter(Scenecode.scene == scene).first().scenecode
        adsl_server_url = request.form.get('ADSL_SERVER_URL')
        if not adsl_server_url:
            adsl_server_url='http://223.105.3.170:18888'

        adsl_server_auth = request.form.get('ADSL_SERVER_AUTH')
        if not adsl_server_auth:
            adsl_server_auth=','.join(['adsl_proxy','changeProxyIp'])

        key=request.form.get('KEY')
        if not key:
            key=','.join(KEYS)

        final_gird = request.form.get('final_grid')
        if not final_gird:
            final_gird = 0


        mission = Scrape_Missions(username=username, email=email, city=city, city_adcode=adcode, scene=scene,
                                        type_code=scenecode, adsl_server_url=adsl_server_url,
                                        adsl_auth=adsl_server_auth, keys=key,final_grid=final_gird,
                                        status='not start yet')

        # 判断是否有重复的任务
        exist_mission = Scrape_Missions.query.filter(Scrape_Missions.city_adcode==mission.city_adcode,Scrape_Missions.type_code==mission.type_code).first()

        if exist_mission:
            return render_template('reconfirm.html',exist_mission=exist_mission,mission=mission)

        else:
            db.session.add(mission)
            db.session.commit()

            return render_template("crawl.html", username=username, email=email, city=city, adcode=adcode,
                                   scene=scene, scenecode=scenecode)


@crawl.route('/reconfirm/',methods=['GET','POST'])
@login_required
def reconfirm():
    if request.method == 'GET':
        # 显示元原任务详情以及当前任务详情
        exist_mission = request.args.get('exist_mission')
        mission = request.args.get('mission')
        return render_template('reconfirm.html',exist_mission=exist_mission,mission=mission)
    else:
        conformed = request.form.get('confirm')
        if conformed == 'yes':
            #重新调度 任务
            return '暂未实现,请联系管理员'
            # db.session.add(mission)
            # db.session.commit()
            #
            # msg = sc.update(mission)
            #
            # return render_template("crawl.html", username=mission.username, email=mission.email,
            #                        city=mission.city, adcode=mission.adcode,
            #                        scene=mission.scene, scenecode=mission.scenecode,
            #                        msg=mission.msg)
        else:
            return '暂未实现,请联系管理员'

