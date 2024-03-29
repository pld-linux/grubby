#
# Conditional build:
%bcond_without	tests		# skip tests

Summary:	Command line tool for updating bootloader configs
Summary(pl.UTF-8):	Działające z linii poleceń narzędzie do konfiguracji gruba, lilo i elilo
Name:		grubby
Version:	8.11
Release:	1
License:	GPL v2
Group:		Base
Source0:	http://pkgs.fedoraproject.org/repo/pkgs/grubby/%{name}-%{version}.tar.bz2/953e26ec497abc2d27254d1b2ea4fd4b/%{name}-%{version}.tar.bz2
# Source0-md5:	953e26ec497abc2d27254d1b2ea4fd4b
URL:		http://git.fedorahosted.org/git/grubby.git
Patch0:		%{name}-menu.lst.patch
Patch1:		%{name}-pld.patch
Patch2:		%{name}-geninitrd.patch
BuildRequires:	glib2-devel
BuildRequires:	libblkid-devel
BuildRequires:	pkgconfig
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

%prep
%setup -q
%patch0 -p1
%patch1 -p2
%patch2 -p1

%build
%{__make} \
	CC="%{__cc}" \
	RPM_OPT_FLAGS="%{rpmcflags} -fno-strict-aliasing "

%if %{with tests}
%{__make} test
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	mandir=%{_mandir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/new-kernel-pkg
%attr(755,root,root) %{_sbindir}/grubby
%attr(755,root,root) %{_sbindir}/installkernel
%{_mandir}/man8/grubby.8*
%{_mandir}/man8/installkernel.8*
%{_mandir}/man8/new-kernel-pkg.8*
