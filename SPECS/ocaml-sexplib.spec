# if the build is running on copr
%if 0%{?copr_username:1}
# define your copr_username and copr_projectname
%global scl %{copr_username}-%{copr_projectname}
%else
# different build system need only name of the collection, ocaml402 in this case
%global scl ocaml402
%endif

%{?scl:%scl_package ocaml-sexplib}
%{!?scl:%global pkg_name %{name}}

%define _use_internal_dependency_generator 0
%define __find_requires scl enable %{scl} "/usr/lib/rpm/ocaml-find-requires.sh -c"
%define __find_provides scl enable %{scl} /usr/lib/rpm/ocaml-find-provides.sh

Name:           %{?scl_prefix}ocaml-sexplib
Version:        112.01.00
Release:        1%{?dist}
Summary:        Convert values to and from s-expressions in OCaml

License:        LGPLv2+ with exceptions and BSD
URL:            https://ocaml.janestreet.com
Source0:        https://ocaml.janestreet.com/ocaml-core/%{version}/individual/sexplib-%{version}.tar.gz


BuildRequires:  %{?scl_prefix}ocaml >= 4.00.0
BuildRequires:  %{?scl_prefix}ocaml-findlib
BuildRequires:  %{?scl_prefix}ocaml-ocamldoc
BuildRequires:  %{?scl_prefix}ocaml-camlp4-devel
BuildRequires:  %{?scl_prefix}ocaml-type-conv

%if 0%{?scl:1}
BuildRequires:  %{?scl_prefix}build
BuildRequires:  %{?scl_prefix}runtime
%endif

%description
Convert values to and from s-expressions in OCaml.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       %{?scl_prefix}ocaml-camlp4-devel%{?_isa}
Requires:       %{?scl_prefix}ocaml-type-conv%{?_isa}

%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%prep
%setup -q -n sexplib-%{version}

%build
%{?scl:scl enable %{scl} "}
make
%{?scl:"}

%install
export DESTDIR=%{buildroot}
export OCAMLFIND_DESTDIR=%{buildroot}/%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR
%{?scl:scl enable %{scl} "}
make install
%{?scl:"}

%files
%doc CHANGES.md
%doc COPYRIGHT.txt
%doc INRIA-DISCLAIMER.txt
%doc INSTALL.txt
%doc LICENSE.txt
%doc LICENSE-Tywith.txt
%doc README.md
%doc THIRD-PARTY.txt
%{_libdir}/ocaml/sexplib
%exclude %{_libdir}/ocaml/sexplib/*.a
%exclude %{_libdir}/ocaml/sexplib/*.cmxa
%exclude %{_libdir}/ocaml/sexplib/*.cmx
%exclude %{_libdir}/ocaml/sexplib/*.mli
%{_libdir}/ocaml/sexplib_num
%exclude %{_libdir}/ocaml/sexplib_num/*.a
%exclude %{_libdir}/ocaml/sexplib_num/*.cmxa
%exclude %{_libdir}/ocaml/sexplib_num/*.cmx
%exclude %{_libdir}/ocaml/sexplib_num/*.mli
%{_libdir}/ocaml/sexplib_unix
%exclude %{_libdir}/ocaml/sexplib_unix/*.a
%exclude %{_libdir}/ocaml/sexplib_unix/*.cmxa
%exclude %{_libdir}/ocaml/sexplib_unix/*.cmx

%files devel
%{_libdir}/ocaml/sexplib/*.a
%{_libdir}/ocaml/sexplib/*.cmx
%{_libdir}/ocaml/sexplib/*.cmxa
%{_libdir}/ocaml/sexplib/*.mli
%{_libdir}/ocaml/sexplib_num/*.a
%{_libdir}/ocaml/sexplib_num/*.cmx
%{_libdir}/ocaml/sexplib_num/*.cmxa
%{_libdir}/ocaml/sexplib_num/*.mli
%{_libdir}/ocaml/sexplib_unix/*.a
%{_libdir}/ocaml/sexplib_unix/*.cmx
%{_libdir}/ocaml/sexplib_unix/*.cmxa

%changelog
* Thu Dec 4 2014 Jon Ludlam <jonathan.ludlam@citrix.com> - 112.01.00-1
- Update to 112.01.00

* Wed Dec 3 2014 Jon Ludlam <jonathan.ludlam@citrix.com> - 111.25.00-2
- SCLify

* Thu Oct 23 2014 David Scott <dave.scott@citrix.com> - 111.25.00-1
- Update to 111.25.00

* Wed Jul 16 2014 David Scott <dave.scott@citrix.com> - 111.17.00-1
- Update to 111.17.00 for Mirage compat

* Fri May 30 2014 Euan Harris <euan.harris@citrix.com> - 109.20.00-2
- Split files correctly between base and devel packages

* Mon Jun  3 2013 David Scott <dave.scott@eu.citrix.com> - 109.20.00-1
- Initial package

