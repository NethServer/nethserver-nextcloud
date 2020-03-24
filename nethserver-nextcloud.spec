Summary: NethServer Nextcloud configuration
Name: nethserver-nextcloud
Version: 1.9.0
Release: 1%{?dist}
License: GPL
Source0: %{name}-%{version}.tar.gz
Source1: %{name}.tar.gz

%define nc_version 18.0.2
Source2: https://download.nextcloud.com/server/releases/nextcloud-%{nc_version}.tar.bz2

BuildArch: noarch
URL: %{url_prefix}/%{name}

BuildRequires: nethserver-devtools

Provides: nextcloud
Obsoletes: nextcloud
Requires: nethserver-httpd
Requires: nethserver-mysql
Requires: nethserver-rh-php72-php-fpm >= 1.1.0
Requires: samba-client

# Required php packages
Requires: rh-php72
Requires: rh-php72-php-fpm
Requires: rh-php72-php-gd
Requires: rh-php72-php-pdo
Requires: rh-php72-php-mbstring
Requires: rh-php72-php-imagick

# Recommended php packages
Requires: rh-php72-php-intl

# Required php packages for specific apps
Requires: rh-php72-php-ldap
Requires: sclo-php72-php-smbclient

# Required php packages for MariaDB
Requires: rh-php72-php-pdo_mysql

%description
NethServer Nextcloud files and configuration.


%prep
%setup


%build
perl createlinks
sed -i 's/_RELEASE_/%{version}/' %{name}.json

%install
rm -rf %{buildroot}
(cd root; find . -depth -print | cpio -dump %{buildroot})

mkdir -p %{buildroot}/usr/share/nextcloud/{config,data,etc,assets,updater}
tar xf %{SOURCE2} -C %{buildroot}/usr/share

mkdir -p %{buildroot}/var/lib/nethserver/nextcloud

mkdir -p %{buildroot}/usr/share/cockpit/%{name}/
mkdir -p %{buildroot}/usr/share/cockpit/nethserver/applications/
mkdir -p %{buildroot}/usr/libexec/nethserver/api/%{name}/
tar xvf %{SOURCE1} -C %{buildroot}/usr/share/cockpit/%{name}/
cp -a %{name}.json %{buildroot}/usr/share/cockpit/nethserver/applications/
cp -a api/* %{buildroot}/usr/libexec/nethserver/api/%{name}/

%{genfilelist} %{buildroot} \
    --file /etc/sudoers.d/50_nsapi_nethserver_nextcloud 'attr(0440,root,root)' \
    --dir /var/lib/nethserver/nextcloud 'attr(0755,apache,apache)' | grep -v '/usr/share/nextcloud' > %{name}-%{version}-filelist


%files -f %{name}-%{version}-filelist
%defattr(-,root,root)
%doc COPYING
%dir %{_nseventsdir}/%{name}-update
%config %attr (0440,root,root) %{_sysconfdir}/sudoers.d/90_nethserver_nextcloud
%config(noreplace) %{_sysconfdir}/opt/rh/rh-php72/php-fpm.d/000-nextcloud.conf
%config(noreplace) %attr(0644,apache,apache) /usr/share/nextcloud/.user.ini
%dir %attr(0755,root,apache) /usr/share/nextcloud
%attr(-,apache,apache) /usr/share/nextcloud
%attr(0755,apache,apache) /usr/share/nextcloud/occ
%attr(0775,apache,apache) /usr/share/nextcloud/data

%changelog
* Wed Feb 26 2020 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.9.0-1
- Nextcloud trusted domains are not deleted - Bug NethServer/dev#6067
- NextCloud 18.0.1  - NethServer/dev#6062

* Mon Jan 27 2020 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.8.5-1
- Update to Nextcloud 18 - NethServer/dev#6039

* Thu Jan 16 2020 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.8.4-1
- facter: improve user count - NethServer/nethserver-nextcloud/69

* Wed Jan 15 2020 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.8.3-1
- Nextcloud: upgrade to v17.0.2 - NethServer/dev#6016
- Cockpit: change package Dashboard page title - NethServer/dev#6004

* Thu Dec 19 2019 Davide Principi <davide.principi@nethesis.it> - 1.8.2-1
- Nextcloud: php-fpm with a linux socket - NethServer/dev#5997

* Mon Dec 09 2019 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.8.1-1
- Inventory: add new application facts - NethServer/dev#5979

* Mon Dec 02 2019 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.8.0-1
- Update to Nextcloud 17 - NethServer/dev#5958

* Wed Oct 09 2019 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.7.1-1
- Nextcloud: upgrade to v16.0.5 - NethServer/dev#5858
- Cockpit: improve English labels - NethServer/dev#5856

* Tue Oct 01 2019 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.7.0-1
- Sudoers based authorizations for Cockpit UI - NethServer/dev#5805

* Tue Sep 03 2019 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.6.2-1
- Nextcloud: upgrade to v16.0.4 - NethServer/dev#5818
- Cockpit. List correct application version - NethServer/dev#5819

* Mon Aug 05 2019 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.6.1-1
- Nextcloud: upgrade to v16.0.3 - NethServer/dev#5798

* Wed Jul 17 2019 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.6.0-1
- Nextcloud Cockpit UI - NethServer/dev#5789

* Tue Jul 09 2019 Davide Principi <davide.principi@nethesis.it> - 1.5.2-1
- Nextcloud: upgrade to v16.0.2 - nethserver/dev#5784
- Cockpit legacy apps implementation - NethServer/dev#5782

* Fri May 24 2019 Davide Principi <davide.principi@nethesis.it> - 1.5.1-1
- Nextcloud: upgrade to v16.0.1 - NethServer/dev#5762

* Wed May 08 2019 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.5.0-1
- Nextcloud 16 - NethServer/dev#5753
- Switch from PHP 7.1 to PHP 7.2

* Mon Apr 29 2019 Alessandro Polidori <alessandro.polidori@gmail.com> - 1.4.4-1
- Nextcloud: upgrade to v15.0.7 - NethServer/dev#5742

* Thu Mar 07 2019 Alessandro Polidori <alessandro.polidori@gmail.com> - 1.4.3-1
- Nextcloud: upgrade to v15.0.5 - nethserver/dev#5726

* Tue Feb 12 2019 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.4.2-1
- Nextcloud: upgrade to 15.0.4 - NethServer/dev#5708

* Thu Jan 17 2019 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.4.1-1
- Nextcloud: upgrade to 15.0.2 - nethserver/dev#5692

* Thu Dec 20 2018 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.4.0-1
- Nextcloud: upgrade to 15.0.0 - NethServer/dev#5674

* Mon Dec 03 2018 Davide Principi <davide.principi@nethesis.it> - 1.3.0-1
- Nextcloud: upgrade to 14.0.4 - NethServer/dev#5658

* Wed Oct 17 2018 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.2.7-1
- Nextcloud: upgrade to 14.0.3 - NethServer/dev#5604

* Wed Sep 26 2018 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.2.6-1
- Nextcloud: upgrade to 14.0.1 - nethserver/dev#5588

* Tue Sep 25 2018 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.2.5-1
- Nextcloud: upgrade to 14.0.0 - nethserver/dev#5578

* Thu Sep 06 2018 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.2.4-1
- Nextcloud: upgrade to 13.0.6 - NethServer/dev#5577

* Wed Aug 01 2018 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.2.3-1
- Nextcloud: upgrade to 13.0.5 - NethServer/dev#5556

* Thu Jun 14 2018 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.2.2-1
- Improve SSL configuration - NethServer/dev#5509
- Upgrade nextcloud  to 13.0.4 - NethServer/dev#5523
- Apache Virtualhost Collision - Bug NethServer/dev#5517

* Tue May 08 2018 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.2.1-1
- Nextcloud: upgrade to 13.0.2 - NethServer/dev#5474

* Tue Mar 20 2018 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.2.0-1
- Nextcloud: upgrade to v13 & optimizations - NethServer/dev#5427

* Tue Jan 30 2018 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.1.11-1
- Nextcloud: upgrade to 12.0.5 - NethServer/dev#5416

* Tue Jan 23 2018 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.1.10-1
- Nextcloud: integrity check after upgrade - Bug NethServer/dev#5409

* Tue Dec 19 2017 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.1.9-1
- Nextcloud: upgrade to 12.0.4 - NethServer/#5398

* Fri Oct 06 2017 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.1.8-1
- Nextcloud 12.0.3 - NS 7.4

* Wed Aug 30 2017 Alessandro Polidori <alessandro.polidori@nethesis.it> - 1.1.7-1
- Nextcloud 12.0.2 - NethServer/dev#5342

* Mon Jul 24 2017 Davide Principi <davide.principi@nethesis.it> - 1.1.6-1
- ownCloud migration script fixes

* Wed Jul 12 2017 Davide Principi <davide.principi@nethesis.it> - 1.1.5-1
- Nextcloud: add logrotate - NethServer/dev#5329

* Wed May 31 2017 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.1.4-1
- Nextcloud: update to 12.0.0 - NethServer/dev#5306

* Mon May 22 2017 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.1.3-1
- Nextcloud: update to 11.0.3 - NethServer/dev#5285
- Default userPrincipalName is not an email address - Bug NethServer/dev#5284

* Wed May 10 2017 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.1.2-1
- Requirements not met for Nextcloud's External Storage App using CIFS/SMB - Bug NethServer/dev#5276
- Upgrade from NS 6 via backup and restore - NethServer/dev#5234

* Mon Apr 24 2017 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.1.1-1
- Nextcloud config not backuped - Bug NethServer/dev#5273

* Tue Apr 04 2017 Davide Principi <davide.principi@nethesis.it> - 1.1.0-1
- Nextcloud 11 - NethServer/dev#5242
- Upgrade from NS 6 via backup and restore - NethServer/dev#5234

* Thu Dec 15 2016 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.0.4-1
- Enable LDAPs protocol on Active Directory clients - NethServer/dev#5161
- Nextcloud: upgrade to version 10.0.2 - NethServer/dev#5155

* Mon Nov 14 2016 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.0.3-1
- LDAP account with read-only privileges - NethServer/dev#5145
- Fix https redirect

* Thu Sep 01 2016 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.0.2-1
- Apache vhost-default template expansion - NethServer/dev#5088
- Nextcloud: upgrade to version 10 - NethServer/dev#5096

* Wed Aug 24 2016 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.0.1-1
- Nextcloud: trusted domains not updated on IP change - NethServer/dev#5076

* Mon Aug 01 2016 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.0.0-1
- First Nextcloud release - NethServer/dev#5055

