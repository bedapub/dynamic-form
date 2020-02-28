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


def get_many_login_forms(num=3):

    forms = []

    for i in range(num):
        form = get_login_form()
        form.name = form.name + f"_{i}"
        forms.append(form)
    return forms

