Summary: NethServer Nextcloud configuration
Name: nethserver-nextcloud
Version: 0.1
Release: 1%{?dist}
License: GPL
Source: %{name}-%{version}.tar.gz
BuildArch: noarch
URL: %{url_prefix}/%{name}

BuildRequires: nethserver-devtools

Requires: nextcloud
Requires: nethserver-httpd, nethserver-mysql

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
%dir %{_nseventsdir}/%{name}-update
%config %attr (0440,root,root) %{_sysconfdir}/sudoers.d/90_nethserver_nextcloud


%changelog
