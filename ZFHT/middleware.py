from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render
class MyMiddleWare(MiddlewareMixin):

    def process_request(self,request):

        if '/login/' in request.path or request.session['status']==1:
            pass
        else:
            return render(request,'login.html')


    def process_response(self, request, response):
        return response