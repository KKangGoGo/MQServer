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


# 전달 받은 요청을 하나씩 celery에 전송(Queue)
@app.route('/request/detect', methods=['POST'])
def request_detect_server():
    data = request.json
    task = celery.send_task('tasks.detect', args=[data], kwargs={})
    if task == 'Connection Exception':
        return jsonify('Connection Exception', 500)
    return str(task.id)


@app.route('/health_check')
def health_check() -> Response:
    return jsonify("OK")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
