################################################################################

%global __python3 %{_bindir}/python3

%global pythonver %(%{__python3} -c "import sys; print sys.version[:3]" 2>/dev/null || echo 0.0)
%{!?python3_sitearch: %global python3_sitearch %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)" 2>/dev/null)}
%{!?python3_sitelib: %global python3_sitelib %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()" 2>/dev/null)}

################################################################################

%define _posixroot        /
%define _root             /root
%define _bin              /bin
%define _sbin             /sbin
%define _srv              /srv
%define _home             /home
%define _lib32            %{_posixroot}lib
%define _lib64            %{_posixroot}lib64
%define _libdir32         %{_prefix}%{_lib32}
%define _libdir64         %{_prefix}%{_lib64}
%define _logdir           %{_localstatedir}/log
%define _rundir           %{_localstatedir}/run
%define _lockdir          %{_localstatedir}/lock/subsys
%define _cachedir         %{_localstatedir}/cache
%define _spooldir         %{_localstatedir}/spool
%define _crondir          %{_sysconfdir}/cron.d
%define _loc_prefix       %{_prefix}/local
%define _loc_exec_prefix  %{_loc_prefix}
%define _loc_bindir       %{_loc_exec_prefix}/bin
%define _loc_libdir       %{_loc_exec_prefix}/%{_lib}
%define _loc_libdir32     %{_loc_exec_prefix}/%{_lib32}
%define _loc_libdir64     %{_loc_exec_prefix}/%{_lib64}
%define _loc_libexecdir   %{_loc_exec_prefix}/libexec
%define _loc_sbindir      %{_loc_exec_prefix}/sbin
%define _loc_bindir       %{_loc_exec_prefix}/bin
%define _loc_datarootdir  %{_loc_prefix}/share
%define _loc_includedir   %{_loc_prefix}/include
%define _loc_mandir       %{_loc_datarootdir}/man
%define _rpmstatedir      %{_sharedstatedir}/rpm-state
%define _pkgconfigdir     %{_libdir}/pkgconfig

%define __ln              %{_bin}/ln
%define __touch           %{_bin}/touch
%define __service         %{_sbin}/service
%define __chkconfig       %{_sbin}/chkconfig
%define __ldconfig        %{_sbin}/ldconfig
%define __groupadd        %{_sbindir}/groupadd
%define __useradd         %{_sbindir}/useradd

################################################################################

%global pkgname tornado

################################################################################

Summary:            Scalable, non-blocking web server and tools
Name:               python34-%{pkgname}
Version:            5.0.2
Release:            0%{?dist}
License:            ASL 2.0
Group:              Development/Libraries
URL:                http://www.tornadoweb.org

Source0:            https://github.com/tornadoweb/%{pkgname}/archive/v%{version}.tar.gz

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      python34-devel python-setuptools python34-backports_abc
BuildRequires:      python34-backports-ssl_match_hostname python34 gcc

Requires:           python34-backports-ssl_match_hostname
Requires:           python34-pycurl python34-certifi python34

Provides:           %{name} = %{version}-%{release}

################################################################################

%description
Tornado is an open source version of the scalable, non-blocking web
server and tools.

The framework is distinct from most mainstream web server frameworks
(and certainly most Python frameworks) because it is non-blocking and
reasonably fast. Because it is non-blocking and uses epoll, it can
handle thousands of simultaneous standing connections, which means it is
ideal for real-time web services.

################################################################################

%package doc
Summary:            Examples for python34-tornado
Group:              Documentation
Requires:           python34-tornado = %{version}-%{release}

%description doc
Tornado is an open source version of the scalable, non-blocking web
server and and tools. This package contains some example applications.

################################################################################

%prep
%setup -qn %{pkgname}-%{version}

%build
%{__python3} setup.py build

%install
rm -rf %{buildroot}

%{__python3} setup.py install -O1 --skip-build --root %{buildroot}

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc README.rst
%{python3_sitearch}/*

%files doc
%defattr(-,root,root,-)
%doc demos docs

################################################################################

%changelog
* Tue Jun 19 2018 Anton Novojilov <andy@essentialkaos.com> - 5.0.2-0
- Updated to latest stable release

* Tue Jun 19 2018 Anton Novojilov <andy@essentialkaos.com> - 5.0.1-0
- Updated to latest stable release

* Tue Jun 19 2018 Anton Novojilov <andy@essentialkaos.com> - 5.0.0-0
- Updated to latest stable release

* Tue Jun 19 2018 Anton Novojilov <andy@essentialkaos.com> - 4.5.3-1
- Improved spec

* Wed Feb 07 2018 Anton Novojilov <andy@essentialkaos.com> - 4.5.3-0
- Rebuilt for Python 3.4
