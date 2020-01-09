class BaseTemplate(object):

    def to_dict(self) -> dict:
        raise NotImplementedError


class PropertyTemplate(BaseTemplate):

    def __init__(self, label, name, level, description):
        self.label = label
        self.name = name
        self.level = level
        self.description = description

    def to_dict(self) -> dict:
        return {
            "label": self.label,
            "name": self.name,
            "level": self.level,
            "description": self.description,
        }


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
            "objects": self.objs.to_dict(),
        }


class FieldTemplate(BaseTemplate):

    def __init__(self, class_name, property: PropertyTemplate, args=None, **kwargs):
        self.class_name = class_name
        self.property = property
        self.args = args or []
        self.kwargs = kwargs

    def to_dict(self) -> dict:
        return {
            "class_name": self.class_name,
            "property": self.property.to_dict(),
            "args": self.args,
            "kwargs": self.kwargs
        }


class FormFieldTemplate(FieldTemplate):

    def __init__(self, property: PropertyTemplate, class_name="FormField", ):
        super(FormFieldTemplate, self).__init__(class_name=class_name, property=property)
        self.fields = []

    def add_field(self, field: FieldTemplate):
        self.fields.append(field)
        return self

    def to_dict(self) -> dict:
        return {
            "class_name": self.class_name,
            "name": self.property.name,
            "property": self.property.to_dict(),
            "fields": [field.to_dict() for field in self.fields]
        }


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


if __name__ == '__main__':
    form_template = FormTemplate("Form", "form", "A simple form")
    form_template = form_template.add_field("StringField", PropertyTemplate("First Name",
                                                                            "first name",
                                                                            "First name of a user"))

    print(form_template)