import pygame as py
import numpy as np
import scipy.integrate

py.init()

# Couleurs
blanc = (255, 255, 255)
noir = (0, 0, 0)
rouge = (255, 0, 0)
bleu = (0, 0, 255)

FPS = 144
ECHELLE = 15  # Ajuster pour mieux correspondre à l'écran

class Cercle:
    def __init__(self, rayon, vitesse):
        self.vitesse = vitesse
        self.rayon = rayon
        self.pos = None
        self.angle = 0

class Marqueur:
    def __init__(self):
        self.pos = [0, 0]

class Affichage:
    def __init__(self, facteur):
        self.dimensions = (int(1920 * facteur), int(1080 * facteur))
        self.fenetre = py.display.set_mode(self.dimensions)
        self.centre = (self.dimensions[0] // 2, self.dimensions[1] // 2)
        self.nb_cercles = nb_cercles
        self.marqueur = Marqueur()
        self.dt = 1 / FPS
        self.liste_cercles = []
        self.liste_rayons = []
        self.liste_phases = []
        self.liste_points = []
        self.calculer_coefficients()
        self.initialiser_cercles()

    def creer_cercle(self, rayon, vitesse):
        cercle = Cercle(rayon, vitesse)
        self.liste_cercles.append(cercle)
        return cercle

    def initialiser_cercles(self):
        pos = list(self.centre)
        for n in range(2 * self.nb_cercles):
            if n % 2 == 0:
                cercle = self.creer_cercle(self.liste_rayons[n] * ECHELLE, n / 2)
            else:
                cercle = self.creer_cercle(self.liste_rayons[n] * ECHELLE, -(n + 1) / 2)
            pos[0] += cercle.rayon * np.cos(self.liste_phases[n])
            pos[1] += cercle.rayon * np.sin(self.liste_phases[n])
            cercle.pos = pos[:]

    def mettre_a_jour_cercles(self):
        self.liste_cercles[0].angle += self.liste_cercles[0].vitesse * self.dt
        for i in range(1, 2 * self.nb_cercles):
            self.liste_cercles[i].pos[0] = (self.liste_cercles[i - 1].pos[0] +
                                            self.liste_cercles[i - 1].rayon * np.cos(self.liste_cercles[i - 1].angle))
            self.liste_cercles[i].pos[1] = (self.liste_cercles[i - 1].pos[1] +
                                            self.liste_cercles[i - 1].rayon * np.sin(self.liste_cercles[i - 1].angle))
            self.liste_cercles[i].angle += self.liste_cercles[i].vitesse * self.dt

    def mettre_a_jour_marqueur(self):
        dernier = self.liste_cercles[-1]
        self.marqueur.pos[0] = dernier.pos[0] + dernier.rayon * np.cos(dernier.angle)
        self.marqueur.pos[1] = dernier.pos[1] + dernier.rayon * np.sin(dernier.angle)
        self.liste_points.append(self.marqueur.pos[:])

    def dessiner(self):
        for i in range(len(self.liste_points) - 1):
            py.draw.line(self.fenetre, rouge, self.liste_points[i], self.liste_points[i + 1], 2)
        py.draw.circle(self.fenetre, bleu, (int(self.marqueur.pos[0]), int(self.marqueur.pos[1])), 2)

    def dessiner_cercles(self):
        for cercle in self.liste_cercles:
            py.draw.circle(self.fenetre, noir, (int(cercle.pos[0]), int(cercle.pos[1])), abs(int(cercle.rayon)), 1)

    def fonction(self, t):
        x = 16 * np.sin(t)**3
        y = 13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t)
        return x + 1j * y  # Combinaison en forme complexe pour Fourier

    def calculer_coefficients(self):
        for i in range(2 * self.nb_cercles):
            n = i // 2 if i % 2 == 0 else -(i + 1) // 2
            re = scipy.integrate.quad(lambda t: self.fonction(t).real * np.cos(n * t), 0, 2 * np.pi)[0]
            im = scipy.integrate.quad(lambda t: self.fonction(t).imag * np.sin(n * t), 0, 2 * np.pi)[0]
            coefficient = (re + 1j * im) / (2 * np.pi)
            self.liste_rayons.append(abs(coefficient))
            self.liste_phases.append(np.angle(coefficient))

    def loop(self):
        horloge = py.time.Clock()
        continuer = True
        while continuer:
            for event in py.event.get():
                if event.type == py.QUIT or (event.type == py.KEYDOWN and event.key == py.K_ESCAPE):
                    continuer = False

            self.fenetre.fill(blanc)
            self.dessiner_cercles()
            self.dessiner()
            self.mettre_a_jour_cercles()
            self.mettre_a_jour_marqueur()

            py.display.flip()
            horloge.tick(FPS)

        py.quit()

# Configuration
nb_cercles = 50  # Augmenté pour une meilleure approximation
facteur = 0.8
affichage = Affichage(facteur)
affichage.loop()
