%global libname libimagequant

Name:           pngquant
Version:        2.12.5
Release:        1%{?dist}
Summary:        PNG quantization tool for reducing image file size

License:        GPLv3+

URL:            http://%{name}.org

Source0:        https://github.com/kornelski/%{name}/archive/%{version}/%{name}-%{version}.tar.gz
Source1:        https://github.com/glennrp/libpng/archive/v1.6.37/libpng-1.6.37.tar.gz
Patch1:         pngquant-old_libpng.patch

BuildRequires:  devtoolset-7-gcc
BuildRequires:  libpng-devel >= 1.2.46-1
BuildRequires:  zlib-devel >= 1.2.3-1
BuildRequires:  lcms2-devel
BuildRequires:  %{libname}-devel >= %{version}

# Requires:       libpng%{?_isa} >= 1.2.46-1
Requires:       zlib%{?_isa} >= 1.2.3-1
Requires:       %{libname}%{?_isa} >= %{version}


%description
%{name} converts 24/32-bit RGBA PNG images to 8-bit palette with alpha channel
preserved.  Such images are compatible with all modern web browsers and a
compatibility setting is available to help transparency degrade well in
Internet Explorer 6.  Quantized files are often 40-70 percent smaller than
their 24/32-bit version. %{name} uses the median cut algorithm.


%prep
%setup -q
%if 0%{?rhel} &&  0%{?rhel} < 8
%patch1 -p1 -b .oldlibpng
%endif

# Enable devtoolset-7-gcc
. /opt/rh/devtoolset-7/enable

cd %{_builddir} && \
    gzip -dc %{_sourcedir}/libpng-1.6.37.tar.gz | tar -xvvf - &>/dev/null && \
    cd libpng-1.6.37 && \
    /usr/bin/chmod -Rf a+rX,u+w,g-w,o-w . && \
    mv %{_builddir}/libpng-1.6.37 %{_builddir}/%{name}-%{version}/libpng


%build

# %%configure can't be used because it adds to all ./configure and prevents libpng static from compiling
# see macro configure source here https://github.com/rpm-software-management/rpm/blob/master/macros.in

cd %{_builddir}/%{name}-%{version}/libpng && \
    %{_configure} --enable-static && \
    make

# add some speed-relevant compiler-flags
export CFLAGS="%{optflags} -fno-math-errno -funroll-loops -fomit-frame-pointer -fPIC"

cd %{_builddir}/%{name}-%{version} && \
    %{_configure} --host=%{_host} --build=%{_build} \
    --program-prefix=%{?_program_prefix} \
    --disable-dependency-tracking \
    --prefix=%{_prefix} \
    --exec-prefix=%{_exec_prefix} \
    --bindir=%{_bindir} \
    --sbindir=%{_sbindir} \
    --sysconfdir=%{_sysconfdir} \
    --datadir=%{_datadir} \
    --includedir=%{_includedir} \
    --libdir=%{_libdir} \
    --libexecdir=%{_libexecdir} \
    --localstatedir=%{_localstatedir} \
    --sharedstatedir=%{_sharedstatedir} \
    --mandir=%{_mandir} \
    --infodir=%{_infodir} \
    --with-openmp --with-lcms2 --with-libimagequant

%make_build


%install
%make_install


%check
%make_build test


%files
%doc README.md CHANGELOG
%license COPYRIGHT
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*


%changelog
* Mon Jul 29 2019 Sandro Mani <manisandro@gmail.com> - 2.12.5-1
- Update to 2.12.5

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.12.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon May 27 2019 Sandro Mani <manisandro@gmail.com< - 2.12.3-1
- Update to 2.12.3

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.12.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Oct 29 2018 Sandro Mani <manisandro@gmail.com> - 2.12.2-1
- Update to 2.12.2

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 08 2018 Sandro Mani <manisandro@gmail.com> - 2.12.1-1
- Update to 2.12.1

* Mon Mar 12 2018 Sandro Mani <manisandro@gmail.com> - 2.11.7-5
- Relax libimagequant version requires

* Wed Mar 07 2018 Adam Williamson <awilliam@redhat.com> - 2.11.7-4
- Rebuild to fix GCC 8 mis-compilation
  See https://da.gd/YJVwk ("GCC 8 ABI change on x86_64")

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.11.7-3
- Escape macros in %%changelog

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 19 2018 Sandro Mani <manisandro@gmail.com> - 2.11.7-1
- Update to 2.11.7

* Thu Jan 18 2018 Sandro Mani <manisandro@gmail.com> - 2.11.6-1
- Update to 2.11.6

* Mon Nov 27 2017 Sandro Mani <manisandro@gmail.com> - 2.11.4-1
- Update to 2.11.4

* Thu Nov 23 2017 Sandro Mani <manisandro@gmail.com> - 2.11.3-1
- Update to 2.11.3

* Sat Nov 11 2017 Sandro Mani <manisandro@gmail.com> - 2.11.2-2
- Require libimagequant greater or equal %%{version}

* Sun Nov 05 2017 Sandro Mani <manisandro@gmail.com> - 2.11.2-1
- Update to 2.11.2

* Wed Nov 01 2017 Sandro Mani <manisandro@gmail.com> - 2.11.0-1
- Update to 2.11.0

* Wed Aug 09 2017 Sandro Mani <manisandro@gmail.com> - 2.10.2-1
- Update to 2.10.2

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 10 2017 Björn Esser <besser82@fedoraproject.org> - 2.10.1-2
- Apply additional compiler flags properly

* Mon Jul 10 2017 Sandro Mani <manisandro@gmail.com> - 2.10.1-1
- Update to 2.10.1

* Mon Jul 03 2017 Sérgio Basto <sergio@serjux.com> - 2.10.0-1
- Update to 2.10.0

* Sat Jul 01 2017 Sérgio Basto <sergio@serjux.com> - 2.9.1-2
- update to pre 2.9.2

* Wed Apr 19 2017 Sérgio Basto <sergio@serjux.com> - 2.9.1-1
- Update pngquant to 2.9.1
- Update Makefile to better handle build the shared libraries
- Remove libimagequant sub-package and use the new libimagequant package.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Dec 02 2016 Sérgio Basto <sergio@serjux.com> - 2.8.1-1
- New upstream vesion, 2.8.1

* Fri Dec 02 2016 Sérgio Basto <sergio@serjux.com> - 2.7.2-1
- Update pngquant 2.7.2

* Fri Jul 15 2016 Sérgio Basto <sergio@serjux.com> - 2.7.1-1
- Update pngquant 2.7.1

* Tue May 10 2016 Sérgio Basto <sergio@serjux.com> - 2.7.0-1
- Update to 2.7.0
- License change to GPLv3+ .

* Thu Mar 17 2016 Sérgio Basto <sergio@serjux.com> - 2.6.0-2
- Compilation with OpenMP

* Sun Feb 21 2016 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 2.6.0-1
- Update to 2.6.0 (#1310413)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 20 2016 Sérgio Basto <sergio@serjux.com> - 2.5.2-6
- Patches from here are upstreamed.

* Sat Dec 19 2015 Sérgio Basto <sergio@serjux.com> - 2.5.2-5
- Following https://fedoraproject.org/wiki/EPEL:Packaging#The_.25license_tag

* Sat Dec 19 2015 Björn Esser <fedora@besser82.io> - 2.5.2-4
- Add '-std=c99' for building the testsuite binary

* Sat Dec 19 2015 Björn Esser <fedora@besser82.io> - 2.5.2-3
- Add Patch1: make the configure-script work with %%configure
- Build and run the testsuite
- Conditionalize %%license
- Remove all el5-related things, since we need gcc >= 4.2 anyways
- Fix %%{?_isa} on (Build)Requires

* Sat Dec 19 2015 Sérgio Basto <sergio@serjux.com> - 2.5.2-2
- Disable pngquant debug (#1291885)

* Thu Nov 26 2015 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 2.5.2-1
- Update to 2.5.2 (#1285589)

* Thu Aug 27 2015 Sérgio Basto <sergio@serjux.com> - 2.5.1-1
- Update to 2.5.1

* Thu Jul 02 2015 Sérgio Basto <sergio@serjux.com> - 2.5.0-1
- Update to 2.5.0 (#1238501)
- Update to pngquant-2.5.0_fix-Makefile.patch .

* Sat Jun 20 2015 Sérgio Basto <sergio@serjux.com> - 2.4.2-3
- pngquant now requires libimagequant with same version

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 2.4.2-1
- Update to 2.4.2 (#1232532)
- Add license tag.

* Mon Apr 20 2015 Sérgio Basto <sergio@serjux.com> - 2.4.1-1
- Update to 2.4.1
- Dropped "epel compile fix" patch

* Sun Apr 19 2015 Sérgio Basto <sergio@serjux.com> - 2.4.0.1-4
- epel compile fix or compile fix for png15

* Sun Apr 19 2015 Sérgio Basto <sergio@serjux.com> - 2.4.0.1-3
- Reenabled SSE on i386, compiling is fixed !
- Better pngquant-2.4.0_fix-Makefile.patch more close to upstream.

* Sun Apr 19 2015 Sérgio Basto <sergio@serjux.com> - 2.4.0.1-2
- Fixed dependency of libimagequant.so.0
- Minor fix on ln to %%{libname}.so

* Sun Apr 19 2015 Sérgio Basto <sergio@serjux.com> - 2.4.0.1-1
- Update to 2.4.0

* Mon Feb 09 2015 Sérgio Basto <sergio@serjux.com> - 2.3.4-1
- Update to 2.3.4

* Wed Jan 07 2015 Sérgio Basto <sergio@serjux.com> - 2.3.2-1
- New bug fix release.

* Fri Oct 17 2014 Sérgio Basto <sergio@serjux.com> - 2.3.1-1
- New bug fixing release

* Sat Sep 27 2014 Sérgio Basto <sergio@serjux.com> - 2.3.0-2
- Disable SSE on i386, to workaround building on i386 ,
  https://github.com/kornelski/pngquant/issues/122

* Sat Sep 27 2014 Sérgio Basto <sergio@serjux.com> - 2.3.0-1
- New upstream version 2.3.0

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Aug 23 2013 Björn Esser <bjoern.esser@gmail.com> - 2.0.0-1
- new upstream version 2.0.0 (#989991)
- fixes FTBFS in F20 / rawhide (#992807)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu May 30 2013 Björn Esser <bjoern.esser@gmail.com> - 1.8.3-6
- improved and added more el5-legacy related stuff

* Fri May 24 2013 Björn Esser <bjoern.esser@gmail.com> - 1.8.3-5
- add el5-build related conditonals

* Wed May 22 2013 Björn Esser <bjoern.esser@gmail.com> - 1.8.3-4
- add Group-Tag to make el5-build happy

* Sun May 19 2013 Björn Esser <bjoern.esser@gmail.com> - 1.8.3-3
- add Patch0: respect system compiler-flags
- touch a fake configure-script during prep
- export system cflags invoking configure-macro

* Fri May 17 2013 Björn Esser <bjoern.esser@gmail.com> - 1.8.3-2
- changed License: BSD --> BSD with advertising
- removed -n{name}-{version} from prep
- removed >= 1.2.46-1 from BuildRequires: libpng-devel

* Tue May 14 2013 Björn Esser <bjoern.esser@gmail.com> - 1.8.3-1
- Initial RPM release.
