source ../bin/activate
export PYTHONPATH=$(pwd)
gunicorn --paste etc/mblog/mblog.ini --config etc/mblog/gunicorn.conf.py
