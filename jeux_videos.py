import sqlite3
from random import randint
import datetime

conn = sqlite3.connect('bd_jeuxvideos.db')
cur = conn.cursor()
auth_donnees = None


def adherer():
    print('----------------------------------------------------------------')
    print("Choisissez Votre nom de famille, Prénom, âge et mot de passe espacés chacun d'un espace")
    donnees = input().split(' ')
    while len(donnees) != 4 or donnees[2].isalpha():
        print('Mauvaise saisie recommencez')
        donnees = input().split(' ')
    cur.execute('SELECT code_adherent FROM ADHERENT')
    conn.commit()
    liste = cur.fetchall()
    while donnees[3] in liste:
        print('Mot de passe déjà pris, choisissez-en un autre')
        donnees[3] = input()
    donnees = (donnees[0],donnees[1],int(donnees[2]),donnees[3])
    cur.execute("INSERT INTO ADHERENT(Nom,Prenom,age,code_adherent) VALUES(?,?,?,?)",donnees)
    conn.commit()
    print('Bienvenue parmis nous !')
    main()

def authentification():
    global authentification,auth_donnees
    print('----------------------------------------------------------------')
    print("Choisissez Votre nom de famille, Prénom et votre mot de passe espacés chacun d'un espace")
    donnees = input().split(' ')
    while len(donnees) != 3:
        print('Mauvaise saisie recommencez')
        donnees = input().split(' ')
    donnees = (donnees[0],donnees[1],donnees[2])
    cur.execute('SELECT Nom,Prenom,code_adherent FROM ADHERENT')
    conn.commit()
    liste = cur.fetchall()
    for users in liste:
        if donnees == users:
            auth_donnees = [donnees[1],donnees[0],donnees[2]]
            main()
            return
    print("Authentification échouée...")
    enregistrement()



def deposer():
    global auth_donnees
    donnees = auth_donnees
    print('----------------------------------------------------------------')
    print("Saisissez les informations du jeux à déposer: nom,éditeur,annee de parution,prix (pas trop cher si possible), son genre")
    print("et enfin l'âge minimum requis pour jouer au jeux, tous séparés par un espace")
    donnees = input().split(' ')
    while len(donnees) != 6 or donnees[3].isalpha():
        print('Mauvaise saisie recommencez')
        donnees = input().split(' ')
    cur.execute('SELECT Nom_jeux FROM JEUX')
    conn.commit()
    liste = cur.fetchall()
    if donnees[0] in liste:
        print('Nous proposons déjà un exemplaire de ce jeux')
        return main()
    cur.execute('SELECT code_jeux FROM JEUX')
    conn.commit()
    liste = cur.fetchall()
    code = str(randint(0,10000))
    while code in liste:
        code = str(randint(0,10000))
    donnees = (donnees[0],donnees[1],donnees[2],int(donnees[3]),code,donnees[4],int(donnees[5]),0,tempdatas[0],tempdatas[1])
    print(donnees)
    cur.execute("INSERT INTO JEUX(Nom_jeux,editeur,annee,prix,code_jeux,genre,age_minimum,nb_emprunt,Prenom_donneur,Nom_donneur) VALUES(?,?,?,?,?,?,?,?,?,?)",donnees)
    conn.commit()
    print('Jeux ajouté avec succès !')
    main()

def louer():
    global auth_donnees
    tempdatas = auth_donnees
    cur.execute("SELECT age FROM ADHERENT WHERE code_adherent = ?;",(tempdatas[2],))
    age = cur.fetchall()[0]
    cur.execute('SELECT Nom_jeux,code_jeux FROM JEUX WHERE NOT code_jeux IN (SELECT code_jeux FROM EMPRUNT) AND ? >= age_minimum;',age)
    conn.commit()
    liste_jeux_code = cur.fetchall()
    if liste_jeux_code == []:
        print("Il n'y a pas de jeux disponibles à la location actuellement, repassez plus tard !")
        return main()
    print('----------------------------------------------------------------')
    print('Choisissez un de ces jeux à louer :')
    print()
    liste_jeux = [nom[0] for nom in liste_jeux_code]
    for jeux in liste_jeux:
        print(jeux)
    choix = input()
    while not choix in liste_jeux:
        print('Veuillez choisir un des jeux parmis la liste suivante :')
        print(liste_jeux)
        choix = input()
    for jeux in liste_jeux_code:
        if jeux[0] == choix:
            code_jeux = jeux[1]
    jour = datetime.date.today().day
    mois = datetime.date.today().month
    annee = datetime.date.today().year
    retour = str(annee)+'-'+str(mois)+'-'+str((jour + 15) % 31)
    donnees = (retour,tempdatas[2],code_jeux)
    choix = (1,choix)
    cur.execute("INSERT INTO EMPRUNT(retour,code_adherent,code_jeux) VALUES(?,?,?)",donnees)
    cur.execute("UPDATE JEUX SET nb_emprunt = nb_emprunt + ? WHERE Nom_jeux = ?",choix)
    conn.commit()
    print('Location enregistrée...')
    main()

def rendre():
    global auth_donnees
    donnees= (auth_donnees[0],auth_donnees[1])
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

def reprendre():
    global auth_donnees
    tempdatas = auth_donnees
    cur.execute("SELECT Nom_jeux,code_jeux FROM JEUX WHERE prenom_donneur = ? AND nom_donneur = ?",(tempdatas[0],tempdatas[1]))
    liste_jeux = cur.fetchall()
    if liste_jeux == []:
        print("Vous n'avez déposé aucun jeux...")
        return main()
    print('Choisissez un jeux à rendre parmis :')
    liste_noms_jeux = [jeux[0] for jeux in liste_jeux]
    for jeux in liste_noms_jeux:
        print(jeux)
    choix = input()
    while not choix in liste_noms_jeux:
        print('Veuillez choisir un jeux parmis la liste de jeux suivante:')
        print(liste_noms_jeux)
        choix = input()
    for jeux in liste_jeux:
        if jeux[0] == choix:
            code = jeux[1]
    cur.execute("DELETE FROM JEUX WHERE code_jeux = ?",(code,))
    conn.commit()
    main()



def action():
    print('----------------------------------------------------------------')
    liste= ["1- Déposer un jeux","2- Louer un jeux","3- Rendre un jeux","4- Reprendre son jeux"]
    for phrase in liste:
        print(phrase)
    rep = input()
    if rep == '1':
        deposer()
    elif rep == '2':
        louer()
    elif rep == '3':
        rendre()
    elif rep == '4':
        reprendre()

def stats():
    print('----------------------------------------------------------------')
    liste= ["1- Jeu qui est le plus emprunté","2- Recettes de la bibliothèque","3- Liste des jeux disponibles","4- Nombre de jeux empruntés par adhérents"]
    for phrase in liste:
        print(phrase)
    choix = input()
    if choix == '1':
        cur.execute("SELECT Nom_jeux,max(nb_emprunt) FROM JEUX;")
        donnees=cur.fetchall()[0]
        print('Le jeux le plus emprunté est {} avec {} emprunt(s)'.format(donnees[0],donnees[1]))

    elif choix == '2':
        cur.execute("SELECT sum(prix * nb_emprunt) as recette_totale FROM JEUX;")
        print('----------------------------------------------------------------')
        print('Recettes globales de la bibliothèque : {} €'.format(cur.fetchall()[0][0]))
        cur.execute("SELECT Nom_jeux, (prix * nb_emprunt) as recette FROM JEUX;")
        print()
        print('Recettes par jeux de la bibliothèque :')
        print()
        for jeux in cur.fetchall():
            print("{} : {} €".format(jeux[0],jeux[1]))

    elif choix == '3':
        cur.execute("SELECT Nom_jeux FROM JEUX WHERE NOT code_jeux IN (SELECT code_jeux FROM EMPRUNT); ")
        print('----------------------------------------------------------------')
        donnees = cur.fetchall()
        if donnees == []:
            print("Désolé mais aucun jeux n'est disponible")
            return main()
        print('Liste des jeux disponibles :')
        print()
        for jeux in donnees:
            print(jeux[0])

    elif choix == '4':
        cur.execute("SELECT Nom,Prenom,count(*) as nb_livres_empruntés FROM EMPRUNT JOIN ADHERENT ON EMPRUNT.code_adherent = ADHERENT.code_adherent GROUP BY Nom,Prenom;")
        print('----------------------------------------------------------------')
        print("Nombre de livres empruntés actuellement par chaque Adhérent à la bibliothèque :")
        print()
        for jeux in cur.fetchall():
            print('{} {} : {} jeux'.format(jeux[0],jeux[1],jeux[2]))

    else:
        stats()

    main()




def main():
    print('----------------------------------------------------------------')
    print('0- Quitter')
    print('1- Actions sur la base')
    print('2- Statistiques')
    rep = input()
    if rep == '0':
        enregistrement()
    elif rep == '1':
        action()
    elif rep == '2':
        stats()
    else:
        main()

def enregistrement():
    print('----------------------------------------------------------------')
    print('0- Quitter')
    print('1- Adhérer à la bibliothèque de jeux-vidéo')
    print('2- Se connecter')
    rep = input()

    if rep == '0':
        print('Au plaisir de vous revoir...')
        cur.close()
        conn.close()
        exit()
    elif rep == '1':
        adherer()
    elif rep == '2':
        authentification()


enregistrement()





