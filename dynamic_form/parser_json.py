from flask_wtf import FlaskForm

from wtforms.fields import *
from wtforms.fields.html5 import *
from wtforms.validators import *
from wtforms.widgets import *

from .interfaces import IFormParser


class JsonFlaskParser(IFormParser):
    """Class to build a FlaskForm from a json object

    # >>> from dynamic_form.template_builder import FormTemplate, FieldTemplate
    # ... form_template = FormTemplate("")
    # ...JsonFlaskParser.to_form()

    """
    def __init__(self, form_type=FlaskForm):
        self.form_type = form_type

    def to_form(self, template_form):

        # Nested forms have their name stored in the property
        form_name = template_form.get("name") or template_form["property"]["name"]

        # Define empty form class with the specified name
        form_cls = type(form_name, (self.form_type,), {})

        # Add fields to form
        for field_template in template_form.get("fields"):
            field_name, field = self._parse_field(field_template)
            setattr(form_cls, field_name, field)

        return form_name, form_cls

    def to_template(self, form, **kwargs):
        raise NotImplementedError

        # template_form = {}
        #
        #
        # template_fields = []
        # field_names = form._fields.keys()
        # for index, field_name in field_names.enumerate():
        #     template_fields.append(cls._parse_form_field(getattr(form, field_name), kwargs['property_ids'][index]))
        #
        # TODO: Include label and description
        # template_form['name'] = form.__class__.__name__
        # template_form['fields'] = template_fields
        #
        # return template_form

    # @classmethod
    # def _parse_form_field(cls, field, property_id):
    #     field = {}
    #
    #     field['property'] = property_id
    #
    #     return field

    @staticmethod
    def _get_cls(cls_name):
        switcher = {
            "StringField": StringField,
            "PasswordField": PasswordField,
            "BooleanField": BooleanField,
            "TextAreaField": TextAreaField,
            "SelectField": SelectField,
            "SelectMultipleField": SelectMultipleField,
            "IntegerField": IntegerField,
            "DateField": DateField,
            "DateTimeField": DateTimeField,
            "FieldList": FieldList,
            "EmailField": EmailField,

            "FormField": FormField,

            "InputRequired": InputRequired,
            "DataRequired": DataRequired,
            "Length": Length,
            "NumberRange": NumberRange,

            "HiddenInput": HiddenInput,
            "PasswordInput": PasswordInput,
            "Input": Input
        }
        try:
            return switcher[cls_name]
        except KeyError:
            raise Exception(f"{cls_name} is not a supported class name")

    @classmethod
    def _parse_field(cls, field_template):

        # Add field attributes from local and global attributes. Local attributes overwrite global attributes
        value = {}
        for lbl in ["label", "description"]:
            if lbl in field_template.get("kwargs", []):
                continue
            if field_template.get(lbl, None):
                value[lbl] = field_template[lbl]
            elif field_template.get("property", {}).get(lbl, None):
                value[lbl] = field_template["property"][lbl]
            else:
                raise AttributeError(f"{lbl} was not found in field_template")

        if field_template["class_name"] == "SelectField":
            value["choices"] = cls.get_choice(field_template)

        if not field_template.get("kwargs"):
            field_template["kwargs"] = {}

        field_template["kwargs"].update(value)

        # The name of field is determined by its property.
        field_name = field_template["property"]["name"]

        field = cls._parse_obj(field_template)

        return field_name, field

    @classmethod
    def _parse_obj(cls, obj):
        """Create instance and add attributes

             "object" : {
                 "class_name" : "ClassName",
                 "args" : {...},
                 "kwargs" : {...}
             }
        """
        # If the form contains a subform
        if obj.get("class_name") == "FormField":
            _, form = JsonFlaskParser().to_form(obj)
            obj_cls = FormField(form_class=form)
            return obj_cls

        args, kwargs = [], {}

        if "args" in obj and obj["args"]:
            args = cls._parse_args(obj["args"])

        if "kwargs" in obj:
            kwargs = cls._parse_kwargs(obj["kwargs"])

        obj_cls = JsonFlaskParser._get_cls(obj["class_name"])
        return obj_cls(*args, **kwargs)

    @classmethod
    def _parse_args(cls, template_args):
        """
        args: { "object" : {...}, }
        or
        args: { "objects" : [{...}, ...], }
        or
        args: { "tuples" : [...] }
        """
        args = []

        if "object" in template_args:
            args.append(cls._parse_obj(template_args["object"]))
        elif "objects" in template_args:
            args.extend(cls._parse_objs(template_args["objects"]))
        elif "tuples" in template_args:
            args.extend(cls._parse_tuple(template_args["tuples"]))
        else:
            raise NotImplementedError

        return args

    @classmethod
    def _parse_kwargs(cls, template_kwargs):
        """
        "kwargs": [ {"key1": "value1"}, {"key2": "value2"} ]
        """
        kwargs = {}
        if not template_kwargs:
            return kwargs
        if not isinstance(template_kwargs, dict):
            raise TypeError(f"{template_kwargs.__name__} has to be a dict")

        for key, value in template_kwargs.items():
            if isinstance(value, (str, int, float, bool)):
                kwargs[key] = value
            elif value == "kwargs":
                # TODO: Check this line
                kwargs[key] = cls._parse_kwargs(value["kwargs"])
            elif isinstance(value, dict):
                # TODO: Check this line
                kwargs[key] = cls._parse_dict(value)
            elif key == "choices":
                continue
            else:
                raise NotImplementedError

        return kwargs

    @classmethod
    def _parse_dict(cls, template_dict):
        if "args" in template_dict:
            value = cls._parse_args(template_dict["args"])
        elif "kwargs" in template_dict:
            value = cls._parse_kwargs(template_dict["kwargs"])
        else:
            raise NotImplementedError

        return value

    @classmethod
    def _parse_objs(cls, template_objects):
        objects = []
        for template_obj in template_objects:
            if not template_obj.get("kwargs"):
                template_obj["kwargs"] = {}
            if template_obj["class_name"] == "SelectField":
                template_obj["kwargs"]["choices"] = cls.get_choice(template_obj)
            objects.append(cls._parse_obj(template_obj))

        return objects

    @classmethod
    def _parse_tuple(cls, tuples):
        """Parse a tuple with multiple values
        "tuples" : [ ["value1", "value2"], ["value1", "value2"] ]
        """
        tuple_list = []
        for values in tuples:
            value_list = []
            for value in values:
                value_list.append(value)
            tuple_list.append(tuple(value_list))

        return tuple_list

    @classmethod
    def get_choice(cls, field_template):
        lbl = "choices"

        # Needs to be removed from template because it's not allowed in WTForm
        allow_synonyms = field_template["kwargs"].pop("allow_synonyms", False)

        if lbl in field_template["kwargs"]:
            return field_template["kwargs"]["choices"]
        elif field_template.get("property", {}).get("value_type", {}).get("data_type") == "ctrl_voc":
            cv_items = field_template["property"]["value_type"].get("controlled_vocabulary", {})["items"]
            choices = []
            for cv_item in cv_items:
                choices.append((cv_item["name"], cv_item["label"]))
                if allow_synonyms:
                    for synonym in cv_item["synonyms"]:
                        choices.append((synonym, synonym))

            return {"args": {"tuples": choices}}
