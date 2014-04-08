%define	oname	freetype
%define	major	2
%define	libname	%mklibname %{oname} %{major}
%define	devname	%mklibname -d %{oname} %{major}

Summary:	TrueType font rasterizer library
Name:		freetype1
Version:	1.4pre.cvs20060210
Release:	1
License:	BSD
Group:		System/Libraries
BuildRequires:	pkgconfig(sm) pkgconfig(x11) pkgconfig(ice)
URL:		http://www.freetype.org
Source0:	%{name}-%{version}.tar.xz
# Patch from X-TT sources, to correctly support Dynalab TTF fonts
# very popular in Taiwan
Patch0:		freetype1.3-adw-nocheck.patch
Patch5:		freetype-1.3.1-format_not_a_string_literal_and_no_format_arguments.diff
Patch6:		freetype1-1.4pre.cvs20060210-add-missing-typedefs.patch
Patch7:		freetype1-1.4pre.cvs20060210-contrib-tools-build-fixes.patch
Patch8:		freetype1-1.4pre.cvs20060210-no-rpath.patch

# debian patches
Patch100:	01_ttf2pk-1.5-omega.dpatch
Patch101:	02_ttf2pk-1.5-kpathsea.dpatch
Patch102:	03_ttf2pk-1.5-uninitialized_length.dpatch
Patch103:	04_ftstrpnm_utf8.dpatch
Patch104:	06_ttfonts_map.dpatch
Patch105:	07_type-punned.dpatch
Patch106:	98_configure_in.dpatch

%description
The FreeType engine is a free and portable TrueType font rendering engine.
It has been developed to provide TT support to a great variety of
platforms and environments. Note that FreeType is a library, not a
stand-alone application, though some utility applications are included.

%package -n	%{oname}-progs
Summary:	Bundled Tests, Demos and Tools for FreeType
Group:		Graphics

%description -n	%{oname}-progs
The FreeType engine is a free and portable TrueType font rendering
engine. It has been developed to provide TT support to a great variety
of platforms and environments.

This package contains several programs bundled with the FreeType engine
for testing and demonstration purposes as well as some contributed
utilities, such as ttf2bdf, ttf2pfb, and ttfbanner.
	
%package -n	%{libname}
Summary:	Shared libraries for a free and portable TrueType font rendering engine
Group:		System/Libraries

%description -n	%{libname}
The FreeType engine is a free and portable TrueType font rendering engine.
It has been developed to provide TT support to a great variety of
platforms and environments. Note that FreeType is a library, not a
stand-alone application, though some utility applications are included.

%package -n	%{devname}
Summary:	Header files and static library for development with FreeType2
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Provides:	%{oname}-devel

%description -n %{devname}
This package is only needed if you intend to develop or compile applications
which rely on the FreeType library. If you simply want to run existing
applications, you won't need this package.

%prep
%setup -q
%patch0 -p0 -b .adw~
%patch5 -p0 -b .strfmt~
%patch6 -p1 -b .typedef~
%patch7 -p1 -b .contrib~
%patch8 -p1 -b .norpath~

%patch100 -p1
%patch101 -p1
%patch102 -p1
%patch103 -p1
%patch104 -p1
%patch105 -p1
%patch106 -p1

for i in . contrib/{ttf2bdf,ttfbanner}; do
	pushd $i
	autoreconf -fiv
	popd
done

%build
%global optflags %{optflags} -DTT_CONFIG_OPTION_EXTEND_ENGINE -DTT_CONFIG_OPTION_GRAY_SCALING
for i in . contrib/{ttf2bdf,ttfbanner}; do
	pushd $i
	%configure2_5x --enable-shared
	%make || %make
	popd
done

%install
for i in . contrib/{ttf2bdf,ttfbanner}; do
	%makeinstall -C $i
done

%find_lang %{oname}

%files -n %{oname}-progs
%{_bindir}/*
%{_mandir}/man1/*.1*

%files -n %{libname} -f %{oname}.lang
%doc README announce
%{_libdir}/libttf.so.%{major}*

%files -n %{devname}
%doc docs
%{_includedir}/freetype
%{_libdir}/libttf.so
