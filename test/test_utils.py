from dynamic_form.template_builder import FormTemplate, FieldTemplate, PropertyTemplate

def get_login_form():
    email = PropertyTemplate("E-Mail", "email", "administrative", "The email")
    password = PropertyTemplate("Password", "password", "administrative", "The password")

    form = FormTemplate("Login", "user_login", "Form to login a user") \
        .add_field(FieldTemplate("StringField", email,
                                 validators={"args": {"objects": [{"class_name": "DataRequired"}]}})) \
        .add_field(FieldTemplate("PasswordField", password,
                                 validators={"args": {"objects": [
                                     {"class_name": "DataRequired"},
                                     {"class_name": "Length", "kwargs": {"max": 64, "min": 8}}
                                 ]}}))

    return form
