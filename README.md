# 📈 Volatilité 3D - Surface de Volatilité Implicite

Une application Streamlit interactive pour visualiser et personnaliser une **surface de volatilité implicite** en 3D.
Elle permet de **générer, charger ou saisir** manuellement les données, et d'explorer dynamiquement l'effet du smile, du skew et de la structure à terme.

🔗 **Application en ligne** : [https://volatility-3d.streamlit.app/](https://volatility-3d.streamlit.app/)

---

## 🚀 Fonctionnalités principales

* 📊 **Visualisation interactive 3D** de la surface de volatilité implicite.
* 🧪 **Génération synthétique** de surfaces personnalisées (Smile, Skew, Term Structure).
* ✍️ **Saisie manuelle** des données de strikes, maturités et volatilités.
* 📁 **Chargement de fichiers CSV** contenant vos propres données de volatilité.
* 🎨 **Personnalisation graphique** :

  * Palette de couleurs
  * Angle de vue (élévation, azimut)
  * Transparence de la surface

---

## 📂 Structure attendue pour les fichiers CSV

Votre fichier doit contenir **au moins trois colonnes** :
`Strike`, `Maturity` (en années), `Vol` (volatilité implicite)

Exemple :

```
Strike,Maturity,Vol
90,0.25,0.25
100,0.25,0.20
110,0.25,0.28
...
```

---

## ⚙️ Lancer l’application en local

1. Clonez le dépôt :

   ```bash
   git clone <votre_repo_git>
   cd votre_repo
   ```

2. Installez les dépendances :

   ```bash
   pip install streamlit numpy matplotlib pandas
   ```

3. Lancez l'application :

   ```bash
   streamlit run app.py
   ```

---

## 📌 Dépendances

* `streamlit`
* `numpy`
* `matplotlib`
* `pandas`
