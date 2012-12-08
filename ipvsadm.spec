Summary:	Administration tool for Linux Virtual Server
Name:		ipvsadm
Version:	1.24
Release:	15
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
Patch3:		ipvsadm-1.24-no-strip.patch
BuildRequires:	popt-devel
Requires(post): rpm-helper
Requires(preun): rpm-helper

%description 
ipvsadm is a utility to administer the IP virtual server services offered by
the Linux kernel with virtual server patch. Virtual Server in Linux kernel can
be used to build a high-performance and highly available server.

%prep
%setup -q
%patch0 -p0 -b .mdk
%patch1 -p1 -b .usage
%patch2 -p0 -b .LDFLAGS
%patch3 -p1 -b .nostrip

cp %{SOURCE1} libipvs/ip_vs.h
cp %{SOURCE2} %{name}.sysconfig
cp %{SOURCE3} rc.firewall.iptables

%build

# parallel make doesn't work [FL Tue Jan 20 09:14:18 2004]
make CFLAGS="%{optflags}" LDFLAGS="%ldflags"

%install
mkdir -p %{buildroot}/{sbin,%{_mandir}/man8,etc/rc.d/init.d,etc/sysconfig}

make BUILD_ROOT=%{buildroot} MANDIR=%{_mandir} install

# 345 default runlevels in the initscript
perl -p -i -e 's@\# chkconfig\: \- 08 92+@\# chkconfig\: 345 08 92@' %{buildroot}%{_initrddir}/%{name};

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




%changelog
* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 1.24-12mdv2011.0
+ Revision: 665522
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 1.24-11mdv2011.0
+ Revision: 605982
- rebuild

* Sun Mar 14 2010 Oden Eriksson <oeriksson@mandriva.com> 1.24-10mdv2010.1
+ Revision: 519012
- rebuild

* Wed Sep 02 2009 Christophe Fergeau <cfergeau@mandriva.com> 1.24-9mdv2010.0
+ Revision: 425382
- rebuild

* Sat Dec 20 2008 Oden Eriksson <oeriksson@mandriva.com> 1.24-8mdv2009.1
+ Revision: 316437
- use the %%ldflags macro

* Fri Dec 19 2008 Oden Eriksson <oeriksson@mandriva.com> 1.24-7mdv2009.1
+ Revision: 316215
- rediffed fuzzy patches
- use LDFLAGS from the %%configure macro

* Tue Jun 17 2008 Thierry Vignaud <tv@mandriva.org> 1.24-6mdv2009.0
+ Revision: 221642
- rebuild

* Sun Jan 13 2008 Thierry Vignaud <tv@mandriva.org> 1.24-5mdv2008.1
+ Revision: 150343
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot


* Wed Nov 22 2006 Oden Eriksson <oeriksson@mandriva.com> 1.24-4mdv2007.0
+ Revision: 86440
- Import ipvsadm

* Wed Nov 22 2006 Oden Eriksson <oeriksson@mandriva.com> 1.24-4mdv2007.1
- bunzip sources and patches
- spec file massage
- fix deps

* Sat Dec 31 2005 Mandriva Linux Team <http://www.mandrivaexpert.com/> 1.24-3mdk
- Rebuild

* Tue Jan 20 2004 Frederic Lepied <flepied@mandrakesoft.com> 1.24-2mdk
- fixed initscript usage string

* Mon Dec 22 2003 Olivier Thauvin <thauvin@aerov.jussieu.fr> 1.24-1mdk
- 1.24
- remove %%patch0, use make MANDIR=%%_mandir instead
- update %%SOURCE1 from kernel 2.6 (ip_vs.h)

