''' Representation of an element
@param element_type: type of the element
@param length: length of the element
'''
from rml.exceptions import PvException


class Element(object):

    def __init__(self, elem_identity, **kwargs):
        '''
        Possible arguments for kwargs:

        :str elem_identity: identifier used to match an element to a pv
        :set elem_family: a set used to store families
        :param cs: type of control system to be used
        '''
        self.identity = elem_identity
        self.families = set()
        self.length = kwargs.get('length', 0)
        self._cs = kwargs.get('cs', None)
        # Keys represent fields and values pv names.
        self._readback = dict()
        self._setpoint = dict()

    def add_to_family(self, family):
        self.families.add(family)

    def get_pv_value(self, handle, field):
        """
        Get pv value for the given field.
        Currently, only supports readback handle
        """

        if handle == 'readback':
            if field in self._readback:
                return self._cs.get(self._readback[field])
        elif handle == 'setpoint':
            if field in self._setpoint:
                return self._cs.get(self._setpoint[field])

        raise PvException("""Something went wrong...
        Handle or field was not recognized {0}{1}.""".format(handle, field))

    def put_pv_value(self, field, value):
        ''' Set the pv value. No need for handle because only the setpoint value
        can be set'''
        if field in self._setpoint:
            self._cs.put(self._setpoint[field], value)
        else:
            raise PvException("""Unknown field {0}.""".format(field))

    def put_pv_name(self, handle, field, pv_name):
        if handle == 'setpoint' or handle == 'put':
            self._setpoint[field] = pv_name
        elif handle == 'readback' or handle == 'get':
            self._readback[field] = pv_name
        else:
            raise PvException("Unknown handle or field {0} {1}"
                              .format(handle, field))

    def get_pv_name(self, handle='readback', field='*'):
        if handle == 'setpoint':
            if field == '*':
                return self._setpoint
            else:
                return self._setpoint[field]
        elif handle == 'readback':
            if field == '*':
                return self._readback
            else:
                return self._readback[field]

        raise PvException("""Something went wrong...
        Handle or field was not recognized {0}{1}.""".format(handle, field))
