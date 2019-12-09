#!/bin/bash

# deployment variables
PYTHON_VERSION='3.7'
PROJECT_NAME='unicauca_vrcb'
BASE_PATH=`pwd`
DUMP_FILE='dump-vrcb_db.sql'
STATIC_PATH='static' # static for dev stage
# MEDIA_URL='' # no media folder needed. S3 bucket setting up in settings.py
# MEDIA_PATH='media' # no me dia folder needed. S3 bucket setting up in settings.py
APP_PORT=6677
DOMAINS='' # add domain/subdomain and IP
MAX_UPLOAD='10M'
PROXY_PASS='http://unix:'$BASE_PATH'/'$PROJECT_NAME'.sock' # change only if you want to deploy over another binding proxy type like http
GUNICORN_SERVICE_USER=$USER # change if you deploy over another user account

# install the environment
sudo apt-get update
sudo apt-get --yes install python$PYTHON_VERSION python$PYTHON_VERSION-distutils nginx software-properties-common
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
sudo python$PYTHON_VERSION get-pip.py
rm get-pip.py
sudo pip install -U pip
sudo pip install pipenv

# setting up the project
pipenv install
pipenv run python manage.py migrate
pipenv run python manage.py loaddata $DUMP_FILE # populate data
pipenv run python manage.py createsuperuser
mkdir $STATIC_PATH
echo 'STATIC_ROOT=os.path.join(BASE_DIR, "'$STATIC_PATH'/")' >> $PROJECT_NAME/settings.py # static for dev stage
cat >> $PROJECT_NAME/settings.py <<- EOM
ALLOWED_HOSTS += [
    'localhost',
    '127.0.0.1',
EOM
for i in $DOMAINS; do
    echo "    '"$i"'," >> $PROJECT_NAME/settings.py
done
echo ']' >> $PROJECT_NAME/settings.py
pipenv run python manage.py collectstatic # only for dev stage
VENV_PATH=`pipenv --venv`

# setting up gunicorn (wsgi server)
cat > gunicorn.service <<- EOM
[Unit]
Description=gunicorn service for $PROJECT_NAME
After=network.target

[Service]
User=$GUNICORN_SERVICE_USER
Group=www-data
WorkingDirectory=$BASE_PATH
ExecStart=$VENV_PATH/bin/gunicorn --access-logfile - --workers 3 --bind unix:$BASE_PATH/$PROJECT_NAME.sock $PROJECT_NAME.wsgi:application

[Install]
WantedBy=multi-user.target
EOM
sudo mv ./gunicorn.service /etc/systemd/system/gunicorn.service
sudo systemctl enable gunicorn
sudo systemctl start gunicorn

# setting up nginx (http server)
cat > $PROJECT_NAME.conf <<- EOM
server {
    listen $APP_PORT;
    listen [::]:$APP_PORT;
    server_name localhost 127.0.0.1 $DOMAINS;
    charset     utf-8;
    client_max_body_size $MAX_UPLOAD;
    server_tokens off;

    location /favicon.ico {access_log off;log_not_found off;}

    location /$MEDIA_URL  {
        alias $BASE_PATH/$MEDIA_PATH; # no me dia folder needed. S3 bucket setting up in settings.py
   6677
    FRONTEND_PORT=80
    DASHBOARD_PORT=8080

    location /static {
        alias $BASE_PATH/$STATIC_PATH;
    }

    location / {
        include proxy_params;
        proxy_pass $PROXY_PASS;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    }
}
EOM
sudo mv ./$PROJECT_NAME.conf /etc/nginx/sites-enabled/
sudo systemctl restart nginx

# install and setting up the SSL certificate
# sudo add-apt-repository universe
# sudo add-apt-repository --yes ppa:certbot/certbot
# sudo apt-get update
# sudo apt-get --yes install python-certbot-nginx
# sudo certbot --nginx
# sudo certbot renew --dry-run

# setting up the firewall
# sudo ufw allow 'OpenSSH'
# sudo ufw allow 'Nginx Full'
# sudo ufw enable

echo "DONE!"

# useful commands
# sudo systemctl status gunicorn # get the gunicorn service status
# sudo journalctl -u gunicorn # get the gunicorn service log
# sudo journalctl -u nginx # get the nginx service log
# sudo nginx -t # test the nginx configuration for syntax errors
# sudo tail -F /var/log/nginx/error.log # show the nginx error log
# sudo tail -F /var/log/nginx/access.log # show the nginx error log
# sudo systemctl daemon-reload && sudo systemctl restart gunicorn # reload the daemon and restart gunicorn if you change
# curl --unix-socket [$PROJECT_NAME].sock http
