import abc
"""A collection of builders to create a form template from python classes"""


class BaseTemplate(abc.ABC):

    @abc.abstractmethod
    def to_dict(self) -> dict:
        raise NotImplementedError


class LNDTemplate(BaseTemplate):
    """Label, Name, Description template"""

    def __init__(self, label, name, description, deprecated=False):
        self.label = label
        self.name = name
        self.description = description
        self.deprecated = deprecated

    def to_dict(self) -> dict:
        return {
            "label": self.label,
            "name": self.name,
            "description": self.description,
            "deprecated": self.deprecated,
        }


class ItemTemplate(BaseTemplate):

    def __init__(self, label, name, description):
        self.label = label
        self.name = name
        self.description = description
        self.synonyms = []

    def add_synonym(self, synonym):
        self.synonyms.append(synonym)
        return self

    def to_dict(self) -> dict:
        result = ({
            "label": self.label,
            "name": self.name,
            "description": self.description,
            "synonyms": [item.to_dict() for item in self.synonyms]
        })
        return result


class ControlledVocabularyTemplate(BaseTemplate):

    def __init__(self, label, name, description):
        self.label = label
        self.name = name
        self.description = description
        self.items = []

    def add_item(self, item: ItemTemplate):
        self.items.append(item)
        return self

    def to_dict(self) -> dict:
        result = {
            "label": self.label,
            "name": self.name,
            "description": self.description,
            "items": [item.to_dict() for item in self.items]
        }
        return result


class ValueTypeTemplate(BaseTemplate):

    def __init__(self, data_type="text", controlled_vocabulary: ControlledVocabularyTemplate = None):

        if data_type not in ["ctrl_voc", "text", "boolean"]:
            raise AttributeError

        self.data_type = data_type
        self.controlled_vocabulary = controlled_vocabulary

    def to_dict(self) -> dict:
        return {
            "data_type": self.data_type,
            "controlled_vocabulary": self.controlled_vocabulary if type(self.controlled_vocabulary) == str else
            self.controlled_vocabulary.to_dict() if
            self.controlled_vocabulary else None
        }


class PropertyTemplate(LNDTemplate):

    def __init__(self, label, name, level, description, value_type: ValueTypeTemplate = ValueTypeTemplate(),
                 synonyms=None, **kwargs):
        super(PropertyTemplate, self).__init__(label, name, description, **kwargs)

        self.level = level
        self.value_type = value_type
        self.synonyms = synonyms

    def to_dict(self) -> dict:
        result = super(PropertyTemplate, self).to_dict()
        result.update({
            "level": self.level,
            "value_type": self.value_type if type(self.value_type) == str else self.value_type.to_dict(),
            "synonyms": [] if not self.synonyms else self.synonyms,
        })

        return result


class ObjectTemplate(BaseTemplate):

    def __init__(self, class_name, property: PropertyTemplate):
        self.class_name = class_name
        self.property = property

    def to_dict(self) -> dict:
        return {
            "class_name": self.class_name,
            "property": self.property.to_dict(),
        }


class ObjectsTemplate(BaseTemplate):

    def __init__(self, objs):
        self.objs = objs

    def to_dict(self) -> dict:
        return {
            "objects": [obj.to_dict() for obj in self.objs],
        }


class ArgsTemplate(BaseTemplate):

    def __init__(self, _cls, objs=None):
        self._cls = _cls
        self.objs = objs

    def to_dict(self) -> dict:
        return {
            "_cls": self._cls,
            "objects": [obj.to_dict() for obj in self.objs]
        }


class FieldTemplate(BaseTemplate):

    def __init__(self, class_name, property, args: ArgsTemplate = None, **kwargs):
        self.class_name = class_name
        self.property = property
        self.args = args or {}
        self.kwargs = kwargs

    def to_dict(self) -> dict:
        result = {
            "class_name": self.class_name,
            "property": self.property if type(self.property) == str else self.property.to_dict(),
            "args": self.args if type(self.args) == str else self.args.to_dict() if self.args else None,
            "kwargs": self.kwargs
        }
        return result


class FormFieldTemplate(FieldTemplate):

    def __init__(self, prop, class_name="FormField", args=None, **kwargs):
        super(FormFieldTemplate, self).__init__(class_name=class_name, property=prop, args=args, **kwargs)
        self.fields = []

    def add_field(self, field: FieldTemplate):
        self.fields.append(field)
        return self

    def to_dict(self) -> dict:
        results = super().to_dict()
        results.update({
            "fields": [field.to_dict() for field in self.fields]
        })
        return results


class FormTemplate(BaseTemplate):

    def __init__(self, label, name, description):
        self.label = label
        self.name = name
        self.description = description
        self.fields = []

    def to_dict(self) -> dict:
        return {
            "label": self.label,
            "name": self.name,
            "description": self.description,
            "fields": [field.to_dict() for field in self.fields],
        }

    def add_field(self, field: FieldTemplate):
        self.fields.append(field)

        return self


class UserTemplate(BaseTemplate):
    def __init__(self, firstname, lastname, email, password):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password

    def to_dict(self) -> dict:
        return {
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
            "password": self.password
        }

