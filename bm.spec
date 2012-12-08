# no need to bzip2 patches, the macro below makes the .src.rpm use
# bzip2 compression instead of gzip (the default one)
%define _source_payload w9.bzdio

Name: bm
Version: 2.1
Release: 227
Summary: BuildManager - rpm package building helper
Group: Development/Other
License: GPL
URL: http://svn.mandriva.com/cgi-bin/viewvc.cgi/soft/build_system/bm/ 
Source: bm-%{version}.tar.bz2
Source1:	%{name}.bash-completion
Patch0: bm-2.1-rpmbuild.patch
Patch1: bm-2.1-only-move-srpm.patch
Patch2: bm-2.1-use-subprocess.patch
patch3: bm-2.1-missing-exceptions.patch
Patch4: bm-2.1-unpack-nodeps.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires: python
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
%patch0 -p1
%patch1 -p0
%patch2 -p1
%patch3 -p0

%build
python setup.py build

%install
rm -rf %{buildroot}
python setup.py install --root=%{buildroot} --record=INSTALLED_FILES

# Using compile inline since niemeyer's python macros still not available on mdk rpm macros
find %{buildroot}%{py_puresitedir} -name '*.pyc' -exec rm -f {} \; 
python -c "import sys, os, compileall; br='%{buildroot}'; compileall.compile_dir(sys.argv[1], ddir=br and 
(sys.argv[1][len(os.path.abspath(br)):]+'/') or None)" %{buildroot}%{py_puresitedir}

# bash completion
install -d -m 755 %{buildroot}%{_sysconfdir}/bash_completion.d
install -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/bash_completion.d/%{name}

%clean
rm -rf %{buildroot}

%files -f INSTALLED_FILES
%defattr(0644,root,root,0755)
%doc LICENSE
%defattr(-,root,root,-)
%{_sysconfdir}/bash_completion.d/%{name}





%changelog
* Fri May 20 2011 Bogdano Arendartchuk <bogdano@mandriva.com> 2.1-225
+ Revision: 676366
- patched to use --nodeps when unpacking source rpms

* Tue May 03 2011 Oden Eriksson <oeriksson@mandriva.com> 2.1-224
+ Revision: 663328
- mass rebuild

  + Eugeni Dodonov <eugeni@mandriva.com>
    - Bring back patches which were removed wrongly.

  + Ural Mullabaev <mur@mandriva.org>
    - remove 2 patches

* Fri Oct 29 2010 Michael Scherer <misc@mandriva.org> 2.1-223mdv2011.0
+ Revision: 590153
- rebuild for python 2.7

* Tue Mar 16 2010 Oden Eriksson <oeriksson@mandriva.com> 2.1-222mdv2010.1
+ Revision: 522239
- rebuilt for 2010.1

* Wed Jun 10 2009 Bogdano Arendartchuk <bogdano@mandriva.com> 2.1-221mdv2010.0
+ Revision: 384983
- added patch to define the exceptions used when the specfile is not found,
  to not show the ugly traceback (pointed by pzanoni)

  + Michael Scherer <misc@mandriva.org>
    - add the url of the svn, this is the only know page ( maybe if someone write something on the wiki ), close bug 37042

* Fri Jan 16 2009 Bogdano Arendartchuk <bogdano@mandriva.com> 2.1-220mdv2009.1
+ Revision: 330266
- added patch to use the subprocess module instead of popen2 (deprecated in
  python-2.6)

* Wed Dec 24 2008 Funda Wang <fwang@mandriva.org> 2.1-219mdv2009.1
+ Revision: 318363
- rebuild for new python

* Mon Jun 16 2008 Thierry Vignaud <tv@mandriva.org> 2.1-218mdv2009.0
+ Revision: 220488
- rebuild

* Fri Jan 11 2008 Thierry Vignaud <tv@mandriva.org> 2.1-217mdv2008.1
+ Revision: 149012
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Bogdano Arendartchuk <bogdano@mandriva.com>
    - added patch to make --move-srpm move only .src.rpm files inside SRPMS/

* Wed Aug 29 2007 Guillaume Rousse <guillomovitch@mandriva.org> 2.1-215mdv2008.0
+ Revision: 74578
- bash completion support


* Wed Dec 13 2006 Nicolas LÃ©cureuil <neoclust@mandriva.org> 2.1-214mdv2007.0
+ Revision: 96492
- Rebuild against new python

* Tue Nov 28 2006 Andreas Hasenack <andreas@mandriva.com> 2.1-213mdv2007.1
+ Revision: 87832
- rebuild with python 2.5
- renamed mdv to packages because mdv is too generic and it's hosting only packages anyway
- uncompressed patch file and marked .src.rpm to use bzip2 compression for its payload

  + GÃ¶tz Waschk <waschk@mandriva.org>
    - rebuild for new python

  + Michael Scherer <misc@mandriva.org>
    - remove duplicated macros
    - clean BuildRoot in %%install
    - this package is not arch dependent, so tag it as noarch
    - use mkrel
    - fix build on x86_64

  + Helio Chissini de Castro <helio@mandriva.com>
    - Removed Buildarch noarch
    - Missing macro %%pyver
    - Fixed lib64 build for x86_64
    - Fixed python macros
    - Created dir structure

* Thu Mar 17 2005 Helio Chissini de Castro <helio@mandrakesoft.com> 2.1-2mdk
- Ordering requires to avoid future mess on next releasesof RPM with PreReq

* Thu Mar 17 2005 Helio Chissini de Castro <helio@mandrakesoft.com> 2.1-1mdk
- First BuildManager release on Mandrake Contrib

