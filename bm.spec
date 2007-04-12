# no need to bzip2 patches, the macro below makes the .src.rpm use
# bzip2 compression instead of gzip (the default one)
%define _source_payload w9.bzdio

Name: bm
Version: 2.1
Release: %mkrel 214
Summary: BuildManager - rpm package building helper
Group: Development/Other
License: GPL
URL: http://moin.conetiva.com.br/BuildManager
Source: bm-%{version}.tar.bz2
Patch: bm-2.1-rpmbuild.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires: python >= %pyver
Requires: rpm-build
BuildRequires: rpm-build
BuildRequires: python 
BuildRequires: python-devel
BuildArch:     noarch

%description
BuildManager, or bm, is a program that wraps and extends rpm while building
packages. Its features allow one to batch process thousand of rpms at once,
controling logs, rpm and srpm moving, filtering the list of files, ignoring
given packages, completely cleaning the build directories, and many other
features.

%description -l pt_BR
O BuildManager, ou bm, é um programa que encapsula e estende o rpm na
construção de pacotes. Suas características permitem o processamento em
série ou paralelo de milhares de rpms em uma única execução, controlando
logs, movendo rpms e srpms, filtrando a lista de arquivos, ignorando pacotes
selecionados, limpando completamente os diretórios de construção, e muitas
outras possibilidades.

%prep
%setup -q
%patch -p1

%build
python setup.py build

%install
rm -rf %{buildroot}
python setup.py install --root=%{buildroot} --record=INSTALLED_FILES

# Using compile inline since niemeyer's python macros still not available on mdk rpm macros
find %{buildroot}%{py_puresitedir} -name '*.pyc' -exec rm -f {} \; 
python -c "import sys, os, compileall; br='%{buildroot}'; compileall.compile_dir(sys.argv[1], ddir=br and 
(sys.argv[1][len(os.path.abspath(br)):]+'/') or None)" %{buildroot}%{py_puresitedir}

%clean
rm -rf %{buildroot}

%files -f INSTALLED_FILES
%defattr(0644,root,root,0755)
%doc LICENSE
%defattr(-,root,root,-)



