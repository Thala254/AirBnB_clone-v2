#!/usr/bin/env bash
<<<<<<< HEAD
# script that sets up my web server for deployment of web_static
apt-get -y update
apt-get -y upgrade
apt-get -y install nginx
mkdir -p /data/web_static/releases/test /data/web_static/shared
echo "<html><head></head><body>Holberton School</body></html>" | sudo tee /data/web_static/releases/test/index.html
ln -sf /data/web_static/releases/test/ /data/web_static/current
chown -Rh ubuntu:ubuntu /data/
sed -i "s/server_name _;/server_name _;\n\n\tlocation \/hbnb_static\/ {\n\t\talias \/data\/web_static\/current\/;\n\t}\n/" /etc/nginx/sites-available/default
service nginx restart
=======
# sets up your web servers for the deployment of web_static
apt-get -y update
apt-get -y install nginx
ufw allow 'Nginx HTTP'
mkdir -p /data/web_static/
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" > /data/web_static/releases/test/index.html
ln -sf /data/web_static/releases/test /data/web_static/current
chown -R ubuntu:ubuntu /data
sed -i '/listen 80 default_server/a location /hbnb_static/ { alias /data/web_static/current/;}' /etc/nginx/sites-available/default
service nginx restart
exit 0
>>>>>>> 40452a7a1310c043bdcf8ac5d260b0c504ebe1f6
