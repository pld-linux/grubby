#
# Conditional build:
%bcond_without	tests		# skip tests
#
Summary:	Command line tool for configuring grub, lilo, and elilo
Summary(pl.UTF-8):	Działające z linii poleceń narzędzie do konfiguracji gruba, lilo i elilo
Name:		grubby
Version:	6.0.24
Release:	3
License:	GPL v2
Group:		Base
Source0:	mkinitrd-%{version}.tar.bz2
# Source0-md5:	4bcef73138bb05da98e54cbfe48cb8f1
Patch0:		%{name}-menu.lst.patch
Patch1:		%{name}-pld.patch
Patch2:		%{name}-geninitrd.patch
Patch3:		%{name}-c99.patch
Patch4:		%{name}-pic.patch
BuildRequires:	device-mapper-devel
BuildRequires:	e2fsprogs-devel
BuildRequires:	libdhcp-devel > 1.9
BuildRequires:	parted-devel >= 1.8.5
BuildRequires:	popt-devel
Requires:	geninitrd >= 10000.3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin

%description
grubby is a command line tool for updating and displaying information
about the configuration files for the grub, lilo, elilo (ia64), and
yaboot (powerpc) boot loaders. It is primarily designed to be used
from scripts which install new kernels and need to find information
about the current boot environment.

%description -l pl.UTF-8
grubby to działające z linii poleceń narzędzie do uaktualniania i
wyświetlania informacji o plikach konfiguracyjnych bootloaderów grub,
lilo, elilo (na architekturze ia64) oraz yaboot (na powerpc). Jest
zaprojektowany głównie do używania z poziomu skryptów instalujących
nowe jądra i potrzebujących odczytać informacje o aktualnym środowisku
startowym.

%package -n bdevid
Summary:	Boot-time device identification
Summary(pl.UTF-8):	Identyfikacja urządzeń w trakcie startu systemu
Group:		Base
Requires:	bdevid-libs = %{version}-%{release}

%description -n bdevid
Boot-time device identification.

%description -n bdevid -l pl.UTF-8
Identyfikacja urządzeń w trakcie startu systemu.

%package -n bdevid-libs
Summary:	Boot-time device identification library
Summary(pl.UTF-8):	Biblioteka do identyfikacji urządzeń w trakcie startu systemu
Group:		Libraries

%description -n bdevid-libs
Boot-time device identification library.

%description -n bdevid-libs -l pl.UTF-8
Biblioteka do identyfikacji urządzeń w trakcie startu systemu.

%package -n bdevid-devel
Summary:	Development files for bdevid library
Summary(pl.UTF-8):	Pliki programistyczne biblioteki bdevid
Group:		Development/Libraries
Requires:	bdevid-libs = %{version}-%{release}

%description -n bdevid-devel
Development files for bdevid library.

%description -n bdevid-devel -l pl.UTF-8
Pliki programistyczne biblioteki bdevid.

%package -n python-bdevid
Summary:	Python bindings for bdevid
Summary(pl.UTF-8):	Wiązania Pythona do biblioteki bdevid
Group:		Libraries/Python
Requires:	bdevid-libs = %{version}-%{release}
Requires:	nash-libs = %{version}-%{release}

%description -n python-bdevid
Python bindings for bdevid.

%description -n python-bdevid -l pl.UTF-8
Wiązania Pythona do biblioteki bdevid.

%package -n nash-libs
Summary:	Nash library
Summary(pl.UTF-8):	Biblioteka nash
Group:		Libraries

%description -n nash-libs
Nash library.

%description -n nash-libs -l pl.UTF-8
Biblioteka nash.

%package -n nash-devel
Summary:	Header files for nash library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki nash
Group:		Development/Libraries
Requires:	nash-libs = %{version}-%{release}

%description -n nash-devel
Header files for nash library.

%description -n nash-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki nash.

%prep
%setup -q -n mkinitrd-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
CFLAGS="%{rpmcflags}"; export CFLAGS
%{__make} \
	CC="%{__cc}" \
	LIB=%{_lib}

%if %{with tests}
%{__make} test
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	LIB=%{_lib} \
	mandir=%{_mandir}

install installkernel $RPM_BUILD_ROOT%{_sbindir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n bdevid-libs -p /sbin/ldconfig
%postun	-n bdevid-libs -p /sbin/ldconfig

%post	-n nash-libs -p /sbin/ldconfig
%postun	-n nash-libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/new-kernel-pkg
%attr(755,root,root) %{_sbindir}/grubby
%attr(755,root,root) %{_sbindir}/installkernel
%{_mandir}/man8/grubby.8*

%files -n bdevid
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/bdevid

%files -n bdevid-libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbdevid.so.%{version}
%dir /%{_lib}/bdevid
%attr(755,root,root) /%{_lib}/bdevid/*.so

%files -n bdevid-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbdevid.so
%attr(755,root,root) %{_libdir}/libbdevidprobe.a
%{_includedir}/bdevid.h
%{_includedir}/bdevid
%{_pkgconfigdir}/libbdevid.pc
%{_pkgconfigdir}/libbdevidprobe.pc

%files -n python-bdevid
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/bdevid.so

%files -n nash-libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnash.so.%{version}

%files -n nash-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnash.so
%{_includedir}/blkent.h
%{_includedir}/nash.h
%{_includedir}/nash
%{_pkgconfigdir}/libnash.pc
