git config --global user.name 'boo'
git config --global user.email 'boo@boo.boo'

rm /etc/nginx.conf
ln -sf /home/box/web/etc/nginx.conf /etc/nginx/nginx.conf
ln -sf /home/box/web/etc/hello.py /etc/gunicorn.d/hello.py

sudo /etc/init.d/nginx restart

cd /home/box/web
sudo gunicorn -c etc/hello.py hello:app

