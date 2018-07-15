gpg-forward - Forward GPG agent over SSH
========================================

This utility implements GPG agent socket forwarding over SSH, in a way similar
to the one described in `GnuPG wiki <https://wiki.gnupg.org/AgentForwarding>`_.

Requiremets
-----------

- `GnuPG <https://www.gnupg.org/>`_ >= 2.1.1
- `OpenSSH <https://www.openssh.com/>`_ >= 6.7

Installation
------------

TBD

Usage
-----

.. code:: sh

   $ gpg-forward user@target.host.example.com

Credits
-------

Created by `Piotr Śliwka <https://github.com/psliwka>`_

License
-------

MIT
