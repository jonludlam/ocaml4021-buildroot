# if the build is running on copr
%if 0%{?copr_username:1}
# define your copr_username and copr_projectname
%global scl %{copr_username}-%{copr_projectname}
%else
# different build system need only name of the collection, ocaml402 in this case
%global scl ocaml402
%endif

%{?scl:%scl_package ocaml-findlib}
%{!?scl:%global pkg_name %{name}}

%global opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)

%define _use_internal_dependency_generator 0
%define __find_requires scl enable %{scl} "/usr/lib/rpm/ocaml-find-requires.sh -c"
%define __find_provides scl enable %{scl} /usr/lib/rpm/ocaml-find-provides.sh

Name:           %{?scl_prefix}ocaml-findlib
Version:        1.5.2
Release:        4%{?dist}
Summary:        Objective CAML package manager and build helper
License:        BSD

URL:            http://projects.camlcity.org/projects/findlib.html
Source0:        http://download.camlcity.org/download/findlib-%{version}.tar.gz

# Use ocamlopt -g patch to include debug information.
Patch1:         findlib-1.4-add-debug.patch

%if 0%{?scl:1}
BuildRequires:  %{?scl_prefix}build
BuildRequires:  %{?scl_prefix}runtime
%endif

BuildRequires:  %{?scl_prefix}ocaml
BuildRequires:  %{?scl_prefix}ocaml-camlp4-devel
BuildRequires:  %{?scl_prefix}ocaml-labltk-devel
BuildRequires:  %{?scl_prefix}ocaml-compiler-libs
BuildRequires:  %{?scl_prefix}ocaml-ocamldoc
BuildRequires:  m4, ncurses-devel
BuildRequires:  gawk
Requires:       %{?scl_prefix}ocaml

%global __ocaml_requires_opts -i Asttypes -i Parsetree


%description
Objective CAML package manager and build helper.


%package        devel
Summary:        Development files for %{pkg_name}
Requires:       %{?scl_prefix}%{pkg_name} = %{version}-%{release}


%description    devel
The %{pkg_name}-devel package contains libraries and header files for
developing applications that use %{pkg_name}.


%prep
%setup -q -n findlib-%{version}
%patch1 -p2


%build
%{?scl:scl enable %{scl} "}
(cd tools/extract_args && make)
tools/extract_args/extract_args -o src/findlib/ocaml_args.ml ocamlc ocamlcp ocamlmktop ocamlopt ocamldep ocamldoc ||:
./configure -config %{_sysconfdir}/ocamlfind.conf \
  -bindir %{_bindir} \
  -sitelib %{_libdir}/ocaml \
  -mandir %{_mandir} \
  -with-toolbox
make all
%if %opt
make opt
%endif
%{?scl:"}
rm doc/guide-html/TIMESTAMP


%install
# Grrr destdir grrrr
mkdir -p $RPM_BUILD_ROOT%{_bindir}
%{?scl:scl enable %{scl} "}
make install prefix=$RPM_BUILD_ROOT OCAMLFIND_BIN=$RPM_BUILD_ROOT%{_bindir}
%{?scl:"}
mv $RPM_BUILD_ROOT/$RPM_BUILD_ROOT%{_bindir}/* $RPM_BUILD_ROOT%{_bindir}


%files
%doc LICENSE doc/README
%config(noreplace) %{_sysconfdir}/ocamlfind.conf
%{_bindir}/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_libdir}/ocaml/*/META
%{_libdir}/ocaml/topfind
%{_libdir}/ocaml/findlib
%if %opt
%exclude %{_libdir}/ocaml/findlib/*.a
%exclude %{_libdir}/ocaml/findlib/*.cmxa
%endif
%exclude %{_libdir}/ocaml/findlib/*.mli
%exclude %{_libdir}/ocaml/findlib/Makefile.config
%exclude %{_libdir}/ocaml/findlib/make_wizard
%exclude %{_libdir}/ocaml/findlib/make_wizard.pattern
%{_libdir}/ocaml/num-top


%files devel
%doc LICENSE doc/README doc/guide-html
%if %opt
%{_libdir}/ocaml/findlib/*.a
%{_libdir}/ocaml/findlib/*.cmxa
%endif
%{_libdir}/ocaml/findlib/*.mli
%{_libdir}/ocaml/findlib/Makefile.config

%changelog
* Thu Nov 27 2014 Jon Ludlam <jonathan.ludlam@citrix.com> - 1.5.2-4
- SCLify

* Sat Aug 30 2014 Richard W.M. Jones <rjones@redhat.com> - 1.5.2-3
- Bump release and rebuild.

* Sat Aug 30 2014 Richard W.M. Jones <rjones@redhat.com> - 1.5.2-2
- ocaml-4.02.0 final rebuild.

* Fri Aug 22 2014 Richard W.M. Jones <rjones@redhat.com> - 1.5.2-1
- New upstream release 1.5.2.
- ocaml-4.02.0+rc1 rebuild.

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Aug 01 2014 Richard W.M. Jones <rjones@redhat.com> - 1.5.1-3
- ocaml-4.02.0-0.8.git10e45753.fc22 rebuild.

* Thu Jul 17 2014 Richard W.M. Jones <rjones@redhat.com> - 1.5.1-2
- Rebuild for new camlp4 package for OCaml 4.02.0 beta rebuild.

* Sat Jul 12 2014 Richard W.M. Jones <rjones@redhat.com> - 1.5.1-1
- New upstream version 1.5.1.
- Disable labltk and camlp4.  We will reenable when they are added back
  into Fedora.
- Remove findlib/make_wizard and findlib/make_wizard.pattern.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Dan Horák <dan[at]danny.cz> - 1.4-2
- drop ExcludeArch

* Fri Sep 13 2013 Richard W.M. Jones <rjones@redhat.com> - 1.4-1
- New upstream version 1.4.
- Build debuginfo.
- Add -g option when running ocamlopt to generate debuginfo.
- Don't need anti-prelink / stripping hacks for modern OCaml.
- Modernize spec file.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 27 2012 Richard W.M. Jones <rjones@redhat.com> - 1.3.3-3
- BR >= OCaml 4.00.1 so we can't build against the wrong OCaml version.

* Tue Oct 16 2012 Richard W.M. Jones <rjones@redhat.com> - 1.3.3-2
- Rebuild for OCaml 4.00.1.

* Sat Jul 28 2012 Richard W.M. Jones <rjones@redhat.com> - 1.3.3-1
- New upstream version 1.3.3.
- Remove patch for OCaml 4 which has been obsoleted by upstream changes.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 10 2012 Richard W.M. Jones <rjones@redhat.com> - 1.3.1-2
- Rebuild for OCaml 4.00.0.

* Thu Jun  7 2012 Richard W.M. Jones <rjones@redhat.com> - 1.3.1-1
- New upstream version 1.3.1.
- This is required for programs using findlib and OCaml 4.00.0.
- Add small patch to fix build of topfind.

* Sat Apr 28 2012 Richard W.M. Jones <rjones@redhat.com> - 1.2.8-1
- New upstream version 1.2.8.

* Fri Jan  6 2012 Richard W.M. Jones <rjones@redhat.com> - 1.2.7-1
- New upstream version 1.2.7.

* Thu Dec  8 2011 Richard W.M. Jones <rjones@redhat.com> - 1.2.6-5
- Don't strip bytecode binary (see RHBZ#435559).

* Fri Jun 3 2011 Orion Poplawski - 1.2.6-3
- Add Requires: ocaml (Bug #710290)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan  5 2011 Richard W.M. Jones <rjones@redhat.com> - 1.2.6-1
- New upstream version 1.2.6.

* Tue Dec 29 2009 Richard W.M. Jones <rjones@redhat.com> - 1.2.5-4
- Rebuild for OCaml 3.11.2.

* Wed Dec 16 2009 Richard W.M. Jones <rjones@redhat.com> - 1.2.5-3
- Use __ocaml_requires_opts / __ocaml_provides_opts.

* Wed Dec 16 2009 Richard W.M. Jones <rjones@redhat.com> - 1.2.5-2
- Update to use RPM dependency generator.

* Sun Oct  4 2009 Richard W.M. Jones <rjones@redhat.com> - 1.2.5-1
- New upstream version 1.2.5.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri May 22 2009 Richard W.M. Jones <rjones@redhat.com> - 1.2.4-3
- Rebuild for OCaml 3.11.1.
- New upstream version 1.2.4.
- camlp4/META patch is now upstream.

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Dec  4 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.3-5
- Change to camlp4/META means that this package really depends on
  the latest OCaml compiler.

* Thu Dec  4 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.3-4
- camlp4/META: camlp4.lib should depend on dynlink.

* Wed Nov 26 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.3-3
- Rebuild for OCaml 3.11.0+rc1.

* Fri Nov 21 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.3-2
- Force rebuild.

* Thu Nov 20 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.3-1
- New upstream version 1.2.3.

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.2-2
- Rebuild for OCaml 3.11.0

* Sun Aug 31 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.2-1
- New upstream version 1.2.2.
- Strip ocamlfind binary.
- Remove zero-length file.

* Mon Apr 21 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.1-3
- New upstream URLs.

* Sat Mar  1 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.1-2
- Experimental rebuild for ppc64.

* Tue Feb 12 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.1-1
- New upstream version 1.2.1.

* Thu Sep  6 2007 Richard W.M. Jones <rjones@redhat.com> - 1.1.2pl1-14
- Ignore Parsetree module, it's a part of the toplevel.

* Mon Sep  3 2007 Richard W.M. Jones <rjones@redhat.com> - 1.1.2pl1-13
- Bump version to force rebuild against ocaml -6 release.

* Thu Aug 30 2007 Richard W.M. Jones <rjones@redhat.com> - 1.1.2pl1-12
- Added BR: gawk.

* Thu Aug 30 2007 Richard W.M. Jones <rjones@redhat.com> - 1.1.2pl1-11
- Force rebuild because of changed BRs in base OCaml.

* Thu Aug  2 2007 Richard W.M. Jones <rjones@redhat.com> - 1.1.2pl1-10
- BR added ocaml-ocamldoc so that ocamlfind ocamldoc works.
- Fix path of camlp4 parsers in Makefile.

* Thu Jul 12 2007 Richard W.M. Jones <rjones@redhat.com> - 1.1.2pl1-9
- Added ExcludeArch: ppc64

* Thu Jul 12 2007 Richard W.M. Jones <rjones@redhat.com> - 1.1.2pl1-8
- Expanded tabs to spaces.
- Readded conditional opt section for files.

* Wed Jul 04 2007 Xavier Lamien <lxtnow[at]gmail.com> - 1.1.2pl1-7
- Fixed BR.

* Wed Jun 27 2007 Richard W.M. Jones <rjones@redhat.com> - 1.1.2pl1-6
- Fix configure line.
- Install doc/guide-html.
- Added dependency on ncurses-devel.

* Mon Jun 11 2007 Richard W.M. Jones <rjones@redhat.com> - 1.1.2pl1-5
- Build against 3.10.
- Update to latest package guidelines.

* Sat Jun  2 2007 Richard W.M. Jones <rjones@redhat.com> - 1.1.2pl1-4
- Handle bytecode-only architectures.

* Sat May 26 2007 Richard W.M. Jones <rjones@redhat.com> - 1.1.2pl1-3
- Missing builddep m4.

* Fri May 25 2007 Richard W.M. Jones <rjones@redhat.com> - 1.1.2pl1-2
- Use OCaml find-requires and find-provides.

* Fri May 18 2007 Richard W.M. Jones <rjones@redhat.com> - 1.1.2pl1-1
- Initial RPM release.

