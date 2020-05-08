"""
Dodaj bota
"""


import szachy_modul
import pygame

gra = True

while gra:
    U = True
    obrot = False
    pygame.init()
    poz = 'TT'
    done = False
    W = False
    clock = pygame.time.Clock()
    plansza = szachy_modul.Plansza()
    plansza.maluj()
    pygame.display.flip()
    pygame.display.set_caption("Szachy")
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                gra = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if not W and U is False:
                    poz = plansza.gdzie_klikniecie(x, y, obrot)
                elif U:
                    if y < 325:
                        obrot = True
                        U = False
                    else:
                        obrot = False
                        U = False
                else:
                    if 8 <= x <= 225 and 273 <= y <= 359:
                        gra = True
                        done = True
                    elif 415 <= x <= 625 and 273 <= y <= 359:
                        gra = False
                        done = True

        if not W and U is False:

            plansza.maluj()
            if obrot is True:
                plansza.obroc()
            plansza.zaznaczony(poz)
            if plansza.czy_K_B('C') or plansza.czy_K_B('B'):
                plansza.czy_szach()
                W = plansza.czy_mat()
            else:
                plansza.B_szach = False
                plansza.C_szach = False
                plansza.B_r_szach = 0
                plansza.C_r_szach = 0
            pygame.display.flip()
        elif U is True:

            plansza.screen.blit(pygame.image.load('ustawienia.png'), (0, 0))
            pygame.display.flip()
        else:
            plansza.screen.blit(pygame.image.load(plansza.win + '_wygrana.png'), (0, 0))
            pygame.display.flip()
        clock.tick(60)
