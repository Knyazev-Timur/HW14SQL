from flask import Flask, send_from_directory
from api.api import api_blueprint

POST_PATH = 'data/posts.json'
UPLOAD_FOLDER = 'uploads/images'

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

app.register_blueprint(api_blueprint)

@app.route('/uploades/<path:path>')
def static_dir(path):
    return send_from_directory('uploades', path)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
