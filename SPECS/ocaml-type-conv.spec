# if the build is running on copr
%if 0%{?copr_username:1}
# define your copr_username and copr_projectname
%global scl %{copr_username}-%{copr_projectname}
%else
# different build system need only name of the collection, ocaml402 in this case
%global scl ocaml402
%endif

%{?scl:%scl_package ocaml-type-conv}
%{!?scl:%global pkg_name %{name}}

%define _use_internal_dependency_generator 0
%define __find_requires scl enable %{scl} "/usr/lib/rpm/ocaml-find-requires.sh -c"
%define __find_provides scl enable %{scl} /usr/lib/rpm/ocaml-find-provides.sh

Name:           %{?scl_prefix}ocaml-type-conv
Version:        112.01.00
Release:        1%{?dist}
Summary:        OCaml base library for type conversion

License:        LGPLv2+ with exceptions and BSD
URL:            http://www.ocaml.info/software.html#type_driven
Source0:        https://ocaml.janestreet.com/ocaml-core/%{version}/individual/type_conv-%{version}.tar.gz
#Patch0:         type-conv-META.patch

BuildRequires:  %{?scl_prefix}ocaml >= 4.02.0
BuildRequires:  %{?scl_prefix}ocaml-findlib
BuildRequires:  %{?scl_prefix}ocaml-ocamldoc
BuildRequires:  %{?scl_prefix}ocaml-camlp4-devel

%if 0%{?scl:1}
BuildRequires:  %{?scl_prefix}build
BuildRequires:  %{?scl_prefix}runtime
%endif

%description
The type-conv mini library factors out functionality needed by
different preprocessors that generate code from type specifications,
because this functionality cannot be duplicated without losing the
ability to use these preprocessors simultaneously.

%prep
%setup -q -n type_conv-%{version}
#%patch0 -p1
#dos2unix LICENSE.Tywith

%build
%{?scl:scl enable %{scl} "}
make
%{?scl:"}

%install
%{?scl:scl enable %{scl} "}
export DESTDIR=%{buildroot}
export OCAMLFIND_DESTDIR=%{buildroot}/%{_libdir}/ocaml
mkdir -p \$OCAMLFIND_DESTDIR
make install
%{?scl:"}

%files
%doc CHANGES.md COPYRIGHT.txt INRIA-DISCLAIMER.txt LICENSE-Tywith.txt LICENSE.txt README.md THIRD-PARTY.txt
%{_libdir}/ocaml/type_conv

%changelog
* Thu Dec 4 2014 Jon Ludlam <jonathan.ludlam@citrix.com> - 112.01.00-1
- Update to 112.01.00

* Tue Dec 2 2014 Jon Ludlam <jonathan.ludlam@citrix.com> - 111.13.00-2
- SCLify

* Wed Jul 16 2014 David Scott <dave.scott@citrix.com> - 111.13.00-1
- Updated to 111.13.00 for Mirage compatibility

* Thu Nov 25 2010 Mike McClurg <mike.mcclurg@citrix.com> - 109.20.00-1
- Updated to version 2.0.1 for compatability with OCaml 3.12.0

* Fri May 14 2010 David Scott <dave.scott@eu.citrix.com>
- Customised for XCP

* Wed Jan 07 2009 Florent Monnier <blue_prawn@mandriva.org> 1.6.5-1mdv2009.1
+ Revision: 326698
- corrected group
- import ocaml-type-conv


* Sat Dec 20 2008 Florent Monnier <fmonnier@linux-nantes.org> 1.6.5-1mdv
- Initial RPM release made from the fedora rpm .spec file (revision 1.9) by Richard W.M. Jones
# found there: http://cvs.fedoraproject.org/viewvc/devel/ocaml-type-conv/ocaml-type-conv.spec
