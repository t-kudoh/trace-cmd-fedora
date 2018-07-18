# git tag
#%%global git_commit trace-cmd-v2.6.2
#%%global git_commit 57371aaa2f469d0ba15fd85276deca7bfdd7ce36

Name: trace-cmd
Version: 2.7
Release: 3%{?dist}
License: GPLv2 and LGPLv2
Summary: A user interface to Ftrace

URL: http://git.kernel.org/?p=linux/kernel/git/rostedt/trace-cmd.git;a=summary
# If upstream does not provide tarballs, to generate:
# git clone git://git.kernel.org/pub/scm/linux/kernel/git/rostedt/trace-cmd.git
# cd trace-cmd
# git archive --prefix=trace-cmd-%%{version}/ -o trace-cmd-v%%{version}.tar.gz %%{git_commit}
Source0: https://git.kernel.org/pub/scm/linux/kernel/git/rostedt/trace-cmd.git/snapshot/%{name}-v%{version}.tar.gz
Source1: kernelshark.desktop
Patch1: 0001-trace-cmd-Figure-out-the-arch-and-install-library-to.patch
Patch2: 0002-trace-cmd-Fix-the-logic-behind-SWIG_DEFINED-in-the-M.patch
BuildRequires:  gcc
BuildRequires: xmlto
BuildRequires: asciidoc
BuildRequires: mlocate
# needed for the GUI parts
BuildRequires: libxml2-devel
BuildRequires: gtk2-devel
BuildRequires: glib2-devel
BuildRequires: desktop-file-utils

%description
trace-cmd is a user interface to Ftrace. Instead of needing to use the
debugfs directly, trace-cmd will handle of setting of options and
tracers and will record into a data file.

%package -n kernelshark
Summary: GUI analysis for Ftrace data captured by trace-cmd
Requires: trace-cmd%{_isa} = %{version}-%{release}

%description -n kernelshark
Kernelshark is the GUI frontend for analyzing data produced by
'trace-cmd extract'

%package python2
Summary: Python plugin support for trace-cmd
Requires: trace-cmd%{_isa} = %{version}-%{release}
BuildRequires: swig
BuildRequires: python2-devel

%description  python2
Python plugin support for trace-cmd

%prep
%setup -q -n %{name}-v%{version}
%patch1 -p1
%patch2 -p1

%build
# MANPAGE_DOCBOOK_XSL define is hack to avoid using locate
MANPAGE_DOCBOOK_XSL=`rpm -ql docbook-style-xsl | grep manpages/docbook.xsl`
make V=1 CFLAGS="%{optflags} -D_GNU_SOURCE" LDFLAGS="%{build_ldflags}" \
  MANPAGE_DOCBOOK_XSL=$MANPAGE_DOCBOOK_XSL prefix=%{_prefix} all doc gui python-plugin


%install
make V=1 DESTDIR=%{buildroot}/ prefix=%{_prefix} install install_doc install_gui install_python
find %{buildroot}%{_mandir} -type f | xargs chmod u-x,g-x,o-x
find %{buildroot}%{_datadir} -type f | xargs chmod u-x,g-x,o-x
find %{buildroot}%{_libdir} -type f -iname "*.so" | xargs chmod 0755
install -dm 755 %{buildroot}/%{_datadir}/applications
install -pm 644 %{SOURCE1} %{buildroot}/%{_datadir}/applications/kernelshark.desktop
desktop-file-validate %{buildroot}/%{_datadir}/applications/kernelshark.desktop

%files
%doc COPYING COPYING.LIB README
%{_bindir}/trace-cmd
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/plugins
%{_libdir}/%{name}/plugins/plugin_blk.so
%{_libdir}/%{name}/plugins/plugin_cfg80211.so
%{_libdir}/%{name}/plugins/plugin_function.so
%{_libdir}/%{name}/plugins/plugin_hrtimer.so
%{_libdir}/%{name}/plugins/plugin_jbd2.so
%{_libdir}/%{name}/plugins/plugin_kmem.so
%{_libdir}/%{name}/plugins/plugin_kvm.so
%{_libdir}/%{name}/plugins/plugin_mac80211.so
%{_libdir}/%{name}/plugins/plugin_sched_switch.so
%{_libdir}/%{name}/plugins/plugin_scsi.so
%{_libdir}/%{name}/plugins/plugin_tlb.so
%{_libdir}/%{name}/plugins/plugin_xen.so
%{_mandir}/man1/*
%{_mandir}/man5/*

%files -n kernelshark
%{_bindir}/trace-view
%{_bindir}/trace-graph
%{_bindir}/kernelshark
%{_datadir}/kernelshark
%{_datadir}/applications/kernelshark.desktop
%{_sysconfdir}/bash_completion.d/trace-cmd.bash

%files python2
%doc Documentation/README.PythonPlugin
%{_libdir}/%{name}/plugins/plugin_python.so
%{_libdir}/%{name}/python/



%changelog
* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Mar 02 2018 Zamir SUN <sztsian@gmail.com> - 2.7-2
- Add python plugins

* Fri Mar 02 2018 Zamir SUN <sztsian@gmail.com> - 2.7-1
- Update to 2.7
- Remove Groups tag

* Fri Feb 23 2018 Florian Weimer <fweimer@redhat.com> - 2.6.2-3
- Use LDFLAGS from redhat-rpm-config

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Nov 11 2017 Zamir SUN <zsun@fedoraproject.org> - 2.6.2-1
- Rebase to 2.6.2.

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue May 23 2017 Zamir SUN <zsun@fedoraproject.org> - 2.6.1-1
- Rebase to 2.6.1.

* Thu Mar 30 2017 Zamir SUN <zsun@fedoraproject.org> - 2.6-4.20170330git013205
- Rebase to newest upstream version to include various bug fixes.

* Mon Mar 27 2017 Zamir SUN <zsun@fedoraproject.org> - 2.6-4
- Fix bz1389219 segmentation fault in trace-cmd snapshot

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Oct 19 2016 Zamir SUN <zsun@fedoraproject.org> - 2.6-2
- Add bz1386451-trace-cmd-record-crash-f-before-e.patch
- Fix rpmlint error unstripped-binary-or-object
- Resolves: rhbz#1386451

* Thu Aug 18 2016 Jon Stanley <jonstanley@gmail.com> - 2.6-1
- Upgrade to uptream 2.6
- Rebase distro patch
- Resolves: rhbz#1365951

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 24 2013 Jon Stanley <jonstanley@gmail.com> - 2.2.1-2
- Remove addition to %%files - not needed with Makefile patch

* Tue Jul 23 2013 Dwight Engen <dwight.engen@oracle.com> - 2.2.1-1
- Update to 2.2.1

* Wed Feb 13 2013 Jon Stanley <jonstanley@gmail.com> - 2.1.0-1
- Update to latest upstream

* Thu Sep 13 2012 Jon Stanley <jonstanley@gmail.com> - 1.2-4.20120606git8266dff
- Remove %%defattr

* Thu Sep 06 2012 Jon Stanley <jonstanley@gmail.com> - 1.2-3.20120606git8266dff
- More review fixups

* Tue Aug 28 2012 Jon Stanley <jonstanley@gmail.com> - 1.2-2.20120606git8266dff
- Rebase to git snapshot so it builds
- Fix license tag per review
- Move plugin dir per review

* Mon Aug 27 2012 Jon Stanley <jonstanley@gmail.com> - 1.2-1
- Rebase to 1.2
- Makefile now supports CFLAGS, drop patch

* Sat Feb 19 2011 Jon Stanley <jonstanley@gmail.com> - 1.0.5-1
- Rebase to 1.0.5
- Add Makefile patch to support passing RPM_OPT_FLAGS
- Add kernelshark subpackage
- Initial Fedora version

* Mon Jul 5 2010 John Kacur <jkacur@redhat.com> - 1.0.4-7
- Rebasing to trace-cmd-1.0.4

* Wed Jun 16 2010 John Kacur <jkacur@redhat.com>
- Rebasing to trace-cmd-1.0.2
- Added parse-events-Do-not-fail-on-FORMAT-TOO-BIG-event-err.patch
- Added trace-cmd-Prevent-latency-tracer-plugins-from-doing-.patch
- Added trace-cmd-Prevent-print_graph_duration-buffer-overfl.patch

* Wed Jun 9 2010 John Kacur <jkacur@redhat.com>
- Added trace-cmd-Makefile-EXTRAVERSION-should-be-set-withou.patch
- Added trace-cmd-Makefile-use-a-substitution-reference.patch
- add-DESTDIR-to-make.patch
- Related: rhbz599507

* Fri Jun 4 2010 John Kacur <jkacur@redhat.com>
- Updating to trace-cmd-1.0.1
- Related: rhbz599507

* Wed Apr 21 2010 John Kacur <jkacur@redhat.com>
- Using trick from William Cohen to avoid the "locate" problem.

* Fri Apr 16 2010 John Kacur <jkacur@redhat.com>
- Update the source to the 1.0.0 version
- Many fixes to the spec file.

* Mon Apr 12 2010 William Cohen <wcohen@redhat.com>
- Include manpages in the package.

* Fri Apr 9 2010 John Kacur <jkacur@redhat.com>
- disabled #patch01
- Updated the trace-cmd source
- Changed version to 0.7.0
- Added bogus patch to satisfy rpm requirements
- Related:bz519630

* Mon Mar 15 2010 John Kacur <jkacur@redhat.com>
- disabled trace-cmd_rusage.patch
- Updated the trace-cmd source
- Related:bz519630

* Fri Nov 16 2007 Luis Claudio R. Goncalves <lgoncalv@redhat.com> - 1.0-1%{?dist}
- Initial packaging
- Added a patch to display rusage information
