# Visualisation 3D de Surface de Volatilité Implicite Synthétique

Ce script Python génère et affiche une surface 3D représentant une **volatilité implicite synthétique** en fonction du prix d'exercice (strike) et du temps jusqu'à l’échéance.

---

## Fonctionnalités

* Création d’une grille 2D de strikes (80 à 120) et maturités (0.1 à 2 ans).
* Simulation d’une surface de volatilité avec effets de smile, skew et structure à terme.
* Affichage en 3D avec `matplotlib`, incluant étiquettes et barre de couleur.

---

## Utilisation

1. Installer les dépendances :

```bash
pip install numpy matplotlib
```

2. Exécuter le script Python.

La visualisation s’ouvre automatiquement et montre la surface de volatilité implicite simulée.

---

## Description rapide

* La fonction `F(K, T, S0)` modélise la volatilité implicite en combinant un niveau ATM, un sourire, un skew et une décroissance avec la maturité.
* La surface est tracée en 3D avec `plot_surface` pour explorer l’impact simultané des strikes et des échéances.
