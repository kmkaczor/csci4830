NEW INSTRUCTIONS:

Turns out python's own package manager has an updated version of django. This makes life easy on us as we don't have to only use outdated documentation:

    $ sudo pip3 install Django pymysql

Don't forget to read: https://docs.djangoproject.com/en/3.2/intro/tutorial01/

Of course, we need someplace to install OUR django files. Since we are wanting to host it under apache, we will
do so under /var/www/

    cd /var/www
    sudo git clone https://github.com/kmkaczor/csci4830.git
    sudo chown -R www-data:www-data csci4830/
    cd csci4830
    sudo git checkout devel
    
    sudo head -n 50 /dev/urandom | sudo md5sum - | sudo tee /var/www/.csci4830-secretkey
    sudo chown www-data:www-data /var/www/.csci4830-secretkey
    sudo chmod 0400 /var/www/.csci4830-secretkey

Apache needs to be configured to recognize both django and python as executable files.
In /etc/apache2/sites-enabled/000-default.conf, using either vim or nano, please add the following lines ABOVE
the <VirtualHost *:80> directive:

    WSGIScriptAlias / /var/www/csci4830/csci4830/csci4830/wsgi.py
    #WSGIPythonHome /path/to/
    WSGIPythonPath /var/www/csci4830/csci4830

    <Directory /var/www/csci4830/csci4830>
        <Files wsgi.py>
        Require all granted
        </Files>
    </Directory>
    
    <Files /var/www/.csci4830-secretkey>
        Deny from all
    </Files>

Apache needs to be restarted in order for it to reread its configuration files

    sudo systemctl restart apache2

==========

This is optional. If you want to have a local testing database, do the following. Otherwise, the program is set to use my Mysql instance for project testing.

We need to create a user and database for the project. The project is set to use the below parameters:

    $ sudo mysql -u root -e "CREATE DATABASE CSCI4830project;"
    $ sudo mysql -u root -e "CREATE USER 'CSCI4830'@'%' IDENTIFIED BY 'CSCI4830Django';"
    $ sudo mysql -u root -e "GRANT ALL PRIVILEGES ON CSCI4830project.* TO 'CSCI4830'@'%';"
