from flask import Flask, url_for, request, redirect
from jinja2 import Template, Environment, FileSystemLoader
import redis
import shortuuid
conn = redis.Redis('localhost', charset="utf-8", decode_responses=True)
File_loader = FileSystemLoader("templates")
env = Environment(loader=File_loader)
app = Flask(__name__)
LISTAURLS = conn.hgetall('tinys')
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
                    break
            if(i == 0):
                LISTAURLS[key_User] = url
            conn.delete('tinys')
            conn.hmset('tinys', LISTAURLS)        
    template = env.get_template('index.html')
    return template.render(key=key_User)
@app.route('/listUrl', methods=["GET", "POST"])
def listUrl():
    template = env.get_template('listado.html')
    return template.render(my_list=LISTAURLS)
@app.route('/stats', methods=["GET", "POST"])
def stats():
    pass
if __name__ == '__main__':
    print(LISTAURLS)
    app.run(host='0.0.0.0', port=5000)