Summary:	The NIS daemon which binds NIS clients to an NIS domain
Summary(es):	Proceso de ligaci�n NIS
Summary(pl):	Demon NIS przy��czaj�cy klient�w NIS do domeny NIS
Summary(pt_BR):	Processo de liga��o NIS
Summary(zh_CN):	NIS ������
Name:		ypbind-mt
Version:	1.13
Release:	1
License:	GPL
Group:		Networking/Daemons
Source0:	ftp://ftp.kernel.org/pub/linux/utils/net/NIS/%{name}-%{version}.tar.bz2
# Source0-md5:	9fabbc25d389b5b9313ca901d2fe01be
Source1:	ypbind.init
Source2:	yp.conf
Patch0:		%{name}-pthread.patch
Patch1:		%{name}-broadcast.patch
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	gettext-devel
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
Requires:	portmap
Requires:	yp-tools
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

%description -l es
Este es un daemon que se ejecuta en clientes NIS/YP y los relaciona a
un dominio NIS. Debe ejecutarse en sistemas basados en la glibc para
funcionaren como clientes NIS.

%description -l pl
NIS (Network Information Service) to system dostarczaj�cy informacje
sieciowe (nazwy u�ytkownik�w, has�a, katalogi domowe, informacje o
grupach) wszystkim maszynom w sieci. NIS mo�e pozwala� u�ytkownikom
logowa� si� na dowolnej maszynie w sieci pod warunkiem, �e maszyna ma
dzia�aj�ce programy klienckie NIS i has�o u�ytkownika jest zapisane w
bazie hase� NIS. NIS by� wcze�niej znany jako YP (Sun Yellow Pages).

Ten pakiet zawiera demona ypbind. Demon ten przy��cza klient�w NIS do
domeny NIS. ypbind musi dzia�a� na ka�dej maszynie, na kt�rej dzia�aj�
programy klienckie NIS.

%description -l pt_BR
Este � um daemon que roda em clientes NIS/YP e os relaciona a um
dom�nio NIS. Ele deve estar rodando em sistemas baseados na glibc para
agirem como clientes NIS.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
rm -f missing
%{__gettextize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/{etc/rc.d/init.d,var/yp/binding}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/ypbind
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/yp.conf

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
%doc README
%attr(755,root,root) %{_sbindir}/ypbind
%attr(754,root,root) /etc/rc.d/init.d/*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/yp.conf
%{_mandir}/man[58]/*
%dir /var/yp/binding
