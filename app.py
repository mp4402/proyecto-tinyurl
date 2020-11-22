from flask import Flask, url_for, request, redirect
from jinja2 import Template, Environment, FileSystemLoader
import redis
import shortuuid
conn = redis.Redis('localhost')
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
    if(request.method == 'POST'):
        url = request.form['url']
        key_User = request.form['customAlias']
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
                
    template = env.get_template('index.html')
    return template.render()

    pass
@app.route('/listUrl', methods=["GET", "POST"])
def listUrl():
    pass
@app.route('/stats', methods=["GET", "POST"])
def stats():
    pass
if __name__ == '__main__':
    print(LISTAURLS)
    app.run(host='0.0.0.0', port=5000)