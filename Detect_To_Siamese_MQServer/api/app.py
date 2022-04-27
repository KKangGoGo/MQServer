import celery.states as states
import base64

from flask import Flask, Response, request
from flask import url_for, jsonify
from worker import celery

dev_mode = True
app = Flask(__name__)


@app.route('/check/<string:task_id>')
def check_task(task_id: str) -> str:
    res = celery.AsyncResult(task_id)
    if res.state == states.PENDING:
        return res.state
    else:
        return str(res.result)


@app.route('/request/siamese', methods=['POST'])
def request_siamese_server():
    img_byte = request.files['file_url'].read()
    data = {
        'img_byte': base64.b64encode(img_byte)
    }
    task = celery.send_task('tasks.siamese', args=[data], kwargs={})
    if task == 'Connection Exception':
        return jsonify('Connection Exception', 500)
    return str(task.id)


@app.route('/health_check')
def health_check() -> Response:
    return jsonify("OK")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
