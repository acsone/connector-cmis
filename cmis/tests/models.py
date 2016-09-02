# -*- coding: utf-8 -*-
# Copyright 2016 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

# DON'T IMPORT THIS MODULE IN INIT TO AVOID THE CREATION OF THE MODELS
# DEFINED FOR TESTS INTO YOUR ODOO INSTANCE

from openerp import api, fields, models
from .. import fields as cmis_fields


class CmisTestModel(models.Model):
    _name = 'cmis.test.model'
    _rec_name = 'name'

    @api.multi
    def _cmis_create(self, backend):
        return '_cmis_create_method'

    name = fields.Char(required=True)
    cmis_folder = cmis_fields.CmisFolder(
        backend_name='cmis.test')
    cmis_folder1 = cmis_fields.CmisFolder(
        backend_name='cmis.test',
        cmis_path='/custom/path')
    cmis_folder2 = cmis_fields.CmisFolder(
        backend_name='cmis.test',
        cmis_create_method='_cmis_create')