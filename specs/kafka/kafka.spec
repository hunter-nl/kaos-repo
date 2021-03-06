################################################################################

%define _posixroot        /
%define _root             /root
%define _bin              /bin
%define _sbin             /sbin
%define _srv              /srv
%define _home             /home
%define _opt              /opt
%define _lib32            %{_posixroot}lib
%define _lib64            %{_posixroot}lib64
%define _libdir32         %{_prefix}%{_lib32}
%define _libdir64         %{_prefix}%{_lib64}
%define _logdir           %{_localstatedir}/log
%define _datadir          %{_localstatedir}/lib
%define _rundir           %{_localstatedir}/run
%define _lockdir          %{_localstatedir}/lock/subsys
%define _cachedir         %{_localstatedir}/cache
%define _spooldir         %{_localstatedir}/spool
%define _crondir          %{_sysconfdir}/cron.d
%define _logrotatedir     %{_sysconfdir}/logrotate.d
%define _sysconfigdir     %{_sysconfdir}/sysconfig
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

################################################################################

%define __ln              %{_bin}/ln
%define __touch           %{_bin}/touch
%define __service         %{_sbin}/service
%define __chkconfig       %{_sbin}/chkconfig
%define __useradd         %{_sbindir}/useradd
%define __groupadd        %{_sbindir}/groupadd
%define __getent          %{_bindir}/getent
%define __systemctl       %{_bindir}/systemctl

################################################################################

%define major_version     2.11
%define user_name         kafka
%define group_name        kafka
%define service_name      kafka
%define home_dir          %{_opt}/%{name}

################################################################################

Summary:             A high-throughput distributed messaging system
Name:                kafka
Version:             1.1.1
Release:             0%{?dist}
License:             APL v2
Group:               Applications/Databases
URL:                 https://kafka.apache.org

Source0:             https://github.com/apache/%{name}/archive/%{version}.tar.gz
Source1:             %{name}.init
Source2:             %{name}.service
Source3:             %{name}.conf
Source4:             %{name}.logrotate
Source5:             %{name}.sysconfig

BuildRoot:           %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:           noarch

%if 0%{?rhel} <= 6
Requires:            kaosv
%else
Requires:            systemd
%endif

BuildRequires:       java-devel gradle which

%if 0%{?rhel} <= 6
Requires(post):      %{__chkconfig} initscripts
Requires(pre):       %{__chkconfig} initscripts
%else
%systemd_requires
%endif

Provides:            %{name} = %{version}-%{release}

################################################################################

%description
Apache Kafka is a distributed publish-subscribe messaging system. It
is designed to support the following:

* Persistent messaging with O(1) disk structures that provide constant
  time performance even with many TB of stored messages.
* High-throughput: even with very modest hardware Kafka can support
  hundreds of thousands of messages per second.
* Explicit support for partitioning messages over Kafka servers and
  distributing consumption over a cluster of consumer machines while
  maintaining per-partition ordering semantics.
* Support for parallel data load into Hadoop.

################################################################################

%package server
Summary:             Kafka server
Group:               Applications/Databases

BuildArch:           noarch

Requires:            kafka

%description server
Configuration and startup files for Apache Kafka broker.

################################################################################

%prep
%setup -q

%build
export PATH=$PATH:/opt/gradle/current/bin
gradle releaseTarGz

pushd core/build/distributions
  tar xvfz %{name}_%{major_version}-%{version}.tgz
popd

%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_opt}/%{name}
install -dm 755 %{buildroot}%{_datadir}/%{name}
install -dm 755 %{buildroot}%{_logdir}/%{name}
install -dm 755 %{buildroot}%{_sysconfdir}/%{name}
install -dm 755 %{buildroot}%{_localstatedir}/%{name}
install -dm 755 %{buildroot}%{_logrotatedir}
install -dm 755 %{buildroot}%{_sysconfigdir}
%if 0%{?rhel} <= 6
install -dm 755 %{buildroot}%{_initrddir}/
%else
install -dm 755 %{buildroot}%{_unitdir}/
%endif

%if 0%{?rhel} <= 6
install -pm 755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}
%else
install -pm 755 %{SOURCE2} %{buildroot}%{_unitdir}/%{name}.service
%endif
install -pm 755 %{SOURCE3} %{buildroot}%{_sysconfdir}/%{name}
install -pm 644 %{SOURCE4} %{buildroot}%{_logrotatedir}/%{name}
install -pm 644 %{SOURCE5} %{buildroot}%{_sysconfigdir}/%{name}

pushd core/build/distributions/%{name}_%{major_version}-%{version}
  mv bin %{buildroot}%{_opt}/%{name}
  mv libs %{buildroot}%{_opt}/%{name}
  mv config %{buildroot}%{_opt}/%{name}
popd

# Remove Windows scripts
rm -rf %{_opt}/%{name}/bin/windows

%clean
rm -rf %{buildroot}

################################################################################

%pre server
getent group %{group_name} >/dev/null || %{__groupadd} -r %{group_name}
getent passwd %{user_name} >/dev/null || %{__useradd} -s /sbin/nologin -M -r -g %{group_name} -d %{home_dir} %{user_name}
exit 0

%post server
if [[ $1 -eq 1 ]] ; then
%if 0%{?rhel} <= 6
  %{__chkconfig} --add %{service_name}
%else
  %{__systemctl} enable %{name}.service &>/dev/null || :
%endif
fi

%preun server
if [[ $1 -eq 0 ]] ; then
%if 0%{?rhel} <= 6
  %{__service} %{service_name} stop &>/dev/null || :
  %{__chkconfig} --del %{service_name}
%else
  %{__systemctl} --no-reload disable %{name}.service &>/dev/null || :
  %{__systemctl} stop %{name}.service &>/dev/null || :
%endif
fi

%postun server
%if 0%{?rhel} >= 7
if [[ $1 -ge 1 ]] ; then
  %{__systemctl} daemon-reload &>/dev/null || :
fi
%endif

################################################################################

%files
%defattr(-,root,root,-)
%{home_dir}

%files server
%defattr(-,%{user_name},%{group_name},-)
%dir %{_datadir}/%{name}
%dir %{_logdir}/%{name}
%dir %{_localstatedir}/%{name}
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/*.conf

%defattr(-,root,root,-)
%if 0%{?rhel} <= 6
%{_initrddir}/%{name}
%else
%{_unitdir}/%{name}.service
%endif
%config(noreplace) %{_logrotatedir}/%{name}
%config(noreplace) %{_sysconfigdir}/%{name}

################################################################################

%changelog
* Wed Sep 05 2018 Anton Novojilov <andy@essentialkaos.com> - 1.1.1-0
- Updated to latest release

* Sun Jun 17 2018 Anton Novojilov <andy@essentialkaos.com> - 1.1.0-0
- Updated to latest release

* Mon Mar 12 2018 Gleb Goncharov <g.goncharov@fun-box.ru> - 1.0.1-0
- Updated to latest release

* Wed Nov 08 2017 Gleb Goncharov <g.goncharov@fun-box.ru> - 1.0.0-0
- Updated to latest release

* Sat Sep 16 2017 Anton Novojilov <andy@essentialkaos.com> - 0.11.0.1-0
- Updated to latest release

* Sun Jul 09 2017 Anton Novojilov <andy@essentialkaos.com> - 0.11.0.0-0
- Updated to latest release

* Tue May 09 2017 Anton Novojilov <andy@essentialkaos.com> - 0.10.2.1-0
- Updated to latest release

* Tue Mar 21 2017 Anton Novojilov <andy@essentialkaos.com> - 0.10.2.0-0
- Updated to latest release

* Sat Jan 21 2017 Anton Novojilov <andy@essentialkaos.com> - 0.10.1.1-0
- Updated to latest release

* Wed Nov 09 2016 Anton Novojilov <andy@essentialkaos.com> - 0.10.1.0-0
- Updated to latest release

* Mon Sep 05 2016 Anton Novojilov <andy@essentialkaos.com> - 0.10.0.1-0
- Updated to latest release

* Sat Jun 18 2016 Anton Novojilov <andy@essentialkaos.com> - 0.10.0.0-0
- Updated to latest release

* Fri Apr 01 2016 Gleb Goncharov <ggoncharov@fun-box.ru> - 0.9.0.1-0
- Updated to latest release

* Thu Jun 25 2015 Anton Novojilov <anovojilov@fun-box.ru> - 0.8.2.1-0
- Initial build
