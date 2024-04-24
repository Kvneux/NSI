import pygame
from random import randint
import time
import random


pygame.init()
largeur, hauteur = 800, 600
monEcran = pygame.display.set_mode((largeur, hauteur))
horloge = pygame.time.Clock()

# Couleurs
COULEUR_FOND = (100, 40, 70)
COULEUR_VAISSEAU = (100, 100, 100)
COULEUR_ASTEROIDE = (255, 255, 255)
COULEUR_MUNITION = (255, 0, 0)
COULEUR_SCORE = (255, 255, 255)
COULEUR_FIN = (0, 0, 0)
COULEUR_TEXTE_FIN = (255, 255, 255)
COULEUR_TEXTE_ACCUEIL = (255, 255, 255)
COULEUR_BARRE_VIE = (0, 255, 0)

# Dimensions
LARGEUR_VAISSEAU = 30
HAUTEUR_VAISSEAU = 80
LARGEUR_BOSS = 100
HAUTEUR_BOSS = 100

# Liste des positions des astéroïdes
asteroides = []

# Liste des positions des munitions
munitions = []

# Score
score = 0
fonte = pygame.font.Font(None, 36)

# Fonte pour l'écran de fin
fonte_fin = pygame.font.Font(None, 50)

# Nombre de munitions initial
munitions_disponibles = 10

# Temps écoulé depuis le dernier rechargement de munitions
temps_dernier_rechargement = time.time()

# Temps écoulé depuis le début du niveau
temps_debut_niveau = 0

# Classement des temps
classement_temps = []

# Boss
boss_x = largeur - LARGEUR_BOSS
boss_y = hauteur // 2 - HAUTEUR_BOSS // 2
boss_vie = 50  # Modifier la santé du boss
boss_y = hauteur // 2 - HAUTEUR_BOSS // 2

# Variables pour le mouvement du boss
boss_vitesse = 2
direction_boss = 1  # 1 pour descendre, -1 pour monter

# Ajout des variables pour l'invincibilité du boss
boss_invincible = False
temps_invincible_debut = 0
TEMPS_INVINCIBILITE = 5  # Durée en secondes d'invincibilité
pygame.init()
largeur, hauteur = 800, 600
monEcran = pygame.display.set_mode((largeur, hauteur))
horloge = pygame.time.Clock()

# Couleurs
COULEUR_FOND = (100, 40, 70)
COULEUR_VAISSEAU = (100, 100, 100)
COULEUR_ASTEROIDE = (255, 255, 255)
COULEUR_MUNITION = (255, 0, 0)
COULEUR_SCORE = (255, 255, 255)
COULEUR_FIN = (0, 0, 0)
COULEUR_TEXTE_FIN = (255, 255, 255)
COULEUR_TEXTE_ACCUEIL = (255, 255, 255)

# Dimensions
LARGEUR_VAISSEAU = 30
HAUTEUR_VAISSEAU = 80

# Listes
asteroides = []
munitions = []

# Scores
score = 0
fonte = pygame.font.Font(None, 36)

# Police pour l'écran de fin
fonte_fin = pygame.font.Font(None, 50)

# Nombre initial de munitions
munitions_disponibles = 10

# Temps depuis le dernier rechargement de munitions
temps_dernier_rechargement = time.time()

# Temps depuis le début du niveau
temps_debut_niveau = 0

# Classements pour les deux niveaux
classement_temps = {"epsilon": [], "zeta": []}


def dessiner_jeu(en_bas):
    monEcran.fill(COULEUR_FOND)
    pygame.draw.rect(
        monEcran, COULEUR_VAISSEAU, (posx, posy, LARGEUR_VAISSEAU, HAUTEUR_VAISSEAU)
    )


def dessiner_asteroide(cx, cy, taille):
    pygame.draw.rect(monEcran, COULEUR_ASTEROIDE, (cx, cy, taille, taille))


def dessiner_munition(mx, my):
    pygame.draw.circle(monEcran, COULEUR_MUNITION, (mx, my), 5)


def afficher_score(score, munitions_disponibles):
    texte_score = fonte.render("Score : " + str(score), True, COULEUR_SCORE)
    texte_munitions = fonte.render(
        "Munitions : " + str(munitions_disponibles), True, COULEUR_SCORE
    )
    monEcran.blit(texte_score, (10, 10))
    monEcran.blit(texte_munitions, (10, 50))


def afficher_fin(message, niveau, temps_ecoule=None):
    monEcran.fill(COULEUR_FIN)
    texte_fin = fonte_fin.render(message, True, COULEUR_TEXTE_FIN)
    if niveau == "epsilon" and temps_ecoule:
        texte_temps = fonte_fin.render(
            f"Temps : {temps_ecoule:.2f} secondes", True, COULEUR_TEXTE_FIN
        )
        monEcran.blit(
            texte_temps, (largeur // 2 - texte_temps.get_width() // 2, hauteur // 2)
        )
    if niveau == "sigma" and temps_ecoule:
        texte_temps = fonte_fin.render(
            f"Temps : {temps_ecoule:.2f} secondes", True, COULEUR_TEXTE_FIN
        )
        monEcran.blit(
            texte_temps, (largeur // 2 - texte_temps.get_width() // 2, hauteur // 2)
        )
    elif niveau == "zeta" and temps_ecoule:
        texte_temps = fonte_fin.render(
            f"Survécu : {temps_ecoule:.2f} secondes", True, COULEUR_TEXTE_FIN
        )
        monEcran.blit(
            texte_temps, (largeur // 2 - texte_temps.get_width() // 2, hauteur // 2)
        )
    monEcran.blit(
        texte_fin, (largeur // 2 - texte_fin.get_width() // 2, hauteur // 2 - 50)
    )
    texte_continuer = fonte.render(
        "Appuyez sur n'importe quelle touche pour retourner à l'écran d'accueil...",
        True,
        COULEUR_SCORE,
    )
    monEcran.blit(
        texte_continuer,
        (largeur // 2 - texte_continuer.get_width() // 2, hauteur // 2 + 50),
    )
    pygame.display.flip()
    attendre_touche()


def afficher_classement():
    monEcran.fill(COULEUR_FOND)
    texte_classement = fonte_fin.render("Classement", True, COULEUR_TEXTE_ACCUEIL)
    monEcran.blit(
        texte_classement, (largeur // 2 - texte_classement.get_width() // 2, 50)
    )
    y_position_epsilon = 150
    for temps_epsilon in classement_temps["epsilon"]:
        texte_temps_epsilon = fonte.render(
            f"Epsilon : {temps_epsilon:.2f} secondes", True, COULEUR_SCORE
        )
        monEcran.blit(
            texte_temps_epsilon,
            (largeur // 4 - texte_temps_epsilon.get_width() // 2, y_position_epsilon),
        )
        y_position_epsilon += 40

    y_position_zeta = 150
    for temps_zeta in classement_temps["zeta"]:
        texte_temps_zeta = fonte.render(
            f"Zeta : {temps_zeta:.2f} secondes", True, COULEUR_SCORE
        )
        monEcran.blit(
            texte_temps_zeta,
            (largeur * 3 // 4 - texte_temps_zeta.get_width() // 2, y_position_zeta),
        )
        y_position_zeta += 40

    # Bouton "Retour"
    texte_retour = fonte_fin.render("Retour", True, COULEUR_TEXTE_ACCUEIL)
    bouton_retour = pygame.Rect(
        largeur // 2 - texte_retour.get_width() // 2,
        hauteur - 100,
        texte_retour.get_width(),
        texte_retour.get_height(),
    )
    pygame.draw.rect(monEcran, (255, 255, 255), bouton_retour, 2)
    monEcran.blit(
        texte_retour, (largeur // 2 - texte_retour.get_width() // 2, hauteur - 100)
    )

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if bouton_retour.collidepoint(event.pos):
                        return
            elif event.type == pygame.KEYDOWN:
                return


def ecran_accueil():
    monEcran.fill(COULEUR_FOND)
    texte_titre = fonte_fin.render(
        "Choisissez un niveau :", True, COULEUR_TEXTE_ACCUEIL
    )
    texte_epsilon = fonte_fin.render("Niveau Epsilon", True, COULEUR_TEXTE_ACCUEIL)
    texte_zeta = fonte_fin.render("Niveau Zeta", True, COULEUR_TEXTE_ACCUEIL)
    texte_sigma = fonte_fin.render(
        "Niveau Sigma", True, COULEUR_TEXTE_ACCUEIL
    )  # Changement du texte du bouton

    monEcran.blit(
        texte_titre, (largeur // 2 - texte_titre.get_width() // 2, hauteur // 2 - 150)
    )

    # Coordonnées et dimensions du bouton "Niveau Epsilon"
    bouton_epsilon = pygame.Rect(
        largeur // 2 - texte_epsilon.get_width() // 2,
        hauteur // 2 - 50,
        texte_epsilon.get_width(),
        texte_epsilon.get_height(),
    )
    pygame.draw.rect(monEcran, (255, 255, 255), bouton_epsilon, 2)
    monEcran.blit(
        texte_epsilon,
        (largeur // 2 - texte_epsilon.get_width() // 2, hauteur // 2 - 50),
    )

    # Coordonnées et dimensions du bouton "Niveau Zeta"
    bouton_zeta = pygame.Rect(
        largeur // 2 - texte_zeta.get_width() // 2,
        hauteur // 2 + 50,
        texte_zeta.get_width(),
        texte_zeta.get_height(),
    )
    pygame.draw.rect(monEcran, (255, 255, 255), bouton_zeta, 2)
    monEcran.blit(
        texte_zeta, (largeur // 2 - texte_zeta.get_width() // 2, hauteur // 2 + 50)
    )
    # Définir les coordonnées et dimensions du bouton "Niveau Sigma"
    bouton_sigma = pygame.Rect(
        largeur // 2 - texte_sigma.get_width() // 2,
        hauteur // 2 + 150,
        texte_sigma.get_width(),
        texte_sigma.get_height(),
    )  # Renommer la variable
    pygame.draw.rect(monEcran, (255, 255, 255), bouton_sigma, 2)  # Renommer la variable
    monEcran.blit(
        texte_sigma, (largeur // 2 - texte_sigma.get_width() // 2, hauteur // 2 + 150)
    )  # Renommer la variable

    # Bouton "Classement"
    texte_classement = fonte_fin.render("Classement", True, COULEUR_TEXTE_ACCUEIL)
    bouton_classement = pygame.Rect(
        largeur // 2 - texte_classement.get_width() // 2,
        hauteur // 2 + 250,
        texte_classement.get_width(),
        texte_classement.get_height(),
    )
    pygame.draw.rect(monEcran, (255, 255, 255), bouton_classement, 2)
    monEcran.blit(
        texte_classement,
        (largeur // 2 - texte_classement.get_width() // 2, hauteur // 2 + 250),
    )

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    return "epsilon"
                if (
                    event.key == pygame.K_s
                ):  # Changer la touche pour accéder au niveau "Sigma"
                    return "sigma"  # Renommer le niveau
                elif event.key == pygame.K_z:
                    return "zeta"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if bouton_epsilon.collidepoint(event.pos):
                        return "epsilon"
                    elif bouton_zeta.collidepoint(event.pos):
                        return "zeta"
                    elif bouton_sigma.collidepoint(event.pos):
                        return "sigma"
                    elif bouton_classement.collidepoint(event.pos):
                        afficher_classement()
                        return
            elif event.type == pygame.QUIT:
                pygame.quit()
                return None


def ecran_pause():
    monEcran.fill(COULEUR_FOND)
    texte_pause = fonte_fin.render("Pause", True, COULEUR_TEXTE_ACCUEIL)
    monEcran.blit(
        texte_pause, (largeur // 2 - texte_pause.get_width() // 2, hauteur // 2)
    )
    pygame.display.flip()
    attendre_touche()


def attendre_touche():
    attente = True
    while attente:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                attente = False
                return


def collision(ast_x, ast_y, taille_ast, mun_x, mun_y):
    return (mun_x >= ast_x and mun_x <= ast_x + taille_ast) and (
        mun_y >= ast_y and mun_y <= ast_y + taille_ast
    )


def collision_astéroide(mun_x, mun_y, ast_x, ast_y, taille_ast):
    return (mun_x >= ast_x and mun_x <= ast_x + taille_ast) and (
        mun_y >= ast_y and mun_y <= ast_y + taille_ast
    )


def collision_vaisseau(
    ast_x, ast_y, taille_ast, vaisseau_x, vaisseau_y, largeur_vaisseau, hauteur_vaisseau
):
    return (
        vaisseau_x + largeur_vaisseau >= ast_x and vaisseau_x <= ast_x + taille_ast
    ) and (vaisseau_y + hauteur_vaisseau >= ast_y and vaisseau_y <= ast_y + taille_ast)


def collision_boss(mun_x, mun_y):
    if boss_invincible:
        return False
    return (mun_x >= boss_x and mun_x <= boss_x + LARGEUR_BOSS) and (
        mun_y >= boss_y and mun_y <= boss_y + HAUTEUR_BOSS
    )


def dessiner_boss():
    if boss_invincible:
        pygame.draw.rect(
            monEcran, (255, 0, 0), (boss_x, boss_y, LARGEUR_BOSS, HAUTEUR_BOSS)
        )  # Rouge quand invincible
    else:
        pygame.draw.rect(
            monEcran, COULEUR_VAISSEAU, (boss_x, boss_y, LARGEUR_BOSS, HAUTEUR_BOSS)
        )


def afficher_barre_vie():
    pygame.draw.rect(
        monEcran, COULEUR_BARRE_VIE, (largeur - 120, 10, boss_vie * 2, 20)
    )  # Largeur multipliée par 2 pour correspondre à 50 PV


def main():
    global posx, posy, asteroides, score, munitions, munitions_disponibles, temps_dernier_rechargement, temps_debut_niveau, classement_temps, munitions_disponibles, temps_dernier_rechargement, temps_debut_niveau, classement_temps, boss_x, boss_y, boss_vie, boss_invincible, temps_invincible_debut
    jeu_en_cours = True
    posx = 255
    posy = 250
    game_over = False
    en_pause = False
    temps_derniere_munition = time.time()

    while jeu_en_cours:
        niveau = ecran_accueil()
        if niveau == "sigma":  # Renommer le niveau
            score = 0
            asteroides = []
            munitions = []
            munitions_disponibles = 100
            temps_dernier_rechargement = time.time()
            temps_debut_niveau = time.time()
            game_over = False
            boss_vie = 50
            boss_invincible = False

            while not game_over:
                horloge.tick(60)

                keys = pygame.key.get_pressed()

                if keys[pygame.K_ESCAPE]:
                    ecran_pause()
                    en_pause = True

                if not en_pause:
                    if keys[pygame.K_DOWN] and posy < hauteur - HAUTEUR_VAISSEAU:
                        posy += 5
                    if keys[pygame.K_UP] and posy > 0:
                        posy -= 5
                    if keys[pygame.K_RIGHT] and posx < largeur - LARGEUR_VAISSEAU:
                        posx += 5
                    if keys[pygame.K_LEFT] and posx > 0:
                        posx -= 5

                    monEcran.fill(COULEUR_FOND)

                    en_bas = keys[pygame.K_DOWN]
                    dessiner_jeu(en_bas)

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            jeu_en_cours = False

                        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                            if munitions_disponibles > 0:
                                munitions.append(
                                    (
                                        posx + LARGEUR_VAISSEAU,
                                        posy + HAUTEUR_VAISSEAU // 2,
                                    )
                                )
                                munitions_disponibles -= 1

                    for asteroide in asteroides:
                        dessiner_asteroide(*asteroide)

                    for munition in munitions:
                        dessiner_munition(*munition)

                    munitions = [(mx + 10, my) for mx, my in munitions]

                    for munition in munitions:
                        if collision_boss(*munition):
                            munitions.remove(munition)
                            boss_vie -= 1
                            if boss_vie <= 0:
                                game_over = True
                                break

                    if (
                        randint(0, 100) < 7 + score // 100
                    ):  # Augmentation de la densité des astéroïdes
                        taille_asteroide = randint(20, 100)
                        asteroides.append(
                            (largeur, randint(0, hauteur - 30), taille_asteroide)
                        )

                    temps_actuel = time.time()
                    if temps_actuel - temps_dernier_rechargement > 5:
                        munitions_disponibles += 1
                        temps_dernier_rechargement = temps_actuel

                    # Ajout de munitions toutes les 2 secondes
                    if temps_actuel - temps_derniere_munition > 2:
                        munitions_disponibles += 1
                        temps_derniere_munition = temps_actuel

                    for asteroide in asteroides:
                        for munition in munitions:
                            if collision_astéroide(*munition, *asteroide):
                                asteroides.remove(asteroide)
                                munitions.remove(munition)
                                score += 10

                    for asteroide in asteroides:
                        if collision_vaisseau(
                            *asteroide, posx, posy, LARGEUR_VAISSEAU, HAUTEUR_VAISSEAU
                        ):
                            game_over = True
                            break

                    if boss_invincible:
                        if temps_actuel - temps_invincible_debut > TEMPS_INVINCIBILITE:
                            boss_invincible = False
                            boss_vie = 1  # Réinitialiser la vie du boss à 1
                            asteroides *= 3  # Triple le nombre d'astéroïdes

                    if boss_vie <= 0:
                        afficher_victoire()

                    afficher_score(score, munitions_disponibles)
                    dessiner_boss()
                    afficher_barre_vie()

                    pygame.display.update()

                    asteroides = [
                        (ast_x - 5, ast_y, taille_ast)
                        for ast_x, ast_y, taille_ast in asteroides
                        if ast_x > -30
                    ]

                    # Mouvement du boss
                    global direction_boss
                    global boss_vitesse
                    # Changer la direction du boss aléatoirement
                    if random.randint(0, 100) < 2:
                        direction_boss *= -1
                    # Changer la vitesse du boss aléatoirement
                    if random.randint(0, 100) < 5:
                        boss_vitesse = random.uniform(1, 3)
                    boss_y += boss_vitesse * direction_boss
                    if boss_y <= 0 or boss_y >= hauteur - HAUTEUR_BOSS:
                        direction_boss *= -1

                if game_over:
                    afficher_fin("Game Over", niveau)

        if niveau in ("epsilon", "zeta"):
            score = 0
            asteroides = []
            munitions = []
            munitions_disponibles = 10
            temps_dernier_rechargement = time.time()
            temps_debut_niveau = time.time()
            game_over = False

            while not game_over:
                horloge.tick(60)

                touches = pygame.key.get_pressed()

                if touches[pygame.K_ESCAPE]:
                    ecran_pause()
                    en_pause = True

                if not en_pause:
                    if touches[pygame.K_DOWN] and posy < hauteur - HAUTEUR_VAISSEAU:
                        posy += 5
                    if touches[pygame.K_UP] and posy > 0:
                        posy -= 5
                    if touches[pygame.K_RIGHT] and posx < largeur - LARGEUR_VAISSEAU:
                        posx += 5
                    if touches[pygame.K_LEFT] and posx > 0:
                        posx -= 5

                    monEcran.fill(COULEUR_FOND)

                    en_bas = touches[pygame.K_DOWN]
                    dessiner_jeu(en_bas)

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            jeu_en_cours = False

                        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                            if munitions_disponibles > 0:
                                munitions.append(
                                    (
                                        posx + LARGEUR_VAISSEAU,
                                        posy + HAUTEUR_VAISSEAU // 2,
                                    )
                                )
                                munitions_disponibles -= 1

                    for asteroide in asteroides:
                        dessiner_asteroide(*asteroide)

                    for munition in munitions:
                        dessiner_munition(*munition)

                    munitions = [(mx + 10, my) for mx, my in munitions]

                    for munition in munitions:
                        for asteroide in asteroides:
                            if collision(*asteroide, *munition):
                                asteroides.remove(asteroide)
                                munitions.remove(munition)
                                score += 10
                                munitions_disponibles += 1

                    if randint(0, 100) < 3:
                        taille_asteroide = randint(20, 100)
                        asteroides.append(
                            (largeur, randint(0, hauteur - 30), taille_asteroide)
                        )

                    if niveau == "zeta":
                        score = int(time.time() - temps_debut_niveau)

                    temps_actuel = time.time()
                    if temps_actuel - temps_dernier_rechargement > 5:
                        munitions_disponibles += 1
                        temps_dernier_rechargement = temps_actuel

                    for asteroide in asteroides:
                        if collision_vaisseau(
                            *asteroide, posx, posy, LARGEUR_VAISSEAU, HAUTEUR_VAISSEAU
                        ):
                            game_over = True
                            break

                    afficher_score(score, munitions_disponibles)

                    pygame.display.update()

                    asteroides = [
                        (ast_x - 5, ast_y, taille_ast)
                        for ast_x, ast_y, taille_ast in asteroides
                        if ast_x > -30
                    ]

                    if score >= 150 and niveau == "epsilon":
                        fin_temps = time.time()
                        temps_ecoule = fin_temps - temps_debut_niveau
                        classement_temps[niveau].append(temps_ecoule)
                        classement_temps[niveau].sort()
                        classement_temps[niveau] = classement_temps[niveau][:5]
                        afficher_fin(
                            "Félicitations ! Atteint 150 points.", niveau, temps_ecoule
                        )
                        game_over = True

                    if game_over:
                        if niveau == "epsilon":
                            if score < 150:
                                afficher_fin("Partie terminée", niveau)
                        else:
                            fin_temps = time.time()
                            temps_ecoule = fin_temps - temps_debut_niveau
                            classement_temps[niveau].append(temps_ecoule)
                            classement_temps[niveau].sort(reverse=True)
                            classement_temps[niveau] = classement_temps[niveau][:5]
                            afficher_fin("Partie terminée", niveau, temps_ecoule)

    pygame.quit()


main()
