from flask import current_app as app
import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

mysql = MySQL(cursorclass=DictCursor)
mysql.init_app(app)
nav = [
    {'name': 'Contact Us', 'url': '/contact'},
    {'name': 'Home', 'url': '/index'}
]


@app.route("/")
def home():
    """Landing page."""
    return render_template("home.html",
                           nav=nav,
                           title="Flask Application")


@app.route("/contact")
def contact():
    return render_template("contact.html", nav=nav, title='Flask Application')


@app.route('/index', methods=['GET'])
def index():
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblCitiesImport')
    result = cursor.fetchall()
    return render_template('index.html', nav=nav, title='Flask Application', cities=result)


@app.route('/view/<int:city_id>', methods=['GET'])
def record_view(city_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblCitiesImport WHERE id=%s', city_id)
    result = cursor.fetchall()
    return render_template('view.html', nav=nav, title='Flask Application', city=result[0])


@app.route('/edit/<int:city_id>', methods=['GET'])
def form_edit_get(city_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblCitiesImport WHERE id=%s', city_id)
    result = cursor.fetchall()
    return render_template('edit.html', nav=nav, title='Flask Application', city=result[0])


@app.route('/edit/<int:city_id>', methods=['POST'])
def form_update_post(city_id):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('fldheight'),
                 request.form.get('fldheight'), city_id)
    sql_update_query = """UPDATE tblCitiesImport t SET t.fldheight = %s, t.fldweight = %s WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/index", code=302)


@app.route('/cities/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', nav=nav, title='Flask Application', )


@app.route('/cities/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('fldheight'),
                 request.form.get('fldweight'))
    sql_insert_query = """INSERT INTO tblCitiesImport (fldheight,fldweight) VALUES (%s,%s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/index", code=302)


@app.route('/delete/<int:city_id>', methods=['POST'])
def form_delete_post(city_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM tblCitiesImport WHERE id = %s """
    cursor.execute(sql_delete_query, city_id)
    mysql.get_db().commit()
    return redirect("/index", code=302)


@app.route('/api/v1/cities', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblCitiesImport')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/cities/<int:city_id>', methods=['GET'])
def api_retrieve(city_id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblCitiesImport WHERE id=%s', city_id)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/cities/<int:city_id>', methods=['PUT'])
def api_edit(city_id) -> str:
    cursor = mysql.get_db().cursor()
    content = request.json
    inputData = (content['fldheight'], content['fldweight'],  city_id)
    sql_update_query = """UPDATE tblCitiesImport t SET t.fldheight = %s, t.fldweight = %s WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/cities', methods=['POST'])
def api_add() -> str:

    content = request.json

    cursor = mysql.get_db().cursor()
    inputData = (content['fldheight'], content['fldweight'])
    sql_insert_query = """INSERT INTO tblCitiesImport (fldheight,fldweight) VALUES (%s, %s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/v1/cities/<int:city_id>', methods=['DELETE'])
def api_delete(city_id) -> str:
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM tblCitiesImport WHERE id = %s """
    cursor.execute(sql_delete_query, city_id)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp

