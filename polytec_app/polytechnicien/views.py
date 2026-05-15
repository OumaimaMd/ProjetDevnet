import os
import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LoginView

from .models import Course, CourseForm, Resource, Reservation
from .forms import AddCourseForm, ResourceForm, CommentForm, RegisterForm, CustomUserCreationForm
import json

# ─────────────────────────────────────────
# 🌐 Open Library API
# ─────────────────────────────────────────

SUBJECT_MAP = {
    'Math':     'mathematics',
    'Physique': 'physics',
    'Langue':   'linguistics',
    'Info':     'computer_science',
}

def get_books_from_api(subject):
    """Récupère des livres depuis Open Library API selon la matière."""
    query = SUBJECT_MAP.get(subject, subject)
    try:
        url = f"https://openlibrary.org/subjects/{query}.json?limit=4"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            books = []
            for work in data.get('works', []):
                books.append({
                    'title': work.get('title', 'Sans titre'),
                    'author': work.get('authors', [{}])[0].get('name', 'Auteur inconnu'),
                    'url': f"https://openlibrary.org{work.get('key', '')}",
                    'cover': f"https://covers.openlibrary.org/b/id/{work.get('cover_id', '')}-M.jpg"
                             if work.get('cover_id') else None,
                })
            return books
    except requests.RequestException:
        pass
    return []


# ─────────────────────────────────────────
# 🏠 Pages générales
# ─────────────────────────────────────────

def home(request):
    courses = Course.objects.all()
    return render(request, 'polytechnicien/index.html', {'courses': courses})


def accueil(request):
    math     = Course.objects.filter(subject=Course.MATH).first()
    physique = Course.objects.filter(subject=Course.PHYS).first()
    langues  = Course.objects.filter(subject=Course.LANG).first()
    info     = Course.objects.filter(subject=Course.INFO).first()
    context  = {
        'math': math,
        'physique': physique,
        'langues': langues,
        'info': info,
    }
    return render(request, 'polytechnicien/accueil.html', context)


def a_propos(request):
    return render(request, 'polytechnicien/a_propos.html')


# ─────────────────────────────────────────
# 📚 Cours
# ─────────────────────────────────────────

def course_detail(request, course_id):
    course    = get_object_or_404(Course, id=course_id)
    resources = Resource.objects.filter(course=course)
    books     = get_books_from_api(course.subject)   # ← Open Library API
    context   = {
        'course':    course,
        'resources': resources,
        'books':     books,               # ← livres disponibles
    }
    return render(request, 'polytechnicien/course_detail.html', context)


def course_list(request):
    courses = Course.objects.all()
    return render(request, 'polytechnicien/course_list.html', {'courses': courses})


def add_course(request):
    if request.method == 'POST':
        form = AddCourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('course_list'))
    else:
        form = AddCourseForm()
    return render(request, 'polytechnicien/add_course.html', {'form': form})


def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = AddCourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = AddCourseForm(instance=course)
    return render(request, 'polytechnicien/edit_course.html', {'form': form, 'course': course})


def edit_course_page(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    form   = CourseForm(instance=course)
    return render(request, 'polytechnicien/edit_course.html', {'form': form, 'course': course})


def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        course.delete()
    return redirect(reverse('course_list'))


# ─────────────────────────────────────────
# 📁 Ressources
# ─────────────────────────────────────────

@login_required
def upload_resource(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            resource             = form.save(commit=False)
            resource.course      = course
            resource.uploaded_by = request.user
            resource.save()
            return redirect('course_detail', course_id=course.id)
    else:
        form = ResourceForm()
    return render(request, 'polytechnicien/upload_resource.html', {'form': form, 'course': course})


# ─────────────────────────────────────────
# 🎓 Réservation
# ─────────────────────────────────────────

@login_required
def reserve_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if not Reservation.objects.filter(user=request.user, course=course).exists():
        Reservation.objects.create(user=request.user, course=course)
    return redirect('course_detail', course_id=course.id)


def select_subject(request):
    subjects = Course.objects.values_list('subject', flat=True).distinct()
    return render(request, 'polytechnicien/select_subject.html', {'subjects': subjects})


def select_year(request, subject):
    years = Course.objects.filter(subject=subject).values_list('year', flat=True).distinct()
    return render(request, 'polytechnicien/select_year.html', {'subject': subject, 'years': years})


# ─────────────────────────────────────────
# 📊 Dashboard
# ─────────────────────────────────────────
@login_required
def dashboard_view(request):
    reservations = Reservation.objects.filter(user=request.user).select_related('course')

    subjects      = [Course.MATH, Course.PHYS, Course.LANG, Course.INFO]
    reserv_counts = [
        reservations.filter(course__subject=s).count()
        for s in subjects
    ]

    context = {
        'reservations': reservations,
        'total_cours':  reservations.count(),
        'chart_labels': json.dumps(['Mathématiques', 'Physique', 'Langues', 'Informatique']),
        'chart_data':   json.dumps(reserv_counts),
    }
    return render(request, 'polytechnicien/dashboard.html', context)

# ─────────────────────────────────────────
# 🔐 Auth
# ─────────────────────────────────────────

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'polytechnicien/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('accueil')


class CustomLoginView(LoginView):
    template_name              = 'polytechnicien/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return '/dashboard/'