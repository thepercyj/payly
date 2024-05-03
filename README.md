# Payly ( Web Apps 2024)
Payly - An Online Payment Service built using Django

## Description
Payly was created as a part of the assignment criteria for the module Web Application and Services. The application primarly focuses on working mechanisms similar to the real world app giants like PayPal and Alipay. The features included are as follows:
- Users can send and request money to each other (i.e., using virtual money and not real money)
- User can view their transaction history
- Admin interface to manage users and transactions
- API for currency conversion with hardcoded rates (i.e., the rates may be subject to change based on real world)

## Installation on Local
Step 1: To install the application, first install IntelliJ or Pycharm or Visual Studio of your liking. you can use the following links provided below to directly access the softwares.

- If you want to install Intellij Ultimate Edition, go to the official Intellij [Website](https://www.jetbrains.com/idea/download/download-thanks.html?platform=windows)
- If you also want to install PyCharm Community Version, go to the official PyCharm [Website](https://www.jetbrains.com/pycharm/download/download-thanks.html?platform=windows&code=PCC)
- If you also want to install Visual Studio, Go to the official VSCode [Website](https://code.visualstudio.com/download)
Download the installer for your operating system (Windows, macOS, or Linux).
Run the installer and follow the installation prompts.

Step 2: Download the project using the git clone command or directly from the GUI. 
```
git clone https://github.com/thepercyj/webapps2024.git
```
Step 3: Open the project in your preffered IDE environment( IntelliJ, Pycharm or Visual Studio)

Step 4: Add a Python Interpreter, the project was built on Python 3.9 so 3.9 or higher is recommended.
Step 5: Since, the production environment is on, you will need to disable it by doing the following
- navigate to settings.py file in webapps2024 directory, inside the settings file do the following
- From this 
  ```
  # SECURITY WARNING: keep the secret key used in production secret!
  # SECRET_KEY = 'django-insecure-&dujvonru9*mw5x6t3$p5-s46xe!)iunddqdxxb!h)+k0ph^(+'
  SECRET_KEY_FILE = os.path.join(BASE_DIR, 'webapps2024/.DJANGO_SECRET_KEY')
  
  with open(SECRET_KEY_FILE) as f:
      SECRET_KEY = f.read().strip()
  
  
  # SECURITY WARNING: don't run with debug turned on in production!
  DEBUG = True
  
  ALLOWED_HOSTS = ['127.0.0.1', 'ec2-34-235-38-137.compute-1.amazonaws.com', '34.235.38.137']
  ```
- To this
  ```
  # SECURITY WARNING: keep the secret key used in production secret!
  SECRET_KEY = 'django-insecure-&dujvonru9*mw5x6t3$p5-s46xe!)iunddqdxxb!h)+k0ph^(+'
  #SECRET_KEY_FILE = os.path.join(BASE_DIR, 'webapps2024/.DJANGO_SECRET_KEY')
  
  # with open(SECRET_KEY_FILE) as f:
  #   SECRET_KEY = f.read().strip()
  
  
  # SECURITY WARNING: don't run with debug turned on in production!
  DEBUG = False
  
  ALLOWED_HOSTS = []
  ```
  This is to ensure that the static files will be served from the current directory and not from your production directory which is generally located outside your Django project folder.

Step 6: Install pip packages from requirements.txt, navigate from your terminal to main folder where requirements.txt is located and then issue the command below:
```
pip install -r requirements.txt
```
Also start the thrift server in background as we will need timestamps for our transactions ( this is one time operation as it will be running until you power off your instance. )
```
python thrift.py &
```
Step 7: Now run the server with either of the following commands, make sure you are issuing this command from the directory where manage.py is located.
-  without SSL
   ```
   python manage.py runserver
   ```
- with SSL ( password for PEM files is "webapps" )
  ```
  python manage.py runserver_plus --cert-file webapps.crt ---key-file webapps.key
  ```
Step 8: In your browser, navigate to the followings
-  without SSL
   ```
   http://127.0.0.1:8000
   ```
- with SSL ( password for PEM files is "webapps" )
  ```
  https://127.0.0.1:8000
  ```
## Installation in Cloud (AWS, Oracle, Digital Ocean etc.)
### USING RUNSERVER_PLUS
( I am assuming that you have opened your http, https, ssh port on your public IP and have managed those settings in your security group.)

Step 1: SSH to your instance from your favourite cloud provider
Step 2: Run updates and upgrades of your linux 
```
apt update && apt upgrade -y
```
Step 3: Make sure you have git installed, if not you can install using the below commands
```
apt install git -y
```
Step 4: Check if you have python venv, development tools installed or not, if not you can install using below command. I am assuming you have python version higher than 3.9 installed.
```
apt install python3-venv python3-dev -y
```
Step 5: In your home directory, clone the repo.
```
git clone https://github.com/thepercyj/webapps2024.git
```
Step 6: Change directory to the cloned folder
```
cd webapps2024
```
Step 7: Crete a new virtual environment.
```
python3 -m venv venv
```
Step 8: Activate the virtual environment.
```
source venv/bin/activate
```
Step 9: Install python requirements
```
pip install requirements.txt
```
Step 10: Since, the production environment is on, you will need to disable it by doing the following
- Navigate to settings.py file in webapps2024 directory, inside the settings file do the following
- From this 
  ```
  # SECURITY WARNING: keep the secret key used in production secret!
  # SECRET_KEY = 'django-insecure-&dujvonru9*mw5x6t3$p5-s46xe!)iunddqdxxb!h)+k0ph^(+'
  SECRET_KEY_FILE = os.path.join(BASE_DIR, 'webapps2024/.DJANGO_SECRET_KEY')
  
  with open(SECRET_KEY_FILE) as f:
      SECRET_KEY = f.read().strip()
  
  
  # SECURITY WARNING: don't run with debug turned on in production!
  DEBUG = True
  
  ALLOWED_HOSTS = ['127.0.0.1', 'ec2-34-235-38-137.compute-1.amazonaws.com', '34.235.38.137']
  ```
- To this
  ```
  # SECURITY WARNING: keep the secret key used in production secret!
  SECRET_KEY = 'django-insecure-&dujvonru9*mw5x6t3$p5-s46xe!)iunddqdxxb!h)+k0ph^(+'
  #SECRET_KEY_FILE = os.path.join(BASE_DIR, 'webapps2024/.DJANGO_SECRET_KEY')
  
  # with open(SECRET_KEY_FILE) as f:
  #   SECRET_KEY = f.read().strip()
  
  
  # SECURITY WARNING: don't run with debug turned on in production!
  DEBUG = False
  
  ALLOWED_HOSTS = []
  ```
  This is to ensure that the static files will be served from the current directory and not from your production directory which is generally located outside your Django project folder.

  Also start the thrift server in background as we will need timestamps for our transactions ( this is one time operation as it will be running until you power off your instance. )
  ```
  python thrift.py &
  ```
Step 11: Now run the server with either of the following commands, make sure you are issuing this command from the directory where manage.py is located.
-  without SSL
   ```
   python manage.py runserver 0.0.0.0:80
   ```
- with SSL ( password for PEM files is "webapps" )
  ```
  python manage.py runserver_plus --cert-file webapps.crt ---key-file webapps.key 0.0.0.0:443
  ```
Step 12: In your browser, navigate to the followings
-  without SSL
   ```
   http://<your-public-ip-or-dns-name-of-instance>
   ```
- with SSL ( password for PEM files is "webapps" )
  ```
  https://<your-public-ip-or-dns-name-of-instance>
  ```
### USING DJANGO PRODUCTION SETTINGS WITH NGINX AND GUNICORN
If you are feeling motivated then, you can deploy it as a production server with some tweaking in the Django project.

Step 1: In you same cloud instance, install nginx
```
apt install nginx
```
Step 2: Navigate to your Django project directory, activate the virtual environment and install gunicorn
```
pip install gunicorn
```
also start the thrift server in background as we will need timestamps for our transactions ( this is one time operation as it will be running until you power off your instance. )
```
python thrift.py &
```
Step 3: Create the following file and add the following details
create a new file name gunicorn.service and gunicorn.socket

gunicorn.service
```
vi /etc/systemd/system/gunicorn.service
```
Paste the following contents below and save the file
```
[Unit]
Description=gunicorn daemon for webapps2024
Requires=gunicorn.socket
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/webapps2024/
ExecStart=/home/ubuntu/webapps2024/venv/bin/gunicorn \
          --workers=3 \
          --bind unix:/run/gunicorn.sock \
          --log-level=error \
          --access-logfile=/home/ubuntu/webapps2024/deployment/gunicorn_access.log \
          --error-logfile=/home/ubuntu/webapps2024/deployment/gunicorn_error.log \
          webapps2024.wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID

[Install]
WantedBy=multi-user.target
```
gunicorn.socket
```
vi /etc/systemd/system/gunicorn.socket
```
Paste the following contents below and save the file
```
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
```
Step 4: Copy your ssl key and certificate to /etc/ssl/ directory
```
mkdir -p /etc/ssl/webapps2024/
```
From your project directory, copy the ssl files 
```
cp webapps.key /etc/ssl/webapps2024/
cp webapps.crt /etc/ssl/webapps2024/
```
### NOTE: It is to be noted that the ssl key pem password were removed because of asking for keys everytime to validate CA certificate. Hence, do this work around to remove the pass from the key.
```
openssl rsa -in /etc/ssl/webapps2024/webapps2024.key -out /etc/ssl/webapps2024/webapps2024_no_pass.key
```
Step 5: add nginx site file for webapps2024 in /etc/nginx/sites-available/
Create file webapps
```
vi /etc/nginx/sites-available/webapps
```
Paste the following content and adjust server names as according to your instance.
```
server {
    listen 80;
    server_name <your-instance-public-ip-or-dns-name>;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name <your-instance-public-ip-or-dns-name>;

    ssl_certificate /etc/ssl/webapps2024/webapps2024.crt;
    ssl_certificate_key /etc/ssl/webapps2024/webapps2024_no_pass.key;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static {
        autoindex on;
        alias /var/www/webapps2024/static/;
    }

    location /media {
        alias /var/www/webapps2024/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}

```
Step 6: Unlink default page and link webapps 
```
sudo unlink /etc/nginx/sites-enabled/default
sudo ln -s /etc/nginx/sites-available/webapps2024 /etc/nginx/sites-enabled 
```
Step 7: verify nginx configuration
```
nginx -t
```
Step 8: Collect static files in /var/www/webapps2024 directory.
```
mkdir -p /var/www/webapps2024/static/
```
From your django project directory copy media files to the newly created directory.
```
cp -r media/ /var/www/webapps2024/
```
From your django project directory, collectstatic using manage.py ( it is to be noted that the STATIC_ROOT has already been configured to serve from the designated directory)
```
python manage.py collectstatic

```
Provide necessary permissions to your project folder and static files ( i am using ubuntu so my home folder is ubuntu and username is ubuntu, this might be different depending on your linux distro )
```
chown -R ubuntu:www-data /home/ubuntu/webapps2024/
chmod 755 -R /home/ubuntu/webapps2024/
chown -R ubuntu:www-data /var/www/webapps2024/
chmod 755 -R /var/www/webapps2024/
```

Step 9: Start the server, enable the server at startup and check the server status if its running or not.
```
systemctl restart gunicorn
systemctl enable gunicorn
systemctl status gunicorn
systemctl restart nginx
systemctl enable nginx
systemctl status nginx
```
Step 10: Browse your ip to check if the project has been deployed or not. 
```
https://<your-public-ip-or-dns-name-of-instance>
```
Cngratulations !! You Did It. !!! Enjoy using the application.
