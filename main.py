import pygame
from random import randint
from math import fabs

class Robotti():
    def __init__(self,v,leveys,korkeus):
        self.x = (640 - leveys)/2
        self.y = 480 - korkeus
        self.v = v # Nopeus
        self.vasemmalle = False
        self.oikealle = False
        self.ylos = False
        self.alas = False
        self.xmax = 640 - leveys
        self.ymax = 480 - korkeus

    def lue_komento(self, tapahtuma):
        if tapahtuma.type == pygame.KEYDOWN:
            if tapahtuma.key == pygame.K_LEFT:
                self.vasemmalle = True
            if tapahtuma.key == pygame.K_RIGHT:
                self.oikealle = True
            if tapahtuma.key == pygame.K_UP:
                self.ylos = True
            if tapahtuma.key == pygame.K_DOWN:
                self.alas = True
        if tapahtuma.type == pygame.KEYUP:
            if tapahtuma.key == pygame.K_LEFT:
                self.vasemmalle = False
            if tapahtuma.key == pygame.K_RIGHT:
                self.oikealle = False
            if tapahtuma.key == pygame.K_UP:
                self.ylos = False
            if tapahtuma.key == pygame.K_DOWN:
                self.alas = False

    def liiku(self):
        # Robotti ei saa mennä yli reunoista
        if self.oikealle and self.x < self.xmax:
            self.x += self.v
        if self.vasemmalle and self.x > 0:
            self.x -= self.v
        if self.alas and self.y < self.ymax:
            self.y += self.v
        if self.ylos and self.y > 0:
            self.y -= self.v

class Kolikko():
    def __init__(self,v,leveys,korkeus):
        self.leveys = leveys
        self.korkeus = korkeus
        self.v = v # Nopeus
        self.xmax = 640 - leveys
        self.ymax = 480 - korkeus
        self.x = randint(0, self.xmax)
        self.y = randint(-4*self.ymax,0)
        self.naytetaan = True

    # Palauttaa True jos liikutaan, False jos kolikko on alareunassa
    def liiku(self):
        if self.y + self.korkeus < 480:
            self.y += self.v
            return True
        return False

class Hirvio():
    def __init__(self,v,leveys,korkeus):
        self.leveys = leveys
        self.korkeus = korkeus
        self.v = v
        self.xmax = 640 - leveys
        self.ymax = 480 - korkeus
        self.x = randint(0, self.xmax)
        self.y = randint(-2*self.ymax,0)
        self.naytetaan = True

    # Liikkuu eteenpäin jos ei ole päässyt pois ikkunasta
    def liiku(self):
        if self.y < 480:
            self.y += self.v

class Peli():
    def __init__(self):
        # Pelialueen valmistelu
        pygame.init()
        pygame.display.set_caption("Nappaa kolikoita, väistä hirviöitä!")
        self.naytto = pygame.display.set_mode((640, 480))
        self.kello = pygame.time.Clock()
        self.fontti = pygame.font.SysFont("Arial", 24)
        self.pisteet = 0
        self.N = 30  # Kolikkojen ja hirviöiden määrä
        peli_jatkuu = True

        # Robotin tiedot
        robo = pygame.image.load("robo.png")
        v_robo = 3  # Robotin nopeus
        self.robotti = Robotti(v_robo, robo.get_width(), robo.get_height())

        # Kolikon ja hirviön tiedot
        kolikko = pygame.image.load("kolikko.png")
        hirvio = pygame.image.load("hirvio.png")
        v = 1  # Kolikon nopeus
        v_hir = 0.5 # Hirviön nopeus

        # Luodaan kolikot ja hirviöt taulukkoon
        kolikot = []
        hirviot = []
        for i in range(self.N):  # Hirviöiden lukumäärä sama kuin kolikoiden
            kolikot.append(Kolikko(v, kolikko.get_width(), kolikko.get_height()))
            hirviot.append(Hirvio(v_hir, hirvio.get_width(), hirvio.get_height()))

        # Maksimikontaktietäisyydet - jos pienempi, niin robotti osuu
        kolikkokontakti_x = (robo.get_width() + kolikko.get_width())/2
        kolikkokontakti_y = (robo.get_height() + kolikko.get_height())/2
        hirviokontakti_x = (robo.get_width() + hirvio.get_width())/2
        hirviokontakti_y = (robo.get_height() + hirvio.get_height())/2

        # Pelisilmukka
        while peli_jatkuu:
            pienin_y = 480  # Näytettävien kolikoiden ja hirviöiden suurin y-koordinaatti
            # Luetaan näppäimistön tapahtuma
            for tapahtuma in pygame.event.get():
                if tapahtuma.type == pygame.QUIT:
                    exit()
                self.robotti.lue_komento(tapahtuma)
            self.robotti.liiku()

            self.naytto.fill((0, 0, 200))  # RGB, välillä 0-255. Sininen tausta jotta hirviö näkyy
            self.naytto.blit(robo, (self.robotti.x, self.robotti.y))
            x_robo_keski = self.robotti.x + robo.get_width()/2 # Robotin keskipisteen koordinaatit
            y_robo_keski = self.robotti.y + robo.get_height()/2

            # Käydään läpi hirviöt ja kolikot (sama määrä)
            for i in range(self.N):
                k = kolikot[i]
                h = hirviot[i]
                if k.naytetaan: # Kolikon näyttäminen
                    if k.y < pienin_y:
                        pienin_y = k.y
                    self.naytto.blit(kolikko, (k.x, k.y))
                    peli_jatkuu = k.liiku() # Onko kolikko liikkunut alareunaan asti?
                    if not peli_jatkuu: # Jos on, peli on ohi
                        break
                    if self.osuuko(k, kolikkokontakti_x, kolikkokontakti_y, x_robo_keski, y_robo_keski, kolikko):
                        self.pisteet += 1
                if h.naytetaan: # Hirviön näyttäminen
                    if h.y < pienin_y:
                        pienin_y = h.y
                    self.naytto.blit(hirvio, (h.x,h.y))
                    h.liiku()
                    if self.osuuko(h, hirviokontakti_x, hirviokontakti_y, x_robo_keski, y_robo_keski, hirvio):
                        self.pisteet -= 1
            if pienin_y >= 480 or not peli_jatkuu: # Kaikki kolikot ja hirviöt ovat reunan alla tai peli ohi
                break
                    
            teksti = self.fontti.render("Pisteet: " + str(self.pisteet), True, (255, 0, 0))
            self.naytto.blit(teksti, (500, 0))
            # Ruudun päivitys
            pygame.display.flip()
            self.kello.tick(60)
        self.loppu(robo)

    def osuuko(self, esine, kontakti_x, kontakti_y, x_robo_keski, y_robo_keski, kuva):
        x_keski = esine.x + kuva.get_width()/2
        y_keski = esine.y + kuva.get_height()/2
        # Pienin mahdollinen ero x- ja y-koordinaateissa osumalle
        osuu_x = fabs(x_robo_keski - x_keski) < kontakti_x
        osuu_y = fabs(y_robo_keski - y_keski) < kontakti_y
        if osuu_x and osuu_y:
            esine.naytetaan = False
        return osuu_x and osuu_y

    # Minkä arvonimen saa tietyllä pistemäärällä?
    def titteli(self, p: int):
        if p < 0:
            return "surkimus"
        if p < 5:
            return "aloittelija"
        if p < 10:
            return "amatööri"
        if p < 15:
            return "hyvä pelaaja"
        if p < 20:
            return "ekspertti"
        return "pelikuningas (paras mahdollinen arvonimi)"

    def loppu(self, robo):
        self.naytto.fill((0, 0, 0))  # RGB, välillä 0-255
        teksti = self.fontti.render("Peli ohi! Sait " + str(self.pisteet) + "/" + str(self.N) + " pistettä.", True, (255, 0, 0))
        arvio = self.fontti.render("Olet " + self.titteli(self.pisteet) + "!", True, (255, 0, 0))
        self.naytto.blit(teksti, (100, 100))
        self.naytto.blit(arvio,  (100, 130))
        self.naytto.blit(robo, (self.robotti.x, self.robotti.ymax))
        pygame.display.flip()

        while True:
            for tapahtuma in pygame.event.get():
                if tapahtuma.type == pygame.QUIT:
                    exit()

peli = Peli()
