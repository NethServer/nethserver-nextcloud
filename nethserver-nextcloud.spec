Summary: NethServer Nextcloud configuration
Name: nethserver-nextcloud
Version: 1.22.5
Release: 1%{?dist}
License: GPL
Source0: %{name}-%{version}.tar.gz
Source1: %{name}.tar.gz

%define nc_version 27.1.11
Source2: https://download.nextcloud.com/server/releases/nextcloud-%{nc_version}.tar.bz2

BuildArch: noarch
URL: %{url_prefix}/%{name}

BuildRequires: nethserver-devtools

Provides: nextcloud
Obsoletes: nextcloud
Requires: nethserver-httpd
Requires: nethserver-rh-mariadb105 rh-mariadb105-mariadb-server-utils
Requires: nethserver-remi-php80-php-fpm
Requires: samba-client

# Required php packages
Requires: php80-php-gd
Requires: php80-php-pdo
Requires: php80-php-mbstring
Requires: php80-php-imagick

# Recommended php packages
Requires: php80-php-intl
Requires: php80-php-gmp
Requires: php80-php-sodium

# Required php packages for specific apps
Requires: php80-php-ldap
Requires:  php80-php-smbclient

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

mkdir -p %{buildroot}/var/opt/rh/rh-mariadb105/lib/mysql-nextcloud

%{genfilelist} %{buildroot} \
    --file /etc/sudoers.d/50_nsapi_nethserver_nextcloud 'attr(0440,root,root)' \
    --dir /var/lib/nethserver/nextcloud 'attr(0755,apache,apache)' | grep -v -e '/usr/share/nextcloud' -e '/var/opt/rh/rh-mariadb105/lib/mysql-nextcloud' > %{name}-%{version}-filelist


%files -f %{name}-%{version}-filelist
%defattr(-,root,root)
%doc COPYING
%dir %{_nseventsdir}/%{name}-update
%config %attr (0440,root,root) %{_sysconfdir}/sudoers.d/90_nethserver_nextcloud
%config(noreplace) %{_sysconfdir}/opt/remi/php80/php-fpm.d/000-nextcloud.conf
%config(noreplace) %attr(0644,apache,apache) /usr/share/nextcloud/.user.ini
%dir %attr(0755,root,apache) /usr/share/nextcloud
%dir %attr(0755,mysql,mysql) /var/opt/rh/rh-mariadb105/lib/mysql-nextcloud
%attr(-,apache,apache) /usr/share/nextcloud
%attr(0755,apache,apache) /usr/share/nextcloud/occ
%attr(0775,apache,apache) /usr/share/nextcloud/data

%changelog
* Fri Aug 02 2024 Stephane de Labrusse <stephdl@de-labrusse.fr> - 1.22.5-1
- Migration of Nextcloud 27.1.11 - NethServer/dev#6964

* Tue Mar 19 2024 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.22.4-1
- Update Nextcloud release to 27.1.7 - NethServer/dev#6899

* Fri Feb 23 2024 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.22.3-1
- Nextcloud 27.1.6 - NethServer/dev#6857

* Tue Nov 21 2023 Stephane de Labrusse <stephdl@de-labrusse.fr> - 1.22.2-1
- Nextcloud 27.1.3 - NethServer/dev#6772

* Thu Jul 27 2023 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.22.1-1
- Nextcloud 27.0.1 - NethServer/dev#6757

* Tue Jun 13 2023 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.22.0-1
- Upgrade nextcloud to 26.0.2 - NethServer/dev#6751

* Tue May 02 2023 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.21.4-1
- nextcloud update 25.0.6 - NethServer/dev#6745

* Mon Apr 03 2023 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.21.3-1
- nextcloud 25.0.5 - NethServer/dev#6737

* Tue Mar 07 2023 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.21.2-1
- nextcloud 25.0.4 available - NethServer/dev#6733

* Tue Jan 31 2023 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.21.1-1
- nextcloud update to 25.0.3 NethServer/dev#6730 

* Mon Dec 19 2022 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.21.0-1
- Nextcloud 25.0.2 - NethServer/dev#6725

* Mon Nov 07 2022 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.20.2-1
- Nextcloud 24.0.7 - NethServer/dev#6719

* Wed Oct 12 2022 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.20.1-1
- Nextcloud 24.0.6 - NethServer/dev#6706

* Tue Sep 13 2022 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.20.0-1
- Nextcloud 24.0.5 - NethServer/dev#6696

* Tue Aug 30 2022 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.19.7-1
- Nextcloud 23.0.8 - NethServer/dev#6694

* Wed Jul 06 2022 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.19.6-1
- Nextcloud 23.0.6 - NethServer/dev#6679

* Tue Apr 26 2022 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.19.5-1
- Nextcloud 23.0.4 - NethServer/dev#6657
- Nextcloud webfinger and nodeinfo URLs changed - Bug NethServer/dev#6655

* Wed Mar 23 2022 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.19.4-1
- Nextcloud 23.0.3 - NethServer/dev#6650

* Mon Feb 21 2022 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.19.3-1
- Nextcloud 23.0.2 - NethServer/dev#6638

* Mon Jan 31 2022 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.19.2-1
- Nextcloud 23.0.1 - NethServer/dev#6630

* Thu Nov 18 2021 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.19.1-1
- Nextcloud 22.2.3 - NethServer/dev#6598

* Tue Oct 05 2021 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.19.0-1
- Nextcloud 22.2.0 - NethServer/dev#6576

* Wed Sep 08 2021 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.18.0-1
- Nextcloud 22.1.1 - NethServer/dev#6566

* Tue Jul 06 2021 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.17.1-1
- Nextcloud 21.0.3 - NethServer/dev#6539

* Mon Jun 21 2021 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.17.0-1
- Nextcloud 21.0.2 - NethServer/dev#6506

* Fri Apr 16 2021 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.16.7-1
- Nextcloud 20.0.9 - NethServer/dev#6478

* Thu Mar 11 2021 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.16.6-1
- Nextcloud 20.0.8 - NethServer/dev#6452

* Mon Feb 08 2021 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.16.5-1
- Nextcloud 20.0.7 - NethServer/dev#6415

* Fri Jan 29 2021 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.16.4-1
- Nextcloud 20.0.6 - NethServer/dev#6404

* Wed Jan 20 2021 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.16.3-1
- Nextcloud 20.0.5 - NethServer/dev#6394

* Tue Jan 05 2021 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.16.2-1
- Nextcloud installation fails if no account provider is installed - Bug NethServer/dev#6384

* Thu Dec 17 2020 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.16.1-1
- Nextcloud 20.0.4 - NethServer/dev#6363

* Mon Nov 30 2020 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.16.0-1
- Nextcloud 20.0.2 - NethServer/dev#6340
- PHP-fpm: php script use a bad file path with '//' - Bug NethServer/dev#6339

* Wed Nov 18 2020 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.15.0-1
- New NethServer 7.9.2009 defaults - NethServer/dev#6320
- Nextcloud 20.0.1 - NethServer/dev#6314
- StartTLS settings not honored by NextCloud conf - NethServer/dev#6318

* Tue Nov 03 2020 Davide Principi <davide.principi@nethesis.it> - 1.14.2-1
- StartTLS settings not honored by NextCloud conf - NethServer/dev#6318

* Fri Oct 16 2020 Davide Principi <davide.principi@nethesis.it> - 1.14.1-1
- Add constraints to Nextcloud users count fact - NethServer/dev#6307

* Mon Sep 14 2020 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.14.0-1
- Nextcloud 19.0.3 - NethServer/dev#6266

* Thu Sep 03 2020 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.13.0-1
- Nextcloud 19.0.2 - NethServer/dev#6257
- Event interface-update fails with Nextcloud - Bug NethServer/dev#6250

* Tue Aug 11 2020 Stephane de Labrusse <stephdl@de-labrusse.fr> - 1.12.4-1
- Nextcloud: Increase php memory for cron job - Bug NethServer/dev#6249

* Mon Jul 20 2020 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.12.3-1
- Nextcloud 19.0.1 - NethServer/dev#6232

* Thu Jul 09 2020 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.12.2-1
- Nextcloud facter. Remove useless "size" attribute - Bug Nethserver/dev#6225

* Thu Jul 02 2020 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.12.1-1
- Human readable numbers in Cockpit dashboards - NethServer/dev#6206

* Mon Jun 15 2020 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.12.0-1
- Nextcloud: files shared with group are not listed in the UI - Bug NethServer/dev#6202

* Mon Jun 08 2020 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.11.0-1
- Nextcloud 19.0.0 - NethServer/dev#6178

* Thu May 07 2020 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.10.1-1
- Nextcloud 18.0.4 - NethServer/dev#6155

* Tue Apr 28 2020 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.10.0-1
- Update Nextcloud stack to PHP 7.3 - NethServer/dev#6120

* Thu Mar 26 2020 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.9.2-1
- Nextcloud 18.0.3 - NethServer/dev#6098

* Wed Mar 25 2020 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.9.1-1
- Nextcloud 18.0.2 - NethServer/dev#6095

* Wed Feb 26 2020 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.9.0-1
- Nextcloud trusted domains are not deleted - Bug NethServer/dev#6067
- Nextcloud 18.0.1  - NethServer/dev#6062

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
