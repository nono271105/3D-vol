import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
import datetime

st.set_page_config(layout="wide", page_title="Surface de Volatilité 3D Avancée")

st.title("Surface de Volatilité Implicite 3D Avancée")

st.markdown("""
Visualisez et personnalisez votre surface de volatilité implicite.
""")

# --- Sidebar pour les options de personnalisation ---
st.sidebar.header("Options de Visualisation")
cmap_option = st.sidebar.selectbox("Palette de Couleurs",
                                   ['viridis', 'plasma', 'cividis', 'inferno', 'magma', 'coolwarm', 'RdYlGn', 'Blues', 'Greens'])
elev_angle = st.sidebar.slider("Angle d'Élévation", 0, 90, 30)
azim_angle = st.sidebar.slider("Angle d'Azimut", -180, 180, -60)
surface_alpha = st.sidebar.slider("Transparence de la Surface", 0.1, 1.0, 0.8)


# --- Choix de la source des données ---
st.header("1. Source des Données de Volatilité")
data_source = st.radio(
    "Comment souhaitez-vous obtenir les données de volatilité ?",
    ("Générer des données synthétiques", "Saisir des données manuellement", "Uploader un fichier CSV")
)

X_strikes, Y_maturities, Z_implied_vol = None, None, None
data_loaded = False

if data_source == "Générer des données synthétiques":
    st.subheader("Génération de Données Synthétiques")
    st.info("Définissez les paramètres pour simuler une surface de volatilité.")

    col_synth1, col_synth2 = st.columns(2)

    with col_synth1:
        st.markdown("**Paramètres de l'actif sous-jacent :**")
        S0_synth = st.number_input("Prix Spot Actuel (S0)", value=100.0, step=5.0)
        risk_free_rate = st.number_input("Taux sans Risque Annuel (r)", value=0.01, format="%.3f", min_value=0.0)

    with col_synth2:
        st.markdown("**Plages pour la Surface :**")
        min_strike = st.number_input("Strike Minimum", value=80.0, step=5.0)
        max_strike = st.number_input("Strike Maximum", value=120.0, step=5.0)
        num_strikes_synth = st.slider("Nombre de points pour les Strikes", 10, 100, 30)

        min_maturity_days = st.number_input("Maturité Minimum (jours)", value=30, min_value=1)
        max_maturity_days = st.number_input("Maturité Maximum (jours)", value=730, min_value=1)
        num_maturities_synth = st.slider("Nombre de points pour les Maturités", 10, 100, 25)

    st.markdown("**Paramètres de la forme de la surface :**")
    col_shape1, col_shape2, col_shape3 = st.columns(3)
    with col_shape1:
        vol_atm_base = st.number_input("Volatilité ATM de base", value=0.20, format="%.3f", min_value=0.01, max_value=1.0)
    with col_shape2:
        smile_coeff = st.number_input("Coefficient du Smile", value=0.5, format="%.2f", min_value=0.0, max_value=2.0)
    with col_shape3:
        skew_coeff = st.number_input("Coefficient du Skew (pente)", value=-0.15, format="%.2f", min_value=-1.0, max_value=1.0)
        term_structure_coeff = st.number_input("Coefficient de la Structure à Terme", value=-0.05, format="%.2f", min_value=-0.5, max_value=0.5)

    def generate_synthetic_volatility(K_grid, T_grid, S0_ref, r_rate, vol_base, smile_c, skew_c, term_c):
        # Utilisation de K_grid et T_grid qui sont déjà des maillages 2D
        # La formule est ajustée pour utiliser les paramètres saisis
        vol_atm = vol_base
        smile_effect = smile_c * ((K_grid / S0_ref) - 1)**2
        skew_effect = skew_c * ((K_grid / S0_ref) - 1)
        # Term structure effect basé sur sqrt(T) pour simuler un comportement typique
        # On normalise par une maturité de référence (ex: 1 an = 365 jours)
        term_structure_effect = term_c * (np.sqrt(T_grid) - np.sqrt(365/365)) # T_grid est déjà en années pour le calcul

        vol = vol_atm + smile_effect + skew_effect + term_structure_effect
        return np.maximum(vol, 0.01) # S'assurer que la volatilité reste positive

    if st.button("Générer la surface synthétique"):
        strikes_synth_1d = np.linspace(min_strike, max_strike, num_strikes_synth)
        maturities_synth_1d = np.linspace(min_maturity_days / 365.25, max_maturity_days / 365.25, num_maturities_synth) # Convertir en années
        X_strikes, Y_maturities = np.meshgrid(strikes_synth_1d, maturities_synth_1d)
        Z_implied_vol = generate_synthetic_volatility(X_strikes, Y_maturities, S0_synth, risk_free_rate, vol_atm_base, smile_coeff, skew_coeff, term_structure_coeff)
        data_loaded = True

elif data_source == "Saisir des données manuellement":
    st.subheader("Saisie Manuelle des Données")
    st.warning("Veuillez saisir vos données sous forme de listes séparées par des virgules.")
    st.markdown("**Exemple de format :**")
    st.code("""
    Strikes: 90, 100, 110
    Maturities: 0.25, 0.5, 1.0
    Volatilities:
    0.25, 0.20, 0.28,
    0.23, 0.18, 0.26,
    0.22, 0.17, 0.25
    """)

    strikes_input = st.text_area("Entrez les Prix d'Exercice (Strikes, K) :", "90, 95, 100, 105, 110")
    maturities_input = st.text_area("Entrez les Temps jusqu'à l'Échéance (T, en années) :", "0.25, 0.5, 1.0, 1.5")
    volatilities_input = st.text_area("Entrez les Volatilités Implicites (Z) :",
                                      "0.25, 0.23, 0.20, 0.22, 0.26,\n"
                                      "0.23, 0.21, 0.19, 0.21, 0.24,\n"
                                      "0.22, 0.20, 0.18, 0.20, 0.23,\n"
                                      "0.21, 0.19, 0.17, 0.19, 0.22")

    if st.button("Charger les données manuelles"):
        try:
            strikes = np.array([float(x.strip()) for x in strikes_input.split(',') if x.strip()])
            maturities = np.array([float(x.strip()) for x in maturities_input.split(',') if x.strip()])
            volatilities_flat = np.array([float(x.strip()) for x in volatilities_input.replace('\n', ',').split(',') if x.strip()])

            if len(volatilities_flat) != len(strikes) * len(maturities):
                st.error(f"Le nombre de volatilités ({len(volatilities_flat)}) ne correspond pas à (nombre de strikes x nombre de maturités) "
                         f"({len(strikes)} x {len(maturities)} = {len(strikes) * len(maturities)}). "
                         f"Veuillez vérifier vos entrées.")
            else:
                Z_implied_vol = volatilities_flat.reshape(len(maturities), len(strikes))
                X_strikes, Y_maturities = np.meshgrid(strikes, maturities)
                data_loaded = True
                st.success("Données manuelles chargées avec succès !")
        except Exception as e:
            st.error(f"Erreur lors du chargement des données manuelles : {e}. Assurez-vous que les formats sont corrects.")

elif data_source == "Uploader un fichier CSV":
    st.subheader("Uploader un Fichier CSV")
    st.info("Le fichier CSV doit contenir au moins trois colonnes : 'Strike', 'Maturity', 'Vol'.")
    st.markdown("**Exemple de format CSV :**")
    st.code("""
    Strike,Maturity,Vol
    90,0.25,0.25
    100,0.25,0.20
    110,0.25,0.28
    90,0.5,0.23
    100,0.5,0.18
    110,0.5,0.26
    """)

    uploaded_file = st.file_uploader("Choisissez un fichier CSV", type="csv")

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.dataframe(df.head()) # Afficher les premières lignes pour vérification

            # Vérifier les colonnes nécessaires
            required_cols = ['Strike', 'Maturity', 'Vol']
            if not all(col in df.columns for col in required_cols):
                st.error(f"Le fichier CSV doit contenir les colonnes : {', '.join(required_cols)}")
            else:
                # Convertir les maturités en années si elles sont en jours (supposition commune)
                # On pourrait ajouter une option pour spécifier l'unité de maturité
                # Pour l'exemple, on suppose que 'Maturity' est déjà en années ou peut être converti si besoin
                
                # Assurez-vous que les données sont triées pour un maillage correct
                df = df.sort_values(by=['Maturity', 'Strike'])

                strikes_unique = df['Strike'].unique()
                maturities_unique = df['Maturity'].unique()

                # Créer une grille vide pour la volatilité
                Z_temp = np.full((len(maturities_unique), len(strikes_unique)), np.nan)

                # Remplir la grille
                for i, mat in enumerate(maturities_unique):
                    for j, strike in enumerate(strikes_unique):
                        vol_val = df[(df['Maturity'] == mat) & (df['Strike'] == strike)]['Vol']
                        if not vol_val.empty:
                            Z_temp[i, j] = vol_val.iloc[0]

                # Gérer les NaNs si le dataset n'est pas une grille parfaite
                if np.isnan(Z_temp).any():
                    st.warning("Certaines combinaisons Strike/Maturity sont manquantes. La surface pourrait être incomplète.")
                    # Vous pouvez choisir d'interpoler ou de laisser les NaNs pour matplotlib (qui les ignorera)
                    # Pour un affichage surf, il est souvent préférable d'avoir une grille complète.
                    # Une interpolation simple peut être ajoutée ici si nécessaire (ex: Z_temp = pd.DataFrame(Z_temp).interpolate(method='linear').values)

                X_strikes, Y_maturities = np.meshgrid(strikes_unique, maturities_unique)
                Z_implied_vol = Z_temp
                data_loaded = True
                st.success("Fichier CSV chargé avec succès !")

        except Exception as e:
            st.error(f"Erreur lors du traitement du fichier CSV : {e}. Assurez-vous du format et du contenu.")

st.markdown("---")
st.header("2. Visualisation de la Surface de Volatilité")

if data_loaded and X_strikes is not None and Y_maturities is not None and Z_implied_vol is not None:
    try:
        fig = plt.figure(figsize=(12, 9))
        ax = fig.add_subplot(111, projection='3d')

        # Utilisation des paramètres de visualisation de la sidebar
        surf = ax.plot_surface(X_strikes, Y_maturities, Z_implied_vol,
                               cmap=cmap_option,
                               edgecolor='none',
                               alpha=surface_alpha)

        ax.set_xlabel("Prix d'Exercice (K)")
        ax.set_ylabel("Temps jusqu'à l'Échéance (T, en années)")
        ax.set_zlabel("Volatilité Implicite ($\sigma$)")
        ax.set_title("Surface de Volatilité Implicite")

        fig.colorbar(surf, shrink=0.5, aspect=5, label="Volatilité Implicite")

        # Utilisation des angles de la sidebar
        ax.view_init(elev=elev_angle, azim=azim_angle)

        st.pyplot(fig)
    except Exception as e:
        st.error(f"Erreur lors de la création du graphique : {e}. Vérifiez que vos données forment une grille cohérente.")
else:
    st.info("Veuillez choisir une source de données et charger/générer la surface pour afficher la visualisation.")

st.markdown("---")
st.markdown("N'hésitez pas à me faire part de suggestions.")
