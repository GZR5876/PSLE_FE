import requests
from flask import request
from secrets import token_hex
import json

key='gYdK$q12@as'
def get_status():
    r = requests.get("https://helloword-221206.appspot.com/status")
    status = r.content.decode("utf-8")
    if 'DB Connection Successful' in status:
        return 'OK'
    else:
        return False

def input_user(pc,email,school,grade,sessionID,clientID,gender):
    data = { \
        'clientID': clientID, 'ip': '0.0.0.0', 'email': email, 'school': school, \
        'postal': pc, 'gender': gender, 'grade': grade, 'key': key, 'sessionId': sessionID}
    data =json.dumps(data)
    r = requests.post("https://helloword-221206.appspot.com/create_user", data)
    status = r.content.decode("utf-8")
    if 'OK' in status:
        return 'OK'
    else:
        return r.content.decode("utf-8")

def input_score(math,science,english,grade,sessionID,MT,term):
    data = { \
        'math_score': math, 'science_score': science, 'eng_score': english, 'mt_score': MT, \
        'score_type': term, 'grade': grade, 'key': key, 'sessionId': sessionID, 'scoresetId':'1'}
    data =json.dumps(data)
    r = requests.post("https://helloword-221206.appspot.com/create_score", data)
    status = r.content.decode("utf-8")
    if 'OK' in status:
        return 'OK'
    else:
        return r.content.decode("utf-8")

def cal_T(sessionID):
    data = {'sessionId': sessionID,'key':key}
    data =json.dumps(data)
    print(data)
    r = requests.post("https://helloword-221206.appspot.com/T_score", data)
    status = r.content.decode("utf-8")

    if 'OK' in status:
        t = json.loads(status)
        str ='OK; Estimated T Score is: {:.2f}; with STDEV: {:.2f}'.format(t['T_SCORE'],t['T_SCORE_STDEV'])
        return str
    else:
        return r.content.decode("utf-8")