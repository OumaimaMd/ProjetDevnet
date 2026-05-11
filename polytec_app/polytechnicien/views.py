from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Course, CourseForm, Resource
from .forms import AddCourseForm, ResourceForm, CommentForm, RegisterForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Course, Reservation
from .forms import CustomUserCreationForm, ResourceForm, CommentForm
from django.views.generic import TemplateView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LoginView

def home(request):
    courses = Course.objects.all()
    return render(request, 'polytechnicien/index.html', {'courses': courses})


def reserve_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    # Vérifier si l'utilisateur a déjà réservé ce cours
    if Reservation.objects.filter(user=request.user, course=course).exists():
        return redirect('course_detail', course_id=course.id)  # Redirige vers la page du cours
    
    # Créer une nouvelle réservation pour l'utilisateur
    Reservation.objects.create(user=request.user, course=course)
    
    # Rediriger l'utilisateur vers la page du cours avec un message de succès
    return redirect('course_detail', course_id=course.id) 




def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Rediriger après enregistrement
    else:
        form = CustomUserCreationForm()

    return render(request, 'polytechnicien/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirection vers le dashboard
        else:
            # Retourner une erreur si l'authentification échoue
            return render(request, 'polytechnicien/login.html', {'error': 'Email ou mot de passe incorrect'})
    
    return render(request, 'polytechnicien/login.html')

def logout_view(request):
    logout(request)
    return redirect('accueil')


from django.shortcuts import render

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    resources = Resource.objects.filter(course=course)  # Récupère les ressources liées à ce cours
    context = {
        'course': course,
        'resources': resources,  # Passe la liste des ressources au template
    }
    return render(request, 'polytechnicien/course_detail.html', context)


@login_required
def upload_resource(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.course = course
            resource.uploaded_by = request.user
            resource.save()
            return redirect('course_detail', course_id=course.id)
    else:
        form = ResourceForm()
    return render(request, 'polytechnicien/upload_resource.html', {'form': form, 'course': course})
def accueil(request):
    math = Course.objects.filter(title__icontains="math").first()
    physique = Course.objects.filter(title__icontains="physique").first()
    langues = Course.objects.filter(title__icontains="langue").first()
    info = Course.objects.filter(title__icontains="info").first()

    context = {
        'math': math,
        'physique': physique,
        'langues': langues,
        'info': info,
    }
    return render(request, 'polytechnicien/accueil.html', context)



################
"""def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Exemple de données de progression (à remplacer par vos données réelles)
    progress_data = {
        'math': 75,
        'physique': 60,
        'langues': 85,
        'informatique': 45
    }
    
    return render(request, 'dashboard.html', {'progress_data': progress_data})

"""
#############
"""def dashboard(request):
    progress_data = {...}  # tes données

    math = Course.objects.filter(subject="Mathématiques").first()
    physique = Course.objects.filter(subject="Physique").first()
    langues = Course.objects.filter(subject="Langues").first()
    info = Course.objects.filter(subject="Informatique").first()

    context = {
        "user": request.user,
        "progress_data": progress_data,
        "math": math,
        "physique": physique,
        "langues": langues,
        "info": info,
    }

    return render(request, "polytechnicien/dashboard.html", context)"""
@login_required
def dashboard_view(request):
    math_course = Course.objects.filter(subject=Course.MATH).first()
    physique_course = Course.objects.filter(subject=Course.PHYS).first()
    langues_course = Course.objects.filter(subject=Course.LANG).first()
    info_course = Course.objects.filter(subject=Course.INFO).first()

    context = {
        'progress_data': { ... },
        'math': math_course,
        'physique': physique_course,
        'langues': langues_course,
        'info': info_course,
    }
    return render(request, 'polytechnicien/dashboard.html', context)



def custom_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Remplace 'dashboard' par l'URL de ton tableau de bord
        else:
            error = "Nom d'utilisateur ou mot de passe incorrect."
            return render(request, 'polytechnicien/login.html', {'error': error})
    return render(request, 'polytechnicien/login.html')

@login_required
def dashboard_view(request):
    # Ajoutez ici la logique pour récupérer les données du dashboard
    return render(request, 'polytechnicien/dashboard.html')

class DashboardView(TemplateView):
    template_name = 'polytechnicien/dashboard.html'


def a_propos(request):
    return render(request, 'polytechnicien/a_propos.html')

class CustomLoginView(LoginView):
    template_name = 'polytechnicien/login.html' 
    redirect_authenticated_user = True  # utile si l'utilisateur est déjà connecté
    success_url = reverse_lazy('dashboard') 
    def get_success_url(self):
        # Redirige vers la page 'dashboard' après une connexion réussie
        return '/dashboard/'
    def form_valid(self, form):
        # Si tu veux rediriger l'utilisateur vers un autre endroit après la connexion
        return super().form_valid(form)


# Affiche les matières disponibles
def select_subject(request):
    subjects = Course.objects.values_list('subject', flat=True).distinct()
    return render(request, 'polytechnicien/select_subject.html', {'subjects': subjects})

# Affiche les années disponibles pour une matière
def select_year(request, subject):
    years = Course.objects.filter(subject=subject).values_list('year', flat=True).distinct()
    return render(request, 'polytechnicien/select_year.html', {'subject': subject, 'years': years})

# Affiche les cours pour une matière et une année
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
        form = AddCourseForm(request.POST, instance=course)  # Remplir le formulaire avec les données existantes
        if form.is_valid():
            form.save()
            return redirect('course_list')  # Rediriger vers la liste des cours
    else:
        form = AddCourseForm(instance=course)  # Afficher le formulaire avec les données existantes
    return render(request, 'polytechnicien/edit_course.html', {'form': form, 'course': course})

def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        course.delete()
        return redirect(reverse('course_list'))  # Rediriger vers la liste des cours
    else:
        # Si quelqu'un essaie d'accéder à l'URL de suppression via GET,
        # vous pouvez afficher une page de confirmation ou rediriger.
        return redirect(reverse('course_list'))
def edit_course_page(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    form = CourseForm(instance=course)
    return render(request, 'polytechnicien/edit_course.html', {'form': form, 'course': course})