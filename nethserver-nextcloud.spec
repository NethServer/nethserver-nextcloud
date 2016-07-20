%define nextcloud_version 9.0.53

%define apache_serverroot       /var/www/html
%define apache_confdir /etc/httpd/conf.d
%define oc_dir  %{apache_serverroot}/nextcloud
%define oc_config_dir   %{oc_dir}/config
%define oc_data_dir     /var/lib/nethserver/nextcloud
%define oc_data_pdir    %{oc_dir}

%define oc_user apache
%define oc_group apache


Summary: NethServer Owncloud configuration
Name: nethserver-nextcloud
Version: %nextcloud_version
Release: 1%{?dist}
License: GPL
Source: %{name}-%{version}.tar.gz
Source1: https://download.nextcloud.com/server/releases/nextcloud-%{nextcloud_version}.tar.bz2
Source2: nextcloud.conf
BuildArch: noarch
URL: %{url_prefix}/%{name}

BuildRequires: nethserver-devtools, httpd

Requires: php-ldap, php-gd, php-pdo, php-mysql, php-pear, php-pear-MDB2, php-pear-MDB2-Driver-mysqli, php-pear-Net-Curl, php-mbstring
Requires: nethserver-httpd, nethserver-mysql

%description
NethServer Owncloud files and configuration.

This package installs as follows:
oc_dir:        %{oc_dir}
oc_data_dir:   %{oc_data_dir}
oc_config_dir: %{oc_config_dir}


%prep
%setup
cp %{SOURCE1} .


%build
perl createlinks

%install
rm -rf %{buildroot}
(cd root   ; find . -depth -print | cpio -dump %{buildroot})
mkdir -p %{buildroot}/%{oc_data_dir}
mkdir -p %{buildroot}/var/www/html
tar xf %{SOURCE1} -C %{buildroot}/var/www/html

idir=%{buildroot}/%{oc_dir}
mkdir -p %{buildroot}/%{oc_dir}
mkdir -p %{buildroot}/%{oc_dir}/etc
mkdir -p %{buildroot}/%{oc_data_dir}
mkdir -p %{buildroot}/%{oc_config_dir}
mkdir -p %{buildroot}/%{oc_dir}/assets
mkdir -p %{buildroot}/%{oc_dir}/updater

mkdir -p %{buildroot}/etc/httpd/conf.d
cp %{SOURCE2} %{buildroot}/etc/httpd/conf.d


%files 
%defattr(0640,root,%{oc_group},0750)
%doc COPYING
%dir %{_nseventsdir}/%{name}-update
%attr(0755,root,%{oc_group})/%{oc_dir}
%attr(0755,%{oc_user},%{oc_group})/%{oc_dir}/occ
%attr(0750,%{oc_user},%{oc_group}) %{oc_dir}/apps
%attr(0750,%{oc_user},%{oc_group}) %{oc_dir}/assets
%attr(0750,%{oc_user},%{oc_group}) %{oc_dir}/updater
%attr(0775,%{oc_user},%{oc_group}) %{oc_data_dir}
%attr(0775,%{oc_user},%{oc_group}) %{oc_config_dir}

%attr(0644,%{oc_user},%{oc_group}) %{oc_dir}/.htaccess
/etc/backup-data.d/nextcloud.include
/etc/e-smith/db/configuration/defaults/nextcloud/type
/etc/e-smith/db/configuration/defaults/nextcloud/TrustedDomains
%attr(0755, root, root) /etc/e-smith/events/actions/nethserver-nextcloud-conf
%attr(0755, root, root) /etc/e-smith/events/actions/nethserver-nextcloud-occ-conf
/etc/e-smith/events/nethserver-nextcloud-save/S30nethserver-nextcloud-occ-conf
/etc/e-smith/events/nethserver-sssd-save/S80nethserver-nextcloud-occ-conf
/etc/e-smith/events/nethserver-directory-update/S80nethserver-nextcloud-occ-conf
/etc/e-smith/events/nethserver-dc-save/S80nethserver-nextcloud-occ-conf
/etc/e-smith/events/nethserver-nextcloud-update/S00initialize-default-databases
/etc/e-smith/events/nethserver-nextcloud-update/S20nethserver-nextcloud-conf
/etc/e-smith/events/nethserver-nextcloud-update/S30nethserver-nextcloud-occ-conf
/etc/e-smith/events/nethserver-nextcloud-update/services2adjust/httpd
/etc/e-smith/events/nethserver-nextcloud-update/templates2expand/etc/httpd/conf.d/nethserver.conf
/etc/e-smith/templates/httpd/vhost-default/40nextcloud
/etc/httpd/conf.d/nextcloud.conf
%attr(0644,root,root) /usr/share/nethesis/NethServer/Module/Dashboard/Applications/Nextcloud.php

%defattr(0644,%{oc_user},%{oc_group},0755)
%dir /var/lib/nethserver/nextcloud
%{oc_dir}



%changelog
