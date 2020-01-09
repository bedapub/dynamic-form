import unittest

from flask import Flask
from flask_wtf import FlaskForm
from wtforms.validators import *
from wtforms.widgets import *

from dynamic_form.parser_json import JsonFlaskParser


class TestInputParserHelper(unittest.TestCase):
    """The following test check the helper functions of parser json."""

    def test_tuple_diff_length(self):
        """Test conversion of tuples"""
        t1v1, t1v2 = "tuple1_value1", "tuple1_value2"
        t2v1, t2v2, t2v3 = "tuple1_value1", "tuple1_value2", "tuple1_value3"

        tuples = [[t1v1, t1v2], [t2v1, t2v2, t2v3]]

        act_tuple = JsonFlaskParser._parse_tuple(tuples)
        exp_tuple = [(t1v1, t1v2), (t2v1, t2v2, t2v3)]

        self.assertEqual(act_tuple, exp_tuple)

    def test_obj_validators_widgets(self):
        """Test validator and widget parsing with and without attributes"""

        validators_widgets = {
            InputRequired: {},
            InputRequired: {"message": "Input required"},
            DataRequired: {},
            Length: {"min": 1},
            Length: {"max": 10},
            NumberRange: {"min": 10},
            NumberRange: {"max": 20},
            HiddenInput: {},
            PasswordInput: {}
        }

        for obj_cls, obj_cls_values in validators_widgets.items():
            obj = {
                "class_name": obj_cls.__name__,
                "kwargs": obj_cls_values
            }
            act_obj = JsonFlaskParser._parse_obj(obj)

            self.assertIsInstance(act_obj, obj_cls)

            if "message" in obj_cls_values:
                self.assertEqual(act_obj.message, obj_cls_values["message"])
            if "min" in obj_cls_values:
                self.assertEqual(act_obj.min, obj_cls_values["min"])
            if "max" in obj_cls_values:
                self.assertEqual(act_obj.max, obj_cls_values["max"])

    def test_simple_field_attributes_in_kwargs(self):
        field_type = "StringField"
        variable_name = "user_name"
        label = "User Name"
        description = "A simple string field"

        template_field = {
            "class_name": field_type,
            "property": {"name": variable_name},
            "args": {},
            "kwargs": {"label": label, "description": description}
        }

        act_name, act_field = JsonFlaskParser._parse_field(template_field)

        self.assertEqual(act_field.kwargs["label"], label)

        app = Flask(__name__)
        app.secret_key = "not secret"
        with app.test_request_context():
            form_cls = type("TestForm", (FlaskForm,), {})
            setattr(form_cls, act_name, act_field)

            form = form_cls()

            self.assertTrue(hasattr(form, variable_name))
            field = getattr(form, variable_name)
            self.assertEqual(getattr(field, "type"), field_type)

    def test_simple_field_attributes_in_field(self):
        field_type = "StringField"
        variable_name = "user_name"
        label = "User Name"
        description = "A simple string field"

        template_field = {
            "class_name": field_type,
            "label": label,
            "description": description,
            "property": {"name": variable_name},
            "args": {},
            "kwargs": {}
        }

        act_name, act_field = JsonFlaskParser._parse_field(template_field)

        self.assertEqual(act_name, variable_name)
        self.assertEqual(act_field.kwargs["label"], label)

    def test_simple_field_attributes_in_property(self):
        field_type = "StringField"
        variable_name = "user_name"
        label = "User Name"
        description = "A simple string field"

        template_field = {
            "class_name": field_type,
            "property": {"name": variable_name,
                         "description": description,
                         "label": label},
            "args": {},
            "kwargs": {}
        }

        act_name, act_field = JsonFlaskParser._parse_field(template_field)

        self.assertEqual(act_name, variable_name)
        self.assertEqual(act_field.kwargs["label"], label)

    def test_create_field_validation(self):
        field_type = "StringField"
        variable_name = "user_name"
        label = "User Name"
        description = "A simple string field"

        template_field = {
            "class_name": field_type,
            "property": {"name": variable_name, "description": description},
            "kwargs": {"label": label,
                       "validators": {
                           "args": {
                               "objects": [
                                   {"class_name": "InputRequired"},
                                   {"class_name": "Length", "kwargs": {"min": 0, "max": 10}}
                               ]
                           }
                       }}
        }

        act_name, act_field = JsonFlaskParser._parse_field(template_field)

        self.assertEqual(act_name, variable_name)
        self.assertEqual(act_field.kwargs["label"], label)
        self.assertIsInstance(act_field.kwargs["validators"], list)
        self.assertIsInstance(act_field.kwargs["validators"][0], InputRequired)
        self.assertIsInstance(act_field.kwargs["validators"][1], Length)
        self.assertEqual(act_field.kwargs["validators"][1].max, 10)

    def test_create_selectfield_choice(self):
        field_type = "SelectField"
        variable_name = "user_name"
        label = "User Name"
        description = "A simple string field"

        choice1 = "choice1"
        choice2 = "choice2"

        template_field = {
            "class_name": field_type,
            "property": {"name": variable_name, "description": description},
            "kwargs": {"label": label,
                       "choices": {
                           "args": {
                               "tuples": [
                                   [choice1, choice1], [choice2, choice2]
                               ]
                           }
                       }}
        }

        act_name, act_field = JsonFlaskParser._parse_field(template_field)

        self.assertEqual(act_name, variable_name)
        self.assertEqual(act_field.kwargs["label"], label)
        self.assertIsInstance(act_field.kwargs["choices"], list)
        self.assertEqual(act_field.kwargs["choices"][0], tuple([choice1, choice1]))
        self.assertEqual(act_field.kwargs["choices"][1], tuple([choice2, choice2]))


#    def test_list_field(self):
#        field_type = "FieldList"
#        variable_name = "synonyms"
#        label = "Synonyms"
#        description = "A list of possible synonyms"
#
#        subfield_type = "StringField"
#
#        template_field = {
#            "class_name": field_type,
#            "label": label,
#            "property": {"name": variable_name, "description": description},
#            "args": {"objects": [{"class_name": subfield_type}]},
#            "kwargs": {"min_entries": 1}
#        }
#
#        act_name, act_field = JsonFlaskParser._parse_field(template_field)

from dynamic_form.template_builder import (
    FormTemplate,
    PropertyTemplate,
    ObjectTemplate,
    FieldTemplate,
    FormFieldTemplate,
)


class TestToTemplate(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.app = Flask(__name__)
        cls.app.secret_key = "not secret"
        cls.app.config["WTF_CSRF_CHECK_DEFAULT"] = False

    def test_to_template(self):
        """Create form which contains a subform"""

        # Create from template
        field_type = "FieldList"
        subfield_type = "StringField"

        template_form = FormTemplate("Property", "property", "Form to change a property")

        synonym_list_property = PropertyTemplate("Synonyms", "synonyms", "administrative", "List of synonyms")
        string_field_property = PropertyTemplate("Synonym", "synonym", "administrative", "A single synonym")
        stringfield_object = ObjectTemplate(subfield_type, string_field_property)

        string_field = FieldTemplate(field_type,
                                     synonym_list_property,
                                     args={"objects": [stringfield_object.to_dict()]},
                                     min_entries=1,
                                     )
        template_form = template_form.add_field(string_field)

        with self.app.test_request_context():
            form_name, form_cls = JsonFlaskParser.to_form(template_form.to_dict())
            form_instance = form_cls()

            self.assertTrue(hasattr(form_instance, "synonyms"))
            synonym_field = getattr(form_instance, "synonyms")
            self.assertEqual(getattr(synonym_field, "type"), field_type)
            string_field = getattr(synonym_field, "entries")[0]
            self.assertEqual(getattr(string_field, "type"), subfield_type)

    def test_formfield(self):
        template_form = FormTemplate("Property", "property", "Form to change a property")

        data_type_property = PropertyTemplate("Data type", "data_type", "administrative", "The data type")
        data_type_field = FieldTemplate("StringField", data_type_property)

        ctrl_voc_property = PropertyTemplate("Controlled Vocabulary", "ctrl_voc", "administrative",
                                             "The controlled vocabulary")
        ctrl_voc_field = FieldTemplate("SelectField", ctrl_voc_property)

        voc_type_property = PropertyTemplate("Subform", "subform", "administrative", description="A subform")
        voc_type_field = FormFieldTemplate(property=voc_type_property)

        voc_type_field = voc_type_field.add_field(ctrl_voc_field)
        voc_type_field = voc_type_field.add_field(data_type_field)

        template_form = template_form.add_field(voc_type_field)

        with self.app.test_request_context():
            form_name, from_cls = JsonFlaskParser.to_form(template_form.to_dict())

            form_instance = from_cls()

            print("Hello World")

    def test_fieldlist_formfield(self):
        form_type = "FieldList"
        form_name = "contact_form"

        # template_form = FormTemplate("Contacts", form_name, description="A form to register multiple contacts")
        #
        # list_property = PropertyTemplate("Contact list", "contact_list", "administrative", "A contact list")
        #
        # list_field = FieldTemplate(form_type, list_property, args=[])

        template_form = {
            "label": "Contacts",
            "name": form_name,
            "description": "A form to register multiple contacts",
            "fields": [
                {"property": {
                    "name": "contact_list",
                    "label": "Contact List",
                    "level": "administrative",
                    "description": "A contact list"
                },
                    "class_name": form_type,
                    "args": {
                        "objects": [
                            {"class_name": "FormField",
                             "name": "contact",
                             "fields": [
                                 {
                                     "class_name": "StringField",
                                     "property": {
                                         "label": "First Name",
                                         "name": "firstname",
                                         "level": "administrative",
                                         "description": "The first name",
                                     },
                                 },
                                 {
                                     "class_name": "StringField",
                                     "property": {
                                         "label": "Last Name",
                                         "name": "lastname",
                                         "level": "administrative",
                                         "description": "The last name"
                                     },
                                 },
                             ]
                             }
                        ]
                    },
                    "kwargs": {"min_entries": 1}}
            ]
        }

        with self.app.test_request_context():
            act_form_name, form_cls = JsonFlaskParser.to_form(template_form)
            form_instance = form_cls()
            self.assertEqual(act_form_name, form_name)
            self.assertTrue(hasattr(form_instance, "contact_list"))
            contact_list_field = getattr(form_instance, "contact_list")
            self.assertEqual(getattr(contact_list_field, "type"), "FieldList")
            entry_form = getattr(contact_list_field, "entries")[0]
            self.assertTrue(hasattr(entry_form.form, "firstname"))
            self.assertTrue(hasattr(entry_form.form, "lastname"))
