%{?!python3_pkgversion:%global python3_pkgversion 3}

%global pkgname journal-to-fedora-messaging-messages
%global srcname journal_to_fedora_messaging_messages

Name:           python-%{pkgname}
Version:        1.0.2
Release:        %autorelease
Summary:        A schema package for messages sent by Journal to Fedora Messaging

License:        LGPL-3.0-or-later
URL:            http://github.com/fedora-infra/journal-to-fedora-messaging-messages
Source:         %{pypi_source %{srcname}}

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-pytest
BuildRequires:  python3-pytest-cov
BuildRequires:  systemd-rpm-macros
# For the RPM macro pyproject_buildrequires.py
BuildRequires:  python3-poetry-core

%global _description %{expand:
A schema package for messages sent by Journal to Fedora Messaging.}

%description %_description

%package -n python3-%{pkgname}
Summary:        %{summary}

%description -n python3-%{pkgname} %_description


%prep
%autosetup -p1 -n %{srcname}-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files %{srcname}


%check
%pytest tests


%postun
%systemd_postun_with_restart journal-to-fedora-messaging.service


%files -n python3-%{pkgname} -f %{pyproject_files}
%{!?_licensedir:%global license %%doc}
%license LICENSES/*
%doc README.*


%changelog
%autochangelog
