# -*- coding: utf-8 -*-
# © 2016 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class CmisBackend(models.Model):
    _inherit = 'cmis.backend'
    _backend_type = 'cmis'

    share_location = fields.Char(
        string='Alfresco Share Url',
        required=True)

    alfresco_api_location = fields.Char(
        string='Alfresco Api Url',
        required=True) 

    @api.multi
    def get_content_details_url(self,cmis_objectid):
        """Return the url to the page into Alfresco Share
        displaying the content details
        """
        self.ensure_one()
        repo = self.check_auth()
        properties = repo.getObject(cmis_objectid).getProperties()
        details_type = 'document-details'
        if properties['cmis:baseTypeId'] == 'cmis:folder':
            details_type = 'folder-details'
        noderef = properties['alfcmis:nodeRef']
        # TODO cmis_alf
        url = "%s/page/%s?nodeRef=%s" % (self.share_location,
                                         details_type,
                                         noderef)
        return url