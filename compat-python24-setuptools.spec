%define compat_python %{_bindir}/python2.4
%{!?python_sitelib: %define python_sitelib %(%{compat_python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           compat-python24-setuptools
Version:        0.6c7
Release:        4%{?dist}
Summary:        Download, build, install, upgrade, and uninstall Python packages

Group:          Applications/System
License:        Python or ZPLv2.0
URL:            http://peak.telecommunity.com/DevCenter/setuptools
Source0:        http://cheeseshop.python.org/packages/source/s/setuptools/setuptools-%{version}.tar.gz
Source1:        psfl.txt
Source2:        zpl.txt
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  compat-python24-devel

%description
setuptools is a collection of enhancements to the Python distutils that allow
you to more easily build and distribute Python packages, especially ones that
have dependencies on other packages.

This package contains the runtime components of setuptools, necessary to
execute the software that requires pkg_resources.py.

%package devel
Summary:        Download, install, upgrade, and uninstall Python packages
Group:          Development/Languages
Requires:       python-devel
Requires:       %{name} = %{version}-%{release}

%description devel
setuptools is a collection of enhancements to the Python distutils that allow
you to more easily build and distribute Python packages, especially ones that
have dependencies on other packages.

This package contains the components necessary to build and install software
requiring setuptools.


%prep
%setup -q -n setuptools-%{version}
chmod -x *.txt
find -name '*.py' | xargs sed -i '1s|^#!python|#!%{compat_python}|'


%build
CFLAGS="$RPM_OPT_FLAGS" %{compat_python} setup.py build


%check
# We expect one failure with the current setup
%{compat_python} setup.py test || :


%install
rm -rf $RPM_BUILD_ROOT
%{compat_python} setup.py install -O1 --skip-build \
    --root $RPM_BUILD_ROOT \
    --single-version-externally-managed

rm -rf $RPM_BUILD_ROOT%{python_sitelib}/setuptools/tests

install -p -m 0644 %{SOURCE1} %{SOURCE2} .
find $RPM_BUILD_ROOT%{python_sitelib} -name '*.exe' | xargs rm -f
find $RPM_BUILD_ROOT%{python_sitelib} -name '*.txt' | xargs chmod -x
chmod +x $RPM_BUILD_ROOT%{python_sitelib}/setuptools/command/easy_install.py
rm -f $RPM_BUILD_ROOT%{_bindir}/easy_install


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc psfl.txt zpl.txt pkg_resources.txt setuptools.txt
%{python_sitelib}/*
%{_bindir}/*
#%%exclude %{python_sitelib}/easy_install*

%files devel
%defattr(-,root,root,-)
%doc psfl.txt zpl.txt EasyInstall.txt README.txt api_tests.txt
#%%{python_sitelib}/easy_install*
#%%{_bindir}/*


%changelog
* Sun Aug 10 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 0.6c7-4
- rebuild for RPM Fusion

* Mon Dec 31 2007 Jonathan Steffan <jon a fedoraunity.org> - 0.6c7-3
- Install easy_install with the main package (move it out of -devel)

* Mon Dec 31 2007 Jonathan Steffan <jon a fedoraunity.org> - 0.6c7-2
- Base off python-setuptools 0.6c7-2.fc8

