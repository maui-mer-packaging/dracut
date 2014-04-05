# 
# Do NOT Edit the Auto-generated Part!
# Generated by: spectacle version 0.27
# 

Name:       dracut

# >> macros
# << macros

Summary:    Initramfs generator using udev
Version:    036
Release:    1
Group:      System/Libraries
License:    GPLv2+ and LGPLv2+
URL:        https://dracut.wiki.kernel.org/
Source0:    dracut-%{version}.tar.xz
Source100:  dracut.yaml
Requires:   bash >= 4
Requires:   coreutils >= 8
Requires:   cpio
Requires:   findutils
Requires:   grep
Requires:   hardlink
Requires:   gzip
Requires:   xz
Requires:   kmod
Requires:   sed
Requires:   kpartx
Requires:   util-linux >= 2.21
Requires:   systemd >= 199
Requires:   procps
BuildRequires:  bash
BuildRequires:  systemd
Conflicts:   grubby < 8.23
Conflicts:   mdadm < 3.2.6

%description
dracut contains tools to create a bootable initramfs for 2.6 Linux kernels.
Unlike existing implementations, dracut does hard-code as little as possible
into the initramfs. dracut contains various modules which are driven by the
event-based udev. Having root on MD, DM, LVM2, LUKS is supported as well as
NFS, iSCSI, NBD, FCoE with the dracut-network package.


%prep
%setup -q -n %{name}-%{version}

# >> setup
# << setup

%build
# >> build pre
cd upstream
# << build pre

%configure --disable-static \
    --systemdsystemunitdir=%{_unitdir} \
    --bashcompletiondir=$(pkg-config --variable=completionsdir bash-completion) \
    --libdir=%{_prefix}/lib \
    --disable-documentation

make %{?_smp_mflags}

# >> build post
# << build post

%install
rm -rf %{buildroot}
# >> install pre
cd upstream
# << install pre
%make_install

# >> install post
# << install post

%files
%defattr(-,root,root,-)
%{_bindir}/dracut*
%{_bindir}/mkinitrd
%{_bindir}/lsinitrd
%{_datadir}/bash-completion/
%{_libdir}/dracut/
%{_libdir}/kernel/
%{_sysconfdir}/dracut.conf.d/
%dir %{_sysconfdir}/dracut.conf.d
%config %{_sysconfdir}/dracut.conf
# >> files
# << files
