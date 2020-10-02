# -*- coding: UTF-8 -*-
import os
import sys
import shutil

from glob import glob
from datetime import datetime

import prg.constantes as const

MAQUETTE = "EnvKUB-K7-V3-1.wfd"

def ecriture_params(params_form):
    client = params_form["client"]
    no_bt = params_form["no_bt"]
    rep_travail = recup_rep_travail_autre(client, no_bt)[0]
    fic_adr_expe_perso = os.path.join(rep_travail, "AdrExpe.txt") 
    fic_backup_env = os.path.join(rep_travail, "BackupEnv.txt")
    with open(fic_backup_env, "w") as f:
        f.writelines("Parametres:\n")
        i = 0  
        for param in params_form:
            if param == "date_timbre":
                date_timbre = datetime.strptime(params_form[param], "%Y-%m-%d").strftime("%d-%m-%Y")
                f.writelines(date_timbre + "\n")
            else:
                f.writelines(params_form[param] + "\n")            
            i += 1 
        f.writelines(fic_adr_expe_perso + "\n")           
        f.writelines(MAQUETTE + "\n")
        f.writelines(const.CONFIG_PNT + "\n")
        f.writelines(const.MOTEUR_PNT + "\n")

def dir_traitfichier(rep_travail): 
    data_input      = []
    retour_transat  = []
    fichiers        = []
    final           = False
    if rep_travail: 
        dir_traitfichier = os.path.join(rep_travail, "TraitFichier")
        if os.path.exists(dir_traitfichier):
            liste_fichiers = glob(f"{dir_traitfichier}/*")
            for fichier in liste_fichiers:
                if not os.path.isdir(fichier):
                    if (fichier.endswith("_brut.csv") or fichier.endswith("_FINAL.csv")):
                        if fichier.endswith("_FINAL.csv"):
                            final = True
                        data_input.append(os.path.basename(fichier)) 
                    elif (fichier.endswith("_RTE.CSV") or fichier.endswith("_ODS.CSV")):
                        retour_transat.append(os.path.basename(fichier))
        else:
            liste_fichiers = glob(f"{rep_travail}/*")
            for fichier in liste_fichiers:
                if not os.path.isdir(fichier):
                    extension = os.path.splitext(fichier)[1]
                    if extension in const.TYPES_FICHERS:
                        fichiers.append(os.path.basename(fichier))
    return (data_input, retour_transat, fichiers, final)

def lecture_param(rep_travail, index):
    # Etape Récupération des parametres dans BackupEnv.txt
    fic_backup = os.path.join(rep_travail, "BackupEnv.txt")
    fic_adr_expe = os.path.join(rep_travail, "AdrExpe.txt")
    param = ""
    if index == "adr_retour":
        if os.path.exists(fic_adr_expe):
            with open(fic_adr_expe, "r") as f:
                param = f.read()
    elif os.path.exists(fic_backup):
        with open(fic_backup, "r") as f:
            params = f.readlines()
            params = [param[:-1] for param in params]
        liste_params = dict(zip(const.LISTE_INDEX,params))
        param = liste_params[index]
        if index == "date_timbre":
            param = datetime.strptime(liste_params[index], "%d-%m-%Y").strftime("%Y-%m-%d")
    return param

def liste_affras_K7():
    affras_K7 = [
                "LGC",
                "EGC",
                "DIK7",
                "DEL",
                "DKDO",
                "DP",
                "EE",
                "EN",
                "LP",
                "LPE",
                "LN",
                "LV",
                "LG2",
                "ECOPLI",
                "DESTINEO",
                "DITRIMAG"
    ]
    return affras_K7
    
def liste_affras_KUB():
    affras_KUB = [
                "DIK-MD4",
                "DIK-MD7",
                "DIK-S",
                "DKDOP",
                "CAT7",
                "CAT7-S",
                "VIDE"
    ]
    return affras_KUB
    
def p_var(): 
    # Etape 2 : Récupération de la liste des clients sur P\VAR
    listes_var = glob(f"{const.DIR_VAR}/*")
    clients = [os.path.basename(liste_var) for liste_var in listes_var]
    return clients 

def recup_rep_travail_autre(client, no_bt): 
    # Etape 3 : Détermination du répertoire de travail
    traitfichier = False
    final        = False	
    rep_client   = os.path.join(const.DIR_VAR, client)
    clients      = glob(f"{rep_client}/*")
    for client in clients:
        if client.find(no_bt) > 0:
            rep_travail = client
    dossier    = os.path.basename(rep_travail)                      
    ope        = "-".join(dossier.split("-")[1:])   
    backup_env = False
    if os.path.exists(os.path.join(rep_travail, "AdrExpe.txt")):
        backup_env = True
    rep_traitfichier = os.path.join(rep_travail, "TraitFichier")
    final            = dir_traitfichier(rep_travail)[3]
    if os.path.exists(rep_traitfichier):
        traitfichier = True
    return (rep_travail, ope, backup_env, traitfichier, final)

def save_adr_retour(rep, params):
    with open(const.FIC_ADR_EXPE, "w") as f:
        params = params.translate({ord(c): None for c in "\r"}) # pour supprimer les sauts de ligne
        f.write(params)

if __name__ == "__main__":
    rep_travail, ope, backup_env, traitfichier, final = recup_rep_travail_autre("SOGEC", 'SEVEN2020090701')
    print(rep_travail, ope, backup_env, traitfichier, final)
    print(dir_traitfichier("P:\\Var\\SOGEC\\SEVEN2020090701-Test"))