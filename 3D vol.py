import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D # Nécessaire pour la projection 3D

# --- 1. Définition des paramètres pour la grille ---
# Plage des prix d'exercice (Strikes, K)
# Supposons un prix spot S0 = 100. On regarde les strikes de 80 à 120.
S0 = 100
strikes = np.linspace(80, 120, 25)  # 25 points pour les strikes

# Plage des temps jusqu'à l'échéance (Maturities, T) en années
maturities = np.linspace(0.1, 2.0, 20) # 20 points pour les échéances (de ~1 mois à 2 ans)

# Création d'une grille 2D pour les strikes et les maturités
# X contiendra les strikes répétés pour chaque maturité
# Y contiendra les maturités répétées pour chaque strike
X_strikes, Y_maturities = np.meshgrid(strikes, maturities)

# --- 2. Génération de données de volatilité implicite synthétiques (Z) ---
# C'est ici que vous utiliseriez vos données réelles si vous en aviez.
# Pour cet exemple, créons une fonction qui simule une surface de volatilité.
# Une surface typique pourrait avoir :
# - un "sourire" (volatilité plus élevée pour les strikes OTM et ITM)
# - une structure à terme (par exemple, volatilité décroissante avec la maturité lointaine)

def F(K, T, S0):
    vol_atm = 0.20  # Volatilité à la monnaie pour une échéance de référence
    # Effet du sourire (parabolique en K/S0)
    smile_effect = 0.5 * ((K / S0) - 1)**2
    # Effet de la pente (skew)
    skew_effect = -0.15 * ((K / S0) - 1)
    # Effet de la structure à terme (par exemple, décroissante avec sqrt(T))
    term_structure_effect = -0.05 * (np.sqrt(T) - np.sqrt(1.0)) # Décroît pour T > 1 an, croît pour T < 1 an

    vol = vol_atm + smile_effect + skew_effect + term_structure_effect
    # S'assurer que la volatilité ne devienne pas négative ou trop petite
    return np.maximum(vol, 0.05)

Z_implied_vol = F(X_strikes, Y_maturities, S0)

# --- 3. Création du graphique 3D ---
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# Tracer la surface
# cmap définit la palette de couleurs (par exemple, 'viridis', 'plasma', 'coolwarm')
surf = ax.plot_surface(X_strikes, Y_maturities, Z_implied_vol, cmap='viridis', edgecolor='none')

# Ajout des étiquettes et du titre
ax.set_xlabel("Prix d'Exercice (K)")
ax.set_ylabel("Temps jusqu'à l'Échéance (T, en années)")
ax.set_zlabel("Volatilité Implicite ($\sigma$)")
ax.set_title("Surface de Volatilité Implicite (Synthétique)")

# Ajout d'une barre de couleur pour la légende des valeurs Z
fig.colorbar(surf, shrink=0.5, aspect=5, label="Volatilité Implicite")

# Ajuster l'angle de vue (optionnel)
ax.view_init(elev=30, azim=-60) # Élévation de 30 degrés, azimut de -60 degrés

plt.tight_layout()
plt.show()