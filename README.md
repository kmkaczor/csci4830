In order to have django installed, you must install it via your Ubuntu linux repository. If it asks for yes/no, say yes.

    sudo apt-get install python3-django

Of course, we need someplace to install OUR django files. Since we are wanting to host it under apache, we will
do so under /var/www/

    cd /var/www
    sudo git clone https://github.com/kmkaczor/csci4830.git
    sudo chown -R www-data:www-data project/
    cd csci4830
    sudo git checkout devel
    sudo git pull

Apache needs to be configured to recognize both django and python as executable files.
In /etc/apache2/sites-enables/000-default.conf, using either vim or nano, please add the following lines ABOVE
the <VirtualHost *:80> directive:

    WSGIScriptAlias / /var/www/project/csci4830/csci4830/wsgi.py
    #WSGIPythonHome /path/to/
    WSGIPythonPath /var/www/project/csci4830

Additionally, add the following lines underneath the WSGI variables to allow apache access to 
where we stored our django files. We are changing the apache root folder from /var/www to /var/www/project.

    <Directory /var/www> 
        Options FollowSymLinks
        AllowOverride None
        Require all denied
    </Directory>

    <Directory /var/www/project>
        Options Indexes FollowSymLinks
        AllowOverride None
        Require all granted
    </Directory>

We need to tell apache how to understand django files. Somewhere BELOW the 
<VirtualHost *:80> directive, but prior to the </VirtualHost> closing tag,
you need to add:

    <Directory /var/www/project>
        <Files wsgi.pyu>
        Require all granted
        </Files>
    </Directory>
    
We need to ensure that there is a /var/www/.csci4830-secretkey file readable by django, as django uses secret key for some security
mechanisms, and we do not want it appearing in github. For the time being let's put something random in there, if we need the same key
later on we can worry about that later.

    sudo head -n 50 /dev/urandom | sudo md5sum - > /var/www/.csci4830-secretkey
    sudo chown www-data:www-data /var/www/.csci4830-secretkey
    sudo chmod 0400 /var/www/.csci4830-secretkey


Apache needs to be restarted in order for it to reread its configuration files

    sudo systemctl restart apache2


Team rm -rf / project members:
<ul>

<li>
* Korey Kaczor
</li>

<li>
* 
</li>

<li>
* 
</li>

<li>
* 
</li>

</ul>
