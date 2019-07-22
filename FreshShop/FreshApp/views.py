import hashlib

from django.shortcuts import render
from django.http import HttpResponseRedirect

from FreshApp.models import Seller

#对密码进行加密
def set_password(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    result = md5.hexdigest()
    return result
#注册功能
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and set_password(password):
            user_obj = Seller.objects.filter(username=username).first()
            if user_obj:
                return HttpResponseRedirect('/Store/register/')
            else:
                user_obj = Seller()
                user_obj.username = username
                user_obj.password = set_password(password)
                user_obj.save()
                return HttpResponseRedirect('/Store/login/')
    return render(request,'freshapp/register.html')
#登录功能
def login(request):
    response = render(request,'freshapp/login.html')
    response.set_cookie('username','lmc')
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        cookie = request.COOKIES.get('username')
        if username and set_password(password) and cookie=='lmc':
            user_obj = Seller.objects.filter(username=username).first()
            if user_obj and user_obj.password==set_password(password):
                response = HttpResponseRedirect('/Store/index/')
                response.set_cookie('username',set_password(user_obj.password))
                request.session['username'] = set_password(user_obj.password)
                return response
            else:
                return HttpResponseRedirect('/Store/login/')
    return response
#装饰器登录index界面检验
def login_valid(fun):
    def inner(request,*args,**kwargs):
        cookie = request.COOKIES.get('username')
        session_id =request.session.get('username')
        if set_password(cookie)==set_password(session_id):
            return fun(request,*args,**kwargs)
        return HttpResponseRedirect('/Store/login/')
    return inner
@login_valid
def index(request):
    return render(request,'freshapp/index.html')