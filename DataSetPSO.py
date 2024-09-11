from DataSet import DataSet
import random as random
from Consts import*
class DataSetPSO(DataSet):
    def __init__(self):
        DataSet.__init__(self)
        self.selfBestTablicaKlas = None
        self.selfBestTablicaNauczycieli = None
        self.selfBestTablicaSal = None
        self.isBest = True
        self.selfBestfitness = 0

    def inicjujBest(self):
        self.selfBestTablicaKlas = self.TablicaKlas
        self.selfBestTablicaNauczycieli = self.TablicaNauczycieli
        self.selfBestTablicaSal = self.TablicaSali
        self.selfBestfitness = self.Simple_fitness()


    def Move_to_best(self,klasy,nauczyciele,sale,zmiany):
        ruchy = random.randint(1,zmiany)
        for _ in range(ruchy):
            for i in range(self.klasy):
                indeksy_rozne = []
                tydzien = self.Get_tydzien_wektora(self.TablicaKlas,i)
                tydzien_best = self.Get_tydzien_wektora(klasy,i)
                for j in range(len(tydzien)):
                    if tydzien[j] != tydzien_best[j]:
                        indeksy_rozne.append(j)
                if len(indeksy_rozne) > 0:
                    random.shuffle(indeksy_rozne)
                    znalezione = False
                    for x in indeksy_rozne:
                        lekcja = self.GetZajecia(KLASA,i,None,x)
                        if lekcja != OKIENKO:
                            nauczyciel = lekcja[0]
                            sala = lekcja[1]
                            lekcje_nauczyciela = []
                            for k in range(len(tydzien_best)):
                                if nauczyciel == tydzien_best[k][0] and k!=x:
                                    lekcje_nauczyciela.append(k)
                            random.shuffle(lekcje_nauczyciela)
                            for k in range(len(lekcje_nauczyciela)):
                                termin = lekcje_nauczyciela[k]
                                sala_best = tydzien_best[termin][1]
                                if self.GetZajecia(NAUCZYCIEL,nauczyciel,None,termin) == OKIENKO  and self.GetZajecia(KLASA,i,None,termin) == OKIENKO:
                                    sale = self.Get_free_rooms(None,termin)
                                    salaN = random.choice(sale)
                                    self.SetZajecia(i, nauczyciel, salaN, None, termin)
                                    self.Wstaw_okienko(i, nauczyciel, sala, None, x)
                                    znalezione = True
                                    break
                            if znalezione:
                                break

    def Get_tydzien_wektora(self, wektor, indeks):
        wynik = []
        for i in range(self.tydzien):
            wynik.append(wektor[self.tydzien*indeks + i])
        return wynik


    def Wstaw_okienko(self, klasa, nauczyciel, sala, dzien_tygodnia, lekcja):
        if (dzien_tygodnia != None):
            self.TablicaKlas[(klasa) * self.tydzien + self.zajecia * (dzien_tygodnia) + lekcja] = (-1, -1)
            self.TablicaNauczycieli[(nauczyciel) * self.tydzien + self.zajecia * (dzien_tygodnia) + lekcja] = (
            -1, -1)
            self.TablicaSali[(sala) * self.tydzien + self.zajecia * (dzien_tygodnia) + lekcja] = (-1, -1)
        else:
            self.TablicaKlas[(klasa) * self.tydzien + lekcja] = (-1, -1)
            self.TablicaNauczycieli[(nauczyciel) * self.tydzien + lekcja] = (-1, -1)
            self.TablicaSali[(sala) * self.tydzien + lekcja] = (-1, -1)

    def Get_okienka(self,wektor,indeks):
        wynik = []
        tydzien = self.Get_tydzien_wektora(wektor,indeks)
        for i in range(len(tydzien)):
            if tydzien[i] == (-1,-1):
                wynik.append(i)
        return wynik

    #usuwam lekcje i wstawiam w okienko
    def Random_Swap_PSO(self):
        klasa =  random.randint(0, self.klasy - 1)
        zajecia = []
        okienka = []
        for i in range(self.tydzien):
            if self.GetZajecia(KLASA,klasa,None,i) == OKIENKO:
                okienka.append(i)
            else:
                zajecia.append(i)
        termin = random.choice(zajecia)
        instancja_terminu = self.GetZajecia(KLASA,klasa,None,termin)
        random.shuffle(okienka)
        for indeks_okienka in okienka:
            if self.GetZajecia(NAUCZYCIEL,instancja_terminu[0],None,indeks_okienka) == OKIENKO and self.GetZajecia(SALA,instancja_terminu[1],None,indeks_okienka) == OKIENKO and indeks_okienka != termin:
                self.SetZajecia(klasa, instancja_terminu[0], instancja_terminu[1], None, indeks_okienka)
                self.Wstaw_okienko(klasa, instancja_terminu[0], instancja_terminu[1], None, termin)
                break

    def Random_Swap_PSO_no_breaks(self):
            klasa = random.randint(0, self.klasy - 1)
            zajecia = []
            for i in range(self.tydzien):
                if self.GetZajecia(KLASA, klasa, None, i) != OKIENKO:
                    zajecia.append(i)
            termin = random.choice(zajecia)
            instancja_terminu = self.GetZajecia(KLASA, klasa, None, termin)
            drugie_terminy = []
            for z in zajecia:
                nauczyciel, sala = self.GetZajecia(KLASA,klasa,None,z)
                if nauczyciel != instancja_terminu[0]:
                    drugie_terminy.append(z)
            random.shuffle(drugie_terminy)
            for d in drugie_terminy:
                nauczyciel1, sala1 = self.GetZajecia(KLASA,klasa,None,d)
                if self.GetZajecia(NAUCZYCIEL,nauczyciel1,None,termin) == OKIENKO and self.GetZajecia(NAUCZYCIEL,instancja_terminu[0],None,d) == OKIENKO:
                    self.SetZajecia(klasa,instancja_terminu[0],sala1,None,d)
                    self.SetZajecia(klasa,nauczyciel1,instancja_terminu[1],None,termin)
                    break


    def better_Random_Swap_PSO(self):
        klasa =  random.randint(0, self.klasy - 1)
        zajecia = []
        okienka = []
        for i in range(self.tydzien):
            if self.GetZajecia(KLASA,klasa,None,i) == OKIENKO:
                if i%self.zajecia != 0 and i%self.zajecia != self.zajecia-1:
                    if self.GetZajecia(KLASA,klasa,None,i+1) != OKIENKO or self.GetZajecia(KLASA,klasa,None,i+1) != OKIENKO:
                        okienka.append(i)
                elif i%self.zajecia == 0:
                    if self.GetZajecia(KLASA,klasa,None,i+1) != OKIENKO:
                        okienka.append(i)
                elif i%self.zajecia != self.zajecia-1:
                    if self.GetZajecia(KLASA,klasa,None,i-1) != OKIENKO:
                        okienka.append(i)
            else:
                if i%self.zajecia != 0 and i%self.zajecia != self.zajecia-1:
                    if self.GetZajecia(KLASA,klasa,None,i+1) == OKIENKO or self.GetZajecia(KLASA,klasa,None,i+1) == OKIENKO:
                        zajecia.append(i)
                elif i%self.zajecia == 0:
                    if self.GetZajecia(KLASA,klasa,None,i+1) == OKIENKO:
                        zajecia.append(i)
                elif i%self.zajecia != self.zajecia-1:
                    if self.GetZajecia(KLASA,klasa,None,i-1) == OKIENKO:
                        zajecia.append(i)
        if len(zajecia) > 0 and len(okienka):
            termin = random.choice(zajecia)
            instancja_terminu = self.GetZajecia(KLASA,klasa,None,termin)
            random.shuffle(okienka)
            for indeks_okienka in okienka:
                if self.GetZajecia(NAUCZYCIEL,instancja_terminu[0],None,indeks_okienka) == OKIENKO and self.GetZajecia(SALA,instancja_terminu[1],None,indeks_okienka) == OKIENKO and indeks_okienka != termin:
                    self.SetZajecia(klasa, instancja_terminu[0], instancja_terminu[1], None, indeks_okienka)
                    self.Wstaw_okienko(klasa, instancja_terminu[0], instancja_terminu[1], None, termin)
                    break