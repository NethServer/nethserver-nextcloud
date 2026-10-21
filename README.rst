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

  su - apache -s /bin/bash -c "source /opt/remi/php80/enable; cd /usr/share/nextcloud/; php occ ldap:show-config"

Log of php80-fpm
===================

The log of php80-fpm can be found at `/opt/remi/php80/log/php-fpm/error-nextcloud.log`

PHP upload limits
=================

To mitigate the PHP vulnerabilities CVE-2026-109618 and CVE-2026-109619
(see the `PHP advisory <https://www.php.net/archive/2026.php#2026-10-21-5>`_),
the php-fpm pool ``/etc/opt/remi/php80/php-fpm.d/000-nextcloud.conf`` keeps the
size of a POST request body low: ::

 php_admin_value[post_max_size] = 32M
 php_admin_value[upload_max_filesize] = 30M

These limits apply only to form uploads (``multipart/form-data`` POST requests),
like the user avatar, the theming logo and some app imports.
Normal file uploads are not affected: the web interface, the desktop and mobile clients
and the public upload shares send files with WebDAV ``PUT`` requests, which are not
limited by these values.

The values are set with ``php_admin_value``, so the ``/usr/share/nextcloud/.user.ini``
file cannot raise them.

If needed, the limits can be raised by hand. Keep the values at 32M or lower:
higher values weaken the mitigation.

1. Edit ``/etc/opt/remi/php80/php-fpm.d/000-nextcloud.conf`` and change the
   ``post_max_size`` and ``upload_max_filesize`` lines; ``upload_max_filesize`` must
   be lower than ``post_max_size``
2. Restart php-fpm: ``systemctl restart php80-php-fpm``

The file is marked as ``%config(noreplace)``, so manual changes survive package updates.

If the file was already edited before the update that introduced these limits,
the update leaves it untouched and saves the new version as
``/etc/opt/remi/php80/php-fpm.d/000-nextcloud.conf.rpmnew``.
In this case, add the ``post_max_size`` and ``upload_max_filesize`` lines
to ``000-nextcloud.conf`` by hand, then restart php-fpm: ::

 diff /etc/opt/remi/php80/php-fpm.d/000-nextcloud.conf /etc/opt/remi/php80/php-fpm.d/000-nextcloud.conf.rpmnew
 systemctl restart php80-php-fpm

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
2. Drop the MySQL database: ``/opt/rh/rh-mariadb105/root/bin/mysql --socket="/var/run/rh-mariadb105-mariadb/nextcloud-mysql.sock" -e "drop database nextcloud;"``
3. Remove the packages: ``yum remove nethserver-nextcloud``
4. Remove the whole Nextcloud directory: ``rm -rf /usr/share/nextcloud/``
5. Remove the e-smith DB configuration: ``config delete nextcloud``
6. Remove the NethServer config directory (WARNING: will remove user data): ``rm -rf /var/lib/nethserver/nextcloud``
7. Install Nextcloud from the Software Center
