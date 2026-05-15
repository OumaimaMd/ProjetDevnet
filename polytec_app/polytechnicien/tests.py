from django.test import TestCase, Client
from django.urls import reverse
from .models import Course, CustomUser, Reservation
import requests


# ─────────────────────────────────────────
# 🗃️ Tests des modèles
# ─────────────────────────────────────────

class CourseModelTest(TestCase):

    def setUp(self):
        self.course = Course.objects.create(
            subject=Course.MATH,
            year=1,
            title='Algèbre Linéaire',
            description='Cours de base en algèbre'
        )

    def test_course_creation(self):
        """Vérifier que le cours est bien créé"""
        self.assertEqual(self.course.title, 'Algèbre Linéaire')
        self.assertEqual(self.course.subject, Course.MATH)

    def test_course_str(self):
        """Vérifier la représentation string du cours"""
        self.assertIn('Algèbre Linéaire', str(self.course))


class UserModelTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='etudiant1',
            password='testpass123'
        )

    def test_user_creation(self):
        """Vérifier que l'utilisateur est bien créé"""
        self.assertEqual(self.user.username, 'etudiant1')

    def test_user_is_active(self):
        """Vérifier que l'utilisateur est actif"""
        self.assertTrue(self.user.is_active)


# ─────────────────────────────────────────
# 🌐 Tests des vues
# ─────────────────────────────────────────

class ViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.course = Course.objects.create(
            subject=Course.MATH,
            year=1,
            title='Test Cours',
            description='Description test'
        )

    def test_accueil_page(self):
        """Page accueil accessible"""
        response = self.client.get(reverse('accueil'))
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        """Page login accessible"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_course_list_page(self):
        """Page liste des cours accessible"""
        response = self.client.get(reverse('course_list'))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_requires_login(self):
        """Dashboard nécessite une connexion"""
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirige vers login

    def test_dashboard_accessible_when_logged_in(self):
        """Dashboard accessible quand connecté"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)


# ─────────────────────────────────────────
# 🔗 Tests connectivité API
# ─────────────────────────────────────────

class APIConnectivityTest(TestCase):

    def test_open_library_api_reachable(self):
        """Vérifier que Open Library API est accessible"""
        try:
            response = requests.get(
                'https://openlibrary.org/subjects/mathematics.json?limit=1',
                timeout=5
            )
            self.assertIn(response.status_code, [200, 301, 302])
        except requests.RequestException:
            self.skipTest("API non accessible depuis cet environnement")

    def test_open_library_returns_data(self):
        """Vérifier que l'API retourne des données"""
        try:
            response = requests.get(
                'https://openlibrary.org/subjects/mathematics.json?limit=1',
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                self.assertIn('works', data)
        except requests.RequestException:
            self.skipTest("API non accessible depuis cet environnement")


# ─────────────────────────────────────────
# 🎓 Tests des réservations
# ─────────────────────────────────────────

class ReservationTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='etudiant',
            password='pass123'
        )
        self.course = Course.objects.create(
            subject=Course.INFO,
            year=2,
            title='Python Avancé',
            description='Cours Python'
        )

    def test_reservation_creation(self):
        """Vérifier qu'une réservation est bien créée"""
        reservation = Reservation.objects.create(
            user=self.user,
            course=self.course
        )
        self.assertEqual(reservation.user, self.user)
        self.assertEqual(reservation.course, self.course)

    def test_unique_reservation(self):
        """Vérifier qu'un utilisateur ne peut pas réserver 2 fois"""
        Reservation.objects.create(user=self.user, course=self.course)
        with self.assertRaises(Exception):
            Reservation.objects.create(user=self.user, course=self.course)