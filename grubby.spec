# TODO
# - Can't find Source URL
# Conditional build:
%bcond_without	tests		# skip tests
Summary:	Command line tool for configuring grub, lilo, and elilo.
Name:		grubby
Version:	4.1.18
Release:	0.2
Epoch:		0
License:	GPL
Group:		System Environment/Base
Source0:	mkinitrd-%{version}.tar.bz2
# Source0-md5:	42714d928e2725ab1180bfc78b851c9d
Patch0:		%{name}-menu.lst.patch
Patch1:		%{name}-pld.patch 
Patch2:		%{name}-geninitrd.patch
Patch3:		%{name}-no-nash.patch
Requires:	geninitrd
Obsoletes:	mkinitrd
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define _sbindir /sbin

%description
grubby is a command line tool for updating and displaying information
about the configuration files for the grub, lilo, elilo (ia64), and
yaboot (powerpc) boot loaders. It is primarily designed to be used
from scripts which install new kernels and need to find information
about the current boot environment.

%prep
%setup -q -n mkinitrd-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
cd %{name}
%{__make}

%if %{with tests}
%{__make} test
%endif

%install
rm -rf $RPM_BUILD_ROOT
cd %{name}
%{__make} install \
	BUILDROOT=$RPM_BUILD_ROOT \
	mandir=%{_mandir}
cd ..

install installkernel $RPM_BUILD_ROOT%{_sbindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/new-kernel-pkg
%attr(755,root,root) %{_sbindir}/grubby
%config %attr(755,root,root) /sbin/installkernel
%{_mandir}/man8/grubby.8*
