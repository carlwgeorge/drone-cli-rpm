%bcond_with debug

%if %{with debug}
%global _dwz_low_mem_die_limit 0
%else
%global debug_package %{nil}
%endif

%if ! 0%{?gobuild:1}
%define gobuild(o:) go build -ldflags "${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n')" -a -v -x %{?**};
%endif

# drone-cli
%global import_path github.com/drone/drone-cli

Name: drone-cli
Version: 0.8.5
Release: 1%{?dist}
Summary: Command line client for the Drone continuous integration server
License: ASL 2.0
URL: https://drone.io
Source0: https://%{import_path}/archive/v%{version}/drone-cli-%{version}.tar.gz
ExclusiveArch: %{go_arches}
BuildRequires: %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}


%description
The Drone command line tools are used to interact with the Drone from the
command line, and provides important utilities for managing users and
repository settings.


%prep
%autosetup
mkdir -p src/%(dirname %{import_path})
ln -s ../../.. src/%{import_path}


%build
export GOPATH=$(pwd):%{gopath}
export LDFLAGS="-X main.version=%{version}"
%gobuild -o bin/drone %{import_path}/drone


%install
install -D -m 0755 bin/drone %{buildroot}%{_bindir}/drone


%files
%license LICENSE
%{_bindir}/drone


%changelog
* Wed Mar 21 2018 Carl George <carl@george.computer> - 0.8.5-1
- Latest upstream

* Sat Mar 03 2018 Carl George <carl@george.computer> - 0.8.4-1
- Latest upstream

* Wed Jan 24 2018 Carl George <carl@george.computer> - 0.8.1-1
- Latest upstream

* Fri Nov 24 2017 Carl George <carl@george.computer> - 0.8.0-1
- Initial package
