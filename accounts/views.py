from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout

# Create your views here.

def signup_view(request):
    print(request.method)
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # retrieve the data from the new user that was created
            user = form.save()
            # this makes the user to be logged in
            login(request, user)
            # reverse url
            return redirect('web_app_navigator:index')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {"form": form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            #get the user
            user = form.get_user()
            # this makes the user to be logged in
            login(request, user)
            if "next" in request.POST:
                return redirect(request.POST.get("next"))
            else:
                return redirect('web_app_navigator:index')
    else:
        form = AuthenticationForm()
    return render(request,'accounts/login.html', {"form":form})


def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('web_app_navigator:index')
    else:
        form = AuthenticationForm()
    return render(request,'accounts/login.html', {"form":form})