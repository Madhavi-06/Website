from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from tensorflow.keras.models import *
from tensorflow.keras.layers import *
from django.contrib.auth import authenticate,login,logout
from .models import *
from tensorflow.keras.preprocessing import image
import os
import pandas as pd
import numpy as np
from django.contrib.auth.hashers import check_password

# Create your views here.
index="index.html"
registerpage="register.html"
loginpage="login.html"
Userhome = 'userhome.html'
uploadpage = 'upload.html'
resultpage = "result.html"

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request,"about.html")

def register(request):   
        if request.method == 'POST':
            name = request.POST['name']
            email = request.POST['email']
            password = request.POST['password']
            conpassword = request.POST['conpassword']
            age = request.POST['Age']
            contact = request.POST['contact']
            if password == conpassword:
                register = Register(name=name, email=email, password=password,
                                age=age,contact=contact)
                register.save()
                print(register)

            msg = f"You've signed up successfully   {name}"
            return render(request, loginpage)
        # else:
        #     msg = "Registration failed. Please try again."
            return render(request, registerpage, {"msg": msg})
        return render(request,'register.html')

def login(request):
    if request.method == 'POST':
        lemail = request.POST['email']
        lpassword = request.POST['password']

        d = Register.objects.filter(email=lemail, password=lpassword).exists()
        print(d)
        if d:
            return redirect(userhome)


        else:
            msg = 'Login failed'
            return render(request, login, {'msg': msg})
    return render(request,'login.html')


def userhome(request):
    return render(request, Userhome)

def upload(request):
    pathss = os.listdir(r"../backend/data/train")
    classes = []
    for i in pathss:
        classes.append(i)
    if request.method == "POST":
        file = request.FILES['file']        
        s = currency(image=file)  
        s.save()
        path1 = os.path.join(os.path.abspath('home/static/output'), s.filename())
       
        model = load_model(r'C:\Users\0618\Documents\projects\NOVEMBER\business\TK127320 -  Identification of Fake Indian Currency using Convolutional Neural Network\SOURCE CODE-YMTS-0618\CODE\backend\alg\cnn.h5')
        x1 = image.load_img(path1, target_size=(256, 256))
        x1 = image.img_to_array(x1)
        x1 = np.expand_dims(x1, axis=0)
        x1 /= 255
        
        result = model.predict(x1)
        b1 = np.argmax(result)
        prediction = classes[b1]

        return render(request, 'result.html', {"result": prediction, "path1": 'static/output/' + s.filename()})

    return render(request, 'upload.html')