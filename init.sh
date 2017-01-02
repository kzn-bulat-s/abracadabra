git config --global user.name 'boo'
git config --global user.email 'boo@boo.boo'

cd /home/box/web
gunicorn -b 0.0.0.0:8080 hello:app &
cd ask
gunicorn -b 0.0.0.0:8000 ask.wsgi &

rm /etc/nginx/nginx.conf
ln -sf /home/box/web/etc/nginx.conf /etc/nginx/nginx.conf
ln -sf /home/box/web/etc/hello.py /etc/gunicorn.d/hello.py

/etc/init.d/nginx restart

