import traceback
from socketserver import ThreadingMixIn
from xmlrpc.server import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
import threading
import torch
from txt2panoimg import Text2360PanoramaImagePipeline
import time
import re
from random import Random
import os
import pdb

class master_rpc_server(ThreadingMixIn, SimpleXMLRPCServer):
    pass
class RequestHandler(SimpleXMLRPCRequestHandler):
    def log_message(self, format, *args):
        pass

sched_queue = []
master_ip = "10.31.245.154"
master_rpc_port = 4343
model_id = 'models'
txt2panoimg = Text2360PanoramaImagePipeline(model_id, torch_dtype=torch.float16)

class task:
    def __init__(self):
        self.task_id = ""
        self.text = ""
        self.output = ""

def gen_key(randomlength = 8):
    str     = ''
    chars   = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length  = len(chars) - 1
    random  = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str

def create_task(text, output=None, task_id=None):
    try:
        new_task = task()
        new_task.task_id = gen_key()
        new_task.output = f'/mnt/mam_1/SD-T2I/{task_id}.png' if output is None else output
        if not os.path.exists(os.path.dirname(new_task.output)):
            os.makedirs(os.path.dirname(new_task.output))
        new_task.text = text 
        sched_queue.append(new_task)
    except:     
        traceback.print_exc()
        return False
    return True
class process(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        print('start the thread for processing...')
        while True:
            try:   
                if len(sched_queue) > 0:
                    to_be_processed_task = sched_queue.pop(0)
                    to_be_processed_task.output = os.path.splitext(to_be_processed_task.output)[0]+'.png' 
                    input = {'prompt':to_be_processed_task.text, 'upscale':True} 
                    print(f'task:{to_be_processed_task.task_id}\nprompt:{to_be_processed_task.text}')
                    output = txt2panoimg(input)
                    
                    output_file_name = os.path.basename(to_be_processed_task.output)
                    output_dir = os.path.dirname(to_be_processed_task.output)
                    file_name = os.path.splitext(output_file_name)[0]
                    suffix = '.png'
                    number = 1
                    while os.path.exists(to_be_processed_task.output) and os.path.exists(os.path.join(output_dir, f'{file_name}.{number}{suffix}')):
                        number += 1
                    if os.path.exists(to_be_processed_task.output):
                        to_be_processed_task.output = os.path.join(output_dir, f'{file_name}.{number}{suffix}')
                    output.save(to_be_processed_task.output)
            except:
                traceback.print_exc()
            finally:
                time.sleep(5)
             

def main():
    server = master_rpc_server((master_ip, master_rpc_port), requestHandler=RequestHandler, allow_none=True)
    server.register_function(create_task, 'create_task')
    t = process()
    t.start()
    server.serve_forever()
if __name__ == '__main__':
    main()
