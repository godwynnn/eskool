from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Level)
admin.site.register(StudentProfile)
admin.site.register(TeacherProfile)
admin.site.register(Courses)
admin.site.register(Result)
admin.site.register(Tag)
admin.site.register(NewsFeed)
admin.site.register(Messages)
# admin.site.register(Product)
# admin.site.register(Cart)
# admin.site.register(Order)
