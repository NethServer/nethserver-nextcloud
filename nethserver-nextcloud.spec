Summary: NethServer Nextcloud configuration
Name: nethserver-nextcloud
Version: 1.1.2
Release: 1%{?dist}
License: GPL
Source: %{name}-%{version}.tar.gz
BuildArch: noarch
URL: %{url_prefix}/%{name}

BuildRequires: nethserver-devtools

Requires: nextcloud >= 11.0.3
Requires: nethserver-httpd, nethserver-mysql
Requires: nethserver-rh-php56-php-fpm
Requires: sclo-php56-php-smbclient samba-client

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
%{genfilelist} %{buildroot} --dir /var/lib/nethserver/nextcloud 'attr(0755,apache,apache)' > %{name}-%{version}-filelist


%files -f %{name}-%{version}-filelist
%defattr(-,root,root)
%doc COPYING
%doc owncloud-migrate
%dir %{_nseventsdir}/%{name}-update
%config %attr (0440,root,root) %{_sysconfdir}/sudoers.d/90_nethserver_nextcloud


%changelog
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

