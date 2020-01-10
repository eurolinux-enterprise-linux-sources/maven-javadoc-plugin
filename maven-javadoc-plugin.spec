%global bootstrap 0

Name:           maven-javadoc-plugin
Version:        2.9
Release:        8%{?dist}
Summary:        Maven Javadoc Plugin

License:        ASL 2.0
URL:            http://maven.apache.org/plugins/maven-javadoc-plugin
Source0:        http://repo1.maven.org/maven2/org/apache/maven/plugins/%{name}/%{version}/%{name}-%{version}-source-release.zip
Patch0:         reduce-exceptions.patch

BuildRequires:  java-devel >= 1:1.7.0
BuildRequires:  apache-commons-io
BuildRequires:  apache-commons-lang
BuildRequires:  apache-commons-logging
BuildRequires:  jakarta-commons-httpclient
BuildRequires:  log4j
BuildRequires:  maven-local
BuildRequires:  maven-archiver
BuildRequires:  maven-artifact
BuildRequires:  maven-artifact-manager
BuildRequires:  maven-common-artifact-filters
BuildRequires:  maven-doxia-sink-api
BuildRequires:  maven-doxia-sitetools
BuildRequires:  maven-enforcer-plugin
BuildRequires:  maven-model
BuildRequires:  maven-plugin-annotations
BuildRequires:  maven-plugin-plugin
BuildRequires:  maven-plugin-testing-harness
BuildRequires:  maven-project
BuildRequires:  maven-resources-plugin
BuildRequires:  maven-settings
BuildRequires:  maven-shade-plugin
BuildRequires:  maven-shared-invoker
BuildRequires:  maven-shared-reporting-api
BuildRequires:  maven-surefire-plugin
BuildRequires:  maven-toolchain
BuildRequires:  maven-wagon
BuildRequires:  modello
BuildRequires:  plexus-archiver
BuildRequires:  plexus-containers-container-default
BuildRequires:  plexus-interactivity
BuildRequires:  plexus-utils
BuildRequires:  qdox
%if ! %{bootstrap}
BuildRequires:  maven-javadoc-plugin
%endif


BuildArch: noarch

%description
The Maven Javadoc Plugin is a plugin that uses the javadoc tool for
generating javadocs for the specified project.

%if ! %{bootstrap}
%package javadoc
Summary:        Javadoc for %{name}

%description javadoc
API documentation for %{name}.
%endif

%prep
%setup -q
# Update source for use with newer doxia
%patch0

# Remove test dependencies because tests are skipped anyways.
%pom_xpath_remove "pom:dependency[pom:scope[text()='test']]"

%pom_add_dep org.codehaus.plexus:plexus-interactivity-api pom.xml "
<exclusions>
    <exclusion>
        <groupId>org.codehaus.plexus</groupId>
        <artifactId>plexus-component-api</artifactId>
    </exclusion>
</exclusions>"

sed -i -e "s|org.apache.maven.doxia.module.xhtml.decoration.render|org.apache.maven.doxia.sink.render|g" src/main/java/org/apache/maven/plugin/javadoc/JavadocReport.java

%build
%if ! %{bootstrap}
%mvn_build -f
%else
# skip javadoc building
%mvn_build -fj
%endif

%install
%mvn_install

%files -f .mfiles
%doc LICENSE NOTICE

%if ! %{bootstrap}
%files javadoc
%doc LICENSE NOTICE
%{_javadocdir}/%{name}
%endif

%changelog
* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2.9-8
- Mass rebuild 2013-12-27

* Thu Aug 15 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.9-7
- Migrate away from mvn-rpmbuild (#997429)

* Wed Apr 10 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.9-6
- Remove test dependencies from POM

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 2.9-4
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Tue Jan  8 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.9-3
- Add missing requires
- Resolves: rhbz#893166

* Mon Nov 26 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.9-2
- Add LICENSE and NOTICE files to packages (#879605)
- Add dependency exclusion to make enforcer happy

* Tue Oct 23 2012 Alexander Kurtakov <akurtako@redhat.com> 2.9-1
- Update to latest upstream version.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jan 24 2012 Alexander Kurtakov <akurtako@redhat.com> 2.8.1-1
- Update to latest upstream version.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 14 2011 Tomas Radej <tradej@redhat.com> - 2.8-4
- Added maven-compat dep to pom.xml

* Mon Dec 12 2011 Alexander Kurtakov <akurtako@redhat.com> 2.8-3
- Add BR on modello.

* Tue Dec 6 2011 Alexander Kurtakov <akurtako@redhat.com> 2.8-2
- FIx build in pure maven 3 environment.

* Wed May 11 2011 Alexander Kurtakov <akurtako@redhat.com> 2.8-1
- Update to latest upstream version.
- Guidelines fixes.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 24 2010 Alexander Kurtakov <akurtako@redhat.com> 2.7-3
- Add missing invoker requires.

* Wed Jul 21 2010 Alexander Kurtakov <akurtako@redhat.com> 2.7-2
- Add missing invoker BR.

* Wed Jul 21 2010 Alexander Kurtakov <akurtako@redhat.com> 2.7-1
- Update to 2.7.

* Fri May  7 2010 Mary Ellen Foster <mefoster at gmail.com> - 2.4-2
- Add jpackage-utils requirements
- Update requirements of javadoc subpackage

* Thu May  6 2010 Mary Ellen Foster <mefoster at gmail.com> - 2.4-1
- Initial version, based on akurtakov's initial spec
