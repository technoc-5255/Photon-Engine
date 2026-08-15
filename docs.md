1. Une caméra lance un rayon pour chaque pixel

Imagine une caméra devant une scène 3D :

                    Objet
                     ●
                    / \
                   /   \
                  /     \
Caméra          /        \
  📷 ──────────→──────────→
        rayon lumineux

        écran
┌─────────────────────┐
│ · · · · · · · · · · │
│ · · · · · · · · · · │
│ · · · · · · · · · · │
└─────────────────────┘

Pour chaque pixel de l'image, on crée un rayon :

rayon = origine + direction

L'origine est généralement la position de la caméra.

2. On cherche ce que le rayon touche

Supposons qu'on ait une sphère.

Pour chaque rayon, on cherche s'il intersecte la sphère.

                  ● sphère
              .-'''''''-.
            .'           '.
           /               \
Caméra ● ───────────X───────→
                   ↑
             intersection

S'il ne touche rien → pixel noir ou couleur du ciel.

S'il touche la sphère → on doit déterminer sa couleur.

3. Calculer la normale

Au point d'intersection, on calcule la normale à la surface.

Pour une sphère, c'est assez simple :

              ●
             /│
            / │ normale
           /  ↓
          X

Mathématiquement :

normal = point - centre
normal = normal / longueur(normal)

La normale est importante pour savoir comment la lumière arrive sur la surface.

4. Calculer l'éclairage

Imaginons une lampe :

       💡
        \
         \
          \ lumière
           \
            X
           / \
          /   \
       objet

On calcule l'angle entre :

la normale de la surface
la direction vers la lumière

On utilise généralement un produit scalaire :

intensite = max(0, normal.dot(direction_lumiere))

Si la surface regarde directement la lumière :

intensité ≈ 1

Si elle est perpendiculaire :

intensité ≈ 0

Cela permet déjà de faire une sphère avec un éclairage réaliste.

5. Ajouter les ombres

C'est là que ça devient intéressant.

Une fois qu'on connaît le point touché, on lance un deuxième rayon vers la lumière.

             💡
              \
               \
                X
               / \
              /   \
             ●     \
           objet    \
                     \

Si ce rayon rencontre un autre objet avant d'atteindre la lumière :

💡
 \
  \
   ● obstacle
    \
     X surface

alors le point est dans l'ombre.

6. Les réflexions

On peut ensuite lancer un nouveau rayon dans la direction réfléchie.

             rayon incident
                    \
                     \
                      X
                     / \
                    /   \ rayon réfléchi
                   /
              surface

La direction de réflexion peut être calculée avec :

reflection = direction - 2 * direction.dot(normal) * normal

On lance ensuite un nouveau rayon dans cette direction.

C'est ce mécanisme qui permet d'obtenir des miroirs.

7. En Python

Pour commencer, je te conseille d'utiliser NumPy uniquement pour les vecteurs, et de faire le ray tracer toi-même.

Tu peux créer une classe :

class Vec3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

Puis représenter un rayon :

class Ray:
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction

Et une sphère :

class Sphere:
    def __init__(self, center, radius, color):
        self.center = center
        self.radius = radius
        self.color = color

Ton programme principal ferait alors quelque chose comme :

pour chaque pixel :

    créer un rayon depuis la caméra

    trouver l'objet touché

    si aucun objet :
        pixel = couleur du ciel

    sinon :
        calculer le point d'intersection
        calculer la normale
        calculer l'éclairage
        vérifier les ombres

        pixel = couleur calculée

Et à la fin tu sauvegardes les pixels dans une image PNG.

🔥 Le plus intéressant pour ton projet

Tu peux construire ton ray tracer progressivement :

Étape 1 → une sphère rouge sur fond noir
Étape 2 → plusieurs sphères
Étape 3 → éclairage
Étape 4 → ombres
Étape 5 → réflexions
Étape 6 → plusieurs sources lumineuses
Étape 7 → matériaux
Étape 8 → triangles et modèles 3D .obj
Étape 9 → anti-aliasing
Étape 10 → parallélisation CPU
Étape 11 → accélération GPU

Et là, tu as un vrai projet de computing : le rendu d'une image peut nécessiter des millions de calculs d'intersection.

Si tu veux, je peux aussi te montrer comment coder un ray tracer minimal en Python d'environ 100 lignes, avec une sphère, une lumière et des ombres, puis t'expliquer chaque partie.
