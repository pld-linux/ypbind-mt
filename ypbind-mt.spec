Summary:	The NIS daemon which binds NIS clients to an NIS domain.
Name:		ypbind-mt
Version:	1.6
Release:	2
Copyright:	GPL
Group:		System Environment/Daemons
Source0:	ftp://ftp.us.kernel.org/pub/linux/NIS/%{name}-%{version}.tar.gz
Source1:	ypbind.init
Source2:	yp.conf
Prereq:		/sbin/chkconfig
Requires:	portmap
Requires:	yp-tools
Requires:	rc-scripts
Provides:	ypbind
Obsoletes:	ypbind
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Network Information Service (NIS) is a system which provides network
information (login names, passwords, home directories, group information)
to all of the machines on a network.  NIS can enable users to login on
any machine on the network, as long as the machine has the NIS client
programs running and the user's password is recorded in the NIS passwd
database.  NIS was formerly known as Sun Yellow Pages (YP).

This package provides the ypbind daemon.  The ypbind daemon binds NIS
clients to an NIS domain.  Ypbind must be running on any machines which
are running NIS client programs.

Install the ypbind package on any machines which are running NIS client
programs (included in the yp-tools package).  If you need an NIS server,
you'll also need to install the ypserv package to a machine on your
network.

%prep
%setup -q

%build
%configure
make

%install
rm -rf $RPM_BUILD_ROOT
make install \
	prefix=$RPM_BUILD_ROOT/usr \
	sbindir=$RPM_BUILD_ROOT/sbin \
	mandir=$RPM_BUILD_ROOT/%{_mandir} \
	sysconfdir=$RPM_BUILD_ROOT/etc

strip --strip-unneeded $RPM_BUILD_ROOT/sbin/ypbind

install -d $RPM_BUILD_ROOT/{etc/rc.d/init.d,var/yp/binding}
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/ypbind
install %{SOURCE2} $RPM_BUILD_ROOT/etc/yp.conf

gzip -9nf README $RPM_BUILD_ROOT/%{_mandir}/man{5,8}/*

%find_lang ypbind-mt

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add ypbind

%postun
if [ $1 = 0 ] ; then
    /sbin/chkconfig --del ypbind
fi

%triggerpostun -- ypbind <= ypbind-3.3-5
/sbin/chkconfig --add ypbind

%files -f ypbind-mt.lang
%defattr(644,root,root,755)
%doc README.gz
%attr(755,root,root) /sbin/ypbind
%attr(754,root,root) %config /etc/rc.d/init.d/*
%config /etc/yp.conf
%{_mandir}/man5/*
%{_mandir}/man8/*
%dir /var/yp/binding
