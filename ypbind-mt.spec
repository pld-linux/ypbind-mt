Summary:	The NIS daemon which binds NIS clients to an NIS domain
Summary(es.UTF-8):   Proceso de ligación NIS
Summary(pl.UTF-8):   Demon NIS przyłączający klientów NIS do domeny NIS
Summary(pt_BR.UTF-8):   Processo de ligação NIS
Summary(zh_CN.UTF-8):   NIS 服务器
Name:		ypbind-mt
Version:	1.19.1
Release:	2
License:	GPL
Group:		Networking/Daemons
Source0:	ftp://ftp.kernel.org/pub/linux/utils/net/NIS/%{name}-%{version}.tar.bz2
# Source0-md5:	34a6e181289a637ebcc1e596c70af6c8
Source1:	ypbind.init
Source2:	yp.conf
Patch0:		%{name}-pthread.patch
Patch1:		%{name}-broadcast.patch
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	gettext-devel
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	nss_nis
Requires:	portmap
Requires:	rc-scripts
Requires:	yp-tools
Provides:	ypbind
Obsoletes:	ypbind
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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

%description -l es.UTF-8
Este es un daemon que se ejecuta en clientes NIS/YP y los relaciona a
un dominio NIS. Debe ejecutarse en sistemas basados en la glibc para
funcionaren como clientes NIS.

%description -l pl.UTF-8
NIS (Network Information Service) to system dostarczający informacje
sieciowe (nazwy użytkowników, hasła, katalogi domowe, informacje o
grupach) wszystkim maszynom w sieci. NIS może pozwalać użytkownikom
logować się na dowolnej maszynie w sieci pod warunkiem, że maszyna ma
działające programy klienckie NIS i hasło użytkownika jest zapisane w
bazie haseł NIS. NIS był wcześniej znany jako YP (Sun Yellow Pages).

Ten pakiet zawiera demona ypbind. Demon ten przyłącza klientów NIS do
domeny NIS. ypbind musi działać na każdej maszynie, na której działają
programy klienckie NIS.

%description -l pt_BR.UTF-8
Este é um daemon que roda em clientes NIS/YP e os relaciona a um
domínio NIS. Ele deve estar rodando em sistemas baseados na glibc para
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
%configure \
	--disable-slp
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
%service ypbind restart

%preun
if [ "$1" = "0" ]; then
	%service ypbind stop
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
