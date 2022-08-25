.. _installation:

============
Installation
============

*You're spoilt for choice*, choose your preferred method of installation.

- :ref:`installation docker`
- :ref:`installation scripts`
- :ref:`installation basic`

The :ref:`installation basic` is good enough for intranet usage and it is a
excellent illustration of *how a searx instance is build up*.  If you place your
instance public to the internet you should really consider to install a
:ref:`filtron reverse proxy <filtron.sh>` and for privacy a :ref:`result proxy
<morty.sh>` is mandatory.

Therefore, if you do not have any special preferences, its recommend to use the
:ref:`installation docker` or the `Installation scripts`_ from our :ref:`tooling
box <toolboxing>` as described below.

.. _installation scripts:

Installation scripts
====================

.. sidebar:: Update OS first!

   To avoid unwanted side effects, update your OS before installing searx.

The following will install a setup as shown in :ref:`architecture`.  First you
need to get a clone.  The clone is only needed for the installation procedure
and some maintenance tasks (alternatively you can create your own fork).

For the installation procedure, use a *sudoer* login to run the scripts.  If you
install from ``root``, take into account that the scripts are creating a
``searx``, a ``filtron`` and a ``morty`` user.  In the installation procedure
these new created users do need read access to the clone of searx, which is not
the case if you clone into a folder below ``/root``.

.. code:: bash

   $ cd ~/Downloads
   $ git clone https://github.com/searx/searx searx
   $ cd searx

.. sidebar:: further read

   - :ref:`toolboxing`
   - :ref:`update searx`
   - :ref:`inspect searx`

**Install** :ref:`searx service <searx.sh>`

This installs searx as described in :ref:`installation basic`.

.. code:: bash

   $ sudo -H ./utils/searx.sh install all

**Install** :ref:`filtron reverse proxy <filtron.sh>`

.. code:: bash

   $ sudo -H ./utils/filtron.sh install all

**Install** :ref:`result proxy <morty.sh>`

.. code:: bash

   $ sudo -H ./utils/morty.sh install all

If all services are running fine, you can add it to your HTTP server:

- :ref:`installation apache`
- :ref:`installation nginx`

.. _git stash: https://git-scm.com/docs/git-stash

.. tip::

   About script's installation options have a look at chapter :ref:`toolboxing
   setup`.  How to brand your instance see chapter :ref:`settings global`.  To
   *stash* your instance's setup, `git stash`_ your clone's :origin:`Makefile`
   and :origin:`.config.sh` file .
