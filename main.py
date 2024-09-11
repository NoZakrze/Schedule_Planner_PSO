from PSO import PSO
import matplotlib.pyplot as plt
from Consts import *
import time
ilosc_prob = 10

#Pojedyncze wywołanie
pso = PSO(200,300)
wynik = pso.GlownaPetla(BETTER,0,BETTER_VECTOR,2)
plt.plot(wynik)
#plt.savefig('wykres3.png')
plt.show()
pso.Print_Best()

#10 Wykonan
'''
czas_3 = 0
fitness_3 = 0
for _ in range(ilosc_prob):
    pso = PSO(200,300)
    start = time.time()
    _ = pso.GlownaPetla(BETTER,0,BETTER_VECTOR,2)
    koniec = time.time()
    fitness_3 += pso.globalFitness
    czas_3 += koniec - start
czas_3 = czas_3 / ilosc_prob
fitness_3 = fitness_3 / ilosc_prob
print(czas_3)
print(fitness_3)
'''