# -*- coding: utf-8 -*-
# Copyright 2016 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
import json
import werkzeug
from openerp import http
from openerp.addons.web.controllers import main


class CmisController(http.Controller):

    @http.route('/web/cmis/field/init_value', type='json', methods=['POST'],
                auth="user")
    @main.serialize_exception
    def init_field_value(self, model_name, res_id, field_name):
        model_inst = http.request.env[model_name].browse(int(res_id))
        value = model_inst._fields[field_name].init_value(model_inst)
        response = werkzeug.Response(json.dumps(
            {'value': value}), mimetype='application/json')
        return response
