Summary:	The NIS daemon which binds NIS clients to an NIS domain.
Name:		ypbind
Version:	3.3
Release:	21
Copyright:	GPL
Group:		System Environment/Daemons
Source0:	ftp://ftp.us.kernel.org/pub/linux/NIS/ypbind-%{version}.tar.gz
Source1:	ypbind.init
Source2:	yp.conf
Patch0:		ypbind-3.3-glibc5.diff.gz
Patch1:		ypbind-3.3-am.patch
Prereq:		/sbin/chkconfig
Requires:	portmap
Requires:	yp-tools
Buildroot:	/tmp/%{name}-%{version}-root

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
%patch0 -p1
%patch1 -p1

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

gzip -9nf README $RPM_BUILD_ROOT/%{_mandir}/man8/*

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

%files
%defattr(644,root,root,755)
%doc README.gz
%attr(755,root,root) /sbin/ypbind
%attr(754,root,root) %config /etc/rc.d/init.d/*
%config /etc/yp.conf
%{_mandir}/man8/*
%dir /var/yp/binding

%changelog
* Wed Jun 23 1999 Jan Rêkorajski <baggins@pld.org.pl>
  [3.3-21]
- FHS 2.0
- cleanup

* Thu Apr 15 1999 Cristian Gafton <gafton@redhat.com>
- requires yp-tools, because ypwhcih is part of that package

* Tue Apr 13 1999 Bill Nottingham <notting@redhat.com>
- don't run ypwhich script if ypbind doesn't start

* Wed Apr 07 1999 Bill Nottingham <notting@redhat.com>
- add a 10 second timeout for initscript...

* Tue Apr 06 1999 Preston Brown <pbrown@redhat.com>
- strip binary

* Thu Apr 01 1999 Preston Brown <pbrown@redhat.com>
- fixed init script to wait until domain is really bound (bug #1928)

* Thu Mar 25 1999 Cristian Gafton <gafton@redhat.com>
- revert to stabdard ypbind; ypbind-mt sucks.

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 5)

* Sat Feb 13 1999 Cristian Gafton <gafton@redhat.com>
- build as ypbind instead of ypbind-mt

* Fri Feb 12 1999 Michael Maher <mike@redhat.com>
- addressed bug #609

* Thu Dec 17 1998 Cristian Gafton <gafton@redhat.com>
- provides ypbind
- switch to ypbind-mt instead of plain ypbind
- build for glibc 2.1
