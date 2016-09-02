# -*- coding: utf-8 -*-
# Copyright 2016 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import mock
from openerp.exceptions import UserError
from . import common


class TestCmisFields(common.BaseTestCmis):

    def test_cmis_folder_default_init(self):
        inst = self.env['cmis.test.model'].create({'name': 'folder_name'})
        with mock.patch("openerp.addons.cmis.models.cmis_backend."
                        "CmisBackend.get_cmis_repository"
                        ) as mocked_get_repository:
            mocked_cmis_repository = mock.MagicMock()
            mocked_get_repository.return_value =  mocked_cmis_repository
            new_mocked_cmis_folder = mock.MagicMock()
            mocked_cmis_repository.createFolder.return_value = \
                new_mocked_cmis_folder
            mocked_cmis_repository.getObjectByPath.return_value = 'root_id'
            new_mocked_cmis_folder.getObjectId.return_value = 'cmis_id'

            # check the value initialization using the method defined on the
            # field. As result the value must be set on the given record
            inst._fields['cmis_folder'].init_value(inst)
            self.assertEquals(inst.cmis_folder, 'cmis_id')

            # in the initialization process the field will compute a path
            # where to store the new folder. This path is used to request the
            # cmis_repository to retrieve the objectId associated to this path
            # by default the path is computed by concatenating the
            # cmis_backend.initial_directory_write + / + model._name
            mocked_cmis_repository.getObjectByPath.assert_called_once_with(
                '/odoo/cmis_test_model')

            # the name of the folder created into the repository is by default
            # the one returned by the name_get method on the record and the
            # parent directory, the one returned by the method getObjectByPath
            mocked_cmis_repository.createFolder.assert_called_once_with(
                'root_id', 'folder_name')

            mocked_cmis_repository.reset_mock()
            # it's also possible to specify a custom cmis_path in the field
            # definition
            inst._fields['cmis_folder1'].init_value(inst)
            mocked_cmis_repository.getObjectByPath.assert_called_once_with(
                '/custom/path')
            # a second call to the init_value must raise a UserError since
            # the value is already initialized
            with self.assertRaises(UserError):
                inst._fields['cmis_folder1'].init_value(inst)

    def test_cmis_folder_cmis_create_method(self):
        # if a cmis_create_method is declared in the field definition, it's
        # called with the backend as argument to initialize the field value
        # and the value returned by the method is used as field's value
        inst = self.env['cmis.test.model'].create({'name': 'folder_name'})
        inst._fields['cmis_folder2'].init_value(inst)
        self.assertEquals(inst.cmis_folder2, '_cmis_create_method')

    def test_cmis_folder_get_desciption(self):
        inst = self.env['cmis.test.model'].create({'name': 'folder_name'})
        # get_description is the method call by the method fields_get
        # to return to the UI the desciption of the UI
        descr = inst._fields['cmis_folder'].get_description(self.env)
        self.assertEquals(descr.get('backend_name'), self.cmis_backend.name)
        self.assertEquals(descr.get('type'), 'cmis_folder')
