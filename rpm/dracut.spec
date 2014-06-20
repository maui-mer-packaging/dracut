# 
# Do NOT Edit the Auto-generated Part!
# Generated by: spectacle version 0.27
# 

Name:       dracut

# >> macros
# << macros

Summary:    Initramfs generator using udev
Version:    037
Release:    1
Group:      System/Libraries
License:    GPLv2+ and LGPLv2+
URL:        https://dracut.wiki.kernel.org/
Source0:    dracut-%{version}.tar.xz
Source100:  dracut.yaml
Requires:   bash >= 1:4.1
Requires:   coreutils >= 1:8.21
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
Requires:   tar
Requires(preun): systemd
Requires(post): systemd
Requires(postun): systemd
BuildRequires:  pkgconfig(systemd)
BuildRequires:  bash
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
    --bashcompletiondir=%{_datadir}/bash-completion \
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
# For systemd, better use systemd-bootchart
rm -rf %{buildroot}%{_prefix}/lib/dracut/modules.d/00bootchart

# We don't support dash in the initramfs
rm -rf %{buildroot}%{_prefix}/lib/dracut/modules.d/00dash

# Remove Gentoo specific modules
rm -rf %{buildroot}%{_prefix}/lib/dracut/modules.d/50gensplash

# With systemd, IMA and selinux modules do not make sense
rm -rf %{buildroot}%{_prefix}/lib/dracut/modules.d/96securityfs
rm -rf %{buildroot}%{_prefix}/lib/dracut/modules.d/97masterkey
rm -rf %{buildroot}%{_prefix}/lib/dracut/modules.d/98integrity

# Create directories
mkdir -p %{buildroot}/boot/dracut
mkdir -p %{buildroot}/var/lib/dracut/overlay
mkdir -p %{buildroot}%{_localstatedir}/log
touch %{buildroot}%{_localstatedir}/log/dracut.log
mkdir -p %{buildroot}%{_sharedstatedir}/initramfs

# Configuration
cat > %{buildroot}%{_prefix}/lib/dracut/dracut.conf.d/01-dist.conf <<EOF
i18n_vars="/etc/vconsole.conf:KEYMAP,KEYMAP_TOGGLE /etc/vconsole.conf:FONT,FONT_MAP,FONT_UNIMAP"
i18n_default_font="latarcyrheb-sun16"
i18n_install_all="yes"
stdloglvl=3
sysloglvl=5
install_items+=" ps grep cat rm "
prefix="/"
systemdutildir=/lib/systemd
systemdsystemunitdir=%{_unitdir}
systemdsystemconfdir=%{_sysconfdir}/systemd/system
udevdir=/lib/udev
hostonly="yes"
hostonly_cmdline="no"
EOF

# Default configuration
echo 'hostonly="no"' > %{buildroot}%{_prefix}/lib/dracut/dracut.conf.d/02-generic-image.conf
echo 'dracut_rescue_image="yes"' > %{buildroot}%{_prefix}/lib/dracut/dracut.conf.d/02-rescue.conf
# << install post

%files
%defattr(-,root,root,-)
%config %{_sysconfdir}/dracut.conf
%dir %{_sysconfdir}/dracut.conf.d
%dir %{_unitdir}/initrd.target.wants
%attr(0644,root,root) %ghost %config(missingok,noreplace) %{_localstatedir}/log/dracut.log
%dir %{_sharedstatedir}/initramfs
%dir /boot/dracut
%dir /var/lib/dracut
%dir /var/lib/dracut/overlay
%{_bindir}/dracut*
%{_bindir}/mkinitrd
%{_bindir}/lsinitrd
%{_datadir}/bash-completion/
%{_prefix}/lib/dracut/
%{_prefix}/lib/kernel/
%{_unitdir}/*
# >> files
# << files
