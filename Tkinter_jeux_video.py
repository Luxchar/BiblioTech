import sqlite3 # Module permettant de relierp python à une BDD
from random import randint # Module random
import datetime # Module pour récupérer la date du jour
from tkinter import* # on importe le module tkinter
from datetime import timedelta, date # pour gérer les dates

# On crée la fenêtre tkinter, on la stocke dans une variable 'fen'
fen= Tk()
fen.title('Bibliotech') # on modifie le titre de la fenêtre
fen.geometry("1100x700") # on modifie la taille de la fenêtre




conn = sqlite3.connect('bd_jeuxvideos.db')
cur = conn.cursor()



def effacer():
    global temp_effacer
    for widgets in temp_effacer:
        if widgets:
            widgets.grid_remove()
    temp_effacer = []

def adherer_afficher():
    global temp_effacer
    effacer()
    texte_adherer.grid(row=0,column=0)
    choix_ids.grid(row=1,column=0)
    temp_effacer.append(texte_adherer)
    temp_effacer.append(choix_ids)

def adherer(event):
    global temp_effacer
    donnees = choix_ids.get().split(' ')
    if len(donnees) != 4 or donnees[2].isalpha():
        texte_erreur.grid(row=2,column=0)
        temp_effacer.append(texte_erreur)
        return
    cur.execute('SELECT code_adherent FROM ADHERENT')
    conn.commit()
    liste = cur.fetchall()
    while donnees[3] in liste:
        donnees[3] = donnees[3] + str(randint(0,2000))
    donnees = (donnees[0],donnees[1],int(donnees[2]),donnees[3])
    effacer()
    texte_annonce.config(text = 'Votre mot de passe est {} \n Votre inscription a bien été enregistrée \n Bienvenue parmis nous {} {} !'.format(donnees[3],donnees[1],donnees[0]))
    texte_annonce.grid(row=0,column=0)
    confirmation.grid(row = 3,column = 0)
    temp_effacer.append(texte_annonce)
    temp_effacer.append(confirmation)
    temp_effacer.append(choix_ids)
    cur.execute("INSERT INTO ADHERENT(Nom,Prenom,age,code_adherent) VALUES(?,?,?,?)",donnees)
    conn.commit()







def afficher_auth():
    global temp_effacer
    choix_accueil.grid_remove()
    texte_accueil.grid_remove()
    texte_nom_adh.grid(row=0,column=0)
    nom_adh.grid(row=1,column=0)
    texte_prenom_adh.grid(row=2,column=0)
    Prenom_adh.grid(row=3,column=0)
    texte_code_adh.grid(row=4,column=0)
    mdp_adherent.grid(row=5,column=0)
    confirmer_auth.grid(row=6,column=0)
    adherer_Bu.grid(row=7,column=0)

    temp_effacer = [texte_nom_adh,nom_adh,texte_prenom_adh,nom_adh,texte_prenom_adh,Prenom_adh,texte_code_adh,mdp_adherent,confirmer_auth,adherer_Bu]




def authentification():
    global auth_donnees,temp_effacer
    donnees = (nom_adh.get(),Prenom_adh.get(),mdp_adherent.get())
    if '' in donnees:
        temp_effacer.append(texte_erreur)
        texte_erreur.grid(row=7,column=0)
        return
    cur.execute('SELECT Nom,Prenom,code_adherent FROM ADHERENT')
    conn.commit()
    liste = cur.fetchall()
    for users in liste:
        if donnees == users:
            auth_donnees = [donnees[1],donnees[0],donnees[2]]
            lancer()
            return
    temp_effacer.append(texte_erreur)
    texte_erreur.grid(row=7,column=0)
    return False




def afficher_deposer():
    global temp_effacer
    effacer()
    texte_deposer.grid(row=0,column=0)
    jeux.grid(row=1,column=0)
    temp_effacer = [texte_deposer,jeux]




def deposer(event):
    global auth_donnees,temp_effacer
    tempdatas = auth_donnees
    donnees = jeux.get().split(' ')
    print(len(donnees))
    if len(donnees) != 6 or donnees[3].isalpha():
        erreur_doublons.grid_remove()
        texte_erreur.grid(row=2,column=0)
        temp_effacer.append(texte_erreur)
        return
    cur.execute('SELECT Nom_jeux FROM JEUX')
    conn.commit()
    liste = [''.join(e) for e in cur.fetchall()]
    if donnees[0] in liste:
        texte_erreur.grid_remove()
        erreur_doublons.grid(row=2,column=0)
        temp_effacer.append(erreur_doublons)
        return
    cur.execute('SELECT code_jeux FROM JEUX')
    conn.commit()
    liste = cur.fetchall()
    code = str(randint(0,10000))
    while code in liste:
        code = str(randint(0,10000))
    donnees = (donnees[0],donnees[1],donnees[2],int(donnees[3]),code,donnees[4],int(donnees[5]),0,tempdatas[0],tempdatas[1])
    cur.execute("INSERT INTO JEUX(Nom_jeux,editeur,annee,prix,code_jeux,genre,age_minimum,nb_emprunt,Prenom_donneur,Nom_donneur) VALUES(?,?,?,?,?,?,?,?,?,?)",donnees)
    conn.commit()
    print('Jeux ajouté avec succès !')
    lancer()

def rendre():
    global auth_donnees
    donnees= auth_donnees
    cur.execute("SELECT Nom_jeux,EMPRUNT.code_jeux FROM EMPRUNT JOIN ADHERENT ON ADHERENT.code_adherent = EMPRUNT.code_adherent JOIN JEUX ON JEUX.code_jeux = EMPRUNT.code_jeux WHERE Prenom = ? and Nom = ?",donnees)
    jeux_a_rendres = cur.fetchall()
    if jeux_a_rendres == []:
        print("Désolé mais vous n'avez encore emprunté aucun livre")
        return main()
    print('----------------------------------------------------------------')
    print('Choisissez un de ces jeux à rendre')
    nom_jeux_a_rendre = [e[0] for e in jeux_a_rendres]
    for nom in nom_jeux_a_rendre:
        print(nom)
    choix = input()
    while not choix in nom_jeux_a_rendre:
        print('Veuillez choisir un des jeux parmis la liste suivante :')
        print(liste_jeux)
        choix = input()
    for jeux in jeux_a_rendres:
        if jeux[0] == choix:
            code_jeux = jeux[1]
    donnees = (tempdatas[2],code_jeux)
    cur.execute("DELETE FROM EMPRUNT WHERE code_adherent = ? AND code_jeux = ?",donnees)
    conn.commit()
    print('Suppression effectuée...')
    main()

def afficher_rendre():
    global temp_effacer,auth_donnees,liste_jeux_code
    effacer()
    tempdatas = auth_donnees
    txt = 'Quel jeu voulez vous rendre ?'
    rendre_jeux2.config(text = txt)
    rendre_jeux2.grid(row=0,column=0)

    cur.execute("SELECT Nom_jeux,EMPRUNT.code_jeux FROM EMPRUNT JOIN ADHERENT ON ADHERENT.code_adherent = EMPRUNT.code_adherent JOIN JEUX ON JEUX.code_jeux = EMPRUNT.code_jeux WHERE Prenom = ? and Nom = ?",donnees)
    liste_jeux_code2 = cur.fetchall()[0]
    conn.commit()

    liste_jeux_code2 = cur.fetchall()
    if liste_jeux_code == []:
        bu_rupture2.grid(row=0,column=0)
        temp_effacer.append(bu_rupture2)
        return
    txt = 'Choisissez un de ces jeux à rendre :'
    liste_jeux = [nom[0] for nom in liste_jeux_code]
    for jeux in liste_jeux:
        txt += '\n' + jeux
    rendre_jeux.config(text = txt)
    rendre_jeux.grid(row=0,column=0)
    temp_effacer.append(rendre_jeux)
    choix_jeux2.grid(row=1,column=0)

def reprendre(event):
    global temp_effacer,auth_donnees,liste_jeux_code2
    effacer()
    donnees = auth_donnees
    tempdatas = auth_donnees
    cur.execute("SELECT Nom_jeux,code_jeux FROM JEUX WHERE prenom_donneur = ? AND nom_donneur = ?",(tempdatas[0],tempdatas[1]))
    liste_jeux_code2 = cur.fetchall()
    choix = choix_jeux2.get()
    liste_jeux = [nom[0] for nom in liste_jeux_code2]
    if not choix in liste_jeux:
        texte_erreur.grid(row=2,column=0)
        temp_effacer.append(texte_erreur)
        return
    for jeux in liste_jeux_code2:
        if jeux[0] == choix:
            code = jeux[1]
    succes.grid(row=0,column=0)
    temp_effacer.append(succes)
    cur.execute("DELETE FROM JEUX WHERE code_jeux = ?",(code,))
    conn.commit()
    lancer()

def afficher_reprendre():
    global temp_effacer,auth_donnees,liste_jeux_code2
    effacer()
    tempdatas = auth_donnees
    cur.execute("SELECT Nom_jeux,code_jeux FROM JEUX WHERE prenom_donneur = ? AND nom_donneur = ?",(tempdatas[0],tempdatas[1]))
    conn.commit()
    liste_jeux_code2 = cur.fetchall()
    if liste_jeux_code2 == []:
        bu_rupture2.grid(row=0,column=0)
        temp_effacer.append(bu_rupture2)
        return
    txt = 'Choisissez un de ces jeux à reprendre :'
    liste_jeux = [nom[0] for nom in liste_jeux_code2]
    for i in liste_jeux:
        txt += '\n' + i
    montrer_jeux_de.config(text = txt)
    montrer_jeux_de.grid(row=0,column=0)
    temp_effacer.append(montrer_jeux_de)
    choix_jeux2.grid(row=1,column=0)
    temp_effacer.append(choix_jeux2)



def afficher_louer():
    global temp_effacer,auth_donnees,liste_jeux_code
    effacer()
    tempdatas = auth_donnees
    cur.execute("SELECT age FROM ADHERENT WHERE code_adherent = ?;",(tempdatas[2],))
    age = cur.fetchall()[0]
    cur.execute('SELECT Nom_jeux,code_jeux FROM JEUX WHERE NOT code_jeux IN (SELECT code_jeux FROM EMPRUNT) AND ? >= age_minimum;',age)
    conn.commit()
    liste_jeux_code = cur.fetchall()
    if liste_jeux_code == []:
        bu_rupture.grid(row=0,column=0)
        temp_effacer.append(bu_rupture)
        return
    txt = 'Choisissez un de ces jeux à louer :'
    liste_jeux = [nom[0] for nom in liste_jeux_code]
    for jeux in liste_jeux:
        txt += '\n' + jeux
    montrer_jeux.config(text = txt)
    montrer_jeux.grid(row=0,column=0)
    temp_effacer.append(montrer_jeux)
    choix_jeux.grid(row=1,column=0)

def louer(event):
    global auth_donnees,temp_effacer,liste_jeux_code
    tempdatas = auth_donnees
    choix = choix_jeux.get()
    liste_jeux = [nom[0] for nom in liste_jeux_code]
    if not choix in liste_jeux:
        texte_erreur.grid(row=0,column=0)
        temp_effacer.append(texte_erreur)
        return
    for jeux in liste_jeux_code:
        if jeux[0] == choix:
            code_jeux = jeux[1]
    retour = date.today() + timedelta(days=15)
    donnees = (retour,tempdatas[2],code_jeux)
    choix = (1,choix)
    cur.execute("INSERT INTO EMPRUNT(retour,code_adherent,code_jeux) VALUES(?,?,?)",donnees)
    cur.execute("UPDATE JEUX SET nb_emprunt = nb_emprunt + ? WHERE Nom_jeux = ?",choix)
    conn.commit()
    lancer()


def action_afficher():
    global temp_effacer
    effacer()
    choix_accueil.grid_remove()
    texte_accueil.grid_remove()
    phrases_action.grid(row = 0,column = 0)
    choix_action.grid(row = 1,column = 0)
    temp_effacer.append(phrases_action)
    temp_effacer.append(choix_action)


def action(event):
    rep = choix_action.get()
    if rep == '1':
        afficher_deposer()
    elif rep == '2':
        afficher_louer()
    elif rep == '3':
        rendre()
    elif rep == '4':
        afficher_reprendre()
    elif rep == '0':
        phrases_action.grid_remove()
        choix_action.grid_remove()
        lancer()




def stats_afficher():
    choix_accueil.grid_remove()
    texte_accueil.grid_remove()
    phrases_stats.grid(row = 0,column = 0)
    choix_stats.grid(row = 1, column = 0)

def stats(event):
    global temp_texte
    if temp_texte:
        temp_texte.grid_remove()
    temp_texte = None
    choix = choix_stats.get()
    if choix == '1':
        cur.execute("SELECT Nom_jeux,max(nb_emprunt) FROM JEUX;")
        donnees=cur.fetchall()[0]
        temp_texte = Label(fen,text='Le jeux le plus emprunté est {} avec {} emprunt(s)'.format(donnees[0],donnees[1]),bg= 'red',font = 'arial 10 bold')
        temp_texte.grid(row=2,column=0)

    elif choix == '2':
        cur.execute("SELECT sum(prix * nb_emprunt) as recette_totale FROM JEUX;")
        texte='Recettes globales de la bibliothèque : {} €'.format(cur.fetchall()[0][0])
        cur.execute("SELECT Nom_jeux, (prix * nb_emprunt) as recette FROM JEUX;")
        texte += '\n \n Recettes par jeux de la bibliothèque :'
        for jeux in cur.fetchall():
            texte += "\n {} : {} €".format(jeux[0],jeux[1])
        temp_texte = Label(fen,text=texte ,bg= 'red',font = 'arial 10 bold')
        temp_texte.grid(row=2,column=0)

    elif choix == '3':
        cur.execute("SELECT Nom_jeux FROM JEUX WHERE NOT code_jeux IN (SELECT code_jeux FROM EMPRUNT); ")
        donnees = cur.fetchall()
        if donnees == []:
            temp_texte = Label(fen,text = "Désolé mais aucun jeux n'est disponible" ,bg= 'red',font = 'arial 10 bold')
            temp_texte.grid(row=2,column=0)
            return
        texte = 'Liste des jeux disponibles : \n'
        for jeux in donnees:
            texte += '\n' + jeux[0]
        temp_texte = Label(fen,text=texte ,bg= 'red',font = 'arial 10 bold')
        temp_texte.grid(row=2,column=0)

    elif choix == '4':
        cur.execute("SELECT Nom,Prenom,count(*) as nb_livres_empruntés FROM EMPRUNT JOIN ADHERENT ON EMPRUNT.code_adherent = ADHERENT.code_adherent GROUP BY Nom,Prenom;")
        texte = "Nombre de livres empruntés actuellement par chaque Adhérent à la bibliothèque : \n"
        donnees = cur.fetchall()
        if donnees == []:
            temp_texte = Label(fen,text= "Désolé mais aucun livre n'est actuellement emprunté" ,bg= 'red',font = 'arial 10 bold')
            temp_texte.grid(row=2,column=0)
            return
        for jeux in donnees:
            texte += '{} {} : {} jeux'.format(jeux[0],jeux[1],jeux[2]) + '\n'
        temp_texte = Label(fen,text=texte ,bg= 'red',font = 'arial 10 bold')
        temp_texte.grid(row=2,column=0)

    elif choix == '0':
        if temp_texte:
            temp_texte.grid_remove()
        phrases_stats.grid_remove()
        choix_stats.grid_remove()
        lancer()


def lancer():
    global temp_effacer
    effacer()
    choix_accueil.grid(row=1,column=0)
    texte_accueil.config(text='Bienvenue chez Bibliotech {} {} \n 0-Quitter \n 1-Actions sur la base \n 2-Statistiques'.format(auth_donnees[0],auth_donnees[1]))
    texte_accueil.grid(row=0,column=0)
    temp_effacer.append(choix_accueil)
    temp_effacer.append(texte_accueil)



def main(event):
    rep = choix_accueil.get()
    if rep == '0':
        fen.destroy()
        cur.close()
        conn.close()
        exit()
    elif rep == '1':
        action_afficher()
    elif rep == '2':
        stats_afficher()
    elif rep == '3':
        afficher_rendre()
    elif rep == '4':
        afficher_reprendre()



# Pour l'accueil
texte_accueil = Label(text = '',bg= 'red',font = 'arial 25 bold')
choix_accueil = Entry(fen,bg='red')
choix_accueil.bind("<Return>",main)

# Pour les stats
temp_texte = None
phrases_stats = Label(text = '0- Quitter \n 1- Jeu qui est le plus emprunté \n 2- Recettes de la bibliothèque \n 3- Liste des jeux disponibles \n 4- Nombre de jeux empruntés par adhérents',bg= 'red',font = 'arial 25 bold')
choix_stats = Entry(fen,bg='red')
choix_stats.bind("<Return>",stats)
choix_action = Entry(fen)
choix_action.bind("<Return>",action)
phrases_action = Label(text = "0-Quitter \n 1- Déposer un jeux \n 2- Louer un jeux \n 3- Rendre un jeux \n 4- Reprendre son jeux",bg= 'red',font = 'arial 25 bold')


# Pour la fonction d'authentification
texte_nom_adh = Label(text = 'Nom',bg= 'red',font = 'arial 25 bold')
nom_adh = Entry(fen,bg='red')
texte_prenom_adh = Label(text = 'Prenom',bg= 'red',font = 'arial 25 bold')
Prenom_adh = Entry(fen,bg='red')
texte_code_adh = Label(text = 'Mot de passe',bg= 'red',font = 'arial 25 bold')
mdp_adherent = Entry(fen,bg='red')
confirmer_auth = Button(fen,command=authentification,text='Confirmer')
adherer_Bu = Button(fen,command=adherer_afficher,text='Adhérer')




# pour la fonction adhérer
choix_ids = Entry(fen)
choix_ids.bind('<Return>',adherer)
texte_adherer = Label(text = "Choisissez Votre nom de famille, Prénom, âge et mot de passe \n espacés chacun d'un espace",bg= 'red',font = 'arial 25 bold')
texte_annonce = Label(text = '',font = 'arial 25 bold',bg='red')
confirmation = Button(fen,command = lancer,text = 'Retour Au Menu')


# pour la fonction déposer
texte_deposer = Label(text="Saisissez les informations du jeux à déposer: nom,éditeur,annee de parution,prix (pas trop cher si possible), son genre \n et enfin l'âge minimum requis pour jouer au jeux, tous séparés par un espace",bg= 'red',font = 'arial 15 bold')
jeux = Entry(fen)
jeux.bind('<Return>',deposer)
erreur_doublons = Label(text = 'Nous proposons déjà un exemplaire de ce jeux',bg= 'red',font = 'arial 25 bold')

# pour la fonction louer
liste_jeux_code = None
bu_rupture = Button(text = "Il n'y a pas de jeux disponibles à la location actuellement, repassez plus tard !",command = action_afficher)
montrer_jeux= Label(text = '',bg= 'red',font = 'arial 25 bold')
choix_jeux = Entry(fen)
choix_jeux.bind('<Return>',louer)

# pour la fonction reprendre
liste_jeux_code2 = None
bu_rupture2 = Button(text = "Tu n'as aucun jeu à reprendre ! Met en un en location d'abord",command = action_afficher)
succes = Button(text = "Jeu supprimé avec succès !",command = action_afficher)
montrer_jeux_de= Label(text = '',bg= 'red',font = 'arial 25 bold')
choix_jeux2 = Entry(fen)
choix_jeux2.bind('<Return>',reprendre)

texte_erreur = Label(text = 'Mauvaise saisie recommencez',bg= 'red',font = 'arial 25 bold')
auth_donnees = None
temp_effacer = []
afficher_auth()
fen.mainloop()



