Summary: NethServer Nextcloud configuration
Name: nethserver-nextcloud
Version: 1.5.1
Release: 1%{?dist}
License: GPL
Source: %{name}-%{version}.tar.gz
BuildArch: noarch
URL: %{url_prefix}/%{name}

BuildRequires: nethserver-devtools

Requires: nextcloud >= 16.0.2
Requires: nethserver-httpd
Requires: nethserver-mysql
Requires: nethserver-rh-php72-php-fpm
Requires: samba-client
Requires: sclo-php72-php-smbclient
Requires: rh-php72-php-opcache
Requires: rh-php72-php-pecl-apcu

%description
NethServer Nextcloud files and configuration.


%prep
%setup


%build
perl createlinks

%install
rm -rf %{buildroot}
(cd root; find . -depth -print | cpio -dump %{buildroot})
mkdir -p %{buildroot}/var/lib/nethserver/nextcloud
install -v -m 644 -D %{name}.json %{buildroot}/usr/share/cockpit/nethserver/applications/%{name}.json
install -v -m 644 -D ui/public/logo.png %{buildroot}/usr/share/cockpit/%{name}/logo.png
install -v -m 644 -D ui/public/manifest.json %{buildroot}/usr/share/cockpit/%{name}/manifest.json
install -v -m 755 -D api/read %{buildroot}/usr/libexec/nethserver/api/%{name}/read
%{genfilelist} %{buildroot} --dir /var/lib/nethserver/nextcloud 'attr(0755,apache,apache)' > %{name}-%{version}-filelist


%files -f %{name}-%{version}-filelist
%defattr(-,root,root)
%doc COPYING
%dir %{_nseventsdir}/%{name}-update
%config %attr (0440,root,root) %{_sysconfdir}/sudoers.d/90_nethserver_nextcloud


%changelog
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

