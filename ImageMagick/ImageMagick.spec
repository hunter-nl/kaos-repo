###############################################################################

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

###############################################################################

%define pkg_version       6.7.2
%define pkg_patchlevel    7

###############################################################################

Summary:          An X application for displaying and manipulating images
Name:             ImageMagick
Version:          %{pkg_version}.%{pkg_patchlevel}
Release:          11%{?dist}
License:          ImageMagick
Group:            Applications/Multimedia
URL:              http://www.imagemagick.org

Source0:          http://ftp.nluug.nl/pub/%{name}/%{name}-%{pkg_version}-%{pkg_patchlevel}.tar.gz
Source1:          %{name}-policy.xml

BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Patch1:           %{name}-6.4.0-multilib.patch
Patch2:           %{name}-%{pkg_version}-multiarch-fix.patch
Patch3:           %{name}-%{pkg_version}-cve-2012-0247-0248.patch
Patch4:           %{name}-%{pkg_version}-cve-2012-0259-0260.patch
Patch5:           %{name}-%{pkg_version}-cve-2016-5118.patch

BuildRequires:    make gcc gcc-c++
BuildRequires:    bzip2-devel freetype-devel libjpeg-devel libpng-devel
BuildRequires:    libtiff-devel giflib-devel zlib-devel perl-devel
BuildRequires:    ghostscript-devel libwmf-devel jasper-devel
BuildRequires:    libtool-ltdl-devel libX11-devel libXext-devel libXt-devel
BuildRequires:    lcms-devel libxml2-devel librsvg2-devel OpenEXR-devel

Provides:         %{name} = %{version}-%{release}

###############################################################################

%description
ImageMagick is an image display and manipulation tool for the X 
Window System. ImageMagick can read and write JPEG, TIFF, PNM, GIF, 
and Photo CD image formats. It can resize, rotate, sharpen, color 
reduce, or add special effects to an image, and when finished you can 
either save the completed work in the original format or a different 
one. ImageMagick also includes command line programs for creating 
animated or transparent .gifs, creating composite images, creating 
thumbnail images, and more.

ImageMagick is one of your choices if you need a program to manipulate 
and display images. If you want to develop your own applications 
which use ImageMagick code or APIs, you need to install 
ImageMagick-devel as well.

###############################################################################

%package devel
Summary:          Library links and header files for ImageMagick app development
Group:            Development/Libraries
Requires:         %{name} = %{version}-%{release}

Requires:         libX11-devel libXext-devel libXt-devel ghostscript-devel
Requires:         bzip2-devel freetype-devel libtiff-devel libjpeg-devel
Requires:         lcms-devel jasper-devel pkgconfig

%description devel
ImageMagick-devel contains the library links and header files you'll 
need to develop ImageMagick applications. ImageMagick is an image 
manipulation program.

If you want to create applications that will use ImageMagick code or 
APIs, you need to install ImageMagick-devel as well as ImageMagick. 
You do not need to install it if you just want to use ImageMagick, 
however.

###############################################################################

%package doc
Summary:          ImageMagick html documentation
Group:            Documentation

%description doc
ImageMagick documentation, this package contains usage (for the 
commandline tools) and API (for the libraries) documentation in html format. 
Note this documentation can also be found on the ImageMagick website: 
http://www.imagemagick.org

###############################################################################

%package perl
Summary:          ImageMagick perl bindings
Group:            System Environment/Libraries
Requires:         %{name} = %{version}-%{release}
Requires:         perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description perl
Perl bindings to ImageMagick.

Install ImageMagick-perl if you want to use any perl scripts that use 
ImageMagick.

###############################################################################

%package c++
Summary:          ImageMagick Magick++ library (C++ bindings)
Group:            System Environment/Libraries
Requires:         %{name} = %{version}-%{release}

%description c++
This package contains the Magick++ library, a C++ binding to the ImageMagick 
graphics manipulation library. 

Install ImageMagick-c++ if you want to use any applications that use Magick++.

###############################################################################

%package c++-devel
Summary:          C++ bindings for the ImageMagick library
Group:            Development/Libraries

Requires:         %{name}-c++ = %{version}-%{release}
Requires:         %{name}-devel = %{version}-%{release}

%description c++-devel
ImageMagick-devel contains the static libraries and header files you'll 
need to develop ImageMagick applications using the Magick++ C++ bindings. 
ImageMagick is an image manipulation program. 

If you want to create applications that will use Magick++ code 
or APIs, you'll need to install ImageMagick-c++-devel, ImageMagick-devel and 
ImageMagick.
You don't need to install it if you just want to use ImageMagick, or if you 
want to develop/compile applications using the ImageMagick C interface, 
however.

###############################################################################

%prep
%setup -q -n %{name}-%{pkg_version}-%{pkg_patchlevel}

%patch1 -p1 -b .multilib
%patch2 -p1 -b .multiarch-fix
%patch3 -p1 -b .cve-2012-0247-0248
%patch4 -p1 -b .cve-2012-0259-0260
%patch5 -p1 -b .cve-2016-5118

sed -i 's/libltdl.la/libltdl.so/g' configure
iconv -f ISO-8859-1 -t UTF-8 README.txt > README.txt.tmp
touch -r README.txt README.txt.tmp
mv README.txt.tmp README.txt

mkdir Magick++/examples
cp -p Magick++/demo/*.cpp Magick++/demo/*.miff Magick++/examples

%build
%configure --enable-shared \
           --disable-static \
           --with-modules \
           --with-perl \
           --with-x \
           --with-threads \
           --with-magick_plus_plus \
           --with-gslib \
           --with-wmf \
           --with-lcms \
           --with-rsvg \
           --with-xml \
           --with-perl-options="INSTALLDIRS=vendor %{?perl_prefix} CC='%__cc -L$PWD/magick/.libs' LDDLFLAGS='-shared -L$PWD/magick/.libs'" \
           --without-dps \
           --without-included-ltdl --with-ltdl-include=%{_includedir} \
           --with-ltdl-lib=%{_libdir}

# Disable rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

# Do *NOT* use %%{?_smp_mflags}, this causes PerlMagick to be silently misbuild
%{__make}

%install
rm -rf %{buildroot}

%{make_install} INSTALL="install -p"

# Install policy file
install -pm 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/%{name}/policy.xml

cp -a www/source %{buildroot}%{_datadir}/doc/%{name}-%{pkg_version}
rm %{buildroot}%{_libdir}/*.la

# fix weird perl Magick.so permissions
chmod 755 %{buildroot}%{perl_vendorarch}/auto/Image/Magick/Magick.so

# perlmagick: fix perl path of demo files
%{__perl} -MExtUtils::MakeMaker -e 'MY->fixin(@ARGV)' PerlMagick/demo/*.pl

# perlmagick: cleanup various perl tempfiles from the build which get installed
find %{buildroot} -name "*.bs" |xargs rm -f
find %{buildroot} -name ".packlist" |xargs rm -f
find %{buildroot} -name "perllocal.pod" |xargs rm -f

# perlmagick: build files list
echo "%defattr(-,root,root,-)" > perl-pkg-files

find %{buildroot}%{_libdir}/perl* -type f -print \
        | sed "s@^$RPM_BUILD_ROOT@@g" > perl-pkg-files 

find %{buildroot}%{perl_vendorarch} -type d -print \
        | sed "s@^$RPM_BUILD_ROOT@%dir @g" \
        | grep -v '^%dir %{perl_vendorarch}$' \
        | grep -v '/auto$' >> perl-pkg-files 

if [[ -z perl-pkg-files ]] ; then
    echo "ERROR: EMPTY FILE LIST"
    exit 1
fi

# fix multilib issues
%ifarch x86_64 s390x ia64 ppc64 alpha sparc64
%define wordsize 64
%else
%define wordsize 32
%endif

mv %{buildroot}%{_includedir}/%{name}/magick/magick-config.h \
   %{buildroot}%{_includedir}/%{name}/magick/magick-config-%{wordsize}.h

cat >%{buildroot}%{_includedir}/%{name}/magick/magick-config.h <<EOF
#ifndef IMAGEMAGICK_MULTILIB
#define IMAGEMAGICK_MULTILIB

#include <bits/wordsize.h>

#if __WORDSIZE == 32
# include "magick-config-32.h"
#elif __WORDSIZE == 64
# include "magick-config-64.h"
#else
# error "unexpected value for __WORDSIZE macro"
#endif

#endif
EOF

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%post c++ -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%postun c++ -p /sbin/ldconfig

###############################################################################

%files
%defattr(-,root,root,-)
%doc QuickStart.txt ChangeLog Platforms.txt
%doc README.txt LICENSE NOTICE AUTHORS.txt NEWS.txt
%{_libdir}/libMagickCore.so.*
%{_libdir}/libMagickWand.so.*
%{_bindir}/[a-z]*
%{_libdir}/%{name}-%{pkg_version}
%{_datadir}/%{name}-%{pkg_version}
%{_mandir}/man[145]/[a-z]*
%{_mandir}/man1/%{name}.*
%{_sysconfdir}/%{name}

%files devel
%defattr(-,root,root,-)
%{_bindir}/MagickCore-config
%{_bindir}/Magick-config
%{_bindir}/MagickWand-config
%{_bindir}/Wand-config
%{_libdir}/libMagickCore.so
%{_libdir}/libMagickWand.so
%{_libdir}/pkgconfig/MagickCore.pc
%{_libdir}/pkgconfig/ImageMagick.pc
%{_libdir}/pkgconfig/MagickWand.pc
%{_libdir}/pkgconfig/Wand.pc
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/magick
%{_includedir}/%{name}/wand
%{_mandir}/man1/Magick-config.*
%{_mandir}/man1/MagickCore-config.*
%{_mandir}/man1/Wand-config.*
%{_mandir}/man1/MagickWand-config.*

%files doc
%defattr(-,root,root,-)
%doc %{_datadir}/doc/%{name}-%{pkg_version}

%files c++
%defattr(-,root,root,-)
%doc Magick++/AUTHORS Magick++/ChangeLog Magick++/NEWS Magick++/README
%doc www/Magick++/COPYING
%{_libdir}/libMagick++.so.*

%files c++-devel
%defattr(-,root,root,-)
%doc Magick++/examples
%{_bindir}/Magick++-config
%{_includedir}/%{name}/Magick++
%{_includedir}/%{name}/Magick++.h
%{_libdir}/libMagick++.so
%{_libdir}/pkgconfig/Magick++.pc
%{_libdir}/pkgconfig/ImageMagick++.pc
%{_mandir}/man1/Magick++-config.*

%files perl -f perl-pkg-files
%defattr(-,root,root,-)
%{_mandir}/man3/*
%doc PerlMagick/demo/ PerlMagick/Changelog PerlMagick/README.txt

###############################################################################

%changelog
* Wed Jun 01 2016 Anton Novojilov <andy@essentialkaos.com> - 6.7.2.7-11
- Added fix for CVE-2016-5118 vulnerability

* Wed May 04 2016 Anton Novojilov <andy@essentialkaos.com> - 6.7.2.7-10
- Refactored spec for kaos repo