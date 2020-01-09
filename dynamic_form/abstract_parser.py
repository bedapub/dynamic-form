from abc import ABC, abstractmethod


class ParseException(Exception):
    pass


class AbstractParserAdapter(ABC):
    """Interface class for all parser adapters."""

    @classmethod
    @abstractmethod
    def to_form(cls, template_form):
        """"The template is converted into a form"""
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def to_template(cls, form, **kwargs):
        """Create a template from a given form"""
        raise NotImplementedError
