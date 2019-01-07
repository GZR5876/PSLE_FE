from flask import Flask,request,jsonify,make_response,render_template,session,redirect
from secrets import token_hex

import datetime
import function
app = Flask(__name__)
app.secret_key = token_hex(24)


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return "basic server load success"

@app.route('/demo')
def demo():
    clientID = request.cookies.get('username')
    if clientID is None:
        resp = make_response(render_template('index.html'))
        resp.set_cookie('username', token_hex(16), expires=datetime.datetime.now() + datetime.timedelta(days=30))
    else:
        resp = make_response(render_template('index.html'))
    session['clientID'] = clientID
    session.permanent = False
    return resp

@app.route('/demo_result')
def demo_result():
    sessionID = token_hex(12)
    math = request.args.get('math', default='*', type=float)
    science = request.args.get('science', default='*', type=float)
    english = request.args.get('english', default='*', type=float)
    MT = request.args.get('MT', default='*', type=float)
    pc = request.args.get('pc', default='*', type=str)
    email = request.args.get('email', default='*', type=str)
    school = request.args.get('school', default='*', type=str)
    grade = request.args.get('grade', default='*', type=str)
    gender = request.args.get('gender', default='*', type=str)
    term = request.args.get('term', default='*', type=str)
    DB_status = function.get_status()
    clientID = session.get('clientID', None)
    user_status = function.input_user(pc,email,school,grade,sessionID,clientID,gender)
    user_score=function.input_score(math,science,english,grade,sessionID,MT,term)
    Tscore=function.cal_T(sessionID)
    session['user_status'] = user_status
    session['user_score'] = user_score
    session['DB_status'] = DB_status
    session['T_Score'] = Tscore

    return redirect("/demo_display", code=302)

@app.route('/demo_display')
def demo_display():
    string ="""
    Run with below result: <br>
    1) DB Status: """ + str(session['DB_status'])+ """ <br>
    2) Create User Status: """+ session['user_status']+ """ <br>
    3) Upload Score Status: """+ session['user_score']+ """ <br>
    4) T Score Status: """+ session['T_Score']+ """ <br><br><br>
    
    Demo Complete!
    
"""
    return string

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'STATUS': 'Not found'}), 404)

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/shutdown', methods=['GET'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]
