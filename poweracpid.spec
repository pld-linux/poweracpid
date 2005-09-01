Summary:	Power ACPI Event Daemon
Summary(pl):	Demon zdarzeñ ACPI
Name:		poweracpid
Version:	0.2
Release:	2
License:	GPL v2
Group:		Daemons
Source0:	http://dl.sourceforge.net/poweracpid/%{name}-%{version}.tar.bz2
# Source0-md5:	abb2962b7781ba5d92b2e9fa6d969ed2
Source1:	%{name}.init
Source2:	%{name}.sysconfig
URL:		http://sourceforge.net/projects/poweracpid/
BuildRequires:	automake
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
Provides:	acpid
Obsoletes:	apmd
Obsoletes:	acpid
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Power acpid is an ACPI (Advanced Configuration and Power Interface)
daemon designed to be more functional and improve on the design of the
current acpid. Power acpid is very loosely based on work from
<http://acpid.sourceforge.net/>.

%description -l pl
Power acpid to demon ACPI (Advanced Configuration and Power Interface,
czyli zaawansowanego interfejsu do konfiguracji i zarz±dzania energi±)
zaprojektowany tak, aby by³ bardziej funkcjonalny i bardziej doskona³y
ni¿ aktualny acpid. Power acpid jest bardzo lu¼no oparty na pracach z
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
if [ -f /var/lock/subsys/%{name} ]; then
	/etc/rc.d/init.d/%{name} restart >&2
else
	echo "Run \"/etc/rc.d/init.d/%{name} start\" to start PowerACPI daemon."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/%{name} ]; then
		/etc/rc.d/init.d/%{name} stop>&2
	fi
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%attr(755,root,root) %{_bindir}/%{name}
