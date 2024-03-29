Summary:	Power ACPI Event Daemon
Summary(pl.UTF-8):	Demon zdarzeń ACPI
Name:		poweracpid
Version:	0.2
Release:	4
License:	GPL v2+
Group:		Daemons
Source0:	http://dl.sourceforge.net/poweracpid/%{name}-%{version}.tar.bz2
# Source0-md5:	abb2962b7781ba5d92b2e9fa6d969ed2
Source1:	%{name}.init
Source2:	%{name}.sysconfig
URL:		http://sourceforge.net/projects/poweracpid/
BuildRequires:	automake
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
Provides:	acpi-daemon
Obsoletes:	acpi-daemon
Obsoletes:	apm-daemon
ExclusiveArch:	%{ix86} %{x8664} ia64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Power acpid is an ACPI (Advanced Configuration and Power Interface)
daemon designed to be more functional and improve on the design of the
current acpid. Power acpid is very loosely based on work from
<http://acpid.sourceforge.net/>.

%description -l pl.UTF-8
Power acpid to demon ACPI (Advanced Configuration and Power Interface,
czyli zaawansowanego interfejsu do konfiguracji i zarządzania energią)
zaprojektowany tak, aby był bardziej funkcjonalny i bardziej doskonały
niż aktualny acpid. Power acpid jest bardzo luźno oparty na pracach z
<http://acpid.sourceforge.net/>.

%prep
%setup -q

%build
cp -f /usr/share/automake/config.* .
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
%service %{name} restart "PowerACPI daemon"

%preun
if [ "$1" = "0" ]; then
	%service %{name} stop
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%attr(755,root,root) %{_bindir}/%{name}
