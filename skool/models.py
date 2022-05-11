from django.db import models
from django.conf import settings
# from django.contrib.auth.models import User
# Create your models here.



User=settings.AUTH_USER_MODEL
class Level(models.Model):
    level_no=models.IntegerField(null=True)
    # course=models.ManyToManyField(Courses)
   

    def __str__(self):
        return f'level-{self.level_no}'


class TeacherProfile(models.Model):
    user=models.OneToOneField(User,null=True,on_delete=models.CASCADE,blank=True)
    level=models.ForeignKey(Level, null=True, blank=True,on_delete=models.CASCADE)
    id_no=models.CharField(max_length=200,null=True)
    dob=models.DateField(null=True, blank=True)
    date_added=models.DateField(auto_now_add=True)


    class Meta:
        ordering=['-date_added']

    def __str__(self):
        return f'{self.user}|{self.id_no}'



class Courses(models.Model):
    name=models.CharField(max_length=200, null=True)
    level=models.ForeignKey(Level,null=True,on_delete=models.SET_NULL)
    teacher=models.ForeignKey(TeacherProfile, null=True, blank=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.name



class StudentProfile(models.Model):
    user=models.OneToOneField(User,null=True,on_delete=models.CASCADE,blank=True)
    level=models.ForeignKey(Level,null=True,on_delete=models.CASCADE, default=1)
    id_no=models.CharField(max_length=200,null=True,unique=True,blank=True)
    picture=models.ImageField(null=True,blank=True, upload_to='pictures/')
    dob=models.DateField(null=True, blank=True)
    date_added=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.username




class Result(models.Model):
    Grade=(
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('E', 'E'),
    )

    Review=(
        ('excellent', 'excellent'),
        ('Good', 'Good'),
        ('Satisfactory', 'Satisfactory'),
        ('Poor', 'Poor'),
        ('Fail', 'Fail'),
    )
    Term=(
        ('first','first'),
        ('second','second'),
        ('third','third')
    )
    studentprofile=models.ForeignKey(StudentProfile,default=1,null=True,on_delete=models.SET_NULL)
    level=models.ForeignKey(Level,null=True,blank=True, on_delete=models.CASCADE)
    term=models.CharField(max_length=200,null=True,choices=Term)
    first_test=models.PositiveIntegerField(null=True,blank=True)
    second_test=models.PositiveIntegerField(null=True,blank=True)
    exam=models.PositiveIntegerField(null=True,blank=True)
    course=models.ForeignKey(Courses,null=True,on_delete=models.CASCADE)
    # grade=models.CharField(max_length=200,null=True,choices=Grade)
    # review=models.CharField(max_length=200,null=True,choices=Review)
    date_added=models.DateField(auto_now_add=True)

    class Meta:
        ordering=['-date_added']

    def __str__(self):
        return f'{self.studentprofile}'
    
    def total_score(self):
        return self.first_test + self.second_test + self.exam
    
    def student_grade(self):
        grade= ''
        score=self.total_score()

        
        if 85<= score <= 100:
            grade = 'A'

        elif 70 <= score <85:
            grade ='B'

        elif 55<= score <70:
            grade ='C'

        elif 40 <= score <55:
            grade ='D'

        elif 30<=score <40:
            grade= 'E'

        elif score < 30:
            grade = 'F'
        else:
            print('you did not write this course')

        return grade   

    def student_review(self):
        review=''

        if self.student_grade()== 'A':
            review ='Excellent'

        elif self.student_grade()== 'B':
            review ='Good'

        elif self.student_grade()== 'C':
            review ='Satisfactory'

        elif self.student_grade()== 'D':
            review ='Average'

        elif self.student_grade()== 'E':
            review ='Poor'

        elif self.student_grade()== 'F':
            review ='Fail'

        else:
            print('you did not write this course')

        return review
        
class Tag(models.Model):
    name=models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.name


# ########################################################################################################

class NewsFeed(models.Model):
    Category=(
        ('News','News'),
        ('Tech','Tech'),
        ('Business','Business'),
        ('Lifestyle','Lifestyle'),
        ('Feature','Feature')
    )
    title=models.CharField(max_length=500)
    image=models.ImageField(upload_to='images/',null=True, blank=True, )
    category=models.CharField(max_length=200,null=True,blank=True,choices=Category, default='News')
    tags=models.ManyToManyField(Tag, blank=True)
    slug=models.SlugField(unique=True,null=True, blank=True)
    content=models.TextField(blank=True,null=True)
    date_added=models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering=['-date_added']

    def __str__(self):
        return self.title

class Messages(models.Model):
    name=models.CharField(max_length=4000 ,null=True, blank=True)
    email=models.EmailField(null=True, blank=True)
    message=models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.name}|{self.email}'



# class Product(models.Model):

#     name=models.CharField(max_length=200,null=True,blank=True)
#     price=models.IntegerField(default=0)
#     image=models.ImageField(null=True, blank=True)
#     url=models.URLField(max_length=2000, null=True,blank=True)
#     description=models.CharField(max_length=10000,null=True,blank=True)
#     date_added=models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering=['-date_added']

#     def __str__(self):
#         return self.name



# class Cart(models.Model):
#     owner=models.ForeignKey(StudentProfile,null=True,blank=True,on_delete=models.CASCADE)
#     product=models.ManyToManyField(Product)
#     ordered=models.BooleanField(default=False)
#     date_added=models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering=['-date_added']

#     def __str__(self):
#         return self.product.name

    

# class Order(models.Model):
#     owner=models.OneToOneField(StudentProfile, on_delete=models.CASCADE)
#     ordered=models.BooleanField(default=False)
#     carts=models.ForeignKey(Cart, on_delete=models.CASCADE)
#     date_ordered=models.DateTimeField(auto_now=True)
