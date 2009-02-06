ufw2web is a web interface for ubuntu-firewall (ufw). Right now, the only 
option for ufw2web, is to enable or disable the firewall. 

Configuration of ufw it self, must be done via the approriate commands
on the command line. See https://wiki.ubuntu.com/UbuntuFirewall and 'man ufw'
for more details.

SYSTEM REQUIREMENTS
- Ubuntu Linux: Hardy 8.04 (server or desktop) or higher
  - on these systems, ufw is installed by default

INSTALLATION
- install CherryPy3 and ConfigObj:
  sudo apt-get install python-cherrypy3 python-configobj
- copy files of ufw2web to a local location, preferable: /usr/local/bin/ufw2web
- test: start webserver with sudo (root) privileges
  (sudo) python ufw2web.py
  - exit: Ctrl-C
- autostart on system boot via /etc/rc.local:
  - add the following line in /etc/rc.local (just before 'exit 0'):
    python <location of ufw2web files>/ufw2web.py

CONFIGURATION
- defaults:
  - WebServerPort: 80
  - UseAuthentication: 0 (off)
  - LoginUser/LoginPassword: admin/admin
    - not used when UseAuthentication is off
- change defaults:
  - uncomment keys in config/ufw2web.conf and place the desired values

TRANSLATIONS
- by default, language is English
- all strings can be translated by ufw2web-translations.conf
  - placed in config/
- provided are two files: 
  - ufw2web-translations-nl.conf (out-of-the-box Dutch translation)
  - ufw2web-translations-template.conf (base file for any other language)
- just rename one of them to ufw2web-translations.conf and restart the server

