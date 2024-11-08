import pygame as py
import math
import random as rd
import time

py.init()



blanc=(255,255,255)
noir=(0,0,0)

rouge=(255,0,0)
vert=(0,255,0)
bleu=(0,0,255)

phi=0.5*(math.sqrt(5)+1)

class Cercle:
    def __init__(self,rayon,vitesse):
        self.vitesse=vitesse
        self.rayon=rayon
        self.pos=None
        self.angle=0

class Marqueur:
    def __init__(self):
        self.pos=[0,0]



class Affichage:
    def __init__(self,facteur):
        self.dimensions=(int(1920*facteur),int(1080*facteur))
        self.fenetre=py.display.set_mode(self.dimensions)
        self.centre=(self.dimensions[0]//2+70,self.dimensions[1]//2)
        self.nb_cercles=nb_cercles


        self.marqueur=Marqueur()

        self.dt=1/120

        self.liste_cercles=[]
        self.liste_rayons=[1,2,3]
        self.liste_points=[]
        
        self.nb_cercles=len(self.liste_rayons)

        self.initialiser_cercles()


    def creer_cercle(self,rayon,vitesse):
        cercle=Cercle(rayon,vitesse)
        self.liste_cercles.append(cercle)
        return cercle

    def initialiser_cercles(self):
        pos=[self.centre[0],self.centre[1]]
        for n in range(0,self.nb_cercles):
            cercle=self.creer_cercle(self.liste_rayons[n],n)
            cercle.pos=pos[:]
            pos[0]+=cercle.rayon

    def mettre_a_jour_cercles(self):
        for i in range(0,len(self.liste_cercles)):
            # if i==0:
            #     continue
            if i!=0:
                self.liste_cercles[i].pos[0]=self.liste_cercles[i-1].pos[0]+self.liste_cercles[i-1].rayon*math.cos(self.liste_cercles[i-1].angle)
                self.liste_cercles[i].pos[1]=self.liste_cercles[i-1].pos[1]+self.liste_cercles[i-1].rayon*math.sin(self.liste_cercles[i-1].angle)

            self.liste_cercles[i].angle+=self.liste_cercles[i].vitesse*self.dt

    def mettre_a_jour_marqueur(self):

        self.marqueur.pos[0]=self.liste_cercles[-1].pos[0]+self.liste_cercles[-1].rayon*math.cos(self.liste_cercles[-1].angle)
        self.marqueur.pos[1]=self.liste_cercles[-1].pos[1]+self.liste_cercles[-1].rayon*math.sin(self.liste_cercles[-1].angle)

        self.liste_points.append(self.marqueur.pos[:])



    def dessiner(self):
        for i in range(len(self.liste_points)-1):
            py.draw.line(self.fenetre,rouge,self.liste_points[i],self.liste_points[i+1],2)

        py.draw.circle(self.fenetre,bleu,self.marqueur.pos,2)

    def dessiner_cercles(self):
        for cercle in self.liste_cercles:
            py.draw.circle(self.fenetre,noir,cercle.pos,2)
            py.draw.circle(self.fenetre,noir,cercle.pos,abs(cercle.rayon),1)

    def loop(self):
        horloge=py.time.Clock()

        police=py.font.Font(None, 36)

        # boucle de jeu
        continuer=True
        # time.sleep(0.3)
        while continuer:
            for event in py.event.get():
                if event.type==py.QUIT:
                    continuer=False
                if event.type==py.KEYDOWN:
                    if event.key==py.K_ESCAPE:
                        continuer=False
            horloge.tick(120)
            py.display.set_caption(str(round(horloge.get_fps(),1)))


            self.fenetre.fill(blanc)

            self.dessiner_cercles()
            self.dessiner()

            self.mettre_a_jour_cercles()
            self.mettre_a_jour_marqueur()



            # texte_surface1 = police.render("number of circles: "+str(nb_cercles-1),False,noir)
            # self.fenetre.blit(texte_surface1,(655,200))

            py.display.flip()

        py.quit()


nb_cercles=5




facteur=0.8

affichage=Affichage(facteur)
affichage.loop()