# Real-time Data Pipeline with Kafka, Spark, BigQuery, and Docker

## 📖 Introduction

Ce projet vise à construire un pipeline de données en temps réel, combinant des données issues de différentes API (Kraken et OpenMétéo). Les données sont traitées et analysées via une chaîne d'outils modernes pour un stockage et une visualisation efficaces, en utilisant : **FastAPI**, **Kafka**, **Apache Spark**, **BigQuery**, **Apache Airflow** et **Docker**. 

> 🚧 Note : Le README sera mis à jour continuellement en fonction de l'avancement du projet pour mon apprentissage.

Le pipeline est conçu pour être :
- 🔬 Modulaire
- 🚀 Extensible 
- 🌐 Entièrement déployable

Objectif de déploiement sur des plateformes gratuites comme **Render**, **Heroku**, et **Astronomer** pour **Airflow**.

---

## 🏗️ Architecture

Le pipeline suit ces étapes précises :
1. **Ingestion des données** via les APIs Kraken et OpenMétéo
2. **Récupération primaire** avec FastAPI
3. **Streaming des données** via Kafka 
4. **Traitement en temps réel** avec Apache Spark
5. **Stockage final** dans BigQuery
6. **Visualisation** (à définir)

### 📊 Schéma d'architecture
```
[Données à venir]
```

---

## 🛠️ Technologies utilisées

### APIs Sources
- Kraken
- OpenMétéo

### Infrastructure de Données
- **FastAPI** : Ingestion des données
- **Apache Kafka** : Streaming 
- **Apache Spark** : Traitement temps réel
- **BigQuery** : Stockage et analyse
- **Docker** : Conteneurisation
- **Apache Airflow** : Orchestration (futur)

---

## 🔧 Prérequis Techniques

- **Docker et Docker Compose** (pour tests locaux)
- **Python 3.9+**

### Comptes Nécessaires
- Google Cloud Platform
- Compte API Kraken
- (Visualisation : à définir)

---

## 🚀 Installation Rapide

### Clonage du Projet
```bash
git clone https://votre-repository/data-pipeline-project.git
cd data-pipeline-project
```

### Configuration de l'Environnement
Créez un fichier `.env` :
```bash
URL_WEATHER=https://api.open-meteo.com/v1/forecast
URL_CRYPTO=https://api.kraken.com/0/public/Depth
TEST_ROOT_APP=Bienvenue dans le service de collecte de données météo et crypto-monnaie
```

---

## 🔍 Fonctionnalités Principales

- 📥 Récupération multi-sources via APIs 
- 🔄 Streaming temps réel
- 🔬 Transformation avec Spark
- 💾 Stockage BigQuery
- 🛠️ Orchestration flexible

---

## 🤝 Contribution

1. Forker le projet
2. Créer une branche de fonctionnalité
3. Commiter les modifications
4. Ouvrir une Pull Request

---

## 📄 Licence

Libre (Open Source)

---

## 📧 Contact

georgesanogbre06@gmail.com
