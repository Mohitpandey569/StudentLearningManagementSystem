from django.contrib import admin
from .models import *

#Register your models here.
class what_you_learn_TubularInline(admin.TabularInline):
    model =What_you_learn

class Requirments_TubularInline(admin.TabularInline):
    model = Requirements

class Video_TubularInline(admin.TabularInline):
    model = Video

class course_admin(admin.ModelAdmin):
    inlines =(what_you_learn_TubularInline,Requirments_TubularInline,Video_TubularInline)

admin.site.register(Categories)
admin.site.register(Author)
admin.site.register(Course ,course_admin)
admin.site.register(Level)
admin.site.register(What_you_learn)
admin.site.register(Requirements)
admin.site.register(Lesson)
admin.site.register(Language)
admin.site.register(UserCourse)
admin.site.register(Payment)