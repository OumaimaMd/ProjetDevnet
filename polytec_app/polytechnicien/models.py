from django import forms
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User


class CustomUser(AbstractUser):
    # Tu peux ajouter des champs personnalisés ici si tu veux
    pass


class Course(models.Model):
    MATH, PHYS, LANG, INFO = 'Math','Physique','Langue','Info'
    SUBJECT_CHOICES = [
        (MATH, 'Mathématiques'),
        (PHYS, 'Physique'),
        (LANG, 'Langues'),
        (INFO, 'Informatique'),
    ]

    YEAR1, YEAR2, YEAR3 = 1, 2, 3
    YEAR_CHOICES = [
        (YEAR1, '1ère année'),
        (YEAR2, '2ème année'),
        (YEAR3, '3ème année'),
    ]

    subject = models.CharField(max_length=20, choices=SUBJECT_CHOICES)
    year = models.PositiveSmallIntegerField(choices=YEAR_CHOICES)
    title   = models.CharField(max_length=100)
    description = models.TextField()
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    
    def reservations_count(self):
        return self.reservation_set.count() 
    
    def __str__(self):
        return f"{self.get_subject_display()} – {self.get_year_display()}: {self.title}"



class Resource(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='resources/')
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


class Reservation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    reserved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')  # Un utilisateur ne peut réserver un même cours qu'une seule fois

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['subject', 'year', 'title', 'description']

