# Release notes

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

This project uses [*towncrier*](https://towncrier.readthedocs.io/) and the changes for the upcoming release can be found in [the `changelog.d` directory](http://github.com/fedora-infra/journal-to-fedora-messaging/tree/develop/changelog.d/).


## Version 1.0.1

- Set the `IpaGroupMessage`s' severity to `DEBUG`, because Noggin also emits a message for this action and we don't want to notify users twice.

## Version 1.0.0

- Initial release
