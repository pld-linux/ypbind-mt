Summary:	The NIS daemon which binds NIS clients to an NIS domain
Name:		ypbind-mt
Version:	1.8
Release:	2
License:	GPL
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
Source0:	ftp://ftp.us.kernel.org/pub/linux/utils/net/NIS/%{name}-%{version}.tar.bz2
Source1:	ypbind.init
Source2:	yp.conf
Patch0:		%{name}-pthread.patch
Patch1:		%{name}-broadcast.patch
Buildrequires:	autoconf
Buildrequires:	automake
Buildrequires:	bison
Buildrequires:	gettext-devel
Prereq:		/sbin/chkconfig
Requires:	portmap
Requires:	yp-tools
Prereq:		rc-scripts
Requires:	nss_nis
Provides:	ypbind
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	ypbind

%define		_sbindir	/sbin

%description
The Network Information Service (NIS) is a system which provides
network information (login names, passwords, home directories, group
information) to all of the machines on a network. NIS can enable users
to login on any machine on the network, as long as the machine has the
NIS client programs running and the user's password is recorded in the
NIS passwd database. NIS was formerly known as Sun Yellow Pages (YP).

This package provides the ypbind daemon. The ypbind daemon binds NIS
clients to an NIS domain. Ypbind must be running on any machines which
are running NIS client programs.

Install the ypbind package on any machines which are running NIS
client programs (included in the yp-tools package). If you need an NIS
server, you'll also need to install the ypserv package to a machine on
your network.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
gettextize --copy --force
aclocal
autoconf
automake -a -c
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/{etc/rc.d/init.d,var/yp/binding}
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/ypbind
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/yp.conf

gzip -9nf README

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add ypbind

if [ -f /var/lock/subsys/ypbind ]; then
	/etc/rc.d/init.d/ypbind restart >&2
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/ypbind ]; then
		/etc/rc.d/init.d/ypbind stop >&2
	fi
	/sbin/chkconfig --del ypbind
fi

%triggerpostun -- ypbind <= ypbind-3.3-5
/sbin/chkconfig --add ypbind

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc *.gz
%attr(755,root,root) %{_sbindir}/ypbind
%attr(754,root,root) /etc/rc.d/init.d/*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/yp.conf
%{_mandir}/man[58]/*
%dir /var/yp/binding
