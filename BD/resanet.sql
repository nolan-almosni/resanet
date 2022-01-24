drop database if exists resanet ;
create database resanet default character set utf8 default collate utf8_general_ci ;

use resanet ;

create table Fonction (
	idFonction int unsigned not null ,
	libelleFonction varchar(20) not null ,
	tarifRepas float not null ,
	primary key(idFonction)
) ENGINE=InnoDB ;

create table Service (
	idService int unsigned not null ,
	nomService varchar(20) not null ,
	primary key(idService)
) ENGINE=InnoDB ;

create table Personnel (
	matricule int unsigned not null ,
	nom varchar(20) not null ,
	prenom varchar(20) not null ,
	dateNaissance date not null ,
	idFonction int unsigned ,
	idService int unsigned ,
	primary key(matricule)
) ENGINE=InnoDB ;

create table Carte (
	numeroCarte int unsigned not null auto_increment ,
	mdpCarte varchar(20) not null default 'azerty',
	solde float not null default 0.0 ,
	dateCreation date not null ,
	activee boolean default false ,
	matricule int unsigned not null ,
	primary key(numeroCarte)
) ENGINE=InnoDB ;

create table Gestionnaire (
	login varchar(20) not null ,
	mdp varchar(20) not null default 'baobab' ,
	matricule int unsigned not null ,
	primary key(login)
) ENGINE=InnoDB ;

create table Reservation (
	dateResa date not null ,
	numeroCarte int unsigned not null ,
	primary key(dateResa,numeroCarte)
) ENGINE=InnoDB ;

create table Dates (
	datesImmuable date
) ;

insert into Fonction values(1,'Directeur',8.2) ;
insert into Fonction values(2,'Cadre',7.3) ;
insert into Fonction values(3,'Technicien',5.7) ;
insert into Fonction values(4,'Secrétaire',3.5) ;
insert into Fonction values(5,'Stagiaire',3.1) ;

insert into Service values(1,'Direction') ;
insert into Service values(2,'Commercial') ;
insert into Service values(3,'R&D') ;
insert into Service values(4,'DRH') ;
insert into Service values(5,'Comptable') ;
insert into Service values(6,'Juridique') ;
insert into Service values(7,'Accueil') ;
insert into Service values(8,'DSI') ;
insert into Service values(9,'Formation') ;
insert into Service values(10,'Communication') ;

insert into Personnel values(1,'PRIGENT','Ewen','1975-12-11',1,1) ;
insert into Personnel values(2,'HECKER','Amal','1977-02-14',2,1) ;
insert into Personnel values(3,'CAPITAINE','Xavier','1970-04-23',2,1) ;
insert into Personnel values(4,'THOMAS','Jean-Yves','1972-11-18',2,1) ;
insert into Personnel values(5,'FONTAINE','Christophe','1968-09-02',5,4) ;
insert into Personnel values(6,'AFCHAIN','Pierre','1994-12-23',3,8) ;
insert into Personnel values(7,'AISSOU','Yaniss','1994-05-15',3,8) ;
insert into Personnel values(8,'ALI','Adnane','1994-11-03',3,8) ;
insert into Personnel values(9,'ALVES','Aurélien','1994-12-03',3,8) ;
insert into Personnel values(10,'BA','Béchir','1994-12-03',3,8) ;
insert into Personnel values(11,'BEN DAHMANE','Yassir','1994-12-08',3,3) ;
insert into Personnel values(12,'BOURAOUI','Rahma','1994-03-15',3,3) ;
insert into Personnel values(13,'CHAUDEY','Caroline','1994-12-21',3,3) ;
insert into Personnel values(14,'CISTA','Walid','1994-12-03',3,3) ;
insert into Personnel values(15,'CLERGEOT','Anthony','1994-12-09',3,3) ;
insert into Personnel values(16,'CORY','Yohan','1993-11-13',3,3) ;
insert into Personnel values(17,'EIBERT','Julien','1994-12-10',3,8) ;
insert into Personnel values(18,'EL AYACHI','Meryeme','1994-12-11',3,3) ;
insert into Personnel values(19,'FERGUENE','Juba','1994-12-03',3,3) ;
insert into Personnel values(20,'GHAZARIAN','Thibaut','1994-12-22',3,3) ;
insert into Personnel values(21,'GODEFROY','Yoann','1994-04-21',3,3) ;
insert into Personnel values(22,'HONG','Vathanak','1994-05-20',3,8) ;
insert into Personnel values(23,'HUMBERT','Cédric','1993-12-03',3,3) ;
insert into Personnel values(24,'KABACHE','Hugo','1993-08-11',3,3) ;
insert into Personnel values(25,'LABEL','Pierre','1994-03-03',3,3) ;
insert into Personnel values(26,'LANDIM SEMEDO','Maxime','1994-12-03',3,3) ;
insert into Personnel values(27,'LE GUEVEL','Vincent','1994-12-03',3,3) ;
insert into Personnel values(28,'LEBEAU','Mike','1993-11-03',3,3) ;
insert into Personnel values(29,'LEFAUCONNIER','José','1994-12-20',3,3) ;
insert into Personnel values(30,"LOZAC'H",'Bastien','1987-07-17',3,3) ;
insert into Personnel values(31,'MAGBODU','Michee','1994-12-03',3,8) ;
insert into Personnel values(32,'MAUREL','Axel','1990-12-03',3,3) ;
insert into Personnel values(33,'MERHRIOUI','Adam','1994-12-07',3,3) ;
insert into Personnel values(34,'NLANDU','Christian','1994-05-03',3,3) ;
insert into Personnel values(35,'PEQUERY','Grégory','1994-11-03',3,3) ;
insert into Personnel values(36,'PERELLO-Y-BESTARD','Clément','1994-01-08',3,3) ;
insert into Personnel values(37,'ROLAND','Mathieu','1990-12-03',3,3) ;
insert into Personnel values(38,'ROSA','Baptiste','1993-12-03',3,3) ;
insert into Personnel values(39,'TOINON','Tom','1994-12-03',3,3) ;
insert into Personnel values(40,'TROUILLET','Mickaël','1994-11-01',2,3) ;
insert into Personnel values(41,'BELHADJ','Taslim','1991-09-03',2,3) ;
insert into Personnel values(42,'BELLAICHE','Mikaël','1991-12-02',2,3) ;
insert into Personnel values(43,'HURON','Kévin','1994-12-03',2,3) ;
insert into Personnel values(44,'JACQUIER','Nicolas','1994-02-03',2,3) ;
insert into Personnel values(45,'POIRIER','Nicolas','1994-12-04',2,3) ;
insert into Personnel values(46,'RAFINA','Dany','1994-07-03',2,3) ;
insert into Personnel values(47,'ROSCO','Steve','1992-03-05',2,3) ;
insert into Personnel values(48,'UZAN','Alexis','1989-09-07',2,3) ;
insert into Personnel values(49,'WEBER','Guillaume','1994-08-03',2,3) ;
insert into Personnel values(50,'WELLE','Guillaume','1994-12-20',2,3) ;


insert into Carte(solde,dateCreation,activee,matricule) values(100.0,current_date(),True,1) ;
insert into Carte(solde,dateCreation,activee,matricule) values(80.0,current_date(),True,2) ;
insert into Carte(solde,dateCreation,activee,matricule) values(210.0,current_date(),True,3) ;
insert into Carte(solde,dateCreation,activee,matricule) values(130.0,current_date(),False,4) ;
insert into Carte(solde,dateCreation,activee,matricule) values(42.0,current_date(),True,5) ;

insert into Gestionnaire values('admin','azerty',5) ;

insert into Dates values('2000-01-01') ;
insert into Dates values('2000-05-01') ;
insert into Dates values('2000-05-08') ;
insert into Dates values('2000-07-14') ;
insert into Dates values('2000-08-15') ;
insert into Dates values('2000-11-01') ;
insert into Dates values('2000-11-11') ;
insert into Dates values('2000-12-25') ;
