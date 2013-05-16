Summary:	Administration tool for Linux Virtual Server
Name:		ipvsadm
Version:	1.26
Release:	1
License:	GPLv2
Group:		System/Kernel and hardware
Url:		http://www.linuxvirtualserver.org/software/ipvs.html
Source0:	http://www.linuxvirtualserver.org/software/kernel-2.6/%{name}-%{version}.tar.gz
Source2:	ipvsadm.sysconfig
Source3:	rc.firewall.iptables
Patch1:		ipvsadm-1.24-usage.patch
BuildRequires:	pkgconfig(popt)
Requires(post,preun):	rpm-helper

%description 
ipvsadm is a utility to administer the IP virtual server services offered by
the Linux kernel with virtual server patch. Virtual Server in Linux kernel can
be used to build a high-performance and highly available server.

%prep
%setup -q
%apply_patches

cp %{SOURCE2} %{name}.sysconfig
cp %{SOURCE3} rc.firewall.iptables

%build
# parallel make doesn't work [FL Tue Jan 20 09:14:18 2004]
make CFLAGS="%{optflags}" LDFLAGS="%ldflags"

%install
mkdir -p %{buildroot}/{sbin,%{_mandir}/man8,etc/rc.d/init.d,etc/sysconfig}

make BUILD_ROOT=%{buildroot} MANDIR=%{_mandir} install

# 345 default runlevels in the initscript
sed -i -e 's@# chkconfig: - 08 92@# chkconfig: 345 08 92@' %{buildroot}%{_initrddir}/%{name}

install -m0644 %{name}.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/%{name}

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%files
%doc README rc.firewall.iptables
%attr(0755,root,root) %config(noreplace) %{_initrddir}/%{name}
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%attr(0755,root,root) /sbin/*
%attr(0644,root,root) %{_mandir}/*/*

