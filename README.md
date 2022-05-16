This was a class project to create a web application using a high-level framework. Unfortunately, my team had agreed to use Python and then they realized that not only did they not know how to program in Python, they were incapable of learning it. So, unfortunately, the code is not ideal as I had to carry a 4-man project by myself. Please excuse any sloppiness if you have any interest in this simple application.

==========================
====AWS: Instructions:====
==========================

Turns out python's own package manager has an updated version of django. This makes life easy on us as we don't have to only use outdated documentation:

Say yes to any questions it asks.

    $ sudo pip3 install Django pymysql pillow mysqlconnector
    $ sudo apt install libapache2-mod-wsgi-py3


Don't forget to read: https://docs.djangoproject.com/en/3.2/intro/tutorial01/

Of course, we need someplace to install OUR django files. Since we are wanting to host it under apache, we will
do so under /var/www/

    cd /var/www
    sudo git clone https://github.com/kmkaczor/csci4830.git
    sudo chown -R www-data:www-data csci4830/
    cd csci4830
    sudo git checkout devel
    
    sudo bash -c "echo THISISTHEKEY > /var/www/.csci4830-secretkey"
    sudo chown www-data:www-data /var/www/.csci4830-secretkey
    sudo chmod 0400 /var/www/.csci4830-secretkey

Apache needs to be configured to recognize both django and python as executable files. Additionally, we need to allow apache to allow users access to /static/ and /files/. 
In /etc/apache2/sites-enabled/000-default.conf, using either vim or nano, please add the following lines ABOVE
the <VirtualHost *:80> directive:

    WSGIScriptAlias / /var/www/csci4830/csci4830/csci4830/wsgi.py
    #WSGIPythonHome /path/to/
    WSGIPythonPath /var/www/csci4830/csci4830

    Alias /files/ /var/www/csci4830/csci4830/files/
    Alias /static/ /var/www/csci4830/csci4830/static/

    <Directory /var/www/csci4830/csci4830/static>
        Options Indexes FollowSymLinks
        Require all granted
        AllowOverride None
    </Directory>

    <Directory /var/www/csci4830/csci4830/files>
        Options Indexes FollowSymLinks
        Require all granted
        AllowOverride None
    </Directory>

    <Directory /var/www/csci4830/csci4830>
        <Files wsgi.py>
        Require all granted
        </Files>
    </Directory>

Apache needs to be restarted in order for it to reread its configuration files

    sudo systemctl restart apache2

==========

Don't forget that you can use your local computer as a development environment. In command line, 

    $ python3 manage.py runserver

will start up a temporary local HTTP server that you can connect to locally, just like with Tomcat. It will be much more efficient than constantly pushing
via git and then pulling. It will use my AWS database by default, so you won't have to worry about that.


==========================
====Home: Instructions:====
==========================
If any of these commands fail, you will need to run as administrator. Find "Powershell" for windows in windows search, right click on it and "Run as Adminstrator"

Install python for windows: go into powershell or windows command line and type "python3". The windows store will open and will ask to install python 3.9. Do so.

Once it is installed:

    py -m pip install Django pymysql pillow mysqlconnector

Now, we need to clone the git repository to your hard drive: $DIRECTORY here means whatever directory you plan to install to your hard drive:

    cd $DIRECTORY
    git clone https://github.com/kmkaczor/csci4830.git
    cd csci4830
    git checkout devel
    
Create a text file with the contents "THISISTHEKEY" in whatever is the home folder for your user and name it .csci4830-secretkey

If you run "python3 manage.py runserver" (in the csci4830/csci4830/ directory) it will complain about a non-existent key (or something). Use the directory it tells you. 

Also ensure you have your github auth token or login information set accordingly. In windows powershell (NOT as admin!)

    git config --global user.email "EMAIL"
    git config --global user.name "NAME"

... with appropriate changes. Now when you attempt to push to the repository with visual studio code it will prompt for a login in your browser, which will allow you to push and pull without having to ever worry about git ever again.

==========================
====Optional====
==========================

This is optional. If you want to have a local testing database, do the following. Otherwise, the program is set to use my Mysql instance for project testing.

We need to create a user and database for the project. The project is set to use the below parameters:

    $ sudo mysql -u root -e "CREATE DATABASE CSCI4830project;"
    $ sudo mysql -u root -e "CREATE USER 'CSCI4830'@'%' IDENTIFIED BY 'CSCI4830Django';"
    $ sudo mysql -u root -e "GRANT ALL PRIVILEGES ON CSCI4830project.* TO 'CSCI4830'@'%';"
