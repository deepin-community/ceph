"""
This file is automatically generated.
Do not modify.
"""

try:
    from typing import Any, Optional, Union, List
except ImportError:
    pass

from .._helper import _omit, CrdObject, CrdObjectList, CrdClass

class Spec(CrdObject):
    _properties = [
        ('realm', 'realm', str, True, False)
    ]        

    def __init__(self,
                 realm,  # type: str
                 ):
        super(Spec, self).__init__(
            realm=realm,
        )

    @property
    def realm(self):
        # type: () -> str
        return self._property_impl('realm')
    
    @realm.setter
    def realm(self, new_val):
        # type: (str) -> None
        self._realm = new_val


class Status(CrdObject):
    _properties = [
        ('phase', 'phase', str, False, False)
    ]        

    def __init__(self,
                 phase=_omit,  # type: Optional[str]
                 ):
        super(Status, self).__init__(
            phase=phase,
        )

    @property
    def phase(self):
        # type: () -> str
        return self._property_impl('phase')
    
    @phase.setter
    def phase(self, new_val):
        # type: (Optional[str]) -> None
        self._phase = new_val


class CephObjectZoneGroup(CrdClass):
    _properties = [
        ('apiVersion', 'apiVersion', str, False, False),
        ('kind', 'kind', str, False, False),
        ('metadata', 'metadata', object, False, False),
        ('spec', 'spec', 'Spec', True, False),
        ('status', 'status', 'Status', False, False)
    ]        

    def __init__(self,
                 spec,  # type: Spec
                 apiVersion=_omit,  # type: Optional[str]
                 kind=_omit,  # type: Optional[str]
                 metadata=_omit,  # type: Optional[Any]
                 status=_omit,  # type: Optional[Status]
                 ):
        super(CephObjectZoneGroup, self).__init__(
            spec=spec,
            apiVersion=apiVersion,
            kind=kind,
            metadata=metadata,
            status=status,
        )

    @property
    def apiVersion(self):
        # type: () -> str
        return self._property_impl('apiVersion')
    
    @apiVersion.setter
    def apiVersion(self, new_val):
        # type: (Optional[str]) -> None
        self._apiVersion = new_val
    
    @property
    def kind(self):
        # type: () -> str
        return self._property_impl('kind')
    
    @kind.setter
    def kind(self, new_val):
        # type: (Optional[str]) -> None
        self._kind = new_val
    
    @property
    def metadata(self):
        # type: () -> Any
        return self._property_impl('metadata')
    
    @metadata.setter
    def metadata(self, new_val):
        # type: (Optional[Any]) -> None
        self._metadata = new_val
    
    @property
    def spec(self):
        # type: () -> Spec
        return self._property_impl('spec')
    
    @spec.setter
    def spec(self, new_val):
        # type: (Spec) -> None
        self._spec = new_val
    
    @property
    def status(self):
        # type: () -> Status
        return self._property_impl('status')
    
    @status.setter
    def status(self, new_val):
        # type: (Optional[Status]) -> None
        self._status = new_val