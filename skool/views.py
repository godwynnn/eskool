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
from django.core.mail import send_mail
from .filters import ResultFilter
# Create your views here.

@landingdecorator
def Landing_Page(request):
    obj=NewsFeed.objects.all()[:3]
    template='skool/index.html'
    context={'objects':obj}
    return render(request,template,context)


def Register_page(request):
    form=CreateUserForm(request.POST or None)
    if request.method=='POST':
        if form.is_valid():
            email=form.cleaned_data['email']
            user=form.save()
            
            group=None
            if request.POST.get('position')=='teacher':
                group=Group.objects.get(name='teachers')
                user.groups.add(group)
                TeacherProfile.objects.create(user=user,email=email)

            if request.POST.get('position')=='student':
                group=Group.objects.get(name='students')
                user.groups.add(group)
                StudentProfile.objects.create(user=user,email=email)


            username=form.cleaned_data['username']
            messages.success(request,'you have successfully created an account for, '+ username)
            form=CreateUserForm()
            return redirect('login_page')
    context={'form': form}
    template= 'skool/signup.html'
    return render(request,template,context)



def Login_page(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user =authenticate(request,username=username,password=password)
        if user is not None:
            login(request, user)
            return redirect('teacher_page')
    
        else:
            messages.info(request,'Incorrect username Or password')
    template= 'skool/login.html'
    return render(request,template)


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
    fields=('level','course','term','first_test','second_test','exam','grade','review'), extra=10
    )
    
    student=request.user.teacherprofile.level.studentprofile_set.get(id=pk)
    
    # print(student)
    formset=ResultFormSet(request.POST or None,instance=student)
    if request.method=='POST':
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect(reverse('result_page', args=[pk]))
        formset=ResultFormSet()
    context={'formset': formset}
    return render(request,'skool/createresult.html',context)

def Create_result_page(request):
    pass


def Teacher_Result_Page(request,pk):
    # student=request.user.teacherprofile.level.studentprofile_set.get(id=pk)
    # result=student.result_set.all()
    # courses=student.course.all()
    student=StudentProfile.objects.get(id=pk)
    courses=student.level.courses_set.all()
    result=student.result_set.all()
    print("THE COURSE IS :",courses)
    # print(result)
    context={'student':student,'result':result,'courses':courses}
    return render(request,'skool/teacher_result.html',context)


def Student_Page(request):
    students=StudentProfile.objects.get(user=request.user)
    # students=request.user.studentprofile
    filter=ResultFilter()
    context={'students':students,'filter':filter}
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


