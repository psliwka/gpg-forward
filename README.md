gpg-forward - Forward GPG agent over SSH
========================================
[![Build status](https://travis-ci.org/psliwka/gpg-forward.svg?branch=master)](https://travis-ci.org/psliwka/gpg-forward)
[![PyPI page](https://img.shields.io/pypi/v/gpg-forward.svg)](https://pypi.python.org/pypi/gpg-forward/)

This utility implements GPG agent socket forwarding over SSH, in a way similar
to the one described in [GnuPG wiki](https://wiki.gnupg.org/AgentForwarding).

Requirements
------------

- [GnuPG](https://www.gnupg.org/) >= 2.1.1
- [OpenSSH](https://www.openssh.com/) >= 6.7


Installation
------------

```sh
$ pip install gpg-forward
```

Usage
-----

```sh
$ gpg-forward user@target.host.example.com
```

Credits
-------

Created by [Piotr Śliwka](https://github.com/psliwka)

License
-------

MIT
