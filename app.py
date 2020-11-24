from flask import Flask, url_for, request, redirect
from jinja2 import Template, Environment, FileSystemLoader
import redis
import shortuuid
import os
REDIS_HOST = os.getenv("REDIS_HOST", None)
conn = redis.Redis(host=REDIS_HOST, charset="utf-8", decode_responses=True, port=6379)
File_loader = FileSystemLoader("templates")
env = Environment(loader=File_loader)
app = Flask(__name__)
LISTAURLS = conn.hgetall('tinys')
LISTAVISTAS = conn.hget('tvisitas')
url = ""
key_User = ""

def tocken():
    str_ = shortuuid.ShortUUID().random(length=5)
    return str_

@app.route('/', methods=["GET", "POST"])
def tiny():
    key_User = ""
    url = " "
    if(request.method == 'POST'):
        url = request.form['url']
        key_User = request.form['customAlias']
        print(url)
        print(key_User)
        if(url == ""):
            pass
        else:
            if(key_User == ""):
                key_User = tocken()
                #funcion shortuuid
            i = 0
            for k in LISTAURLS.keys():
                if(LISTAURLS[k] == url):
                    i = 1
                    LISTAURLS[key_User] = LISTAURLS.pop(k)
                    LISTAVISTAS[key_User] = LISTAVISTAS.pop(k)
                    break
            if(i == 0):
                LISTAURLS[key_User] = url
                LISTAVISTAS[key_User] = 0
            conn.delete('tinys')
            conn.delete('tvisitas')
            conn.hmset('tinys', LISTAURLS) 
            conn.hmset('tvisitas', LISTAVISTAS)       
    template = env.get_template('index.html')
    return template.render(key=key_User)

@app.route('/listUrl', methods=["GET", "POST"])
def listUrl():
    botonV = ""
    if(request.method == 'POST'):
        botonV = request.form['delete']
        LISTAURLS.pop(botonV)
        LISTAVISTAS.pop(botonV)
        conn.delete('tinys')
        conn.delete('tvisitas')
        if(len(LISTAURLS) == 0):
            pass
        else:
            conn.hmset('tinys', LISTAURLS)
            conn.hmset('tvisitas', LISTAVISTAS)
    template = env.get_template('listado.html')
    return template.render(my_list=LISTAURLS)

@app.route('/stats')
def stats():
    template = env.get_template('stats.html')
    return template.render(my_list=LISTAURLS, my_list2=LISTAVISTAS)

@app.route('/<keyredict>', methods=["GET", "POST"])
def redireccionar(keyredict=None):
    print(keyredict)
    i=0
    for k in LISTAURLS.keys():
        if(k==keyredict):
            i=1
            break
    if(i == 0):
        template = env.get_template('notfound.html')
        return template.render()
    else:
        cont = LISTAVISTAS[keyredict]
        cont = cont + 1
        LISTAVISTAS[keyredict] = cont
        return redirect(LISTAURLS[keyredict]), 301
       
    

if __name__ == '__main__':
    print(LISTAURLS)
    app.run(host='0.0.0.0', port=5000)