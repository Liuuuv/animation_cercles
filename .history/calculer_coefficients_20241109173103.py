import numpy as np
import matplotlib.pyplot as plt
from skimage import color, feature, io, filters
from scipy import ndimage


def calculer_coefficients():
    # Charger l'image et la convertir en niveaux de gris
    # image = io.imread('C:/Users/olivi/kDrive/projets/loisir/image/rui_tachibana2.png')  # Remplace par le chemin de ton image
    image=io.imread('C:/Users/olivi/Downloads/caca.png')
    resolution=(len(image[0]),len(image))
    gray_image = color.rgb2gray(image)

    # Appliquer un filtre pour lisser et réduire le bruit
    smoothed_image = filters.gaussian(gray_image, sigma=1)

    # Détecter les contours avec l'algorithme de Canny
    edges = feature.canny(smoothed_image, sigma=0.6)

    # Extraire les coordonnées des points du contour
    y, x = np.nonzero(edges)  # y et x représentent les coordonnées des pixels du contour

    # Convertir les points du contour en coordonnées complexes
    contour_points = x-(resolution[0]/2) + 1j * (y-(resolution[1]/2))

    # Utiliser un ordre de parcours par proximité pour assurer une continuité du contour
    # Initialisation du tableau pour les points ordonnés
    ordered_contour_points = [contour_points[0]]
    contour_points = np.delete(contour_points, 0)  # Retirer le point de départ de contour_points

    while len(contour_points) > 0:
        last_point = ordered_contour_points[-1]
        # Calculer les distances vers tous les autres points restants
        distances = np.abs(contour_points - last_point)
        # Trouver le point le plus proche suivant
        nearest_index = np.argmin(distances)
        ordered_contour_points.append(contour_points[nearest_index])
        contour_points = np.delete(contour_points, nearest_index)

    # Convertir en tableau pour le tracé
    ordered_contour_points = np.array(ordered_contour_points)

    # Définir le facteur de réduction
    reduction_factor = 1  # Ajustez pour obtenir le nombre de points souhaité

    # Sélectionner un point tous les 'reduction_factor' indices
    reduced_contour_points = ordered_contour_points[::reduction_factor]





    # Tracer les points avec des annotations
    plt.figure(figsize=(6, 6))
    plt.scatter(np.real(reduced_contour_points), np.imag(reduced_contour_points), marker='.')

    # # Ajouter une annotation avec le numéro de chaque point
    # for idx, point in enumerate(reduced_contour_points):
    #     plt.text(np.real(point), np.imag(point), str(idx), fontsize=8, color='red')

    plt.gca().invert_yaxis()
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()
    
    return reduced_contour_points

if __name__=='__main__':
    calculer_coefficients()
