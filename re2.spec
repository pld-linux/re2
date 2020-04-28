#
# Conditional build:
%bcond_without	tests		# build without tests
%bcond_without	static_libs	# don't build static libraries

%define		tagver	2020-04-01
%define		ver		%(echo %{tagver} | tr -d -)
Summary:	C++ fast alternative to backtracking RE engines
Summary(pl.UTF-8):	Szybka alternatywna dla silników RE w C++
Name:		re2
Version:	%{ver}
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/google/re2/releases
Source0:	https://github.com/google/re2/archive/%{tagver}/%{name}-%{tagver}.tar.gz
# Source0-md5:	8e6079dff019309f1e1f0fad8cd637b8
Patch0:		test-compile.patch
URL:		https://github.com/google/re2
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	rpmbuild(macros) >= 1.734
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

%description -l pl.UTF-8
RE2 to biblioteka C++ będąca szybką, bezpieczną, przyjazną dla wątków
alternatywą dla silników wyrażeń regularnych ze śledzeniem, takimi jak
używane w PCRE, Perlu i Pythonie.

Silniki ze śledzeniem mają zwykle dużo możliwości i wygodny lukier
składniowy, ale można je zmusić do wykładniczej złożoności czasowej
nawet przy niewielkim wejściu.

Dla odmiany RE2 używa teorii automatów, aby zagwarantować czas
wyszukiwania liniowy względem rozmiaru wejścia kosztem braku
niektórych możliwości (np. odwołań wstecznych i uogólnionych
zapewnień).

%package devel
Summary:	C++ header files and library symbolic link for RE2
Summary(pl.UTF-8):	Pliki nagłówkowe C++ i dowiązanie do biblioteki RE2
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel >= 6:4.7

%description devel
This package contains the C++ header files and symbolic link to the
shared RE2 library.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe C++ oraz dowiązanie symboliczne do
biblioteki współdzielonej RE2.

%package static
Summary:	Static RE2 library
Summary(pl.UTF-8):	Statyczna biblioteka RE2
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static RE2 library.

%description static -l pl.UTF-8
Statyczna biblioteka RE2.

%prep
%setup -q -n %{name}-%{tagver}
%patch0 -p1

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
%attr(755,root,root) %ghost %{_libdir}/libre2.so.6

%files devel
%defattr(644,root,root,755)
%doc doc/syntax.txt
%attr(755,root,root) %{_libdir}/libre2.so
%{_includedir}/re2
%{_pkgconfigdir}/re2.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libre2.a
%endif
