from django.contrib import admin
from .models import Course, Resource, Comment, Reservation

admin.site.register(Course)
admin.site.register(Resource)
admin.site.register(Comment)
admin.site.register(Reservation)