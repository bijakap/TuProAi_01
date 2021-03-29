import random
import math
from functools import reduce
from operator import itemgetter, attrgetter


def BagianKromoson():
    kromosom = []
    for i in range(10):
       kromosom.append(random.randint(0,1))
    x = decodeX(kromosom)
    y = decodeY(kromosom)
    fitness = fitnessInd(x,y)
    return kromosom,fitness

def decodeX(kromosom):
    jumlah = 0
    sigma = reduce(lambda a, x: a + (2**-((x+1))), [0]+list(range(0,5)))
    for i in range(5):
        jumlah = jumlah + (kromosom[i]*2**(-(i+1)))
    x = -1 + ((2-(-1))/sigma * jumlah)
    return x

def decodeY(kromosom):
    jumlah = 0
    sigma = reduce(lambda a, x: a + (2**-((x+1))), [0]+list(range(0,5)))
    for i in range(5):
        jumlah = jumlah + (kromosom[i+5]*2**(-(i+1)))
    y = -1 + ((1-(-1))/sigma * jumlah)
    return y

def Populasi(BanyakPopulasi):
    populasi = []
    for i in range(BanyakPopulasi):
        kromosom_temp = BagianKromoson()
        populasi.append(kromosom_temp)
    return populasi

def PrintAllKromosomDanFitness(populasi, BanyakPopulasi):
    for i in range(BanyakPopulasi):
        print(populasi[i])
    print()

def PrintPopulasi(populasi, BanyakPopulasi):
    temp = []
    for i in range(BanyakPopulasi):
        temp = populasi[i]
        print(temp[0])
    print()

def fitnessInd(x,y): ##Perhitungan fitness
    return (math.cos(x**2)*math.sin(y**2) + (x + y))

def pengurutanfitness(populasi):
    populasi = sorted(populasi, key=itemgetter(1), reverse=1)
    return populasi

def tournamentSelection(populasi):
    JumParent = int((0.8)*len(populasi))
    MaxPerTorunament = len(populasi)//JumParent
    parent = []
    for i in range(JumParent):
        parent.append(populasi[i])
    return parent

def elitism(populasi):
    elitism = []
    jumElitism = int(math.floor(len(populasi))/5)
    if jumElitism % 2 != 0:
        jumElitism = jumElitism + 1
    for i in range(jumElitism):
        elitism.append(populasi[i])
    return elitism


def mutasi(anak):
    for i in range(len(anak)):
        for j in range(len(anak[0][0])):
            if random.random() < 0.3: #Probabilitas Mutasi
                # if anak[i][0][j] == 0:
                #     anak[i][0][j] = 1
                # else :
                #     anak[i][0][j] = 0
                anak[i][0][random.randint(0,9)] = random.randint(0,1)
    return anak

def CalonPasangan(parent):
    pasangan = []
    acak = 0
    for i in range(int(len(parent)//2)):
        temp1 = []
        while acak == i:
            acak = random.randint(0,len(parent)-1)
        temp1.append(parent[i])
        temp1.append(parent[acak])
        pasangan.append(temp1)
    return pasangan


def CrossOver(pasangan):
    anak = []
    for n in range(len(pasangan)):
        simpan1 = []
        simpan2 = []
        parent1 = pasangan[n][0]
        parent2 = pasangan[n][1]
        Perpotongan = random.randint(1,8)
        for i in range(Perpotongan):
            simpan1.append(parent1[0][i])
        for j in range(Perpotongan):
            simpan2.append(parent2[0][j])
        for i in range(len(parent1[0])-Perpotongan):
            simpan1.append(parent2[0][i+Perpotongan])
        for j in range(len(parent2[0])-Perpotongan):
            simpan2.append(parent1[0][j+Perpotongan])
        temp1 = []
        temp1.append(simpan1)
        temp1.append(fitnessInd(decodeX(simpan1),decodeY(simpan1)))
        temp2 = []
        temp2.append(simpan2)
        temp2.append(fitnessInd(decodeX(simpan2),decodeY(simpan2)))
        temp1 = tuple(temp1)
        temp2 = tuple(temp2)
        anak.append(temp1)
        anak.append(temp2)
    return anak

def HitungFitnessPop(anak):
    anak_baru = []
    for i in range(len(anak)):
        tampung = []
        gabung = []
        for j in range(len(anak[0][0])):
            tampung.append(anak[i][0][j])   
        jumfitness = fitnessInd(decodeX(tampung),decodeY(tampung))
        gabung.append(tampung)
        gabung.append(jumfitness)
        gabung = tuple(gabung)
        anak_baru.append(gabung)
    return anak_baru


def GenerasiBaru(survivor,anak):
    GenBaru = []
    for i in range(len(survivor)):
        GenBaru.append(survivor[i])
    for i in range(len(anak)):
        GenBaru.append(anak[i])
    return GenBaru

def main():
    BanyakPopulasi = int(input("Banyak Polulasi: "))
    while BanyakPopulasi <= 0 :
        BanyakPopulasi = int(input("Banyak Polulasi: "))
    BanyakGenerasi = int(input("Banyak Generasi: "))

    populasi = Populasi(BanyakPopulasi)
    
    print("Generasi Pertama :\n")
    PrintAllKromosomDanFitness(populasi,len(populasi))

    generasi = 0
    genBest = 0
    kromosom_terbaik = populasi[0]

    for i in range(BanyakGenerasi):
        survivor = elitism(pengurutanfitness(populasi))
        parent = tournamentSelection(populasi)
        pasangan = CalonPasangan(parent)
        anak = CrossOver(pasangan)
        anak = mutasi(anak)
        anak = pengurutanfitness(HitungFitnessPop(anak))
        newPopulation = GenerasiBaru(survivor,anak)
        generasi = generasi + 1
        print("Generasi :",generasi,"\n")
        PrintAllKromosomDanFitness(newPopulation,len(newPopulation))
        print(format(populasi[4][1], '.3f'),format(kromosom_terbaik[1], '.3f'))
        if format(newPopulation[0][1], '.3f') > format(kromosom_terbaik[1], '.3f'):
            kromosom_terbaik = newPopulation[0]
            genBest = generasi
        populasi = newPopulation

    print("Keromosom Terbaik :", kromosom_terbaik,"\nDari Generasi :", genBest)


if __name__ == '__main__':
	import random
	main()