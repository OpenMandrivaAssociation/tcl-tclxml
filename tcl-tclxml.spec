%define oname tclxml

Summary:	XML parsing library for the Tcl scripting language
Name:		tcl-%{oname}
Version:	3.2
Release:	1
License:	BSD
Group:		System/Libraries
Url:		http://tclxml.sourceforge.net/
Source0:	http://downloads.sourceforge.net/tclxml/tclxml-%{version}.tar.gz
Source1:	pkgIndex.tcl.in.gui
Patch0:		tclxml-3.2-sgmlparser.patch
Patch1:		tclxml-3.2-sfmt.patch
BuildRequires:	tcl-devel
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(libxslt)
Provides:	tclxml = %{EVRD}
Provides:	tcldom = %{EVRD}
Provides:	tclxslt = %{EVRD}
Requires:	tcl
Requires:	tcl-tcllib

%description
TclXML is a package that provides XML, DOM, and XSLT parsing for the
Tcl scripting language.

%files
%doc LICENSE ANNOUNCE ChangeLog README.html
%doc doc/*.html
%dir %{tcl_sitearch}/%{oname}%{version}
%{tcl_sitearch}/%{oname}%{version}/*.so
%{tcl_sitearch}/%{oname}%{version}/*.tcl
%{_libdir}/libTclxml%{version}.so

#----------------------------------------------------------------------------

%package gui
Summary:	UI widgets for manipulating a DOM tree
Group:		System/Libraries
Requires:	%{name} = %{EVRD}

%description gui
This package provides some useful widgets for manipulating a DOM tree.

%files gui
%dir %{tcl_sitelib}/%{oname}-gui%{version}
%{tcl_sitelib}/%{oname}-gui%{version}/*.tcl

#----------------------------------------------------------------------------

%package devel
Summary:	Development files for the tclxml packages
Group:		Development/Other
Requires:	%{name} = %{EVRD}

%description devel
Development header files for the tclxml packages. This includes all of the
header files for the tclxml, tcldom, and tclxslt packages

%files devel
%{_includedir}/tclxml
%{_includedir}/tcldom-libxml2
%{_includedir}/tclxml-libxml2
%{_libdir}/TclxmlConfig.sh
%{tcl_sitearch}/%{oname}%{version}/*.a

#----------------------------------------------------------------------------

%prep
%setup -q -n %{oname}-%{version}
%patch0 -p1
%patch1 -p1

# Fix a few spurious execute permissions
chmod -x ChangeLog doc/xsltsl/cmp.xsl *.c

# Clean up some DOS line endings
sed -i -e 's/\r//' doc/README.xml.in

%build
%configure2_5x
%make

%install
%makeinstall_std
install -p -m 0644 include/tclxml/*.h %{buildroot}%{_includedir}/tclxml
mkdir -p %{buildroot}%{_includedir}/tcldom-libxml2
install -p -m 0644 include/tcldom-libxml2/*.h %{buildroot}%{_includedir}/tcldom-libxml2
mkdir -p %{buildroot}%{_includedir}/tclxml-libxml2
install -p -m 0644 include/tclxml-libxml2/*.h %{buildroot}%{_includedir}/tclxml-libxml2

mkdir -p %{buildroot}%{tcl_sitearch}
mv %{buildroot}%{_libdir}/Tclxml%{version} %{buildroot}%{tcl_sitearch}/%{oname}%{version}

ln -s tcl%{tcl_version}/%{oname}%{version}/libTclxml%{version}.so %{buildroot}%{_libdir}/libTclxml%{version}.so

sed s,"%{_libdir}/Tclxml%{version}","%{tcl_sitearch}/%{oname}%{version}",g -i %{buildroot}%{_libdir}/TclxmlConfig.sh

chmod a-x %{buildroot}%{tcl_sitearch}/%{oname}%{version}/*.a

# Install the examples in a -gui subpackage
install -d %{buildroot}%{tcl_sitelib}/%{oname}-gui%{version}
sed -e 's/@VERSION@/%{version}/' < %{SOURCE1} > %{buildroot}%{tcl_sitelib}/%{oname}-gui%{version}/pkgIndex.tcl
install -p -m 0644 examples/tcldom/domtree.tcl \
	examples/tcldom/domtree-treectrl.tcl \
	examples/tcldom/domtext.tcl \
	examples/tcldom/cgi2dom.tcl \
	%{buildroot}%{tcl_sitelib}/%{oname}-gui%{version}/

