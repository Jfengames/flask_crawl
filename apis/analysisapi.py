import zipfile
from flask import render_template, request, redirect, url_for, session, send_from_directory, flash, Blueprint
from database import User, db, CommonParameters_tagged, Gaodemapscene_tagged, Todos
from decorators import login_required
import os
from toolbox import downloadcsvanalysis, allowed_file, upload_file, downloadcsvanalysis_gaode, celery_task
from config import DIRECTORY
from werkzeug.utils import secure_filename
# celery worker -l info -A main.celery


analysis = Blueprint('analysis', __name__)


@analysis.route('/analysis/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'GET':
        return render_template('analysis.html')


@analysis.route('/analysis/new_mission_todos/', methods=['GET', 'POST'])
def new_mission_todos():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 4))
    paginate = Todos.query.order_by('-id').paginate(page, per_page, error_out=False)

    if request.method == 'GET':
        todos = paginate.items
        return render_template('analysis_new_mission.html', todos=todos,paginate=paginate)

    else:
        _city = request.form.get('city')
        city = _city[0:-1]
        todo_list = Todos.query.filter().all()
        if todo_list == []:
            todo = Todos(todo_city=_city)
            user_id = session['user_id']
            user = User.query.filter(User.id == user_id).first()
            todo.author = user
            db.session.add(todo)
            db.session.commit()
            todos = Todos.query.order_by('-id').all()
            todo_id = Todos.query.order_by('-id').first().id
            celery_task(city, _city, todo_id)
            return render_template('analysis_new_mission.html', todos=todos, paginate=paginate)

        else:
            for todo_city in todo_list:
                if todo_city.todo_city == _city and todo_city.status == True:
                    return redirect(url_for('analysis.new_mission_todos'))
                elif todo_city.todo_city == _city and todo_city.status == False:
                    todos = Todos.query.order_by('-id').all()
                    return render_template('analysis_new_mission.html',todos=todos, paginate=paginate)

            todo = Todos(todo_city=_city)
            user_id = session['user_id']
            user = User.query.filter(User.id == user_id).first()
            todo.author = user
            db.session.add(todo)
            db.session.commit()
            todos = Todos.query.order_by('-id').all()
            todo_id = Todos.query.order_by('-id').first().id
            celery_task(city,_city,todo_id)
            return render_template('analysis_new_mission.html', todos=todos,paginate=paginate)


@analysis.route('/analysis/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(url_for('analysis.new_mission_todos'))
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(url_for('analysis.new_mission_todos'))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(DIRECTORY, filename))
            upload_file(filename)
            return redirect(url_for('analysis.new_mission_todos',filename=filename))

    return render_template('analysis_new_mission.html')



@analysis.route('/analysis/data_search', methods=['GET','POST'])
def data_search():
    if request.method == 'GET':
        return render_template('analysis_data_search.html')
    else:
        _city = request.form.get('city')
        city = _city[0:-1]

        commonparameters_tagged = CommonParameters_tagged.query.filter(CommonParameters_tagged.city == city).limit(1000).all()
        downloadcsvanalysis(city)

        gaodemapscene_tagged = Gaodemapscene_tagged.query.filter(Gaodemapscene_tagged.city == _city).limit(100).all()
        downloadcsvanalysis_gaode(_city)

        return render_template('analysis_data_search.html', commonparameters_tagged=commonparameters_tagged,gaodemapscene_tagged=gaodemapscene_tagged)


@analysis.route('/analysis/data_search/download/', methods=['GET'])
def download2():
    filename = "downloadcsvanalysis.xls"
    return send_from_directory(DIRECTORY, filename, as_attachment=True)


@analysis.route('/analysis/data_search/download_gaode/', methods=['GET'])
def download2_gaode():
    filename = "downloadcsvanalysis_gaode.xls"
    return send_from_directory(DIRECTORY, filename, as_attachment=True)


@analysis.route('/analysis/new_mission_todos/download/', methods=['GET'])
def download():
    z = zipfile.ZipFile('download_new_mission.zip', 'w', zipfile.ZIP_STORED)
    filename_commonparameters = "downloadcsvanalysis.xls"
    filename_gaode = "downloadcsvanalysis_gaode.xls"
    z.write(filename_commonparameters)
    z.write(filename_gaode)
    z.close()

    filename = 'download_new_mission.zip'

    return send_from_directory(DIRECTORY, filename, as_attachment=True)