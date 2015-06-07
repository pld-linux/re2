#
# Conditional build:
%bcond_without	tests		# build without tests
%bcond_without	static_libs	# don't build static libraries

%define		subver	2015-05-01
%define		ver		%(echo %{subver} | tr -d -)
Summary:	C++ fast alternative to backtracking RE engines
Name:		re2
Version:	%{ver}
Release:	1
License:	BSD
Group:		Libraries
Source0:	https://github.com/google/re2/archive/%{subver}/%{name}-%{version}.tar.gz
# Source0-md5:	72025cc33750878d0457c9422b396ee7
Patch0:		test-compile.patch
Patch1:		symbols.patch
URL:		https://github.com/google/re2
BuildRequires:	libstdc++-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
RE2 is a C++ library providing a fast, safe, thread-friendly
alternative to backtracking regular expression engines like those used
in PCRE, Perl, and Python.

Backtracking engines are typically full of features and convenient
syntactic sugar but can be forced into taking exponential amounts of
time on even small inputs.

In contrast, RE2 uses automata theory to guarantee that regular
expression searches run in time linear in the size of the input, at
the expense of some missing features (e.g back references and
generalized assertions).

%package devel
Summary:	C++ header files and library symbolic links for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the C++ header files and symbolic links to the
shared libraries for %{name}. If you would like to develop programs
using %{name}, you will need to install %{name}-devel.

%package static
Summary:	Static %{name} library
Summary(pl.UTF-8):	Statyczna biblioteka %{name}
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static %{name} library.

%description static -l pl.UTF-8
Statyczna biblioteka %{name}.

%prep
%setup -q -n %{name}-%{subver}
%patch0 -p1
%patch1 -p1

%build
# The -pthread flag issue has been submitted upstream:
# http://groups.google.com/forum/?fromgroups=#!topic/re2-dev/bkUDtO5l6Lo
%{__make} all %{?with_tests:compile-test} \
	CXX="%{__cxx}" \
	CXXFLAGS="%{rpmcxxflags}" \
	LDFLAGS="%{rpmldflags} -pthread" \
	includedir=%{_includedir} \
	libdir=%{_libdir}

%if %{with tests}
%{__make} test \
	CXX="%{__cxx}" \
	CXXFLAGS="%{rpmcxxflags}"
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	INSTALL="install -p" \
	includedir=%{_includedir} \
	libdir=%{_libdir} \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS CONTRIBUTORS LICENSE README
%attr(755,root,root) %{_libdir}/libre2.so.*.*.*
%ghost %{_libdir}/libre2.so.0

%files devel
%defattr(644,root,root,755)
%doc doc/syntax.txt
%{_libdir}/libre2.so
%{_includedir}/re2

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libre2.a
%endif
