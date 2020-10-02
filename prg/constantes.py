import os

DIR_INTERFACE       = os.path.dirname(os.path.dirname(__file__))
DIR_PROD            = "C:\\PROD"
DIR_VAR             = "P:\\Var"
PYAUTOMATE          = "C:\\PYTHON38\\python.exe"
DIR_AUTOMATE_NH     = os.path.join(DIR_PROD, "Nievre_habitat", "_automate")
DIR_AUTOMATE_ENV    = os.path.join(DIR_PROD, "Enveloppes", "_automate")
DIR_AUTOMATE_ENV_PRG= os.path.join(DIR_AUTOMATE_ENV, "_prg")
FIC_ADR_EXPE        = os.path.join(DIR_AUTOMATE_ENV_PRG, "AdrExpe.txt")
FIC_DATA_MIF        = os.path.join(DIR_INTERFACE, "data", "Mif", "data.json")
FIC_DATA_QUITTANCES = os.path.join(DIR_INTERFACE, "data", "Quittances", "data.json")
FIC_DATA_SLS        = os.path.join(DIR_INTERFACE, "data", "Sls", "data.json")
CONFIG_PNT          = "P:\\Var\\_CommunPNT\\SevenForceCMYK-2018.job"
MOTEUR_PNT          = chr(34) + "C:\\Program Files\\Quadient\\Inspire Designer 12.0\\InspireCLI.exe"+ chr(34) 
LISTE_INDEX         = [
                "entete",
                "client",
                "no_bt",
                "ope",
                "idope",
                "env",
                "imp_fenetre",
                "affra",
                "imp_affra",
                "date_timbre",
                "imp_date_timbre",
                "adr_expe",
                "ligne0",
                "etiquette",
                "lettre",
                "nb_page",
                "rv",
                "logo",
                "alliage",
                "alliage_c3",
                "rep_alliage",
                "retour_transat",
                "data_input",
                "fic_adr_expe_perso",
                "maquette",
                "config_pnt",
                "moteur"
]
TYPES_FICHERS       = [
                ".csv",
                ".CSV",
                ".txt",
                ".TXT",
                ".xlsx",
                ".XLSX",
                ".xls",
                ".XLS"
]
# Lanceurs
LINDAB               = os.path.join(DIR_PROD, "Lindab", "_automate", "lindab.py")
NHAVISECHEANCES      = os.path.join(DIR_AUTOMATE_NH, "NH-QUITTANCES", "nh_quittances.py")
NHAVISRELANCES       = os.path.join(DIR_AUTOMATE_NH, "NH-RELANCES", "NHAvisRelances.py")
NHREGULARISATIONS    = os.path.join(DIR_AUTOMATE_NH, "NH-REGULARISATIONS", "REG01-LanceRegularisations.bat")
NHSLS                = os.path.join(DIR_AUTOMATE_NH, "NH-SLS", "nh_sls.py")
MIF                  = os.path.join(DIR_PROD, "Mif", "_automate", "mif.py")
P2R                  = os.path.join(DIR_PROD, "P2r", "_automate", "p2r.py")
ENVELOPPES           = os.path.join(DIR_AUTOMATE_ENV, "enveloppes.py")