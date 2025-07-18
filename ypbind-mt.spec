Summary:	The NIS daemon which binds NIS clients to an NIS domain
Summary(es.UTF-8):	Proceso de ligación NIS
Summary(pl.UTF-8):	Demon NIS przyłączający klientów NIS do domeny NIS
Summary(pt_BR.UTF-8):	Processo de ligação NIS
Summary(zh_CN.UTF-8):	NIS 服务器
Name:		ypbind-mt
Version:	2.7.2
Release:	1
License:	GPL v2
Group:		Networking/Daemons
#Source0Download: https://github.com/thkukuk/ypbind-mt/releases
Source0:	https://github.com/thkukuk/ypbind-mt/releases/download/v%{version}/%{name}-%{version}.tar.xz
# Source0-md5:	130ddec4c31192cbefefc66d9d8ffbd8
Source1:	ypbind.init
Source2:	yp.conf
Patch0:		%{name}-broadcast.patch
URL:		http://www.linux-nis.org/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake >= 1.6
BuildRequires:	bison
BuildRequires:	docbook-dtd43-xml
BuildRequires:	gettext-tools >= 0.19
BuildRequires:	libnsl-devel >= 1.0.4
BuildRequires:	libtirpc-devel >= 1.0.1
BuildRequires:	libxslt-progs
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	systemd-devel >= 1:209
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires(post,preun):	/sbin/chkconfig
Requires:	libnsl >= 1.0.4
Requires:	libtirpc >= 1.0.1
Requires:	nss_nis
Requires:	rc-scripts >= 0.4.1.5
Requires:	rpcbind
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
%patch -P0 -p1

%build
%{__gettextize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
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
%service ypbind restart

%preun
if [ "$1" = "0" ]; then
	%service ypbind stop
	/sbin/chkconfig --del ypbind
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_sbindir}/ypbind
%attr(754,root,root) /etc/rc.d/init.d/ypbind
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/yp.conf
%{_mandir}/man5/yp.conf.5*
%{_mandir}/man8/ypbind.8*
%dir /var/yp/binding
