import pygame

pygame.init()


class Plansza():

    def __init__(self):
        # tworzenie ekranu
        self.screen = pygame.display.set_mode((655, 655))
        self.screen.blit(pygame.image.load("plansza.png"), (0, 0))
        pygame.display.update()

        # mechanika
        self.pozycje = []
        self.ruch = 1
        self.C_szach = False
        self.C_r_szach = 0
        self.B_szach = False
        self.B_r_szach = 0
        self.win = 'B'

        # tworzenie slownika bez pionow
        self.G_plansza = {}
        litery = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        liczby = ['1', '2', '3', '4', '5', '6', '7', '8']
        x_l = 22
        for i in litery:
            y_g = 558
            for j in liczby:
                self.G_plansza.setdefault(i + j, 0)
                self.G_plansza[i + j] = [x_l, y_g]
                y_g -= 77
            x_l += 77

        # dodawanie pionow
        for key in self.G_plansza.keys():
            if key[1] == '2':
                self.G_plansza[key].append(Bierka('pion', 'B', key))
            elif key[1] == '7':
                self.G_plansza[key].append(Bierka('pion', 'C', key))

        # dodawanie innych figur oprócz króla i hetmana
        biery = ['wieza', 'kon', 'goniec', 'goniec', 'kon', 'wieza']
        lit = ['A', 'B', 'C', 'F', 'G', 'H']
        n = ['1', 'B', '8', 'C']
        for j in range(0, 4, 2):
            for i in range(6):
                self.G_plansza[lit[i] + n[j]].append(Bierka(biery[i], n[j + 1], lit[i] + n[j]))

        # dodawanie króla i hetmana
        self.G_plansza['D1'].append(Bierka('hetman', 'B', 'D1'))
        self.G_plansza['E1'].append(Bierka('krol', 'B', 'E1'))
        self.G_plansza['E8'].append(Bierka('hetman', 'C', 'E8'))
        self.G_plansza['D8'].append(Bierka('krol', 'C', 'D8'))

        # pomocniczy klucz
        self.G_plansza.setdefault('TT', 0)
        self.G_plansza['TT'] = [0, 0]

    def maluj(self):  # wyswietla figury z G_slownik
        self.screen.blit(pygame.image.load("plansza.png"), (0, 0))
        for key in self.G_plansza.keys():
            if len(self.G_plansza[key]) == 3:
                self.screen.blit(self.G_plansza[key][2].name(), [self.G_plansza[key][0], self.G_plansza[key][1]])

    def czy_K_B(self, r):  # sprawdza czy król jest bity
        for key, value in self.G_plansza.items():
            if len(self.G_plansza[key]) == 3 and self.G_plansza[key][2].rodzaj != 'krol':
                if self.G_plansza[key][2].kolor == r:
                    if self.G_plansza[key][2].wyznacz_ruchy(self.G_plansza, T='Krol'):
                        return True
        return False

    def obroc(self):
        if self.ruch % 2 == 1:
            litery = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
            liczby = ['1', '2', '3', '4', '5', '6', '7', '8']
            x_l = 22
            for i in litery:
                y_g = 558
                for j in liczby:
                    self.G_plansza[i + j][0] = x_l
                    self.G_plansza[i + j][1] = y_g
                    y_g -= 77
                x_l += 77
        else:
            litery = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
            liczby = ['1', '2', '3', '4', '5', '6', '7', '8']
            x_l = 561
            for i in litery:
                y_g = 19
                for j in liczby:
                    self.G_plansza[i + j][0] = x_l
                    self.G_plansza[i + j][1] = y_g
                    y_g += 77
                x_l -= 77

    def czy_szach(self):  # zmienia wartosc zmienncyh odpowiedzialnych za szach i potrzebnych do matu
        if self.czy_K_B('B') and self.czy_K_B('C') and self.C_szach is False and self.B_szach is False:
            self.C_szach = True
            self.C_r_szach = self.ruch
            self.B_szach = True
            self.B_r_szach = self.ruch
        elif self.czy_K_B('B') and not self.czy_K_B('C') and self.B_szach is False:
            self.C_szach = False
            self.C_r_szach = 0
            self.B_szach = True
            self.B_r_szach = self.ruch
        elif not self.czy_K_B('B') and self.czy_K_B('C') and self.C_szach is False:
            self.C_szach = True
            self.C_r_szach = self.ruch
            self.B_szach = False
            self.B_r_szach = 0

    def czy_mat(self):  # sprawdza czy jest mat
        if self.B_szach is True and self.ruch != self.B_r_szach and self.ruch - self.B_r_szach <= 2:
            self.win = 'B'
            return True
        elif self.C_szach is True and self.ruch != self.C_r_szach and self.ruch - self.C_r_szach <= 2:
            self.win = 'C'
            return True
        else:
            return False

    def bicie(self, stary, nowy):  # zmienia polozenie figur jesli zachodzi bicie
        x = self.G_plansza[stary].pop()
        x.poz = nowy
        self.G_plansza[nowy].pop()
        self.G_plansza[nowy].append(x)

    def zmiana(self, stary, nowy):  # zmienia polozenie figur dla pustych pol
        x = self.G_plansza[stary].pop()
        x.poz = nowy
        self.G_plansza[nowy].append(x)

    def roszada(self, k):  # wyznacza czy roszada jest mozliwa
        rosz_k = []
        if k.rodzaj != 'krol':
            return rosz_k
        else:
            if k.rosz is True:
                if k.kolor == 'B':
                    if len(self.G_plansza['H1']) == 3 and self.G_plansza['H1'][2].rosz is True:
                        if len(self.G_plansza['G1']) == 2 and len(self.G_plansza['F1']) == 2:
                            rosz_k.append('G1')
                    if len(self.G_plansza['A1']) == 3 and self.G_plansza['A1'][2].rosz is True:
                        if len(self.G_plansza['B1']) == 2 and len(self.G_plansza['C1']) == 2 and len(
                                self.G_plansza['D1']) == 2:
                            rosz_k.append('C1')
                else:
                    if len(self.G_plansza['H8']) == 3 and self.G_plansza['H8'][2].rosz is True:
                        if len(self.G_plansza['E8']) == 2 and len(self.G_plansza['F8']) == 2 and len(
                                self.G_plansza['G8']) == 2:
                            rosz_k.append('F8')
                    if len(self.G_plansza['A8']) == 3 and self.G_plansza['A8'][2].rosz is True:
                        if len(self.G_plansza['B8']) == 2 and len(self.G_plansza['C8']) == 2:
                            rosz_k.append('B8')
            return rosz_k

    def en_passe(self, p):  # sprawdza czy mozna wykonac bicie en passe
        ruchy_en = []
        if p.rodzaj != 'pion':
            return ruchy_en
        else:
            k = 'C'
            j = 1
            if p.kolor == 'C':
                k = 'B'
                j = -1
            tab = [1, -1]
            for i in range(2):
                poz = chr(ord(p.poz[0]) + tab[i]) + p.poz[1]
                if poz in self.G_plansza and len(self.G_plansza[poz]) == 3 and self.G_plansza[poz][2].rodzaj == 'pion':
                    if self.ruch - self.G_plansza[poz][2].ruch_passe == 1 and self.G_plansza[poz][2].kolor == k:
                        ruchy_en.append(chr(ord(p.poz[0]) + tab[i]) + chr(ord(p.poz[1]) + j))
            return ruchy_en

    def zaznaczony(self, poz):  # reguje na klikniecia
        r = 'C'
        if self.ruch % 2 == 1:
            r = 'B'

        if len(self.G_plansza[poz]) == 3:
            if self.G_plansza[poz][2].kolor == r:
                if len(self.pozycje) == 1:
                    if self.G_plansza[self.pozycje[0]][2].kolor != self.G_plansza[poz][2].kolor:
                        if poz in self.G_plansza[self.pozycje[0]][2].wyznacz_ruchy(self.G_plansza):
                            self.bicie(self.pozycje[0], poz)
                            self.G_plansza[poz][2].rosz = False
                            self.ruch += 1
                            self.pozycje.pop()
                    else:
                        self.pozycje[0] = poz
                        poz = self.pozycje[0]
                        tab = self.G_plansza[poz][2].wyznacz_ruchy(self.G_plansza) + self.roszada(
                            self.G_plansza[poz][2])
                        tab += self.en_passe(self.G_plansza[poz][2])
                        for key in tab:
                            self.screen.blit(pygame.image.load("kropka.png"),
                                             [self.G_plansza[key][0], self.G_plansza[key][1]])
                else:
                    self.pozycje.append(poz)
                    tab = self.G_plansza[poz][2].wyznacz_ruchy(self.G_plansza) + self.roszada(self.G_plansza[poz][2])
                    tab += self.en_passe(self.G_plansza[poz][2])
                    for key in tab:
                        self.screen.blit(pygame.image.load("kropka.png"),
                                         [self.G_plansza[key][0], self.G_plansza[key][1]])
            elif len(self.pozycje) == 1 and self.G_plansza[self.pozycje[0]][2].kolor != self.G_plansza[poz][2].kolor:
                if poz in self.G_plansza[self.pozycje[0]][2].wyznacz_ruchy(self.G_plansza):
                    self.bicie(self.pozycje[0], poz)
                    self.G_plansza[poz][2].rosz = False
                    self.ruch += 1
                    self.pozycje.pop()

        else:
            if len(self.pozycje) == 1:
                if poz in self.G_plansza[self.pozycje[0]][2].wyznacz_ruchy(self.G_plansza):
                    self.G_plansza[self.pozycje[0]][2].ruch_passe = self.ruch
                    self.zmiana(self.pozycje[0], poz)
                    self.G_plansza[poz][2].rosz = False
                    self.pozycje.pop()
                    self.ruch += 1
                elif poz in self.roszada(self.G_plansza[self.pozycje[0]][2]):
                    self.zmiana(self.pozycje[0], poz)
                    self.G_plansza[poz][2].rosz = False
                    if self.G_plansza[poz][2].kolor == 'B':
                        if poz[0] > self.pozycje[0][0]:
                            self.zmiana('H1', 'F1')
                        if poz[0] < self.pozycje[0][0]:
                            self.zmiana('A1', 'D1')
                    else:
                        if poz[0] > self.pozycje[0][0]:
                            self.zmiana('H8', 'E8')
                        if poz[0] < self.pozycje[0][0]:
                            self.zmiana('A8', 'C8')
                    self.pozycje.pop()
                    self.ruch += 1
                elif poz in self.en_passe(self.G_plansza[self.pozycje[0]][2]):
                    self.zmiana(self.pozycje[0], poz)
                    self.G_plansza[poz[0] + self.pozycje[0][1]].pop()
                    self.pozycje.pop()
                    self.ruch += 1

    def gdzie_klikniecie(self, x, y, O):  # zwraca gdzie kliknieto
        slownik = {}
        litery = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        liczby = ['1', '2', '3', '4', '5', '6', '7', '8']
        if O is True:
            if self.ruch % 2 == 0:
                litery = litery[::-1]
                liczby = liczby[::-1]
        x_l, x_p = 22, 97

        for i in litery:
            y_g, y_d = 558, 633
            for j in liczby:
                slownik.setdefault(i + j, 0)
                slownik[i + j] = [x_l, x_p, y_g, y_d]
                y_g -= 75
                y_d -= 75
            x_l += 75
            x_p += 75

        for key, value in slownik.items():
            if value[0] <= x <= value[1] and value[2] <= y <= value[3]:
                return (key)
        return 'TT'


class Bierka():
    def __init__(self, rodzaj='pion', kolor='B', poz='A2'):
        self.rodzaj = rodzaj
        self.kolor = kolor
        self.poz = poz
        self.rosz = True
        if rodzaj == 'pion':
            self.ruch_passe = 0

    def name(self):
        return pygame.image.load(self.kolor + '_' + self.rodzaj + '.png')

    def wyznacz_ruchy(self, slownik, T='Bierka'):
        def ruchy_piona(self, slownik, kolor, T):
            K = False
            ruchy_b = []
            if kolor == 'B':
                m = 1
            else:
                m = -1
            ruchy_p = []
            ruchy_p.append(chr(ord(self.poz[0]) + 1 * m) + chr(ord(self.poz[1]) + 1 * m))
            ruchy_p.append(chr(ord(self.poz[0]) - 1 * m) + chr(ord(self.poz[1]) + 1 * m))
            for POZ in ruchy_p:
                if POZ in slownik:
                    if T[0] == 'B':
                        if len(slownik[POZ]) == 3 and slownik[POZ][2].kolor != self.kolor and slownik[POZ][2] != 'krol':
                            ruchy_b.append(POZ)
                    else:
                        if len(slownik[POZ]) == 3 and slownik[POZ][2].kolor != self.kolor:
                            if slownik[POZ][2].rodzaj == 'krol':
                                K = True

            ruchy_p = []
            if self.poz[1] == '2' and self.kolor == 'B' or self.poz[1] == '7' and self.kolor == 'C':
                ruchy_p.append(self.poz[0] + chr(ord(self.poz[1]) + 1 * m))
                ruchy_p.append(self.poz[0] + chr(ord(self.poz[1]) + 2 * m))
            else:
                ruchy_p.append(self.poz[0] + chr(ord(self.poz[1]) + 1 * m))

            for POZ in ruchy_p:
                if POZ in slownik:
                    if len(slownik[POZ]) == 2:
                        ruchy_b.append(POZ)
                    else:
                        break
            if T[0] == 'B':
                return ruchy_b
            else:
                return K

        def ruchy_konia(self, slownik, T):
            K = False
            ruchy_k = []
            ruchy_p = []
            tab = [2, 1, 2, -1, -2, 1, -2, -1, 1, 2, 1, -2, -1, 2, -1, -2]
            for i in range(0, len(tab), 2):
                ruchy_p.append(chr(ord(self.poz[0]) + tab[i]) + chr(ord(self.poz[1]) + tab[i + 1]))
            for POZ in ruchy_p:
                if POZ in slownik:
                    if T[0] == 'B':
                        if len(slownik[POZ]) == 2 or slownik[POZ][2].kolor != self.kolor:
                            if slownik[POZ][2].rodzaj != 'krol':
                                ruchy_k.append(POZ)
                    else:
                        if len(slownik[POZ]) == 3 and slownik[POZ][2].kolor != self.kolor:
                            if slownik[POZ][2].rodzaj == 'krol':
                                K = True
            if T[0] == 'B':
                return ruchy_k
            else:
                return K

        def ruchy_wiezy(self, slownik, T):
            K = False
            ruchy_w = []
            tab = [1, 0, -1, 0, 0, 1, 0, -1]
            for i in range(0, len(tab), 2):
                for j in range(1, 8):
                    POZ = chr(ord(self.poz[0]) + j * tab[i]) + chr(ord(self.poz[1]) + j * tab[i + 1])
                    if POZ in slownik:
                        if len(slownik[POZ]) == 2:
                            ruchy_w.append(POZ)
                        elif len(slownik[POZ]) == 3 and slownik[POZ][2].kolor == self.kolor:
                            break
                        elif len(slownik[POZ]) == 3 and slownik[POZ][2].kolor != self.kolor:
                            if T[0] == 'B':
                                if slownik[POZ][2].rodzaj != 'krol':
                                    ruchy_w.append(POZ)
                                    break
                                else:
                                    break
                            else:
                                if slownik[POZ][2].rodzaj != 'krol':
                                    break
                                else:
                                    K = True
                                    break
                        else:
                            break
                    else:
                        break
            if T[0] == 'B':
                return ruchy_w
            else:
                return K

        def ruchy_gonca(self, slownik, T):
            K = False
            ruchy_g = []
            tab = [1, 1, -1, -1, 1, -1, -1, 1]
            for i in range(0, len(tab), 2):
                for j in range(1, 8):
                    POZ = chr(ord(self.poz[0]) + j * tab[i]) + chr(ord(self.poz[1]) + j * tab[i + 1])
                    if POZ in slownik:
                        if len(slownik[POZ]) == 2:
                            ruchy_g.append(POZ)
                        elif len(slownik[POZ]) == 3 and slownik[POZ][2].kolor != self.kolor:
                            if T[0] == 'B':
                                if slownik[POZ][2].rodzaj != 'krol':
                                    ruchy_g.append(POZ)
                                    break
                                else:
                                    break
                            else:
                                if slownik[POZ][2].rodzaj != 'krol':
                                    break
                                else:
                                    K = True
                                    break
                        else:
                            break
                    else:
                        break
            if T[0] == 'B':
                return ruchy_g
            else:
                return K

        def ruchy_hetmana(self, slownik, T):
            if T[0] == 'B':
                return ruchy_gonca(self, slownik, T) + ruchy_wiezy(self, slownik, T)
            else:
                if ruchy_wiezy(self, slownik, T):
                    return True
                elif ruchy_gonca(self, slownik, T):
                    return True
                else:
                    return False

        def ruchy_krola(self, slownik, T):
            if T[0] != 'B':
                return False
            ruchy_K = []
            ruchy_p = []
            tab = [1, 0, -1, 0, 0, 1, 0, -1, 1, 1, -1, -1, 1, -1, -1, 1]
            for i in range(0, 16, 2):
                ruchy_p.append(chr(ord(self.poz[0]) + tab[i]) + chr(ord(self.poz[1]) + tab[i + 1]))

            for poz in ruchy_p:
                if poz in slownik:
                    if len(slownik[poz]) == 2 or slownik[poz][2].kolor != self.kolor:
                        ruchy_K.append(poz)

            return ruchy_K

        if self.rodzaj == 'pion':
            if self.poz[1] == '8' or self.poz[1] == '1':
                self.rodzaj = 'hetman'
                return ruchy_hetmana(self, slownik, T)
            else:
                return ruchy_piona(self, slownik, self.kolor, T)
        elif self.rodzaj == 'kon':
            return ruchy_konia(self, slownik, T)
        elif self.rodzaj == 'wieza':
            return ruchy_wiezy(self, slownik, T)
        elif self.rodzaj == 'goniec':
            return ruchy_gonca(self, slownik, T)
        elif self.rodzaj == 'hetman':
            return ruchy_hetmana(self, slownik, T)
        else:
            return ruchy_krola(self, slownik, T)
