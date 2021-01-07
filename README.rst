====================
nethserver-nextcloud
====================

This package can be installed before or after any user provider like nethserver-dc
and nethserver-directory.

If nethserver-dc or nethserver-directory are installed, the nethserver-nextcloud-save
event will automatically enable all local users.

The package does the following:

* create ``nextcloud`` mysql database
* create default database credentials: user `nextcloud` and password stored in ``/var/lib/nethserver/secrets/nextcloud``
* add trusted domains to use with web access
* create default credentials for web login: user `"admin"` and password `"Nethesis,1234"`
* set english as the default language
* set the user data directory as ``/var/lib/nethserver/nextcloud``

The configuration is stored inside the ``configuration`` db, under the ``nextcloud`` key. To show it: ::

 config show nextcloud

Properties:

* ``TrustedDomains``: list of trusted domains added to Nextcloud config file
* ``VirtualHost``: set custom virtual host, e.g. `mycloud.mydomain.it`
* ``Wellknown``: can be ``enabled`` or ``disabled``. If enabled, add redirects for calDAV and cardDAV.
  This property has effect only if ``VirtualHost`` is empty.
* ``HonorAdStartTls``: can be ``enabled`` or ``disabled``.  The StartTLS option from SSSD
  configuration was historyically ignored. If set to ``enabled``, the ``sssd/StartTls`` prop value
  is honored.


Admin user
==========

After installation the application is accesible using the following credentials:

* User: admin
* Password: Nethesis,1234

Please, remember to change the default password after the first login!

Customize virtual host
======================

Set custom virtual host and add it to trusted domains as follow: ::

 config setprop nextcloud VirtualHost <VHOST>.<DOMAIN_NAME>
 config setprop nextcloud TrustedDomains <VHOST>.<DOMAIN_NAME>
 signal-event nethserver-nextcloud-update


Backup
======

The Nextcloud backup includes the configuration file and all data of the users: ::

 /var/lib/nethserver/nextcloud
 /usr/share/nextcloud/config/config.php

The database is automatically saved by ``nethserver-mysql``.

OCC
===

When using ``occ`` command, PHP 7.3 should be enabled inside the environment.

Invocation example: ::

  occ ldap:show-config"

The ``occ`` command is just a wrapper around: ::

  su - apache -s /bin/bash -c "source /opt/rh/rh-php73/enable; cd /usr/share/nextcloud/; php occ ldap:show-config"

Log of rh-php73-fpm
===================

The log of rh-php73-fpm can be found at `/var/opt/rh/rh-php73/log/php-fpm/error-nextcloud.log`

Cockpit API
===========

read
----

Return mattermost status and configuration.

Input
^^^^^
- ``app-info`` or ``configuration``

Output
^^^^^^

Example (``app-info``): ::

 {
  "url": "https://your.host.domain"
 }

Example (``configuration``): ::

 {
  "props": {
    "Wellknown": "enabled",
    "VirtualHost": "eccoci.rva.org",
    "TrustedDomains": "a.b,b.c"
  },
  "stats": {
    "version": "16.0.2.1",
    "admin_pass_warn": true,
    "users": "3"
  }
 }


validate
--------

Constraints:

- ``VirtualHost``: must be a valid FQDN or EMPTY
- ``TrustedDomains``: must be an array of valid FQDN

Input
^^^^^

Example: ::

 {
  "props": {
    "Wellknown": "enabled",
    "VirtualHost": "eccoci.rva.org",
    "TrustedDomains": "a.b,b.c"
  }
 }


update
------

Same input as validate.

Full reinstall
===============
As with many other applications in NethServer, un-installing the Nextcloud application **does not** remove the settings, stored files, or the database. Here are the suggested steps to do a full un-install and re-install with a fresh configuration:

1. Uninstall Nextcloud using the admin page
2. Remove the packages: ``yum remove nethserver-nextcloud nextcloud``
3. Drop the MySQL database: ``mysql -e "drop database nextcloud"``
4. Remove the whole Nextcloud directory: ``rm -rf /usr/share/nextcloud/``
5. Remove the e-smith DB configuration: ``config delete nextcloud``
6. Remove the NethServer config directory (WARNING: will remove user data): ``rm -rf /var/lib/nethserver/nextcloud``
7. Install Nextcloud from the Software Center
