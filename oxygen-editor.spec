# TODO
# - get evaluation key from http://www.oxygenxml.com/register.html
Summary:	<oXygen/> XML Editor
Name:		oxygen-editor
Version:	12.1
Release:	0.1
License:	?
Group:		Development/Tools
Source0:	http://www.oxygenxml.com/InstData/Editor/Linux/VM/oxygen32.sh
# NoSource0-md5:	5b1be07b602c0e94e6d49d6600b89f22
NoSource:	0
Source1:	http://www.oxygenxml.com/InstData/Editor/Linux64/VM/oxygen64.sh
# NoSource1-md5:	012ee56a167af4a8979f3e8fb7078360
NoSource:	1
URL:		http://www.oxygenxml.com/download_oxygenxml_editor.html
BuildRequires:	unzip
Requires:	jdk >= 1.6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_appdir		%{_libdir}/%{name}

%description
<oXygen/> XML Editor is a complete XML development platform providing
the necessary tools for working with a wide range of XML standards and
technologies:
- XML editing
- XML conversion
- XML Schema development
- XSLT/ XQuery/ XPath execution and debugging
- SOAP and WSDL testing
- Native XML and relational database support

%prep
%setup -qc
%ifarch %{ix86}
SOURCE=%{SOURCE0}
%endif
%ifarch %{x8664}
SOURCE=%{SOURCE1}
%endif
offset=$(grep -a 'tail -c' $SOURCE | awk '{print $3}')
tail -c $offset $SOURCE > sfx_archive.tar.gz
tar zxf sfx_archive.tar.gz
ln -s $SOURCE src.sh

%install
rm -rf $RPM_BUILD_ROOT
# make the license not span screen
head -n6 i4j_extf_15_1im7gi7.txt > lic.txt
sed -i -e 's,i4j_extf_15_1im7gi7.txt,lic.txt,' i4jparams.conf

# nuke previous install info, confuses our answers sequence
export HOME=$(pwd)
rm -f $HOME/.java/.userPrefs/com/install4j/installations/prefs.xml

# command sequence to installer
cat > cmd.txt <<EOF
2
o
1
$RPM_BUILD_ROOT%{_appdir}
1,2,3
y
$RPM_BUILD_ROOT%{_bindir}
y
y
EOF

%java \
	-Dinstall4j.jvmDir="%java_home" \
	-Dexe4j.moduleName="$(pwd)/src.sh" \
	-Dexe4j.totalDataLength=97160734 \
	-Dinstall4j.cwd="$(pwd)" \
	-Xmx128m \
	-Dsun.java2d.noddraw=true \
	-Di4j.vmov=true \
	-Di4j.vpt=true \
	-classpath i4jruntime.jar:user.jar:user/i4jCustom.jar \
	com.install4j.runtime.launcher.Launcher launch \
	com.install4j.runtime.installer.Installer false false "" "" false true false "" true true 0 0 "" 20 20 "Arial" "0,0,0" 8 500 "version 12.1" 20 40 "Arial" "0,0,0" 8 500 -1 -c < cmd.txt

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{name}
%dir %{_appdir}
