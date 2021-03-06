.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

======================================
Attach files from a remote CMIS Server
======================================

This module allows you to use the CMIS backend to search in the DMS repository
and attach documents to OpenERP records.

Installation
============

You need to install the CMIS python library:

 pip install cmislib

Configuration
=============

Create a new CMIS backend with the host, login and password.

Usage
=====

To use this module:

* On one OpenERP record, click "Add from DMS".
* Type your query and then click on "Search".
* Filter your results if necessary
* Select the documents you want to attach
* Selected documents will be enqueued for importing

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/104/7.0

Known issues / Roadmap
======================

* https://github.com/OCA/connector-cmis/issues 

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/connector-cmis/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smashing it by providing a detailed and welcomed `feedback
<https://github.com/OCA/connector-cmis/issues/new?body=module:%20
cmis_read%0Aversion:%20
7.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Credits
=======

Images
------

* Odoo Community Association: `Icon <https://github.com/OCA/maintainer-tools/blob/master/template/module/static/description/icon.svg>`_.

Contributors
------------

* El Hadji Dem (elhadji.dem@savoirfairelinux.com)
* Maxime Chambreuil (maxime.chambreuil@savoirfairelinux.com)

Maintainer
----------

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit http://odoo-community.org.
