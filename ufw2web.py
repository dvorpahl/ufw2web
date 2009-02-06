#!/usr/bin/python
#
#  uwf2web: Web interface for UFW (Ubuntu FireWall)
#
#  Usage: (sudo) python uwf2web
#
#    Copyright (C) 2009 Mark Baaijens <mark.baaijens@gmail.com>
#
#    This file is part of uwf2web.
#
#    uwf2web is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    uwf2web is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
import cherrypy  # From package python-cherrypy
import subprocess
from string import *
import os.path
import os
from configobj import ConfigObj # From package python-configobj

# UFW status codes
usUnknown = -1 
usDisabled = 0  
usEnabled = 1  

# Static page segments
_header = '''<html>
  <head>
    <title>Web interface for Ubuntu Firewall (UFW)</title>
    <link rel="icon" type="image/png" href="images/icon.png">
  </head>
  <body>
  <div class="container">'''

_footer = '''
  </div>
  </body>
</html>'''

# Some constants
ConfigFolder = os.path.dirname( os.path.realpath( __file__ )) + '/config'
Version = '0.3'

class Start:
  def index(self):
    text = _header
    ufwStatus = self.uwfStatus()
    if ufwStatus == usDisabled:
      text = text + '''
          <img src="images/disabled.png" align="left">
          <h2>%s</h2>
          <p>
          <form action="enablefirewall" method="GET">
          %s<p>
          <input type="submit" value="%s"/>
          </form>''' % (strFirewallStatusDisabled, strSystemUnprotected, strEnableFirewall)

    elif ufwStatus == usEnabled:
      text = text + '''
          <img src="images/enabled.png" align="left">
          <h2>%s</h2>
          <p>
          <form action="disablefirewall" method="GET">
          %s<p>
          <input type="submit" value="%s"/>
          </form>''' % (strFirewallStatusEnabled, strSystemProtected, strDisableFirewall)

    elif ufwStatus == usUnknown:
      text = text + '''
          <img src="images/unknown.png" align="left">
          <h2>%s</h2>
          <p>
          %s
          <p>''' % (strFirewallStatusUnknown, strIsSudoPrivileges)

    text = text + _footer
    return text
  index.exposed = True

  def enablefirewall(self):
    process = subprocess.Popen(["ufw","enable"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Page will be redirected after a timeout to the main page
    text = '''
        <html>
        <head>
        <meta http-equiv="refresh" content="2; url=./">
        </head>
        <body>%s</body>
        <html>''' % strFirewallIsEnabled
    return text
  enablefirewall.exposed = True  

  def disablefirewall(self):
    process = subprocess.Popen(["ufw","disable"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Page will be redirected after a timeout to the main page
    text = '''
        <html>
        <head>
        <meta http-equiv="refresh" content="2; url=./">
        </head>
        <body>%s</body>
        <html>''' % strFirewallIsDisabled
    return text
  disablefirewall.exposed = True  

  def uwfStatus(self):
    process = subprocess.Popen(["ufw","status"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = process.communicate()[0]

    # Apparently, 'ufw status' is trailed by an invisible character, so it is impossible
    # to do a direct string comparison with '=='; that's why only the 'in' operator is 
    # working here
    if 'not loaded' in output:
      result = 0
    elif 'loaded' in output: # Just to make sure there *is* some output
      result = 1
    else:
      # Probably no sudo privileges: these are essential, even for 'ufw status'
      result = -1  
    return result

# Output to console
print 'ufw2web version %s' % Version
print '- Copyright (C) 2009 Mark Baaijens'
print '- License GNU GPL version 3 or later'

#
# Translations
#

# Translation strings (default)
strFirewallStatusDisabled = 'Firewall (UFW) is disabled.'
strFirewallStatusEnabled = 'Firewall (UFW) is enabled.'
strFirewallStatusUnknown = 'Firewall (UFW) status is unknown.'
strFirewallIsDisabled = 'Firewall (UFW) is deactivated.'
strFirewallIsEnabled = 'Firewall (UFW) is activated.'
strSystemUnprotected = 'The system is unprotected.'
strSystemProtected = 'The system is protected.'
strEnableFirewall = 'Enable firewall'
strDisableFirewall = 'Disable firewall'
strIsSudoPrivileges = 'Is ufw2web.py running with sudo privileges?'

# Translations can be done externally, by the file ufw2web-translations.conf.
TranslationsFile = ConfigFolder + "/ufw2web-translations.conf"
if os.path.isfile(TranslationsFile):
  print 'Reading translations from ' + TranslationsFile
  config = ConfigObj(TranslationsFile)
  try:
    strFirewallStatusDisabled = config['FirewallStatusDisabled']
    strFirewallStatusEnabled = config['FirewallStatusEnabled']
    strFirewallStatusUnknown = config['FirewallStatusUnknown']
    strFirewallIsDisabled = config['FirewallIsDisabled']
    strFirewallIsEnabled = config['FirewallIsEnabled']
    strSystemUnprotected = config['SystemUnprotected']
    strSystemProtected = config['SystemProtected']
    strEnableFirewall = config['EnableFirewall']
    strDisableFirewall = config['DisableFirewall']
    strIsSudoPrivileges = config['IsSudoPrivileges']
  except KeyError:
    print '- Warning: one or more keys not found in %s' % TranslationsFile
else:
  print 'No translation file %s, using defaults (English)' % TranslationsFile

#
# Server configuration
#

# Default settings
WebServerPort = 80
UseAuthentication = 0
LoginUser = 'admin'
LoginPassword = 'admin'

# Read settings from config file (if existing)
ConfigFile = ConfigFolder + '/ufw2web.conf'
if os.path.isfile(ConfigFile):
  print 'Reading settings from ' + ConfigFile
  config = ConfigObj(ConfigFile)

  # Retrieve settings
  try:
    WebServerPort = config['WebServerPort']
    try:
      WebServerPort = int(WebServerPort)
    except ValueError:
      print '- Warning: no valid value for WebServerPort'
    print '- WebServerPort: %d' % WebServerPort
  except KeyError:
    print '- WebServerPort not found, using default: %d' % WebServerPort

  try:
    UseAuthentication = config['UseAuthentication']
    try:
      UseAuthentication = int(UseAuthentication)
    except ValueError:
      print '- Warning: no valid value for UseAuthentication'
    print '- UseAuthentication: %d' % UseAuthentication
  except KeyError:
    print '- UseAuthentication not found, using default: %d' % UseAuthentication

  # If there's no authentication, there is no use for user credentials
  if (UseAuthentication == 1):
    try:
      LoginUser = config['LoginUser']
      print '- LoginUser: %s' % LoginUser
    except KeyError:
      print '- LoginUser not found, using default: %s' % LoginUser

    try:
      LoginPassword = config['LoginPassword']
      print '- LoginPassword: %s' % LoginPassword
    except KeyError:
      print '- LoginPassword not found, using default: %s' % LoginPassword

# Basic server configuration
current_dir = os.path.dirname(os.path.abspath(__file__))
cherrypy.config.update({'server.socket_port':WebServerPort,
                        'server.socket_host':'0.0.0.0',
                        'tools.staticdir.root':current_dir}) # Root for static folders

# User dictionairy for authentication
users = {LoginUser: LoginPassword}
        
# Extra config       
conf = {'/images': {'tools.staticdir.on': True,    # Folder 'images' is a static folder
                    'tools.staticdir.dir': 'images'},
        '/': {'tools.digest_auth.on': (UseAuthentication == 1), # Activate authentication (on demand)
              'tools.digest_auth.realm': '',
              'tools.digest_auth.users': users}}
#
# And start the webserver...
#
cherrypy.quickstart(Start(), '/', config=conf)

