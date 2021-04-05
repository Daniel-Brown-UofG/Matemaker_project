from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from matemaker.models import UserProfile, Genre, Interest
from matemaker.forms import UserForm, UserProfileForm, GenreForm, InterestForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.models import User

def visitor_cookie_handler(request, response, interest):
    last_visit_cookie = request.COOKIES.get('last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],'%Y-%m-%d %H:%M:%S')
    # If it's been more than an hour since the last visit...
    if (datetime.now() - last_visit_time).days > 0:
        interest.views = int(interest.views)+1
        genre = interest.genre
        genre.views = int(genre.views)+1
        interest.save()
        genre.save()
        response.set_cookie('last_visit', str(datetime.now()))
    else:
        response.set_cookie('last_visit', last_visit_cookie)
        # Update/set the visits cookie

def home(request):
    context_dict = {}
    return render (request, 'matemaker/home.html', context=context_dict)

def contact_us(request):
    context_dict = {}
    return render (request, 'matemaker/contact_us.html', context=context_dict)

@login_required
def join(request, genre_name, interest_name):
    interest = Interest.objects.get(slug=interest_name)
    profile = UserProfile.objects.get(user=request.user)
    profile.intersts.add(interest)
    genre = interest.genre
    genre.members = int(genre.members)+1   
    interest.members = int(interest.members)+1
    interest.save()
    genre.save()
    return redirect(reverse('matemaker:interest', kwargs={'genre_name' : genre_name, 'interest_name' : interest_name}))

@login_required
def leave(request, genre_name, interest_name):
    interest = Interest.objects.get(slug=interest_name)
    profile = UserProfile.objects.get(user=request.user)
    profile.intersts.remove(interest)
    genre = interest.genre
    genre.members = int(genre.members)-1   
    interest.members = int(interest.members)-1
    interest.save()
    genre.save()
    return redirect(reverse('matemaker:interest',  kwargs={'genre_name' : genre_name, 'interest_name' : interest_name}))

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
    return render(request, 'matemaker/signuppage.html', context = {'user_form': user_form,
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
def signout(request):
    logout(request)
    # take the user to homepage
    return redirect(reverse('matemaker:home'))

def restricted(request):
    return render(request, 'matemaker/restricted.html')

@login_required
def add_genre(request):
    form = GenreForm()

    if request.method == 'POST':
        form = GenreForm(request.POST)
        # if form is valid redirect to genres page, not home. 
        if form.is_valid():
                genre = form.save(commit=True)
                genre.creator = request.user
                genre.date = timezone.now()
                genre.members = int(genre.members) +1
                genre.save()
                return redirect('/matemaker/genres/')

        else: 
            print(form.errors)

    return render(request, 'matemaker/creategenrepage.html', {'form': form})

def genres(request):
    context_dict = {}
    return render (request, 'matemaker/genres.html', context=context_dict)


# view for individual genre pages (sorry for all the reused variable names..)
def genre(request, genre_name):     # should probably be a slug
    context_dict = {}

    try: 
        genre = Genre.objects.get(slug=genre_name)
        interests = Interest.objects.filter(genre=genre)

        context_dict['genre'] = genre
        context_dict['interests'] = interests
    except Genre.doesNotExist:
        context_dict['genre'] = None
        context_dict['interests'] = None
    return render(request, 'matemaker/genre.html', context = context_dict)


# view for individual interest pages 
def interest(request, genre_name, interest_name):
    context_dict = {}
    genre = Genre.objects.get(slug=genre_name)
    interests = Interest.objects.filter(genre=genre)   # get interests related to genre
    interest = interests.get(slug=interest_name)    # search through genre interests for specified interest. 

    context_dict['genre'] = genre
    context_dict['interest'] = interest
    context_dict['genre_slug'] = genre.slug
    context_dict['interest_slug'] = interest.slug
    response = render(request, 'matemaker/intrest.html', context = context_dict)
    visitor_cookie_handler(request,response,Interest)

    return response

@login_required
def add_interest(request, genre_name):
    try:
        genre = Genre.objects.get(slug=genre_name)
    except Genre.DoesNotExist:
        genre = None
    if genre is None:
        return redirect('/matemaker/genres/')
    
    form = InterestForm()

    if request.method == 'POST':
        form = InterestForm(request.POST)
        if form.is_valid():
            if genre:
                interest = form.save(commit=False)
                interest.genre = genre
                interest.creator = request.user
                interest.date = timezone.now()
                interest.members = int(interest.members)+1
                interest.save()
                return redirect('/matemaker/genres/<slug:genre_name>')

        else: 
            print(form.errors)
    context_dict = {'form': form, 'genre': genre}
    return render(request, 'matemaker/createintrestpage.html', context_dict)


def profile_page(request, user_profile):
    context_dict={}

    try:
        user = User.objects.get(username=user_profile)
        user_prof=UserProfile.objects.get(user=user)
        context_dict['user']=user_prof
    except:
        context_dict['user'] = None
    return render(request, 'matemaker/profile.html', context = context_dict)