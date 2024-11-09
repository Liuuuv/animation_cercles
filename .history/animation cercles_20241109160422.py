import pygame as py
import math
import random as rd
import time
import scipy
import numpy as np
import scipy.integrate
from calculer_coefficients import c

py.init()



blanc=(255,255,255)
noir=(0,0,0)

rouge=(255,0,0)
vert=(0,255,0)
bleu=(0,0,255)


FPS=144
ECHELLE=10


class Cercle:
    def __init__(self,rayon,vitesse,angle):
        self.vitesse=vitesse
        self.rayon=rayon
        self.pos=None
        self.angle=angle

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

        self.dt=1/FPS

        self.liste_cercles=[]
        self.liste_rayons=[]
        self.liste_phases=[]
        self.liste_points=[]
        
        self.calculer_coefficients()
        

        self.initialiser_cercles()


    def creer_cercle(self,rayon,vitesse,angle):
        cercle=Cercle(rayon,vitesse,angle)
        self.liste_cercles.append(cercle)
        return cercle

    def initialiser_cercles(self):
        pos=[self.centre[0],self.centre[1]]
        
        for n in range(2*self.nb_cercles):
            if n%2==0:
                cercle=self.creer_cercle(self.liste_rayons[n]*ECHELLE,n/2,self.liste_phases[n])
                pos[0]+=cercle.rayon*np.cos(self.liste_phases[n])
                pos[1]+=cercle.rayon*np.sin(self.liste_phases[n])
            else:
                cercle=self.creer_cercle(self.liste_rayons[n]*ECHELLE,-(n+1)/2,self.liste_phases[n])
                pos[0]+=cercle.rayon*np.cos(self.liste_phases[n])
                pos[1]+=cercle.rayon*np.sin(self.liste_phases[n])
            
            
            cercle.pos=pos[:]

    def mettre_a_jour_cercles(self):
        self.liste_cercles[0].angle+=self.liste_cercles[0].vitesse*self.dt
        for i in range(1,2*self.nb_cercles):
            self.liste_cercles[i].pos[0]=self.liste_cercles[i-1].pos[0]+self.liste_cercles[i-1].rayon*math.cos(self.liste_cercles[i-1].angle)
            self.liste_cercles[i].pos[1]=self.liste_cercles[i-1].pos[1]+self.liste_cercles[i-1].rayon*math.sin(self.liste_cercles[i-1].angle)

            self.liste_cercles[i].angle+=self.liste_cercles[i].vitesse*self.dt

    def mettre_a_jour_marqueur(self):

        self.marqueur.pos[0]=self.liste_cercles[-1].pos[0]+self.liste_cercles[-1].rayon*math.cos(self.liste_cercles[-1].angle)
        self.marqueur.pos[1]=self.liste_cercles[-1].pos[1]+self.liste_cercles[-1].rayon*math.sin(self.liste_cercles[-1].angle)

        self.liste_points.append(self.marqueur.pos[:])



    def dessiner(self):
        for i in range(len(self.liste_points)-1):
            py.draw.line(self.fenetre,rouge,self.liste_points[i],self.liste_points[i+1],4)

        py.draw.circle(self.fenetre,bleu,self.marqueur.pos,2)

    def dessiner_cercles(self):
        for cercle in self.liste_cercles:
            py.draw.circle(self.fenetre,noir,cercle.pos,2)
            py.draw.circle(self.fenetre,noir,cercle.pos,cercle.rayon,1)
    
    def fonction(self,t):
        # if t<=math.pi:
        #     return (-2*t/math.pi)+1
        # else:
        #     return (2*t/math.pi)-3
        
        # if t<np.pi/4:
        #     return (1-t/(np.pi/4))+(t/(np.pi/4))*(1+1j)
        # elif t<3*np.pi/4:
        #     return (1-t/(3*np.pi/4))*(1+1j)+(t/(3*np.pi/4))*(-1+1j)
        # elif t<5*np.pi/4:
        #     return (1-t/(5*np.pi/4))*(-1+1j)+(t/(5*np.pi/4))*(-1-1j)
        # elif t<7*np.pi/4:
        #     return (1-t/(7*np.pi/4))*(-1-1j)+(t/(7*np.pi/4))*(1-1j)
        # else:
        #     return (1-t/(2*np.pi))*(1-1j)+(t/(2*np.pi))
        
        # return np.cos(t)+1j*np.sin(t)
        
        x = 16 * np.sin(t)**3
        y = 13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t)
        return x + 1j * -y  # Combinaison en forme complexe pour Fourier
    
    def exp_complexe(self,t):
        return np.exp(1j*t)
    
    def calculer_coefficients(self):
        for i in range(2*self.nb_cercles):
            n = i // 2 if i % 2 == 0 else -(i + 1) // 2
            coefficient=scipy.integrate.quad(lambda t:(self.fonction(t)*self.exp_complexe(-n*t)).real,0,2*np.pi)[0] + 1j*scipy.integrate.quad(lambda t:(self.fonction(t)*self.exp_complexe(-n*t)).imag,0,2*np.pi)[0]
            coefficient/=2*np.pi
            
            # if i%2==1:
            #     coefficient=0
            
            # if n%2==1:
            #     coefficient=2/(n*np.pi*1j)
            # else:
            #     coefficient=0
                
            
            self.liste_rayons.append(abs(coefficient))
            self.liste_phases.append(np.angle(coefficient))
            
            
            
        # print(self.liste_phases)
        # print(self.liste_rayons)
        
        
        
        # x_values = np.linspace(-1, 1, num=self.nb_cercles)
        # # Calculer la transformée de Fourier discrète
        # coefficients = np.fft.fft([self.fonction(t) for t in x_values]) / len(x_values)
        
        
        # for n in range(self.nb_cercles):
        #     self.liste_rayons.append(abs(coefficients[n]))
        #     self.liste_phases.append(np.angle(coefficients[n]))
    
        
            

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
            horloge.tick(FPS)
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


nb_cercles=50




facteur=0.8

affichage=Affichage(facteur)
affichage.loop()