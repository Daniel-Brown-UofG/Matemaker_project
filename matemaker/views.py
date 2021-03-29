from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from matemaker.models import UserProfile
from matemaker.forms import UserForm, UserProfileForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required

def home(request):
    context_dict = {}
    return render (request, 'matemaker/home.html', context=context_dict)

def contact_us(request):
    context_dict = {}
    return render (request, 'matemaker/contact_us.html', context=context_dict)

def register(request):
    # boolean to tell template if register was successful. set to false initially
    registered = False

    if request.method =='POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            # this method hashes the password and then we can save user
            user.set_password(user.password)
            user.save()

            # Now the UserProfile instance. set commit to false to delay model saving
            # until we're ready
            profile = profile_form.save(commit=False)
            profile.user = user

            # check if profile picture was set
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture'] 
            
            profile.save()

            # update registered as registration was successful
            registered = True
        
        else:
            # invalid form? 
            print(user_form.errors, profile_form.errors)
    else:
        # not POST request, so render form using two ModelForm instances
        # These forms will be blank and ready for input.
        user_form = UserForm() 
        profile_form = UserProfileForm()

    # Render template depending on context
    return render(request, 'matemaker/register.html', context = {'user_form': user_form,
                                                            'profile_form': profile_form,
                                                            'registered': registered})

def user_login(request):
    if request.method == 'POST':

        # gather pword and username from user
        username = request.POST.get('username')
        password = request.POST.get('password')

        # django machinery checks if user/pword corresponds to user. If it does, returns a user object
        user = authenticate(username=username, password=password)

        # if login details are correct
        if user:

            # check if account is disabled
            if user.is_active:

                # login the user and redirect to index page
                login(request, user)
                return redirect(reverse('matemaker:home'))
            else:

                # deactivated account can't be logged in 
                return HttpResponse("Your Rango account is disabled.")
        else:

            # wrong login details 
            print(f"Invalid logic details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")

    else:

        # in the case of a GET request, we post the form (no context variables needed)
        return render(request, 'matemaker/login.html')

@login_required
def user_logout(request):
    logout(request)
    # take the user to homepage
    return redirect(reverse('rango:index'))

def restricted(request):
    return render(request, 'rango/restricted.html')
