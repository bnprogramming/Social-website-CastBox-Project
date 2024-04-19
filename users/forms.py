from django import forms
from django.core import validators


class UserRegisterForm(forms.Form):
    # region: first_name Field
    first_name = forms.CharField(
        label='First_Name',
        max_length=150,
        error_messages={
            'required': 'Enter Valid Name',
            'max_length': 'First name must be at last 150 characters',
        },
        widget=forms.TextInput(attrs={
            'placeholder': 'First Name',
            'class': 'input--style-4',
        }))
    # endregion

    # region: last_name Field
    last_name = forms.CharField(
        label='Last Name',
        max_length=150,
        error_messages={
            'required': 'Enter Valid Name',
            'max_length': 'Last name must be at last 150 characters',
        },
        widget=forms.TextInput(attrs={
            'placeholder': 'Last Name',
            'class': 'input--style-4',
        }))
    # endregion

    # region: username Field
    username = forms.CharField(
        label='User Name',
        max_length=150,
        error_messages={
            'required': 'Enter Valid UserName',
            'max_length': 'UserName must be at last 150 characters',
        },
        widget=forms.TextInput(attrs={
            'placeholder': 'User Name',
            'class': 'input--style-4',
        }),
        validators=[
            validators.MaxLengthValidator(150),
        ]
    )
    # endregion

    # region: email Field
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'placeholder': 'yourname@gmail.com',
            'class': 'input--style-4',
            'id': '',
        }),
        validators=[
            validators.MaxLengthValidator(100),
            validators.EmailValidator,
        ]
    )
    # endregion

    # region: phone Field
    phone = forms.CharField(
        label='Phone',
        max_length=20,
        widget=forms.TextInput(attrs={
            'placeholder': '989126620321',
            'class': 'input--style-4',
            'id': '',
        }),
        validators=[
            validators.MaxLengthValidator(20),
        ]
    )
    # endregion

    # region: avatar Field
    avatar = forms.FileField(
        label='Avatar',
        widget=forms.FileInput(attrs={
            'placeholder': 'Your Avatar picture',
            'class': 'input--style-4',
            'id': '',
        }),
    )
    # endregion

    # region: password Field
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter the password',
            'class': 'input--style-4',
            'id': '',
        }),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )
    # endregion

    # region: confirm_password Field
    confirm_password = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repeat the password',
            'class': 'col-sm-6 input--style-4',
            'id': '',
        }),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )
    # endregion

    # region: description Field
    description = forms.CharField(
        label='About You',
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Tell us about your self',
                'class': 'col-center input--style-4',
                'id': '',
                'rows': 3,
                'cols': 50,

            }))

    # endregion

    # Validators :
    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password == confirm_password:
            return confirm_password

        raise forms.ValidationError('Password and Confirm Password are not the same')


class UserLoginForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'col-center input--style-4',
        }),
        validators=[
            validators.MaxLengthValidator(100),
            validators.EmailValidator,
        ]
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'col-center input--style-4',
        }),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )


class UserEditProfileForm(UserRegisterForm):
    pass
