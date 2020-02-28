class DynamicFormException(Exception):
    """Base exception for dynamic forms"""
    pass


class FormManagerException(DynamicFormException):
    pass


class DataStoreException(DynamicFormException):
    pass


class FormParserException(DynamicFormException):
    pass
