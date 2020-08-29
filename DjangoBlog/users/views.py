from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required #decorator to allow to view profile only when you're logged in
from django.contrib import messages
#from django.contrib.auth.forms import UserCreationForm <UserCreationForm is a class that gets converted to html, it's a class to generate a form>
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save() #saves the user when the form validates
            username = form.cleaned_data.get('username') #the validated data will be stored in the form.cleaned_data dictionary
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login') #after filling the form and getting registered, the user has to be redirected to the login page; 'login' is the name that we gave to our urlpattern for our login page
    else:
        form = UserRegisterForm() #we're creating an instance called 'form' of the class UserCreationForm
    return render(request, 'users/register.html', {'form': form}) #we render a template that uses this form, we pass the form as the context to the template so that we can access the form from withon the template. We do this by making use of a dictionary, where 'form' is a variable and form is the instance that we created in line 15

@login_required #decorator to change the functionality of the function profile, it allows to view profile only if logged in
def profile(request): #route which takes the user to his profile page
    if request.method == 'POST':
        u_form=UserUpdateForm(request.POST,instance=request.user)
        p_form=ProfileUpdateForm(request.POST,
                                 request.FILES,
                                 instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form=UserUpdateForm(instance=request.user)
        p_form=ProfileUpdateForm(instance=request.user.profile)
    context={
        'u_form': u_form,
        'p_form' : p_form
    }

    return render(request, 'users/profile.html', context)


