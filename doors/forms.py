from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import DoorsUser


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput)

    class Meta:
        model = DoorsUser
        fields = (
            'surname',
            'first_name',
            'last_name',
            'document_number',
            'phone_number',
            'pin_code',
            'email',
            'password',
            'is_superuser',
            'staff'
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = DoorsUser.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("Пользователь с таким email уже существует")
        return email

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают")
        return password2


class UserAdminCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput)

    class Meta:
        model = DoorsUser
        fields = (
            'surname',
            'first_name',
            'last_name',
            'document_number',
            'phone_number',
            'pin_code',
            'email',
            'password',
            'is_superuser',
            'staff'
        )

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField(label='Пароль',
                                         help_text="Чтобы изменить пароль Вы можете воспользоваться "
                                                    "<a href=\"../password/\">формой</a>")

    class Meta:
        model = DoorsUser
        fields = (
            'surname',
            'first_name',
            'last_name',
            'document_number',
            'phone_number',
            'pin_code',
            'email',
            'password',
            'is_superuser',
            'staff'
        )

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]