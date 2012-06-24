# Conditional build:
%bcond_without	tests		# skip tests
#
Summary:	Command line tool for configuring grub, lilo, and elilo
Summary(pl):	Dzia�aj�ce z linii polece� narz�dzie do konfiguracji gruba, lilo i elilo
Name:		grubby
Version:	5.0.4
Release:	3
License:	GPL
Group:		Base
Source0:	mkinitrd-%{version}.tar.bz2
# Source0-md5:	2ba9ccda4f10e80239ca86fed9bb81d0
Patch0:		%{name}-menu.lst.patch
Patch1:		%{name}-pld.patch
Patch2:		%{name}-geninitrd.patch
Patch3:		%{name}-poptshared.patch
Patch4:		%{name}-xen.patch
BuildRequires:	popt-devel
Requires:	geninitrd >= 8243
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin

%description
grubby is a command line tool for updating and displaying information
about the configuration files for the grub, lilo, elilo (ia64), and
yaboot (powerpc) boot loaders. It is primarily designed to be used
from scripts which install new kernels and need to find information
about the current boot environment.

%description -l pl
grubby to dzia�aj�ce z linii polece� narz�dzie do uaktualniania i
wy�wietlania informacji o plikach konfiguracyjnych bootloader�w grub,
lilo, elilo (na architekturze ia64) oraz yaboot (na powerpc). Jest
zaprojektowany g��wnie do u�ywania z poziomu skrypt�w instaluj�cych
nowe j�dra i potrzebuj�cych odczyta� informacje o aktualnym �rodowisku
startowym.

%prep
%setup -q -n mkinitrd-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
cd %{name}
%{__make} CC="%{__cc}"

%if %{with tests}
%{__make} test
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C %{name} install \
	BUILDROOT=$RPM_BUILD_ROOT \
	mandir=%{_mandir}

install installkernel $RPM_BUILD_ROOT%{_sbindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/new-kernel-pkg
%attr(755,root,root) %{_sbindir}/grubby
%attr(755,root,root) %{_sbindir}/installkernel
%{_mandir}/man8/grubby.8*
