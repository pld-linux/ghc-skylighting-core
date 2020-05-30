#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	skylighting-core
Summary:	Syntax highlighting library
Name:		ghc-%{pkgname}
Version:	0.8.4
Release:	1
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/skylighting-core
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	2db93ad3dda9e34b3b917835c56a0920
URL:		http://hackage.haskell.org/package/skylighting-core
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-aeson >= 1.0
BuildRequires:	ghc-ansi-terminal >= 0.7
BuildRequires:	ghc-attoparsec
BuildRequires:	ghc-base64-bytestring
BuildRequires:	ghc-blaze-html >= 0.5
BuildRequires:	ghc-case-insensitive
BuildRequires:	ghc-colour >= 2.0
BuildRequires:	ghc-hxt
BuildRequires:	ghc-regex-pcre
BuildRequires:	ghc-safe
BuildRequires:	ghc-transformers
BuildRequires:	ghc-utf8-string
%if %{with prof}
BuildRequires:	ghc-prof
BuildRequires:	ghc-aeson-prof >= 1.0
BuildRequires:	ghc-ansi-terminal-prof >= 0.7
BuildRequires:	ghc-attoparsec-prof
BuildRequires:	ghc-base64-bytestring-prof
BuildRequires:	ghc-blaze-html-prof >= 0.5
BuildRequires:	ghc-case-insensitive-prof
BuildRequires:	ghc-colour-prof >= 2.0
BuildRequires:	ghc-hxt-prof
BuildRequires:	ghc-regex-pcre-prof
BuildRequires:	ghc-safe-prof
BuildRequires:	ghc-transformers-prof
BuildRequires:	ghc-utf8-string-prof
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_eq	ghc
Requires(post,postun):	/usr/bin/ghc-pkg
Requires:	ghc-aeson >= 1.0
Requires:	ghc-ansi-terminal >= 0.7
Requires:	ghc-attoparsec
Requires:	ghc-base64-bytestring
Requires:	ghc-blaze-html >= 0.5
Requires:	ghc-case-insensitive
Requires:	ghc-colour >= 2.0
Requires:	ghc-hxt
Requires:	ghc-regex-pcre
Requires:	ghc-safe
Requires:	ghc-transformers
Requires:	ghc-utf8-string
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
This package provides the core functionality of the Skylighting
project, a Haskell syntax highlighting library with support for KDE
XML syntax highlighting descriptions.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-aeson-prof >= 1.0
Requires:	ghc-ansi-terminal-prof >= 0.7
Requires:	ghc-attoparsec-prof
Requires:	ghc-base64-bytestring-prof
Requires:	ghc-blaze-html-prof >= 0.5
Requires:	ghc-case-insensitive-prof
Requires:	ghc-colour-prof >= 2.0
Requires:	ghc-hxt-prof
Requires:	ghc-regex-pcre-prof
Requires:	ghc-safe-prof
Requires:	ghc-transformers-prof
Requires:	ghc-utf8-string-prof

%description prof
Profiling %{pkgname} library for GHC.  Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--flags="system-pcre" \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build
runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc changelog.md README.md %{name}-%{version}-doc/*
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a

%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Skylighting
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Skylighting/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Skylighting/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Skylighting/Format
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Skylighting/Format/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Skylighting/Format/*.dyn_hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Skylighting/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Skylighting/Format/*.p_hi
%endif
