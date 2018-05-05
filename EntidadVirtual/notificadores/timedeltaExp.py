from datetime import timedelta
from datetime import datetime
import time


delta = timedelta(seconds=10)

ahora = datetime.now()
index = 0
contador = 0

heartbeat = "I'm alive"
salida = True

while salida:
    while ahora+delta > datetime.now():
        print(index)
        index = index+1
        time.sleep(1)

        if "alive" in heartbeat:
            contador = 0
            ahora = datetime.now()
            heartbeat = "sadsad"

    contador += 1
    print(contador)
    if contador >=3:
        salida=False

    ahora = datetime.now()






