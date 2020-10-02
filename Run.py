import shutil

from flask import Flask
from flask import request, render_template, url_for, redirect
from datetime import datetime
from glob import glob

import prg.constantes as c

from prg.fonctions import p_var, recup_rep_travail_autre, dir_traitfichier
from prg.fonctions import lecture_param, ecriture_params, save_adr_retour
from prg.fonctions import read_datas, lance_application

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("pages/index.html")

@app.route("/<lanceur>", methods=['POST', 'GET'])
def lanceur(lanceur):
    if request.method == "POST":
        if lanceur == "Lindab":			
            date_traitement = request.form["lindab"]
            lance_application(lanceur=lanceur, date_traitement=date_traitement)
            return render_template("pages/prise_en_compte.html")
        elif lanceur == "Mif":         
            date_timbre = request.form['mif']
            lance_application(lanceur=lanceur, date_timbre=date_timbre)
            if read_datas(c.FIC_DATA_MIF)["lotissement"] == "non":
                return redirect(url_for("lanceur", lanceur="Mif_lotissement"))
            return render_template("pages/prise_en_compte.html")    
        elif lanceur == "Mif_lotissement":
            lance_application(lanceur="Mif")
            if read_datas(c.FIC_DATA_MIF)["lotissement"] == "non":
                return redirect(url_for("lanceur", lanceur="Mif_lotissement"))
            return render_template("pages/prise_en_compte.html")
        elif lanceur == "P2r": 
            lance_application(lanceur=lanceur)
            return render_template("pages/prise_en_compte.html")
        elif lanceur == "Quittances":
            if not request.form:	
                lance_application(lanceur=lanceur)
                datas = read_datas(c.FIC_DATA_QUITTANCES)
                if datas["annexe"] == "True":
                    return render_template("pages/quittance_form_annexe.html")	
                return render_template("pages/prise_en_compte.html")
            elif request.form["type_imp"]:
                lance_application(lanceur=lanceur, datas=dict(request.form))
                return render_template("pages/prise_en_compte.html")
        elif lanceur == "Relance": 
            lance_application(lanceur=lanceur)
            return render_template("pages/prise_en_compte.html")	
        elif lanceur == "Sls":
            lance_application(lanceur=lanceur, date_timbre=request.form["sls"])
            if read_datas(c.FIC_DATA_SLS)["correction"] == "oui":
                return redirect(url_for("lanceur", lanceur="Sls_correction"))
            return render_template("pages/prise_en_compte.html")    
        elif lanceur == "Sls_correction":
            lance_application(lanceur="Sls")
            if read_datas(c.FIC_DATA_SLS)["correction"] == "oui":
                return redirect(url_for("lanceur", lanceur="Sls_correction"))
            return render_template("pages/prise_en_compte.html")        
    elif lanceur == "Enveloppes":
        return redirect(url_for("enveloppes_client"))
    return render_template("pages/lanceur.html", lanceur=lanceur)

@app.route("/Enveloppes_client", methods=['POST', 'GET'])
@app.route("/Enveloppes_client/<client>/<bt>/<final>", methods=['POST', 'GET'])
@app.route("/Enveloppes_client/<rep>/<client>/<bt>/<traitfichier>", methods=['POST', 'GET'])
@app.route("/Enveloppes_client/<lanceur>/<rep>/<client>/<bt>/<traitfichier>", methods=['POST', 'GET'])
def enveloppes_client(rep=None,client=None,bt=None,traitfichier=None,final=None,lotissement=None):
    if request.method == "POST":
        print(request.form)
        if "debut" in request.form:
            client = request.form["client"]
            no_bt = request.form["bt"]
            debut = request.form["debut"]
            rep_travail, ope, backup_env, traitfichier, final = recup_rep_travail_autre(client=client, no_bt=no_bt)
            if not traitfichier:
                if debut == "False": #Recupération donnée pour Traific
                    return redirect(url_for("enveloppes_client", rep=rep_travail, client=client, bt=no_bt, traitfichier=True))
                elif debut == "True": #Lance Traific 
                    fic_traific = request.form["traific"]
                    lance_application(lanceur="Enveloppes", rep=rep, fichier=fic_traific)
                    return render_template("pages/enveloppes_lotissement.html", client=client, bt=bt, final=final)                
            else: # Si Traitfichier existe
                if not backup_env and debut == "False": #Vérifie backup_env
                    return redirect(url_for("enveloppes_params", client=client, no_bt=no_bt, ope=ope, rep=rep_travail))
                elif backup_env and final: #Présence fichier FINAL
                    return redirect(url_for("enveloppes_recup", rep=rep_travail))
                elif not final:
                    return render_template("pages/enveloppes_lotissement.html", client=client, bt=no_bt, lotissment=True)
    elif traitfichier:
        return render_template("pages/enveloppes_client.html", rep=rep, client=client, bt=bt, traitfichier=traitfichier)
    return render_template("pages/enveloppes_client.html")

@app.route("/Enveloppes_params", methods=['POST', 'GET'])
@app.route("/Enveloppes_params/<client>/<no_bt>/<ope>/<rep>", methods=['POST', 'GET'])
def enveloppes_params(client=None, no_bt=None, ope=None, rep=None):
    if request.method == "POST":
        ecriture_params(request.form) # Création fichier BackupEnv.txt dans rep_travail
        if request.form["adr_expe"] == "PERSO":
            return redirect(url_for("enveloppes_adr_expe", rep=rep, adr_retour=None))
        lance_application(lanceur="Enveloppes", rep=rep)        
        return render_template("pages/prise_en_compte.html")
    if rep and client and ope and no_bt:
        return render_template("pages/enveloppes_params.html", client=client, no_bt=no_bt, ope=ope, rep=rep)
    return render_template("pages/enveloppes_params.html", client=client, no_bt=no_bt, ope=ope,  rep="")

@app.route("/Enveloppes_recup", methods=['POST', 'GET'])
@app.route("/Enveloppes_recup/<rep>", methods=['POST', 'GET'])
def enveloppes_recup(rep=None):
    if request.method == "POST":
        ecriture_params(request.form) # Création fichier BackupEnv.txt dans rep_travail
        if request.form["adr_expe"] == "PERSO":
            return redirect(url_for("enveloppes_adr_expe", rep=rep, adr_retour=True))
        lance_application(lanceur="Enveloppes", rep=rep)        
        return render_template("pages/prise_en_compte.html")
    return render_template("pages/enveloppes_recup.html", rep=rep)

@app.route("/Enveloppes_adr_expe/<rep>", methods=['POST', 'GET'])
@app.route("/Enveloppes_adr_expe/<rep>/<adr_retour>", methods=['POST', 'GET'])
def enveloppes_adr_expe(rep=None, adr_retour=None):
    if request.method == "POST":
        save_adr_retour(rep, request.form["adr_retour"])             
        shutil.copy(c.FIC_ADR_EXPE, rep)
        lance_application(lanceur="Enveloppes", rep=rep)        
        return render_template("pages/prise_en_compte.html")
    return render_template("pages/enveloppes_adr_expe.html", rep=rep, adr_retour=adr_retour)

@app.route("/NH")
def menu():
    return render_template("pages/nh/menu.html")

@app.route('/NH/PEC/<lanceur>')
def resultat(lanceur):
    lance_application(lanceur=lanceur)
    return render_template("pages/prise_en_compte.html")

@app.context_processor
def clients():
    clients = p_var()
    return dict(clients=clients) 

@app.context_processor
def affras(): 
    affras = (c.AFFRAS_K7, c.AFFRAS_KUB)
    return dict(affras=affras)

@app.context_processor
def utility_processor_fichiers():
    def fichiers(rep_travail):
        return dir_traitfichier(rep_travail)
    return dict(fichiers=fichiers)

@app.context_processor
def utility_processor_params():
    def param(rep_travail, index): 
        param = lecture_param(rep_travail, index)
        return param
    return dict(param=param)

@app.context_processor
def nom_lotissement():
    datas = read_datas(c.FIC_DATA_MIF)
    traitement = ""
    if datas:
        traitement = datas['traitement']
    nom_lotissement = f"MIF-{traitement}"
    return dict(nom_lotissement=nom_lotissement)

@app.context_processor
def inject_now():
    return dict(now=datetime.now())

@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404

if __name__ == "__main__":
    app.run(debug=True)