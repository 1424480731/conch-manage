from django.shortcuts import render
from django.http import HttpResponse
from signin.models import User
# Create your views here.
def index(req):
    return render(req,'login.html')

def login(req):

    if req.method == 'POST':

        username =req.POST.get('username')
        password = req.POST.get('password')
        user = User.objects.filter(username=username,password=password)
        if user:
            req.session['status']=1
            return render(req,'manager.html')


    return render(req,'login.html',{'msg':'无此用户'})

def login_out(req):

    req.session['status']=0
    return render(req,'login.html',{'msg':'请先登录'})