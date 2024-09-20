#
# Conditional build:
%bcond_without	tests		# unit tests
%bcond_without	static_libs	# static library

# 2024-06-01+ require abseil-cpp 2024+
%define		tagver	2024-05-01
%define		ver		%(echo %{tagver} | tr -d -)
Summary:	C++ fast alternative to backtracking RE engines
Summary(pl.UTF-8):	Szybka alternatywna dla silników RE w C++
Name:		re2
Version:	%{ver}
Release:	2
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/google/re2/releases
Source0:	https://github.com/google/re2/archive/%{tagver}/%{name}-%{tagver}.tar.gz
# Source0-md5:	ad0d8b0639b84b89095e3ea583c89125
Patch0:		test-compile.patch
URL:		https://github.com/google/re2
BuildRequires:	abseil-cpp-devel
BuildRequires:	cmake >= 3.13
%{?with_tests:BuildRequires:	google-benchmark-devel}
%{?with_tests:BuildRequires:	gtest-devel}
BuildRequires:	libstdc++-devel >= 6:5
BuildRequires:	rpmbuild(macros) >= 1.742
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
Requires:	abseil-cpp-devel
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
%if %{with static_libs}
%cmake -B build-static \
	-DBUILD_SHARED_LIBS=OFF

%{__make} -C build-static
%endif

%cmake -B build \
	%{cmake_on_off tests RE2_BUILD_TESTING}

%{__make} -C build

%if %{with tests}
%{__make} -C build test
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with static_libs}
%{__make} -C build-static install \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CONTRIBUTING.md LICENSE README SECURITY.md
%attr(755,root,root) %{_libdir}/libre2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libre2.so.11

%files devel
%defattr(644,root,root,755)
%doc doc/syntax.txt
%attr(755,root,root) %{_libdir}/libre2.so
%{_includedir}/re2
%{_pkgconfigdir}/re2.pc
%{_libdir}/cmake/re2

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libre2.a
%endif
