Summary:	Administration tool for Linux Virtual Server
Name:		ipvsadm
Version:	1.24
Release:	%mkrel 12
License:	GPL 
Group:		System/Kernel and hardware
URL:		http://www.linuxvirtualserver.org
Source:		http://www.linuxvirtualserver.org/software/%{name}-%{version}.tar.bz2
Source1:	ip_vs.h
Source2:	ipvsadm.sysconfig
Source3:	rc.firewall.iptables
Patch0:		ipvsadm-1.24-mdk.patch
Patch1:		ipvsadm-1.24-usage.patch
Patch2:		ipvsadm-1.24-LDFLAGS.diff
BuildRequires:	popt-devel
Requires(post): rpm-helper
Requires(preun): rpm-helper
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description 
ipvsadm is a utility to administer the IP virtual server services offered by
the Linux kernel with virtual server patch. Virtual Server in Linux kernel can
be used to build a high-performance and highly available server.

%prep

%setup -q
%patch0 -p0 -b .mdk
%patch1 -p1 -b .usage
%patch2 -p0 -b .LDFLAGS

cp %{SOURCE1} libipvs/ip_vs.h
cp %{SOURCE2} %{name}.sysconfig
cp %{SOURCE3} rc.firewall.iptables

%build

# parallel make doesn't work [FL Tue Jan 20 09:14:18 2004]
make CFLAGS="%{optflags}" LDFLAGS="%ldflags"

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}/{sbin,%{_mandir}/man8,etc/rc.d/init.d,etc/sysconfig}

make BUILD_ROOT=%{buildroot} MANDIR=%{_mandir} install

# 345 default runlevels in the initscript
perl -p -i -e 's@\# chkconfig\: \- 08 92+@\# chkconfig\: 345 08 92@' %{buildroot}%{_initrddir}/%{name};

install -m0644 %{name}.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/%{name}

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README rc.firewall.iptables
%attr(0755,root,root) %config(noreplace) %{_initrddir}/%{name}
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%attr(0755,root,root) /sbin/*
%attr(0644,root,root) %{_mandir}/*/*


