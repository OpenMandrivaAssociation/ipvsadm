%ifarch %{arm}
%define kflavour kirkwood
%else
%define kflavour desktop
%endif

Summary:	Administration tool for Linux Virtual Server
Name:		ipvsadm
Version:	1.27
Release:	9
License:	GPL 
Group:		System/Kernel and hardware
URL:		https://kernel.org/pub/linux/utils/kernel/ipvsadm/
Source0:	https://kernel.org/pub/linux/utils/kernel/ipvsadm/%{name}-%{version}.tar.gz
Source2:	ipvsadm.sysconfig
Source3:	rc.firewall.iptables
Patch1:		ipvsadm-1.24-usage.patch
Patch2:		ipvsadm-1.26-LDFLAGS.diff
Patch3:		ipvsadm-1.2-lsb.patch
BuildRequires:	popt-devel
Requires(post): rpm-helper
Requires(preun): rpm-helper
BuildRequires:	pkgconfig(libnl-1)

%description
ipvsadm is a utility to administer the IP virtual server services offered by
the Linux kernel with virtual server patch. Virtual Server in Linux kernel can
be used to build a high-performance and highly available server.

%prep

%setup -q
%patch1 -p1 -b .usage
%patch2 -p0 -b .LDFLAGS
%patch3 -p1 -b .lsb

cp %{SOURCE2} %{name}.sysconfig
cp %{SOURCE3} rc.firewall.iptables

%build

# parallel make doesn't work [FL Tue Jan 20 09:14:18 2004]
make POPT_LIB="-lpopt" CFLAGS="%{optflags} -fPIC -DHAVE_POPT -DLIBIPVS_USE_NL" LDFLAGS="%ldflags"

%install
mkdir -p %{buildroot}/{sbin,%{_mandir}/man8,etc/rc.d/init.d,etc/sysconfig}

make BUILD_ROOT=%{buildroot} MANDIR=%{_mandir} install

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
