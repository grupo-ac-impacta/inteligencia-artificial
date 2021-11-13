# %%
from Jogo import JogoDaOnca
import random

C_WAIT_JAGUAR = "WAITING JAGUAR"
C_WAIT_DOG = "WAITING DOG"

a = JogoDaOnca()

while True:
    a.newBoard()
    while a.getStatus() not in ["JAGUAR_WIN", "DOGS_WIN"]:
        a.getBoard()
        a.JaguarAround(a.getJaguarPosition()-1)
        a.checkQttDogs()
        if a.getStatus() == C_WAIT_JAGUAR:
            print("Vez da Onça")
            a.jaguarWalk(random.choice(a.JaguarIA(a.getJaguarPosition()-1)))
        elif a.getStatus() == C_WAIT_DOG:
            print("Vez do Cachorro")
            while True:
                if a.dogPlay(int(input()), int(input())):
                    break
                print("Entrada inválida")
    break
