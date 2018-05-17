from multiprocessing import Process
import API_REST.server as server
import API_REST.test_cerradura as cerradura
import time


def funt():
    server.app.run()


def funt2():
    cerradura.app.run()

def funt3():
    import notificadores.listenerHeartbeat as lh


def funt4():
    import horarios.horariosLogic as hl


def funt5():
    import ServidorMensajeriaYCorreo.Notificador

p1 = Process(target=funt)
p2 = Process(target=funt2)
p3 = Process(target=funt3)
p4 = Process(target=funt4)
p5 = Process(target=funt5)
"""
def f1(b):
    if b:
        while True:
            print("process 1 running")


def f2(b):
    if b:
        while True:
            print("process 2 running")

a= True

p1 = Process(target=f1, args=(a,))
p2 = Process(target=f2, args=(a,))
"""
if __name__ == '__main__':
    p1.start()
    print("correra el proceso 2 -------------------------------------------------------------------------------")
    p2.start()
    print("correra el proceso 3 -------------------------------------------------------------------------------")
    p3.start()
    print("correra el proceso 4 -------------------------------------------------------------------------------")
    p4.start()
    print("correra el proceso 5 -------------------------------------------------------------------------------")
    p5.start()