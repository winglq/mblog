source ../bin/activate
export PYTHONPATH=$(pwd)
mkdir /var/log/mblog
gunicorn --paste etc/mblog/mblog.ini --config etc/mblog/gunicorn.conf.py --access-logfile /var/log/mblog/access.log
