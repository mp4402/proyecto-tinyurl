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
@app.route('/tiny', methods=["GET", "POST"])
def tiny():
    if(request.method == 'POST'):
        url = request.form['']
        key_User = request.form['']
        if(url == ""):
            pass #alerta
        else:
            if(key_User == ""):
                pass #funcion shortuuid
            else:
                pass #funcion nuestra
    template = env.get_template('')
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