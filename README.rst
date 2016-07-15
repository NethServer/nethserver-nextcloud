====================
nethserver-nextcloud
====================

This package can be installer before or after any user provider like nethserver-dc
and nethserver-directory.

If nethserver-dc or nethserver-directory are installed, the nethserver-nextcloud-save
event will automatically enable all local users.

Trusted domains
===============

The Nexcloud application is accessible using the following URLs:

* https://localhost
* https://<FQDN> where <FQDN> is the name of the server
* https://<IP> where <IP> is any static IP address of the server
* Any additional name or IP added to the TrustedDomains prop


Add extra IPs and name ::

    config setprop TrustedDomains nextcloud.nethserver.org,10.10.10.1
    signal-event nethserver-nextcloud-save
