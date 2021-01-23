from django.shortcuts import render, redirect
from .models import *
from .supporting_func import *
from django.contrib import messages
from django.http import HttpResponse
from django.http import JsonResponse
from django.conf import settings
import json
import os


# rendering test of 20 recordings
def test(request):
    context = {}
    if not request.user.is_authenticated:
        return redirect("index")

    if initial_test.objects.filter(new_user = request.user).exists():
        messages.info(request, "You already have taken this test")
        return redirect("index")
    else:
        # Take 20 random sentences from master.txt file

        base_url = settings.BASE_DIR

        # location of master.txt file
        master_text_file = os.path.join(base_url, "static", "master-text", "master.txt")
        
        # get 20 sentences from this file by using the function we have prepared
        # that function has been saved in ./supporting_func.py
        all_selected_sentences = select_sentences(master_text_file, 20)
        context['all_selected_sentences'] = json.dumps(all_selected_sentences)
        print(all_selected_sentences)

    return render(request, "test.html", context)



def abcc(request):
    output = {}
    if request.method == "GET":
        # myData = request.FILES['audio_data']
        for i, j in request.GET.items():
            print(i, "=>", j)
        
        # print(myData)

    return JsonResponse(output)

def abc(request):
    if request.method == "POST":
        for i, j in request.POST.items():
            print(i, "=>", j)

    return render(request, "abc.html")

def upload_file(request):
    """
    to upload file
    """
    if request.method == "POST":
        targetfile = request.FILES.get("targetfile")
        messages.info(request, "File has been uploaded successfully!")

        new_txt_file = txt_file(
            myFile = targetfile,
            uploaded_by = request.user
        )

        new_txt_file.save()

        base_url = settings.BASE_DIR

        master_text_file = os.path.join(base_url, "static", "master-text", "master.txt")
        new_file = os.path.join(base_url, "media", str(new_txt_file.myFile))

        # appneding content in master text file
        append_content(master_text_file, new_file)

    return redirect("index")

# main page function

def index(request):

    if not request.user.is_authenticated:
        return redirect("login")
    
    return render(request, 'main.html')


# function for signup

def signup(request):
    if request.method == "POST":
        name = request.POST['name']
        l_name = request.POST['l_name']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        context = {
            "name":name,
            "l_name":l_name,
            "email":email,
            "pass1":pass1,
            "pass2":pass2,
        }
        if pass1==pass2:
            if User.objects.filter(username=email).exists():
                print("Email already taken")
                messages.info(request, "Entered email already in use!")
                context['border'] = "email" 
                return render(request, "signup.html", context)

            user = User.objects.create_user(username=email, first_name=name, password=pass1, last_name=l_name)
            user.save()
            
            return redirect("login")
        else:
            messages.info(request, "Your pasword doesn't match!")
            context['border'] = "password"
            return render(request, "signup.html", context)


    
    return render(request, "signup.html")


# function for login

def login(request):

    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        context = {
            'email': email,
            'password': password
        }
        user = auth.authenticate(username=email, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("index")
        else:
            messages.info(request, "Incorrect login details!")
            return render(request, "login.html", context)
            # return redirect("login")
    else:
        return render(request, "login.html")


# function for logout

def logout(request):
    auth.logout(request)
    return redirect("index")

