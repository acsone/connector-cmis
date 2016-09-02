# -*- coding: utf-8 -*-
# © 2014-2015 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# Copyright 2016 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import cmislib.exceptions
from cmislib.model import CmisClient
from cmislib.browser.binding import BrowserBinding
from cmislib.exceptions import ObjectNotFoundException

from openerp import api, fields, models, tools
from openerp.exceptions import Warning
from openerp.tools.translate import _
from ..exceptions import CMISError


class CmisBackend(models.Model):
    _name = 'cmis.backend'
    _description = 'CMIS Backend'
    _order = 'name desc'

    name = fields.Char(required=True)
    location = fields.Char(
        required=True)
    username = fields.Char(
        required=True)
    password = fields.Char(
        required=True)
    initial_directory_write = fields.Char(
        'Initial directory for writing', required=True, default='/')

    def _clear_caches(self):
        pass
        #self.get_cmis_client.clear()
        #self.get_by_name.clear()

    @api.multi
    def write(self, vals):
        self._clear_caches()
        return super(CmisBackend, self).write(vals)

    #@tools.cache
    @api.multi
    def get_cmis_client(self):
        """
        Get an initialized CmisClient for the using the CMISBrowserBinding
        """
        self.ensure_one()
        return CmisClient(
            self.location,
            self.username,
            self.password,
            binding=BrowserBinding())

    #@tools.cache
    @api.model
    def get_by_name(self, name):
        backend = self.search([('name', '=', name)])
        backend.ensure_one()
        return backend

    @api.multi
    def get_cmis_repository(self):
        """ Check the authentication with DMS """
        self.ensure_one()
        client = self.get_cmis_client()
        return client.defaultRepository

    @api.multi
    def check_directory_of_write(self):
        """Check access right to write from the path"""
        datas_fname = 'testdoc'
        for this in self:
            # login with the cmis account
            repo = this.get_cmis_repository()
            folder_path_write = this.initial_directory_write
            path_write_objectid = self.get_folder_by_path(
                folder_path_write,
                create_if_not_found=False,
                cmis_parent_objectid=None)
            # Check if we can create a doc from OE to EDM
            # Document properties
            if path_write_objectid:
                try:
                    path_write_objectid.createDocumentFromString(
                        datas_fname,
                        contentString='hello, world',
                        contentType='text/plain')
                except cmislib.exceptions.UpdateConflictException:
                    raise CMISError(
                        _("The test file already exists in the DMS. "
                          "Please remove it and try again."))
                except cmislib.exceptions.RuntimeException:
                    raise CMISError(
                        ("Please check your access right."))
            self.get_error_for_path(path_write_objectid != False,
                                    folder_path_write)

    @api.multi
    def get_folder_by_path(self, path, create_if_not_found=True,
                           cmis_parent_objectid=None):
        self.ensure_one()
        repo = self.get_cmis_repository()
        if cmis_parent_objectid:
            path = repo.getObject(
                cmis_parent_objectid).getPaths()[0] + '/' + path
        traversed = []
        try:
            return repo.getObjectByPath(path)
        except ObjectNotFoundException:
            if not create_if_not_found:
                return False
        # The path doesn't exist and must be created
        for part in path.split('/'):
            try:
                part = '%s' % part
                traversed.append(part)
                new_root = repo.getObjectByPath('/'.join(traversed))
            except ObjectNotFoundException:
                new_root = repo.createFolder(new_root, part)
            root = new_root
        return root

    def get_error_for_path(self, is_valid, path):
        """Return following the boolean the right error message"""
        if is_valid:
            raise Warning(_("Path is correct for : %s") % path)
        else:
            raise CMISError(_("Error path for : %s") % path)

    def sanitize_input(self, file_name):
        """Prevent injection by escaping: '%_"""
        file_name = file_name.replace("'", r"\'")
        file_name = file_name.replace("%", r"\%")
        file_name = file_name.replace("_", r"\_")
        return file_name

    def safe_query(self, query, file_name, repo):
        args = map(self.sanitize_input, file_name)
        return repo.query(query % ''.join(args))
