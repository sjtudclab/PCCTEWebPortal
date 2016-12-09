#!/usr/bin/python3
import traceback
import logging
import bottle
import bottle_mysql
import models
import dbm
import time
import json
import os
from beaker.middleware import SessionMiddleware

logging.basicConfig(filename='smartycity-DBM.log', level=logging.DEBUG)

app = bottle.Bottle()
app.config.load_config('app.conf')
# dbhost: optional, default is localhost
# keyword: The keyword argument name that triggers the plugin (default: ‘db’).
plugin = bottle_mysql.Plugin(dbuser=app.config['mysql.user'], dbpass=app.config['mysql.pwd'],
                             dbname=app.config['mysql.dbname'], dbhost=app.config['mysql.host'],
                             dictrows=['mysql.dictrows'] == 'True')
app.install(plugin)


def getCurrentDayTime():
    return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))


logging.info(getCurrentDayTime() + ' bottle_mysql installed.')

session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 300,  # 300s
    'session.data_dir': './data',
    'session.auto': True
}
app_middlware = SessionMiddleware(app, session_opts)


def excep_handler(fn):
    def wrapper(*args, **kargs):
        try:
            return fn(*args, **kargs)
        except Exception as e:
            logging.debug(getCurrentDayTime() + ' ' + traceback.format_exc())
            return error500()
    return wrapper
app.install(excep_handler)


# @app.hook('before_request')
def setup_request():
    try:
        bottle.request.session = bottle.request.environ['beaker.session']
    except:
        logging.info(401, getCurrentDayTime() + " Failed beaker_session in slash")
        bottle.abort(401, "Failed beaker_session in slash")

    try:
        exclude_path = ['/', '/admin/login']
        if bottle.request.urlparts.path in exclude_path:
            return
        username = bottle.request.session['username']
    except Exception as e:
        logging.info(getCurrentDayTime() + ' Authenticated failed!')
        bottle.redirect('/')


# Description : document template.
#
# Input : None
#
# Output : test page
@app.route('/test/<userid>',mysql={'dbname': 'community_dbm'})
def test(userid,db):
    return bottle.jinja2_template('template/base.html')


# Description : get static files.
#
# Input : filepath
#
# Output : static file
@app.route('/static/<filepath:path>')
def server_static(filepath):
    return bottle.static_file(filepath, root='static')


@app.route('/files/<filepath:path>')
def server_file(filepath):
    return bottle.static_file(filepath, root='files')


# Description : login page.
#
# Input : None
#
# Output : login page
@app.get('/')
# @app.get('/admin/login')
def admin_login():
    return bottle.jinja2_template('template/index.html')


@app.get('/test/upload')
def test_upload():
    return bottle.jinja2_template('template/test_upload.html')


@app.get('/test/list')
@app.post('/test/list')
def test_list():
    return bottle.jinja2_template('template/test_list.html')

@app.get('/test/submit/<name>')
def test_submit(name):
    os.chdir('/tmp/underTest')
    os.system('git init')
    os.system('git add .')
    os.system('git commit -m "1" ')
    os.system('git push -f origin master:'+name)
    os.chdir('/home/hadoop/Work/PCCTEWebPortal')
    return name

# Description : login process.
#
# Input : None
#
# Output : login result page
@app.post('/admin/login', mysql={'dbname': 'community_dbm'})
def admin_login_process(db):
    username = bottle.request.forms.username
    password = bottle.request.forms.password
    db.execute('select password, user_type_id from user where username = "' + username + '"')
    row = db.fetchone()
    if row:
        if str(row[0]) == password and str(row[1]) == '4':
            bottle.request.session['username'] = username
            return admin_index()
        else:
            return "<p>Your username or password is wrong, or you are not an administrator.</p>"
    else:
        return "<p>Login failed.</p>"


# Description : index page.
#
# Input : None
#
# Output : index page
@app.get('/admin')
@app.get('/admin/index')
def admin_index(**dict):
    return bottle.jinja2_template('template/index.html', dict)


# @app.get('/admin/signup')
# def admin_signup():
#     return bottle.jinja2_template('template/signup.html')


# @app.post('/admin/signup')
# def admin_signup_process(db):
#     add_user(db)
#     return bottle.jinja2_template('template/login.html')


@app.get('/admin/user')
@app.get('/admin/user/list')
def admin_user_list(db):
    sql = 'select image, username, password, user_type_id,name, email, identity_number, card_id, user_id from user'
    db.execute(sql)
    it = iter(db)
    users = []
    user_type_map = {1: 'managemment', 2: 'service', 3: 'resident', 4: 'admin'}
    for i, row in enumerate(it):
        users.append(models.User(row[8], row[1], row[2][0:10] + '...', user_type_map[row[3]], '/files/' + 'default_user.png',
                                 row[4], row[5], row[6][0:18] if row[6] else None, row[7]))
    return bottle.jinja2_template('template/user_list.html', users=users)


@app.get('/admin/user/<userid>')
def admin_user_detail(userid, db):
    # User Basic Infomation
    sql = 'select user_id, username, password, user_type_id, image, name, email, identity_number,  card_id from user ' \
          'where user_id=' + userid
    db.execute(sql)
    user_row = db.fetchone()
    sql = 'select type from user_type where user_type_id='+ str(user_row[3])
    db.execute(sql)
    user_type_row = db.fetchone()
    user = models.User(user_row[0], user_row[1], user_row[2], user_type_row[0], user_row[4], user_row[5], user_row[6],
                       user_row[7], user_row[8])

    # User Role Information
    sql = 'select user_role_id, user_id, role.role_id, role_type_id,role.description, user_role.description, ' \
          'description_detail from  user_role join role on role.role_id=user_role.role_id where user_id=' + userid
    db.execute(sql)
    it = iter(db)
    user_roles = []
    for i, row in enumerate(it):
        user_roles.append(models.User_Role(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))

    # User Resident Information
    sql = 'select * from citizen_resident where user_id=' + userid
    db.execute(sql)
    user_resident_row = db.fetchone()
    kv_dict = {}
    if user_resident_row is None:
        user_resident_row = []
    for index, val in enumerate(user_resident_row):
        kv_dict[db.description[index][0]] = val
    user_resident_info = models.User_Resident_Info(**kv_dict)

    # Party Card
    sql = 'select * from partycard where user_id=' + userid
    db.execute(sql)
    user_party_row = db.fetchone()
    kv_dict = {}
    if user_party_row is None:
        user_party_row = []
    for index, val in enumerate(user_party_row):
        kv_dict[db.description[index][0]] = val
    user_party_info = models.User_Party_Info(**kv_dict)

    # Net Card
    sql = 'select * from netcard where user_id=' + userid
    db.execute(sql)
    user_net_row = db.fetchone()
    kv_dict = {}
    if user_net_row is None:
        user_net_row = []
    for index, val in enumerate(user_net_row):
        kv_dict[db.description[index][0]] = val
    user_net_info = models.User_Net_Info(**kv_dict)

    # Reside Card
    sql = 'select * from livingcard where user_id=' + userid
    db.execute(sql)
    user_living_row = db.fetchone()
    kv_dict = {}
    if user_living_row is None:
        user_living_row = []
    for index, val in enumerate(user_living_row):
        kv_dict[db.description[index][0]] = val
    user_living = models.User_Living_Info(**kv_dict)

    return bottle.jinja2_template('template/user_detail.html', user=user, user_roles=user_roles,
                                  user_living=user_living,user_net_info=user_net_info,user_party_info=user_party_info
                                  ,user_resident_info=user_resident_info)


@app.get('/admin/apartment')
@app.get('/admin/apartment/list')
def admin_apartment_list():
    return bottle.jinja2_template('template/apartment_list.html',
                                  apartments=[models.Apartment(101, '1号', 'Building 101 description', 101, '201', 60, 'Eugene', '310110196004020311'),
                                              models.Apartment(102, '2号', 'Building 102 description', 102, '202', 80, 'Ernest', '310110196004020312'),
                                              models.Apartment(103, '3号', 'Building 103 description', 103, '203', 90, 'Young', '310110196004020313')])


@app.get('/admin/personnel')
@app.get('/admin/personnel/list')
def admin_personnel_list():
    return bottle.jinja2_template('template/personnel_list.html',
                                  personnels=[models.Personnel(1, 'Eugene', '块长', '块长职责', '居委会', '第一块区（1-11、21、22）', '国和路888弄32号101室'),
                                              models.Personnel(2, 'Ernest', '楼组长', '楼组长职责', '居委会', '第二块区（1-11、21、22）', '国和路888弄32号102室'),
                                              models.Personnel(3, 'Young', '党总支书记', '党总支书记职责', '居委会', '第三块区（1-11、21、22）', '国和路888弄32号103室')])


@app.delete('/admin/user/<userid>')
def admin_user_delete(userid, db):
    sql = 'delete from user where user_id = ' + userid
    db.execute(sql)
    return 'ok'


@app.put('/admin/user/<userid>')
def admin_user_update(userid, db):
    password = bottle.request.forms.password
    email = bottle.request.forms.email
    name = bottle.request.forms.name
    identity_number = bottle.request.forms.identity_number
    card_id = bottle.request.forms.card_id
    user_type_id = bottle.request.forms.user_type_id
    # image = bottle.request.files.get('image')
    # image.save('files')
    vdbm = dbm.DbM(db)
    vdbm.update(table='user', condition=' where user_id=' + userid, password=password, email=email,
                name=name, identity_number=identity_number, card_id=card_id, user_type_id=user_type_id,
                image='default.jpg')


@app.put('/admin/user/role/<user_role_id>')
def admin_user_role_update(user_role_id, db):
    role_id = bottle.request.forms.role_id
    role_description = bottle.request.forms.role_description
    user_role_description = bottle.request.forms.user_role_description
    description_detail = bottle.request.forms.description_detail
    role_type_id = bottle.request.forms.role_type_id

    vdbm = dbm.DbM(db)
    vdbm.update(table='role', condition=' where role_id=' + role_id,  role_type_id=role_type_id, description=role_description)
    vdbm.update(table='user_role', condition=' where user_role_id=' + user_role_id,  role_id=role_id,
                description=user_role_description, description_detail=description_detail)

@app.post('/admin/user/role')
def admin_user_role_add(db):
    vdbm = dbm.DbM(db)
    utf_forms = bottle.request.forms.decode("utf-8")
    vdbm.insert(table='user_role', **utf_forms)


@app.put('/admin/user/livingcard/<livingcard_id>')
def admin_user_livingcard_update(livingcard_id, db):
    vdbm = dbm.DbM(db)
    #数据库字段名参考：livingcard_id, name, address, zip_code, house_number, user_id
    utf_forms = bottle.request.forms.decode("utf-8")
    vdbm.update(table='livingcard', condition=' where livingcard_id=' + livingcard_id,
                form_dict=utf_forms.dict)


@app.post('/admin/user/livingcard')
def admin_user_livingcard_add( db):
    vdbm = dbm.DbM(db)
    # 数据库字段名参考：livingcard_id, name, address, zip_code, house_number, user_id
    utf_forms = bottle.request.forms.decode("utf-8")
    vdbm.insert(table='livingcard', **utf_forms)


@app.put('/admin/user/netcard/<netcard_id>')
def admin_user_netcard_update(netcard_id, db):
    vdbm = dbm.DbM(db)
    #数据库字段名参考：netcard_id, nickname, image, commuity_user_id, user_id
    utf_forms = bottle.request.forms.decode("utf-8")
    vdbm.update(table='netcard', condition=' where netcard_id=' + netcard_id,  form_dict=utf_forms.dict)


@app.post('/admin/user/netcard')
def admin_user_netcard_add(db):
    vdbm = dbm.DbM(db)
    # 数据库字段名参考：netcard_id, nickname, image, commuity_user_id, user_id
    utf_forms = bottle.request.forms.decode("utf-8")
    vdbm.insert(table='netcard', **utf_forms)


@app.put('/admin/user/partycard/<partycard_id>')
def admin_user_partycard_update(partycard_id, db):
     vdbm = dbm.DbM(db)
     # 数据库字段名参考：partycard_id, relation, party_branch, position, type, status, join_date, confirm_date,
     # inspection_person, application_id, user_id
     utf_forms = bottle.request.forms.decode("utf-8")
     vdbm.update(table='partycard', condition=' where partycard_id=' + partycard_id,
                 form_dict=utf_forms.dict)


@app.post('/admin/user/partycard')
def admin_user_partycard_add(db):
     vdbm = dbm.DbM(db)
     # 数据库字段名参考：partycard_id, relation, party_branch, position, type, status, join_date, confirm_date,
     # inspection_person, application_id, user_id
     utf_forms = bottle.request.forms.decode("utf-8")
     vdbm.insert(table='partycard',**utf_forms)


@app.put('/admin/user/citizen/<citizen_id>')
def admin_user_citizencard_update(citizen_id, db):
    vdbm = dbm.DbM(db)
    # 数据库字段名参考：citizen_id, name, identification_type, identification_value, marriage_status,
    # employment_status, residence_category, resident_status, education_status, politics_status,
    # migration_status, income_status, nation, gender, relationship, user_id, apartment_id,
    # age, status, phone
    utf_forms = bottle.request.forms.decode("utf-8")
    vdbm.update(table='citizen_resident', condition=' where citizen_id=' + citizen_id,
                form_dict=utf_forms.dict)


@app.post('/admin/user/citizen')
def admin_user_citizencard_add(db):
    vdbm = dbm.DbM(db)
    # 数据库字段名参考：citizen_id, name, identification_type, identification_value, marriage_status,
    # employment_status, residence_category, resident_status, education_status, politics_status,
    # migration_status, income_status, nation, gender, relationship, user_id, apartment_id,
    # age, status, phone
    utf_forms = bottle.request.forms.decode("utf-8")
    vdbm.insert(table='citizen_resident', **utf_forms)

def add_user(db):
    username = bottle.request.forms.username
    password = bottle.request.forms.password
    email = bottle.request.forms.email
    name = bottle.request.forms.name
    id = bottle.request.forms.identity_number
    card_id = bottle.request.forms.card_number

    convert = lambda x: "'{}'".format(x) if x else 'NULL'

    username, password, email, name, id, card_id = [convert(x) for x in [username, password, email, name, id, card_id]]
    select_user_type = bottle.request.forms.selectUserType
    upload = bottle.request.files.get('upload')
    upload.save('files')
    filename = convert(upload.filename)
    sql = 'insert into user (username, password, user_type_id, email, identity_number, card_id, image) values(' + username +\
          ', ' + password + ',' + select_user_type + "," + email + "," +  id + ',' + card_id + ',' + filename + ')'
    print(sql)
    status = db.execute(sql)


@app.error(404)
def error404(error):
    return bottle.jinja2_template('template/404.html')


@app.error(500)
def error500(error):
    return bottle.jinja2_template('template/500.html')


logging.info('bottle starts to run')

bottle.run(host='localhost', port=1025, debug=True, reloader=True, app=app_middlware)

