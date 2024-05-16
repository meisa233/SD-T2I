from flask import Flask, request
from gevent import pywsgi
from xmlrpc.client import ServerProxy 

app = Flask(__name__)
master_ip = "10.31.245.154"
master_rpc_port = 4343
rpc_addr = f'http://{master_ip}:{master_rpc_port}'
server = ServerProxy(rpc_addr, allow_none=True)

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        text = request.form.get('text', type=str)
        output = request.form.get('output', type=str)
        if text is None:
            return {'code':501, 'msg':'can\'t get "text" value'}
        if output is None:
            return {'code':502, 'msg':'can\'t get "output" value'}
        code = server.create_task(text.strip(), output.strip())
        if code:
            return {'code':200}
        return {'code':500, 'msg':'failed to create a task'} 

if __name__ == '__main__':
    server = pywsgi.WSGIServer(('0.0.0.0',5001), app) 
    server.serve_forever()
