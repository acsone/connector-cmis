# -*- encoding: utf-8 -*-
##############################################################################
#
# OpenERP, Open Source Management Solution
# This module copyright (C) 2015 Savoir-faire Linux
# (<http://www.savoirfairelinux.com>).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.tests.common import TransactionCase


class test_metadata(TransactionCase):

    def setUp(self):
        super(test_metadata, self).setUp()
        # Clean up registries
        self.registry('ir.model').clear_caches()
        self.registry('ir.model.data').clear_caches()
        # Get registries
        self.user_model = self.registry("res.users")
        self.ir_model_model = self.registry('ir.model')
        self.fields_model = self.registry('ir.model.fields')
        self.metadata_model = self.registry('metadata')
        # Get context
        self.context = self.user_model.context_get(self.cr, self.uid)
        self.ir_model_id = self.ir_model_model.search(
            self.cr, self.uid, [('model', '=', 'res.partner')],
            context=self.context)[0]

        self.field_id = self.fields_model.create(
            self.cr, self.uid,
            {'name': 'test',
             'field_description': 'test',
             'model_id': self.ir_model_id,
             'ttype': 'char',
             }, context=None)

        self.vals = {
            'name': 'Test',
            'model_id': self.ir_model_id,
            'field_ids': [(4, self.field_id)],
            'metadata_list_ids': [(0, 0, {
                'field_id': self.field_id,
            })],
            'model_ids': [(4, self.ir_model_id)],
        }

    def test_create_metadata(self):
        cr, uid, vals, context = self.cr, self.uid, self.vals, self.context
        metadata_id = self.metadata_model.create(
            cr, uid, vals, context=context)
        metadata_pool = self.metadata_model.browse(
            cr, uid, metadata_id, context=context)
        self.assertEqual(metadata_pool.name, vals['name'])
        self.assertEqual(metadata_pool.model_id.id, vals['model_id'])

    def test_onchange_model(self):
        cr, uid, vals, context = self.cr, self.uid, self.vals, self.context
        res = self.metadata_model.onchange_model(
            cr, uid, [], vals['model_id'], context=context)
        vals['model_ids'] = res['value']['model_ids']
        metadata_id = self.metadata_model.create(
            cr, uid, vals, context=context)
        metadata_pool = self.metadata_model.browse(
            cr, uid, metadata_id, context=context)
        self.assertEqual(metadata_pool.name, vals['name'])
