import random

from DataSetPSO import DataSetPSO
from Consts import *

class PSO:
    def __init__(self, ilosc_osobnikow, ilosc_ruchow):
        self.osobniki = [DataSetPSO() for _ in range(ilosc_osobnikow)]
        self.SwarmBestTablicaKlas = None
        self.SwarmBestTablicaNauczycieli = None
        self.SwarmBestTablicaSal = None
        self.globalFitness = 0
        self.iloscRuchow = ilosc_ruchow
        self.ruch_od_zmiany = 0
        for o in self.osobniki:
            o.GenerujPlan()
            o.inicjujBest()


    def GlownaPetla(self,fitness,delay,vector,zmiany):
        bests_fitnesses = []
        #1. ustalam najlepszego osobnika
        best_idx = -1
        for i in range(len(self.osobniki)):
            if self.osobniki[i].Evaluate(fitness) > self.globalFitness:
                self.globalFitness = self.osobniki[i].Evaluate(fitness)
                best_idx = i
        self.SwarmBestTablicaKlas = self.osobniki[best_idx].TablicaKlas
        self.SwarmBestTablicaNauczycieli = self.osobniki[best_idx].TablicaNauczycieli
        self.SwarmBestTablicaSal = self.osobniki[best_idx].TablicaSali
        #2. glowna petla algorytmu
        for i in range(self.iloscRuchow):
            zmiana = 0
            for o in self.osobniki:
                if i>delay:
                    rand = random.random()
                    if rand <= 0.7:
                        if vector == SIMPLE_VECTOR:
                            o.Random_Swap_PSO()
                        else:
                            o.better_Random_Swap_PSO()
                    else:
                        o.Random_Swap_PSO_no_breaks()
                o.Move_to_best(o.selfBestTablicaKlas,o.selfBestTablicaNauczycieli,o.selfBestTablicaSal,zmiany)
                o.Move_to_best(self.SwarmBestTablicaKlas,self.SwarmBestTablicaNauczycieli,self.SwarmBestTablicaSal,zmiany)
                if o.Evaluate(fitness) > self.globalFitness:
                    self.globalFitness = o.Evaluate(fitness)
                    self.SwarmBestTablicaKlas = o.TablicaKlas
                    self.SwarmBestTablicaNauczycieli = o.TablicaNauczycieli
                    self.SwarmBestTablicaSal = o.TablicaSali
                    zmiana = 1
                if o.Evaluate(fitness) > o.selfBestfitness:
                    o.selfBestfitness = o.Evaluate(fitness)
                    o.selfBestTablicaKlas = o.TablicaKlas
                    o.selfBestTablicaNauczycieli = o.TablicaNauczycieli
                    o.selfBestTablicaSal = o.TablicaSali
                    o.isBest = True
                else:
                    o.isBest = False
            bests_fitnesses.append(self.globalFitness)
            if zmiana==0:
                self.ruch_od_zmiany+=1
            else:
                self.ruch_od_zmiany=0
            if self.ruch_od_zmiany>30:
                break
        return bests_fitnesses

    def Print_Best(self):
        for i in range(len(self.SwarmBestTablicaKlas)):
            if i % self.osobniki[0].tydzien == self.osobniki[0].tydzien - 1:
                print(self.SwarmBestTablicaKlas[i])
                print('\n')
            elif i % self.osobniki[0].zajecia == self.osobniki[0].zajecia - 1:
                print(self.SwarmBestTablicaKlas[i])
            else:
                print(self.SwarmBestTablicaKlas[i], end=' ')
        print("Best fitness:", self.globalFitness)
