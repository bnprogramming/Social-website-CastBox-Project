from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from users.forms import UserRegisterForm, UserLoginForm, UserEditProfileForm
from users.models import User
from users.serializers import UserSerializer


# region: User Register  View
class UserRegisterView(View):
    def get(self, request):
        register_form = UserRegisterForm()
        context = {
            'form': register_form,
            'Title': "Register",

        }
        return render(request, 'user_module/register_page.html', context)

    def post(self, request):
        register_form = UserRegisterForm(request.POST, request.FILES)
        if register_form.is_valid():
            first_name = register_form.cleaned_data.get('first_name')
            last_name = register_form.cleaned_data.get('last_name')
            username = register_form.cleaned_data.get('username')
            email = register_form.cleaned_data.get('email')
            phone = register_form.cleaned_data.get('phone')
            avatar = register_form.cleaned_data.get('avatar')
            description = register_form.cleaned_data.get('description')
            password = register_form.cleaned_data.get('password')

            # region : Email check
            new_user_by_email: bool = User.objects.filter(email__iexact=email).exists()
            new_user_by_username: bool = User.objects.filter(username__iexact=username).exists()
            new_user_by_phone: bool = User.objects.filter(phone__iexact=phone).exists()
            if new_user_by_email:
                register_form.add_error('email', 'Email is already used by others')
            elif new_user_by_username:
                register_form.add_error('username', 'Username is already used by others')
            elif new_user_by_phone:
                register_form.add_error('phone', 'Phone is already used by others')

            else:
                new_user = User(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    email=email,
                    phone=phone,
                    avatar=avatar,
                    description=description,
                    is_active=False,
                )
                # To make password hashable not store directly the exact password
                new_user.set_password(password)
                new_user.save()
                return redirect(reverse('login_page'))

            context = {
                'form': register_form
            }
            return render(request, 'user_module/register_page.html', context)

        context = {
            'form': register_form,
            'Title': "Register",

        }
        return render(request, 'user_module/register_page.html', context)
# endregion


# region: Login  View
class UserLoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('user_panel_dashboard'))
        login_form = UserLoginForm()
        context = {
            'login_form': login_form
        }
        return render(request, 'user_module/login_page.html', context)

    def post(self, request):
        login_form = UserLoginForm(request.POST)
        if login_form.is_valid():
            email = login_form.cleaned_data.get('email')
            password = login_form.cleaned_data.get('password')
            user: User = User.objects.filter(email__iexact=email).first()
            # First check availability of email
            # Then  check account is_active
            # Then  check correct password
            if user is None:
                login_form.add_error('email', 'User does not exist')
            else:
                if user.is_active:
                    # make input pass to hashable format and check
                    is_password_correct = user.check_password(password)
                    if is_password_correct:
                        login(request, user)  # set the cookie and session id automatically
                        return redirect(reverse('user_panel_dashboard'))
                    else:
                        login_form.add_error('password', 'Password is incorrect')
                else:
                    login_form.add_error('email', 'Your account is not active')

        context = {
            'login_form': login_form
        }
        return render(request, 'user_module/login_page.html', context)
# endregion


# region: UserEditProfile  View
@method_decorator(login_required, name='dispatch')
class UserEditProfileView(View):
    def get(self, request):
        edit_form = UserEditProfileForm(UserSerializer(instance=request.user).data)
        context = {
            'form': edit_form,
            'Title': "Edit Profile",
        }
        return render(request, 'user_module/register_page.html', context)

    def post(self, request):
        edit_form = UserEditProfileForm(request.POST, request.FILES)
        if edit_form.is_valid():
            current_user = User.objects.get(id=request.user.id)
            current_user.first_name = edit_form.cleaned_data.get('first_name')
            current_user.last_name = edit_form.cleaned_data.get('last_name')
            current_user.username = edit_form.cleaned_data.get('username')
            current_user.email = edit_form.cleaned_data.get('email')
            current_user.phone = edit_form.cleaned_data.get('phone')
            current_user.avatar = edit_form.cleaned_data.get('avatar')
            current_user.description = edit_form.cleaned_data.get('description')
            current_user.is_active = True

            current_user.set_password(edit_form.cleaned_data.get('password'))
            current_user.save()
            return redirect(reverse('login_page'))

        context = {
            'form': edit_form,
            'Title': "Edit Profile",

        }
        return render(request, 'user_module/register_page.html', context)
# endregion


# region: log out  View
@method_decorator(login_required, name='dispatch')
class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('login_page'))
# endregion
