from django.shortcuts import render, render_to_response
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.template import RequestContext
from UserApp.forms import LoginForm, UserForm
from django.http.response import HttpResponseRedirect


# Create your views here.

def CheckCredential(request):
    if request.method == 'GET':
        register_form = UserForm()
        login_form = LoginForm()
        return render(request, 'index.html', {'register_form': register_form, 'login_form': login_form},
                      context_instance=RequestContext(request))
    elif request.method == 'POST':
        if request.user.is_authenticated():
            logout(request)
            register_form = UserForm()
            login_form = LoginForm()
            return render(request, 'index.html', {'register_form': register_form, 'login_form': login_form},
                          context_instance=RequestContext(request))
        login_form = LoginForm(request.POST)
        register_form = UserForm()
        if login_form.is_valid():
            userName = login_form.cleaned_data['username']
            passWord = login_form.cleaned_data['password']
            user = authenticate(username=userName, password=passWord)
            if user is not None:
                # the password verified for the user
                if user.is_active:
                    print("User is valid, active and authenticated")
                    login(request, user)
                    return HttpResponseRedirect('../Purchases.html')
                else:
                    print("The password is valid, but the account has been disabled!")
                    print(login_form.errors.as_data())
                    return render(request, 'index.html', {'register_form': register_form, 'login_form': login_form},
                                  context_instance=RequestContext(request))
            else:
                # the authentication system was unable to verify the username and password
                print("The username and password were incorrect.")
                print(login_form.errors.as_data())
                return render(request, 'index.html', {'register_form': register_form, 'login_form': login_form},
                              context_instance=RequestContext(request))
        else:
            print(login_form.errors.as_data())
            return render(request, 'index.html', {'register_form': register_form, 'login_form': login_form},
                          context_instance=RequestContext(request))


def RegisterUser(request):
    if request.method == 'POST':
        register_form = UserForm(request.POST)
        login_form = LoginForm()
        if register_form.is_valid():
            flag = get_user_model().objects.filter(email=request.POST['email']).exists()
            if flag == True:
                #print(register_form.errors.as_data())
                #register_form = UserForm()
                #login_form = LoginForm()
                return render(request, 'index.html', {'register_form': register_form, 'login_form': login_form},
                              context_instance=RequestContext(request))
            if register_form.cleaned_data['password'] == register_form.cleaned_data['password_confirmation']:
                register_form.save()
                return HttpResponseRedirect('../CreateGroup.html')

            else:
                print(register_form.errors.as_data())
                return render(request, 'index.html', {'register_form': register_form, 'login_form': login_form},
                              context_instance=RequestContext(request))
        else:
            print(register_form.errors.as_data())
            return render(request, 'index.html', {'register_form': register_form, 'login_form': login_form},
                          context_instance=RequestContext(request))
    elif request.method == 'GET':
        register_form = UserForm()
        login_form = LoginForm()
        return render(request, 'index.html', {'register_form': register_form, 'login_form': login_form},
                      context_instance=RequestContext(request))


def index(request):
    register_form = UserForm()
    login_form = LoginForm()
    return render(request, 'index.html', {'register_form': register_form, 'login_form':login_form},context_instance=RequestContext(request))
