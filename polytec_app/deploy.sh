#!/bin/bash

# Script de déploiement automatique
# EduTrack — Plateforme de cours en ligne



echo "║   Déploiement de EduTrack       ║"


# Étape 1 : Arrêter les anciens conteneurs 
echo ""
echo "[1/5] Arrêt des anciens conteneurs..."
docker compose down
if [ $? -ne 0 ]; then
    echo "Erreur lors de l'arrêt des conteneurs."
    exit 1
fi
echo "Conteneurs arrêtés."

#  Étape 2 : Construire les images 
echo ""
echo "[2/5] Construction des images Docker..."
docker compose build
if [ $? -ne 0 ]; then
    echo "Erreur lors de la construction des images."
    exit 1
fi
echo "Images construites."

#  Étape 3 : Lancer les conteneurs 
echo ""
echo "[3/5] Lancement des conteneurs..."
docker compose up -d
if [ $? -ne 0 ]; then
    echo "Erreur lors du lancement des conteneurs."
    exit 1
fi
echo "Conteneurs lancés."

#Étape 4 : Attendre que PostgreSQL soit prêt
echo ""
echo "[4/5] Attente de PostgreSQL..."
sleep 8
echo "PostgreSQL prêt."

#Étape 5 : Migrations Django
echo ""
echo "[5/5] Migration de la base de données..."
docker compose exec web python manage.py migrate
if [ $? -ne 0 ]; then
    echo "Erreur lors de la migration."
    exit 1
fi
echo "Migration terminée."

#Collecte des fichiers statiques 
echo ""
echo "Collecte des fichiers statiques..."
docker compose exec web python manage.py collectstatic --noinput
echo "Fichiers statiques collectés."

# Résumé final

echo "║   Déploiement réussi !           ║"
echo "║   http://localhost:8000          ║"
