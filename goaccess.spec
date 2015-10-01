########################################################################################

Summary:         Real-time web log analyzer and interactive viewer
Name:            goaccess
Version:         0.9.3
Release:         0%{?dist}
Group:           Development/Tools
License:         GPLv2+
URL:             http://goaccess.io

Source0:         http://tar.goaccess.io/goaccess-%{version}.tar.gz

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:        GeoIP
BuildRequires:   GeoIP-devel glib2-devel ncurses-devel

########################################################################################

%description
Open source real-time web log analyzer and interactive viewer that runs
in a terminal in *nix systems. It provides fast and valuable HTTP statistics
for system administrators that require a visual server report on the fly.

########################################################################################

%prep
%setup -q

%build
%configure --enable-debug --enable-geoip --enable-utf8

%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}
%{__make} DESTDIR=%{buildroot} install

%clean
rm -rf %{buildroot}

########################################################################################

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README TODO
%config(noreplace) %{_sysconfdir}/%{name}.conf
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*

########################################################################################

%changelog
* Fri Sep 04 2015 Anton Novojilov <andy@essentialkaos.com> - 0.9.3-0
- Added the ability to set custom colors on the terminal output.
- Added the ability to process logs incrementally.
- Added a default color palette (Monokai) to the config file.
- Added column headers for every enabled metric on each panel.
- Added cumulative time served metric.
- Added maximum time served metric (slowest running requests).
- Added the ability to parse the query string specifier '(prc)q' from a log file.
- Added CloudFlare status codes.
- Added command option to disable column name metrics --no-column-names.
- Added AWS Elastic Load Balancing to the list of predefined log/date/time
    formats.
- Added DragonFly BSD to the list of OSs.
- Added Slackbot to the list of crawlers/browsers.
- Disabled REFERRERS by default.
- Ensure bandwidth metric is displayed only if the (prc)b specifier is parsed.
- Fixed issue where the '--sort-panel' option wouldn't sort certain panels.
- Fixed several compiler warnings.
- Set predefined static files when no config file is used.
- Updated Windows 10 user agent from 6.4 (wrong) to 10.0.(actual)

* Mon Jul 06 2015 Anton Novojilov <andy@essentialkaos.com> - 0.9.2-0
- Added ability to fully parse browsers that contain spaces within a token.
- Added multiple user agents to the list of browsers.
- Added the ability to handle time served in milliseconds.
- Added the ability to parse a timestamp in microseconds.
- Added the ability to parse Google Cloud Storage access logs.
- Added the ability to set a custom title and header in the HTML report.
- Added timestamp log-format specifier.
- Ensure agents' hash table is destroyed upon exiting the program.
- Ensure 'Game Systems' are processed correctly.
- Ensure visitors panel header is updated depending if crawlers are parsed or not.
- Fixed issue where the date value was set as time value  in the config dialog.
- Fixed memory leak in the hits metrics when using the in-memory storage (GLib).

* Wed Jul 01 2015 Anton Novojilov <andy@essentialkaos.com> - 0.9.1-0
- Added additional Nginx-specific status codes.
- Added Applebot to the list of web crawlers.
- Added Microsoft Edge to the list of browsers.
- Added the ability to highlight active panel through --hl-header.
- Ensure dump_struct is used only if using __GLIBC__.
- Ensure goaccess image has an alt attribute on the HTML output for valid HTML5.
- Ensure the config file path is displayed when something goes wrong (FATAL).
- Ensure there is a character indicator to see which panel is active.
- Fixed Cygwin compile issue attempting to use -rdynamic.
- Fixed issue where a single IP did not get excluded after an IP range.
- Fixed issue where requests show up in the wrong view even when --no-query-string is used.
- Fixed issue where some browsers were not recognized or marked as 'unknown'.
- Fixed memory leak when excluding an IP range.
- Fixed overflows on sort comparison functions.
- Fixed segfault when using on-disk storage and loading persisted data with -a.
- Removed keyphrases menu item from HTML output.
- Split iOS devices from Mac OS X.

* Thu Mar 19 2015 Anton Novojilov <andy@essentialkaos.com> - 0.9-0
- Added ability to double decode an HTTP referer and agent
- Added ability to sort views through the command line on initial load
- Added additional data values to the backtrace report
- Added additional graph to represent the visitors metric on the HTML output
- Added AM_PROG_CC_C_O to configure.ac
- Added 'Android Lollipop' to the list of operating systems
- Added 'average time served' metric to all panels
- Added 'bandwidth' metric to all panels
- Added command line option to disable summary metrics on the CSV output
- Added numeric formatting to the HTML output to improve readability
- Added request method specifier to the default W3C log format
- Added support for GeoIP Country IPv6 and GeoIP City IPv6 through --geoip-database
- Added the ability to ignore parsing and displaying given panel(s)
- Added the ability to ignore referer sites from being counted
    A good case scenario is to ignore own domains. i.e., owndomain.tld
    This also allows ignoring hosts using wildcards
    For instance, *.mydomain.tld or www.mydomain.* or www?.mydomain.tld
- Added time/hour distribution module. e.g., 00-23
- Added 'visitors' metrics to all panels
- Added Windows 10 (v6.4) to the real windows user agents
- Changed AC_PREREQ macro version so it builds on old versions of autoconf
- Changed GEOIP database load to GEOIP_MEMORY_CACHE for faster lookups
- Changed maximum number of choices to display per panel to 366 fron 300
- Ensure config file is read from home dir if unable to open it from sysconfdir path
- Fixed array overflows when exceeding MAX_* limits on command line options
- Fixed a SEGFAULT where sscanf could not handle special chars within the referer
- Fixed character encoding on geolocation output (ISO-8859 to UTF8)
- Fixed issue on wild cards containing '?' at the end of the string
- Fixed issue where a 'Nothing valid to process' error was triggered when the
    number of invalid hits was equal to the number of valid hits
- Fixed issue where outputting to a file left a zero-byte file in pwd
- Improved parsing of operating systems
- Refactored log parser so it allows with ease the addition of new modules. This
    also attempts to decouple the core functionality from the rendering functions
    It also gives the flexibility to add children metrics to root metrics for any
    module. e.g., Request A was visited by IP1, IP2, IP3, etc
- Restyled HTML output

* Fri Feb 20 2015 Anton Novojilov <andy@essentialkaos.com> - 0.8.5-0
- Initial build
