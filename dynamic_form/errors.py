class DynamicFormException(Exception):
    """Base exception for dynamic forms"""
    pass


class FormManagerException(DynamicFormException):
    pass


class DataStoreException(DynamicFormException):
    pass


class ParserAdapterException(DynamicFormException):
    pass
