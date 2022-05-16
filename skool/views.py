import dataclasses
import json
from multiprocessing import context
from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate,login,logout
from .forms import NewsFeedForm
from django.utils.text import slugify
from django.forms import inlineformset_factory
from django.contrib.auth.decorators import login_required
from .decorators import *
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.core.mail import send_mail,EmailMessage
from .filters import ResultFilter
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
import re
import string
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

@landingdecorator
def Landing_Page(request):
    obj=NewsFeed.objects.all()[:3]
    template='skool/index.html'
    print('LIST OF MESSAGES: ',messages)
    context={'objects':obj}
    return render(request,template,context)



def Member_page(request):
    template= 'skool/auth.html'
    return render(request,template)

def Register_page(request):
    # print('BODY: ', request.body)
    # print('POST: ', request.POST)
    # print('REQUEST IS AJAX: ',request.is_ajax())
    user=User()
    output={}
    
    if request.is_ajax():
        data=json.loads(request.body)
        # print('BODY INSIDE AJAX: ',data)
        if request.method=='POST':
            first_name=data['first_name']
            last_name=data['last_name']
            username=data['username']
            email=data['email']
            password1=data['password1']
            password2=data['password2']

            group=Group.objects.get(name='students')
           
            
           
            
            

            if User.objects.filter(username=username).exists():
                output['response']='Username already exists'
                output['valid']=False
            
            elif User.objects.filter(email__iexact=email).exists():
                output['response']='Email has already been used'
                output['valid']=False
            elif password1 != password2:
                output['response']='Password don\'t match'
                output['valid']=False
            elif not any(char.isdigit() for char in password1):
                output['response']='Password must contain alphanumeric characters in small caps'
                output['valid']=False 
            elif not any(char.islower() for char in password1):
                output['response']='Password must contain alphanumeric characters in small caps'
                output['valid']=False     
            

         
        
                    
            else:
                user.first_name=first_name
                user.last_name=last_name
                user.username=username
                user.email=email
                user.set_password(password1)
                user.is_active=False
                
                user.save()
                user.groups.add(group)
                StudentProfile.objects.create(user=user)
                output['response']='user successfully created confirm via mail'
                output['valid']=True

                
               

                # group=None
                # if request.POST.get('position')=='teacher':
                #     group=Group.objects.get(name='teachers')
                #     user.groups.add(group)
                #     TeacherProfile.objects.create(user=user,email=email)

                # if request.POST.get('position')=='student':
                #     group=Group.objects.get(name='students')
                #     user.groups.add(group)
                #     StudentProfile.objects.create(user=user,email=email)

                current_site = get_current_site(request)
                mail_subject = 'Activate your Academy.co account.'
                message = render_to_string('skool/acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                    'token':account_activation_token.make_token(user),
                })
                # to_email = form.cleaned_data.get('email')
                email = EmailMessage(
                            mail_subject, message, to=[email]
                )
                email.send()
                
                
                
              
    return JsonResponse(output)
    


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

# @landingdecorator
def Login_page(request):
    output={}
    print('LOGIN DATA OUTSIDE AJAX CALL: ',request.body)
    if request.is_ajax():
        data=json.loads(request.body)
        print('LOGIN DATA: ', data)

        if request.method=='POST':
            username=data['username']
            password=data['password']
            user =authenticate(request,username=username,password=password)
            if user is not None:
                
                if user.is_active==False:
                    output['response']='This account is not verified activate via Gmail '
                    output['valid']=False
                else:
                    login(request, user)
                    if user.groups.filter(name='teachers'):
                        output['group']='teacher'
                        output['response']='login sucessfull '
                        output['valid']=True
                    elif user.groups.filter(name='students'):
                        output['group']='student'
                        output['response']='login sucessfull '
                        output['valid']=True        
            else:
                output['response']='incorrect Username or Password'
        # template= 'skool/auth.html'
    return JsonResponse(output)


def logout_page(request): 
    logout(request)
    return redirect('/eskool/log-in/')

@login_required(login_url='/eskool-login')
def CreatePost(request):
    form=NewsFeedForm(request.POST or None,request.FILES or None)
    if request.method=='POST':
        if form.is_valid():
            obj=form.save(commit=False)
            # obj.slug=slugify(obj.title)
            obj.save()
            form=NewsFeedForm()
    template='skool/create.html'
    context={'form': form}
    return render(request,template,context)

@login_required(login_url='/eskool-login')
@authoriseduser
def Teacher_page(request):
    student=request.user.teacherprofile.level.studentprofile_set.all()
    total_student=student.count()
    teacher=request.user.teacherprofile
    course=teacher.courses_set.all()
    level=teacher.level
    print('BODY OUTPUT :', request.body)
    context={'student_list': student,
     'object':teacher,
     'courses':course,
     'total_student': total_student
     }
    template='skool/teacherdashboard.html'
    return render(request,template,context)

    
def Teacher_Create_Page(request):
    form=TeacherProfileForm(request.POST or None)
    if request.method=='POST':
        if form.is_valid():
            form.save()
    template='skool/createtutor.html'
    context={'form': form}
    return render(request,template,context)

def Student_profile_page(request,pk):
    student=StudentProfile.objects.get(id=pk)
    form=StudentProfileForm(request.POST or None, instance=student)
    if request.method=='POST':
        if form.is_valid():
            # dob=form.cleaned_data['dob'].split('-')[:6]

            form.save()
            # obj.dob='esk'+ dob
            # obj.save()
            return redirect('student_page')
        form=StudentProfileForm()
    context={'form':form}
    return render(request,'skool/student_create_page.html', context)

def Update_result_page(request,pk):
    ResultFormSet=inlineformset_factory(StudentProfile,Result, 
    fields=('level','course','term','first_test','second_test','exam'), extra=5)
        
    student=request.user.teacherprofile.level.studentprofile_set.get(id=pk)
        
    # print(student)
    formset=ResultFormSet(request.POST or None,instance=student)
    if request.method=='POST':
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect(reverse('result_page', args=[pk]))
        formset=ResultFormSet()
    context={'formset': formset}
    return render(request,'skool/updateresult.html',context)



def Create_result_page(request,pk):
    ResultFormset=inlineformset_factory(StudentProfile,Result,fields=('course','term','first_test','second_test','exam'),extra=5)

    student=StudentProfile.objects.get(id=pk)

    formset=ResultFormset(request.POST or None, instance=student,queryset=Result.objects.none())
    if request.method=='POST':
        if formset.is_valid():
            forms=formset.save(commit=False)
            for form in forms:
                form.level=student.level
                form.save()
            

            return HttpResponseRedirect(reverse('result_page', args=[pk]))
    formset=ResultFormset()
    context={'formset':formset,'student':student}
    return render(request,'skool/createresult.html',context)



def Teacher_Result_Page(request,pk):
    # student=request.user.teacherprofile.level.studentprofile_set.get(id=pk)
    # result=student.result_set.all()
    # courses=student.course.all()
    student=StudentProfile.objects.get(id=pk)
    courses=student.level.courses_set.all()
    results=student.result_set.all().order_by('-id')
    total_score=''
    grade=''
    review=''
    for result in results:
        total_score=result.total_score()
        grade=result.student_grade()
        review=result.student_review()

    print("THE COURSE IS :",courses)
    # print(result)
    context={'student':student,'results':results,
    'courses':courses,'total_score':total_score,
    'grade':grade, 'review':review
    
    }
    return render(request,'skool/teacher_result.html',context)


def Student_Page(request):
    students=StudentProfile.objects.get(user=request.user)
    result=students.result_set.all()
    # students=request.user.studentprofile
    filter=ResultFilter(request.GET,queryset=result)
    results=filter.qs
    context={'students':students,'filter':filter,'results':results}
    return render(request,'skool/studentpage.html',context)


def Student_Result_Page(request):
    student=StudentProfile.objects.get(user=request.user)
    result=student.result_set.all()
    context={'result':result}
    return render(request,'skool/student_result.html',context)


def contact(request):

    if request.method=='POST':
        name=request.POST['message_name']
        email=request.POST['from_email']
        message=request.POST['message']

        send_mail(
            'message from'+ name,
            email,
            message,
            ['miraclegodwin67@gmail.com'],
        )

        Messages.objects.create(name=name, email=email, message=message)
    context={'name': name}
    return render(request, 'skool/index.html', context)
        

    ####################################################################################


# def Bookstore(request):
#     products=Product.objects.all()
#     context= {'products':products}
#     return render(request,'skool/bookstore.html', context)


# def add_to_cart(request,pk):
#     product=get_object_or_404(Product,id=pk)
#     user=StudentProfile.objects.get(user=request.user)

#     if product in user.cart.product_set.all():
#         messages.info(request,'you already have this item in your cart')
#         pass


