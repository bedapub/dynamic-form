import unittest

from flask import Flask
from flask_wtf import FlaskForm
from wtforms.validators import *
from wtforms.widgets import *

from dynamic_form.parser_json import JsonFlaskParser

from dynamic_form.template_builder import (
    FormTemplate,
    PropertyTemplate,
    FieldTemplate,
    FormFieldTemplate,
    ValueTypeTemplate,
    ControlledVocabularyTemplate,
    ItemTemplate,
    ArgsTemplate
)


class TestJsonFormParser(unittest.TestCase):
    """The following test check the helper functions of parser json."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.app = Flask(__name__)
        cls.app.secret_key = "not secret"
        cls.app.config["WTF_CSRF_CHECK_DEFAULT"] = False

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

        template_field = FieldTemplate("StringField",
                                       PropertyTemplate("User Name", "user_name", None, None),
                                       label="User Name",
                                       description="A simple string field")

        act_name, act_field = JsonFlaskParser._parse_field(template_field.to_dict())

        self.assertEqual(act_field.kwargs["label"], "User Name")
        self.assertEqual(act_field.kwargs["description"], "A simple string field")

        with self.app.test_request_context():
            form_cls = type("TestForm", (FlaskForm,), {})
            setattr(form_cls, act_name, act_field)

            form = form_cls()

            self.assertTrue(hasattr(form, "user_name"))
            field = getattr(form, "user_name")
            self.assertEqual(getattr(field, "type"), "StringField")

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

    def test_form_with_fieldList(self):
        """Create form which contains a FieldList"""

        template_form = FormTemplate("Property", "property", "Form to change a property")\
            .add_field(
            FieldTemplate("FieldList",
                          PropertyTemplate("Synonyms", "synonyms", "administrative", "List of synonyms"),
                          ArgsTemplate("DataObjects", [
                              FieldTemplate("StringField",
                                            PropertyTemplate("Synonym", "synonym", "administrative",
                                                             "A single synonym"))]),
                          min_entries=1))

        with self.app.test_request_context():
            form_name, form_cls = JsonFlaskParser().to_form(template_form.to_dict())
            form_instance = form_cls()

            self.assertTrue(hasattr(form_instance, "synonyms"))
            synonym_field = getattr(form_instance, "synonyms")
            self.assertEqual(getattr(synonym_field, "type"), "FieldList")
            string_field = getattr(synonym_field, "entries")[0]
            self.assertEqual(getattr(string_field, "type"), "StringField")

    def test_form_with_formfield(self):

        data_type_ctrl_voc = ControlledVocabularyTemplate("Data Type", "data_type", "All supported data types")\
            .add_item(ItemTemplate("Text", "text", "Uncontrolled text input"))\
            .add_item(ItemTemplate("Boolean", "boolean", "Boolean input"))\
            .add_item(ItemTemplate("Controlled Vocabulary", "ctrl_voc", "Value from defined list"))

        template_form = FormTemplate("Property", "property", "Form to change a property")\
            .add_field(
            FormFieldTemplate(prop=PropertyTemplate("Vocabulary Type", "voc_type", "administrative",
                                                    "Vocabulary Type restricts the possible inputs."))\

                .add_field(
                FieldTemplate("SelectField",
                              PropertyTemplate("Data type", "data_type", "administrative", "The data type",
                                               ValueTypeTemplate("ctrl_voc", data_type_ctrl_voc))))
                .add_field(
                # TODO replace StringField with SelectField
                FieldTemplate("StringField",
                              PropertyTemplate("Controlled Vocabulary", "ctrl_voc", "administrative",
                                               "The controlled vocabulary"))))

        form_name, from_cls = JsonFlaskParser().to_form(template_form.to_dict())

        with self.app.test_request_context():
            form_instance = from_cls()

    def test_form_with_fieldList_and_FormField(self):

        template_form = FormTemplate("Contacts", "contact_form", "A form to register multiple contacts")\
            .add_field(
            FieldTemplate("FieldList",
                          PropertyTemplate("Contact List", "contact_list", "administrative", "A contact list"),
                          ArgsTemplate("DataObjects", [
                              FormFieldTemplate(PropertyTemplate("Contact", "contact", "administrative", "A contact"))
                                       .add_field(
                                  FieldTemplate("StringField",
                                                PropertyTemplate("First Name", "firstname","administrative",
                                                                 "first name of user")))
                                       .add_field(
                                  FieldTemplate("StringField",
                                                PropertyTemplate("Last Name", "lastname","administrative",
                                                                 "last name of user")))
                          ]),
                          min_entries=1))

        with self.app.test_request_context():
            act_form_name, form_cls = JsonFlaskParser().to_form(template_form.to_dict())
            form_instance = form_cls()
            self.assertEqual(act_form_name, "contact_form")
            self.assertTrue(hasattr(form_instance, "contact_list"))
            contact_list_field = getattr(form_instance, "contact_list")
            self.assertEqual(getattr(contact_list_field, "type"), "FieldList")
            entry_form = getattr(contact_list_field, "entries")[0]
            self.assertTrue(hasattr(entry_form.form, "firstname"))
            self.assertTrue(hasattr(entry_form.form, "lastname"))
