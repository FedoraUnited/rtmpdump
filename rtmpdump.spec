# Patches and tips thanks to Debian
# https://anonscm.debian.org/git/pkg-multimedia/rtmpdump.git/tree/

%global commit fa8646daeb19dfd12c181f7d19de708d623704c0
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global gitdate 20151223

Name:           rtmpdump
Version:        2.4
Release:        8.%{gitdate}.git%{shortcommit}%{?dist}
Summary:        Toolkit for RTMP streams

Group:          Applications/Internet
# The tools are GPLv2+. The library is LGPLv2+, see below.
License:        GPLv2+
URL:            http://rtmpdump.mplayerhq.hu/
Source0:        http://repo.or.cz/w/rtmpdump.git/snapshot/fa8646daeb19dfd12c181f7d19de708d623704c0.tar.gz
Patch0: 	01_unbreak_makefile.diff
Patch1: 	02_gnutls_requires.private.diff
Patch2: 	03_suppress_warning.diff

BuildRequires:  gnutls-devel
BuildRequires:  libgcrypt-devel
BuildRequires:  zlib-devel
BuildRequires:  nettle-devel
BuildRequires:	openssl-devel

%description
rtmpdump is a toolkit for RTMP streams. All forms of RTMP are supported,
including rtmp://, rtmpt://, rtmpe://, rtmpte://, and rtmps://. 

%package -n librtmp
Summary:        Support library for RTMP streams
Group:          Applications/Internet
License:        LGPLv2+

%description -n librtmp
librtmp is a support library for RTMP streams. All forms of RTMP are supported,
including rtmp://, rtmpt://, rtmpe://, rtmpte://, and rtmps://. 

%package -n librtmp-devel
Summary:        Files for librtmp development
Group:          Applications/Internet
License:        LGPLv2+
Requires:       librtmp%{?_isa} = %{version}-%{release}

%description -n librtmp-devel
librtmp is a support library for RTMP streams. The librtmp-devel package
contains include files needed to develop applications using librtmp.

%prep
%autosetup -n %{name}-%{shortcommit} -p1


%build

make prefix=%{_prefix} CRYPTO=GNUTLS libdir=%{_libdir} XCFLAGS="-g -O2 -fstack-protector-strong -Wformat -Werror=format-security -D_FORTIFY_SOURCE=2" XLDFLAGS="-Wl,-z,relro"


%install
make CRYPTO=GNUTLS SHARED=yes DESTDIR=%{buildroot} prefix=%{_prefix} mandir=%{_mandir} libdir=%{_libdir} install
rm -f %{buildroot}%{_libdir}/librtmp.a

%post -n librtmp -p /sbin/ldconfig
%postun -n librtmp -p /sbin/ldconfig

%files
%doc COPYING README
%{_bindir}/rtmpdump
%{_sbindir}/rtmpsrv
%{_sbindir}/rtmpgw
%{_sbindir}/rtmpsuck
%{_mandir}/man1/rtmpdump.1*
%{_mandir}/man8/rtmpgw.8*

%files -n librtmp
%doc librtmp/COPYING ChangeLog
%{_libdir}/librtmp.so.1

%files -n librtmp-devel
%{_includedir}/librtmp/
%{_libdir}/librtmp.so
%{_libdir}/pkgconfig/librtmp.pc
%{_mandir}/man3/librtmp.3*

%changelog

* Fri Aug 25 2017 David Vásquez <davidjeremias82 AT gmail DOT com> - 2.4-8.20151223gitfa8646d
- Rebuilt for Fedora 28
- Patches from Debian

* Fri Jul 08 2016 David Vásquez <davidjeremias82 AT gmail DOT com> - 2.4-6.20151223gitfa8646d
- Massive rebuild

* Tue Feb 23 2016 David Vásquez <davidjeremias82 AT gmail DOT com> - 2.4-5.20151223.gitfa8646d
- Updated to 2.4-5.20151223.gitfa8646d

* Fri Nov 27 2015 Susi Lehtola <jussilehtola@fedoraproject.org> - 2.4-5.20150925.gita107cef
- Fix name of tarball in Sérgio's patch.

* Fri Sep 25 2015 Sérgio Basto <sergio@serjux.com> - 2.4-4.20150925.gita107cef
- Update to git dc76f0a, Jan 14 2015

* Mon Sep 01 2014 Sérgio Basto <sergio@serjux.com> - 2.4-3.20131205.gitdc76f0a
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Apr 26 2014 Nicolas Chauvet <kwizart@gmail.com> - 2.4-2.20131205.gitdc76f0a
- Rebuilt for libgcrypt

* Sun Jan 5 2014 Susi Lehtola <jussilehtola@fedoraproject.org> - 2.4-1.20131205.gitdc76f0a
- Update to newest snapshot.
- Clean up spec file.

* Sun Mar 03 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.4-0.3.20110811gitc58cfb3e
- Mass rebuilt for Fedora 19 Features

* Wed Jan 25 2012 Nicolas Chauvet <kwizart@gmail.com> - 2.4-0.2.20110811gitc58cfb3e
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Aug 29 2011 David Woodhouse <dwmw2@infradead.org> 2.4-0.1.20110811gitc58cfb3e
- Update to almost-2.4 snapshot

* Sun Jul 04 2010 Dominik Mierzejewski <rpm@greysector.net> 2.3-2
- call ldconfig in post(un) scripts for the shared library
- add strict dependency on the library to -devel

* Sun Jul 04 2010 David Woodhouse <dwmw2@infradead.org> 2.3-1
- Update to 2.3; build shared library

* Fri Apr 30 2010 David Woodhouse <dwmw2@infradead.org> 2.2d-1
- Update to 2.2d

* Tue Apr 20 2010 David Woodhouse <dwmw2@infradead.org> 2.2c-2
- Link with libgcrypt explicitly since we call it directly

* Mon Apr 19 2010 David Woodhouse <dwmw2@infradead.org> 2.2c-1
- Initial package
