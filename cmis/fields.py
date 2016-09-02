# -*- coding: utf-8 -*-
# Copyright 2016 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from operator import attrgetter
from openerp import fields
from openerp.exceptions import UserError


class CmisFolder(fields.Field):
    """ A reference to a cmis:folder. The reference must be formatted as
    follow: backend_name + ':' cmis:objectId
    
    :param backend_name:
    
    The attribute ``backend_name`` is mandatory
    
    :param allow_create: (by default True)
    
    :param allow_delete: (by default False)
    
    :param cmis_create_method:
    
    :param cmis_path: (by default backend.initial_directory_write + '/' model._name)
    
    :param cmis_name_get: (by default instance.name_get)

    """
    type = 'char'  # Postgresl
    widget = 'cmis_folder'  # Web widget
    _slots = {
        'backend_name': None,
        'cmis_name_get': 'name_get',
        'allow_create': True,
        'allow_delete': False,
        'cmis_path': None,
        'cmis_create_method': None
    }

    def __init__(self, backend_name=None, string=None, **kwargs):
        super(CmisFolder, self).__init__(
            backend_name=backend_name, string=string, **kwargs)


    def get_description(self, env):
        """ Return a dictionary that describes the field ``self``. """
        desc = super(CmisFolder, self).get_description(env)
        desc['type'] = self.widget
        return desc
    
    _description_backend_name = property(attrgetter('backend_name'))

    def init_value(self, record):
        if record is None:
            return self         # the field is accessed through the owner class

        env = record.env
        if not record:
            # null record -> return the null value for this field
            return self.null(env)
        
        self._check_null(record)
        
        value = None
        backend = env['cmis.backend'].get_by_name(name=self.backend_name)
        if self.cmis_create_method:
            fct = self.cmis_create_method
            if not callable(fct):
                fct = getattr(record, fct)
            value = fct(backend)
        else:
            value = self._create_in_cmis(record, backend)
        self.__set__(record, value)
        return value

    def _create_in_cmis(self, record, backend):
        name = self._get_cmis_name(record)
        path = self._get_cmis_path(record, backend)
        #create
        parent_cmis_object = backend.get_folder_by_path(
            path, create_if_not_found=True)
        repo = backend.get_cmis_repository()
        new_folder = repo.createFolder(
            parent_cmis_object, name)
        return new_folder.getObjectId()

    def _check_null(self, record, raise_exception=True):
        val = self.__get__(record, record)
        if val and raise_exception:
            raise UserError('A value is already assigned to %s' % self)
        return val 

    def _get_cmis_name(self, record):
        if self.cmis_name_get == 'name_get':
            return record.name_get()[0][1]
        fct = self.cmis_name_get
        if not callable(fct):
            fct = getattr(record, fct)
        return fct()

    def _get_cmis_path(self, record, backend):
        if self.cmis_path:
            return self.cmis_path
        else:
            return '/'.join([backend.initial_directory_write,
                             record._name.replace('.', '_')])