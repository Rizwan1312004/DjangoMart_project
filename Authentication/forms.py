from django import forms
from accounts.models import Account
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column


class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        label="Password"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        label="Confirm Password"
    )

    class Meta:
        model = Account
        # Only include fields that are safe to set at registration
        # phone_number is optional so we exclude it here
        fields = ["first_name", "last_name", "username", "email"]

        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Make phone_number not required (it's excluded from form fields anyway)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_tag = False  # We render the form tag manually in the template

        self.helper.layout = Layout(
            Row(
                Column("first_name", css_class="col-md-6 mb-3"),
                Column("last_name", css_class="col-md-6 mb-3"),
            ),
            Row(
                Column("username", css_class="col-md-6 mb-3"),
                Column("email", css_class="col-md-6 mb-3"),
            ),
            Row(
                Column("password", css_class="col-md-6 mb-3"),
                Column("confirm_password", css_class="col-md-6 mb-3"),
            ),
        )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data

    def save(self, commit=True):
        # Use super().save() to get the unsaved model instance (excludes extra fields like confirm_password)
        user = super().save(commit=False)
        # Hash the password properly
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    """Custom login form that uses email instead of username."""
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "your@email.com"}),
        label="Email"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        label="Password"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_tag = False
