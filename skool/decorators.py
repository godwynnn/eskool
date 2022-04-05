from django.shortcuts import redirect
from django.http import HttpResponse

def authoriseduser(view_func):
    def verify_func(request,*args,**kwargs):
        group=None
        if request.user.groups.exists():
            group=request.user.groups.all()[0].name
        if group =='teachers':
            return view_func(request,*args,**kwargs)
        if group =='students':
            return redirect('/eskool/student')
    return verify_func


def landingdecorator(view_func):
    def verify_func(request,*args,**kwargs):
        
        if request.user.is_authenticated:
            group=None
            if request.user.groups.exists():
                group=request.user.groups.all()[0].name
            if group =='teachers':
                return redirect('eskool/teachers/')
            if group =='students':
                return redirect('/eskool/student')
        else:
            return view_func(request,*args,**kwargs)  
    return verify_func