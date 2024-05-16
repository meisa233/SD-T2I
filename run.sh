cd /home/nvidia/SD-T2I/ &&
nohup /home/nvidia/SD-T2I-360PanoImage/venv/bin/gunicorn --workers=4 --timeout 1000 flask_:app -b 0.0.0.0:5001 > gunicorn.log 2>&1 & 
nohup /home/nvidia/SD-T2I-360PanoImage/venv/bin/python -u master.py > master.log 2>&1 &
