#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import *
from modeles import modeleResanet
from technique import datesResanet


app = Flask( __name__ )
app.secret_key = 'resanet'


@app.route( '/' , methods = [ 'GET' ] )
def index() :
	return render_template( 'vueAccueil.html' )

@app.route( '/usager/session/choisir' , methods = [ 'GET' ] )
def choisirSessionUsager() :
	return render_template( 'vueConnexionUsager.html' , carteBloquee = False , echecConnexion = False , saisieIncomplete = False )

@app.route( '/usager/seConnecter' , methods = [ 'POST' ] )
def seConnecterUsager() :
	numeroCarte = request.form[ 'numeroCarte' ]
	mdp = request.form[ 'mdp' ]

	if numeroCarte != '' and mdp != '' :
		usager = modeleResanet.seConnecterUsager( numeroCarte , mdp )
		if len(usager) != 0 :
			if usager[ 'activee' ] == True :
				session[ 'numeroCarte' ] = usager[ 'numeroCarte' ]
				session[ 'nom' ] = usager[ 'nom' ]
				session[ 'prenom' ] = usager[ 'prenom' ]
				session[ 'mdp' ] = mdp
				
				return redirect( '/usager/reservations/lister' )
				
			else :
				return render_template('vueConnexionUsager.html', carteBloquee = True , echecConnexion = False , saisieIncomplete = False )
		else :
			return render_template('vueConnexionUsager.html', carteBloquee = False , echecConnexion = True , saisieIncomplete = False )
	else :
		return render_template('vueConnexionUsager.html', carteBloquee = False , echecConnexion = False , saisieIncomplete = True)


@app.route( '/usager/seDeconnecter' , methods = [ 'GET' ] )
def seDeconnecterUsager() :
	session.pop( 'numeroCarte' , None )
	session.pop( 'nom' , None )
	session.pop( 'prenom' , None )
	return redirect( '/' )


@app.route( '/usager/reservations/lister' , methods = [ 'GET' ] )
def listerReservations() :
	print '[START] appResanet::listerReservation()'
	tarifRepas = modeleResanet.getTarifRepas( session[ 'numeroCarte' ] )
	
	soldeCarte = modeleResanet.getSolde( session[ 'numeroCarte' ] )
	
	solde = '%.2f' % ( soldeCarte , )

	aujourdhui = datesResanet.getDateAujourdhuiISO()

	datesPeriodeISO = datesResanet.getDatesPeriodeCouranteISO()
	
	datesResas = modeleResanet.getReservationsCarte( session[ 'numeroCarte' ] , datesPeriodeISO[ 0 ] , datesPeriodeISO[ -1 ] )
	numJour=[]
	dates = []
	for uneDateISO in datesPeriodeISO :
		uneDate = {}
		uneDate[ 'iso' ] = uneDateISO
		uneDate[ 'fr' ] = datesResanet.convertirDateISOversFR( uneDateISO )
		
		if uneDateISO <= aujourdhui :
			uneDate[ 'verrouillee' ] = True
		else :
			uneDate[ 'verrouillee' ] = False

		if uneDateISO in datesResas :
			uneDate[ 'reservee' ] = True
		else :
			uneDate[ 'reservee' ] = False
			
		if soldeCarte < tarifRepas and uneDate[ 'reservee' ] == False :
			uneDate[ 'verrouillee' ] = True
			
		dates.append( uneDate )

		dt=uneDateISO
		day, month, year = (int(x) for x in dt.split('-'))
		numJourAujourdhui = datesResanet.getJourWeek(day, month, year)
		numJour.append(numJourAujourdhui)
	
	if soldeCarte < tarifRepas :
		soldeInsuffisant = True
	else :
		soldeInsuffisant = False

	print '[STOP] appResanet::listerReservation()'
	return render_template( 'vueListeReservations.html' , numAjd= numJour, laSession = session , leSolde = solde , lesDates = dates, soldeInsuffisant = soldeInsuffisant )

	
@app.route( '/usager/reservations/annuler/<dateISO>' , methods = [ 'GET' ] )
def annulerReservation( dateISO ) :
	modeleResanet.annulerReservation( session[ 'numeroCarte' ] , dateISO )
	modeleResanet.crediterSolde( session[ 'numeroCarte' ] )
	return redirect( '/usager/reservations/lister' )
	
@app.route( '/usager/reservations/enregistrer/<dateISO>' , methods = [ 'GET' ] )
def enregistrerReservation( dateISO ) :
	modeleResanet.enregistrerReservation( session[ 'numeroCarte' ] , dateISO )
	modeleResanet.debiterSolde( session[ 'numeroCarte' ] )
	return redirect( '/usager/reservations/lister' )

@app.route( '/usager/mdp/modification/choisir' , methods = [ 'GET' ] )
def choisirModifierMdpUsager() :
	soldeCarte = modeleResanet.getSolde( session[ 'numeroCarte' ] )
	solde = '%.2f' % ( soldeCarte , )
	
	return render_template( 'vueModificationMdp.html' , laSession = session , leSolde = solde , modifMdp = '' )

@app.route( '/usager/mdp/modification/appliquer' , methods = [ 'POST' ] )
def modifierMdpUsager() :
	ancienMdp = request.form[ 'ancienMDP' ]
	nouveauMdp = request.form[ 'nouveauMDP' ]
	
	soldeCarte = modeleResanet.getSolde( session[ 'numeroCarte' ] )
	solde = '%.2f' % ( soldeCarte , )
	
	if ancienMdp != session[ 'mdp' ] or nouveauMdp == '' :
		return render_template( 'vueModificationMdp.html' , laSession = session , leSolde = solde , modifMdp = 'Nok' )
		
	else :
		modeleResanet.modifierMdpUsager( session[ 'numeroCarte' ] , nouveauMdp )
		session[ 'mdp' ] = nouveauMdp
		return render_template( 'vueModificationMdp.html' , laSession = session , leSolde = solde , modifMdp = 'Ok' )


@app.route( '/gestionnaire/session/choisir' , methods = [ 'GET' ] )
def choisirSessionGestionnaire() :
	return render_template('vueConnexionGestionnaire.html', echecConnexion=False, saisieIncomplete=False)

@app.route( '/gestionnaire/seConnecter' , methods = [ 'POST' ] )
def seConnecterGestionnaire() :
	login = request.form['login']
	mdp = request.form['mdp']

	if login != '' and mdp != '':
		gestionnaire = modeleResanet.seConnecterGestionnaire(login, mdp)
		if len(gestionnaire) != 0:
			session['login'] = gestionnaire['login']
			session['nom'] = gestionnaire['nom']
			session['prenom'] = gestionnaire['prenom']
			session['mdp'] = mdp
			return redirect('/gestionnaire/listePersonnelAvecCarte')

			return 'connexion ok ' + session['prenom'] + ' ' + session['nom']

		else:
			return render_template('vueConnexionGestionnaire.html',echecConnexion=True,saisieIncomplete=False)

	else:
		return render_template('vueConnexionGestionnaire.html',echecConnexion=False,saisieIncomplete=True)

@app.route( '/gestionnaire/seDeconnecter' , methods = [ 'GET' ] )
def seDeconnecterGestionnaire() :
	session.pop('login', None)
	session.pop('nom', None)
	session.pop('prenom', None)
	return redirect('/')


@app.route('/gestionnaire/listePersonnelAvecCarte', methods = [ 'GET'])
def listePersonnelAvecCarte():
	personnel = modeleResanet.getPersonnelsAvecCarte()
	for i in range(2):
		print personnel[i]
	return render_template('listePersonnelAvecCarte.html', listePersonnel = personnel )

@app.route('/gestionnaire/listePersonnelSansCarte', methods = ['GET'])
def listePersonnelSansCarte():
	personnel = modeleResanet.getPersonnelsSansCarte()
	for i in range(len(personnel)):
		print personnel[i]
	return render_template('listePersonnelSansCarte.html', listePersonnel = personnel )

@app.route('/gestionnaire/BloqueCarte/<numCarte>', methods = ['GET'])
def bloqueCarte(numCarte):
	modeleResanet.bloquerCarte(numCarte)
	return redirect('/gestionnaire/listePersonnelAvecCarte')

@app.route('/gestionnaire/ActiverCarte/<numCarte>', methods = ['GET'])
def activerCarte(numCarte):
	modeleResanet.activerCarte(numCarte)
	return redirect('/gestionnaire/listePersonnelAvecCarte')

@app.route('/gestionnaire/resetMdpCarte/<numCarte>', methods= ['GET'])
def resetMdp(numCarte):
	modeleResanet.reinitialiserMdp(numCarte)
	return redirect('/gestionnaire/listePersonnelAvecCarte')

@app.route('/gestionnaire/creerCarte/<numCarte>/<validee>', methods= ['GET'])
def creerCarte(numCarte, validee):
	modeleResanet.creerCarte(numCarte, validee)
	return redirect('/gestionnaire/listePersonnelSansCarte')

@app.route('/gestionnaire/crediter',methods = ['POST', 'GET'])
def crediter():
   if request.method == 'POST':
    crediter = request.form
    personnel = modeleResanet.getPersonnelsAvecCarte()
    matricule = []
    for i in range(0, len(personnel)):
        matricule.append(personnel[i]['matricule'])

    for i in range(0, len(matricule)):
        if int(crediter['numCarte']) == int(matricule[i]):
            modeleResanet.crediterCarte(crediter['numCarte'], crediter['somme'])
    return redirect("/gestionnaire/listePersonnelAvecCarte")

@app.route('/gestionnaire/dateReservation', methods = ['POST'])
def dateReservation():
	dateResa = request.form
	personnel = modeleResanet.getReservationsDate(dateResa['date'])
	return render_template('dateReservation.html', listePersonnel = personnel )

@app.route('/gestionnaire/historique/<numCarte>',methods = ['GET'])
def historiqueGET(numCarte):
    reservation = []
    reservation = modeleResanet.getHistoriqueReservationsCarte(numCarte)
    return render_template("historique.html" , Reservations = reservation)

@app.route('/gestionnaire/historique/',methods = ['POST'])
def historiquePOST():
    if request.method == 'POST':
        result = request.form
        reservation = []
        reservation = modeleResanet.getHistoriqueReservationsCarte(result['numCarte'])
        return render_template("historique.html", Reservations=reservation)

if __name__ == '__main__' :
	app.run( debug = True , host = '0.0.0.0' , port = 5000 )
