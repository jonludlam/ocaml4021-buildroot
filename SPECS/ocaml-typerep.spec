# if the build is running on copr
%if 0%{?copr_username:1}
# define your copr_username and copr_projectname
%global scl %{copr_username}-%{copr_projectname}
%else
# different build system need only name of the collection, ocaml402 in this case
%global scl ocaml402
%endif

%{?scl:%scl_package ocaml-pa-ounit}
%{!?scl:%global pkg_name %{name}}

%define _use_internal_dependency_generator 0
%define __find_requires scl enable %{scl} "/usr/lib/rpm/ocaml-find-requires.sh -c"
%define __find_provides scl enable %{scl} /usr/lib/rpm/ocaml-find-provides.sh

%define opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)

Name:           %{?scl_prefix}ocaml-typerep
Version:        111.17.00
Release:        2%{?dist}
Summary:        Runtime types for OCaml.

Group:          Development/Libraries
License:        Apache Software License 2.0
URL:            https://github.com/janestreet/typerep
Source0:        https://ocaml.janestreet.com/ocaml-core/%{version}/individual/typerep-%{version}.tar.gz
ExcludeArch:    sparc64 s390 s390x

BuildRequires:  %{?scl_prefix}ocaml >= 4.00.1
BuildRequires:  %{?scl_prefix}ocaml-findlib-devel
BuildRequires:  %{?scl_prefix}ocaml-camlp4-devel
BuildRequires:  %{?scl_prefix}ocaml-ocamldoc
BuildRequires:  %{?scl_prefix}ocaml-bin-prot >= 109.53.02
BuildRequires:  %{?scl_prefix}ocaml-sexplib >= 109.55.02
BuildRequires:  %{?scl_prefix}ocaml-type-conv

%if 0%{?scl:1}
BuildRequires:  %{?scl_prefix}build
BuildRequires:  %{?scl_prefix}runtime
%endif

%description
Runtime types for OCaml.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       %{?scl_prefix}ocaml-sexplib
Requires:       %{?scl_prefix}ocaml-bin-prot
Requires:       %{?scl_prefix}ocaml-type-conv

%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.


%prep
%setup -q -n typerep-%{version}

%build
%{?scl:scl enable %{scl} "}
ocaml setup.ml -configure --prefix %{_prefix} \
      --libdir %{_libdir} \
      --libexecdir %{_libexecdir} \
      --exec-prefix %{_exec_prefix} \
      --bindir %{_bindir} \
      --sbindir %{_sbindir} \
      --mandir %{_mandir} \
      --datadir %{_datadir} \
      --localstatedir %{_localstatedir} \
      --sharedstatedir %{_sharedstatedir}
ocaml setup.ml -build
%{?scl:"}

%check
%{?scl:scl enable %{scl} "}
ocaml setup.ml -test
%{?scl:"}


%install
rm -rf $RPM_BUILD_ROOT
export DESTDIR=$RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR $OCAMLFIND_DESTDIR/stublibs
%{?scl:scl enable %{scl} "}
ocaml setup.ml -install
%{?scl:"}

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc LICENSE.txt  THIRD-PARTY.txt INRIA-DISCLAIMER.txt
%{_libdir}/ocaml/typerep_lib
%{_libdir}/ocaml/typerep_extended
%{_libdir}/ocaml/typerep_generics_sexprep
%if %opt
%exclude %{_libdir}/ocaml/typerep_lib/*.a
%exclude %{_libdir}/ocaml/typerep_lib/*.cmxa
%exclude %{_libdir}/ocaml/typerep_extended/*.a
%exclude %{_libdir}/ocaml/typerep_extended/*.cmxa
%exclude %{_libdir}/ocaml/typerep_generics_sexprep/*.cmxa
%endif
%exclude %{_libdir}/ocaml/typerep_lib/*.ml
%exclude %{_libdir}/ocaml/typerep_lib/*.mli
%exclude %{_libdir}/ocaml/typerep_extended/*.ml
%exclude %{_libdir}/ocaml/typerep_extended/*.mli
%exclude %{_libdir}/ocaml/typerep_generics_sexprep/*.mli


%files devel
%defattr(-,root,root,-)
%doc LICENSE.txt  THIRD-PARTY.txt INRIA-DISCLAIMER.txt
%if %opt
%{_libdir}/ocaml/typerep_lib/*.a
%{_libdir}/ocaml/typerep_lib/*.cmxa
%{_libdir}/ocaml/typerep_extended/*.a
%{_libdir}/ocaml/typerep_extended/*.cmxa
%{_libdir}/ocaml/typerep_generics_sexprep/*.cmxa
%endif
%{_libdir}/ocaml/typerep_lib/*.ml
%{_libdir}/ocaml/typerep_lib/*.mli
%{_libdir}/ocaml/typerep_extended/*.ml
%{_libdir}/ocaml/typerep_extended/*.mli
%{_libdir}/ocaml/typerep_generics_sexprep/*.mli

%changelog
* Wed Dec 3 2014 Jon Ludlam <jonathan.ludlam@citrix.com> - 111.17.00-2
- SCLify

* Tue Oct 14 2014 David Scott <dave.scott@citrix.com> - 111.17.00-1
- Update to 111.17.00

* Wed Jan 01 2014 Edvard Fagerholm <edvard.fagerholm@gmail.com> - 109.55.02-1
- Initial package for Fedora 20.
