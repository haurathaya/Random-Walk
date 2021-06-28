import random
from matplotlib import animation, rc
import matplotlib.pyplot as plt
from IPython.display import HTML
from celluloid import Camera as Camera

fig = plt.figure()
Camera = Camera(fig)

## INISIALISASI VARIABLE SCALAR ##
individu = 200
rasio = 5  # 5%
prob = 0.8  # 80%
waktuPulih = 10  # hari pemulihan

jml_terinfeksi = 0  # inisialisasi jumlah terinfeksi

# UKURAN RUANG SIMULASI #
x_min = int(0)
x_max = int(20)
y_min = int(0)
y_max = int(20)
x_range = x_max - x_min
y_range = y_max - y_min

## INISIALISASI VARIABEL LIST ##
statusHealth = []  # status terinfeksi /  tidak
waktuInfeksi = []  # waktu terinfeksi / recovery
totalInfeksi = []  # total individu yang terinfeksi
hari = []

x_pos = []  # posisi X
y_pos = []  # posisi Y

# STATUS INDIVIDU AWAL #
for i in range(individu):
    x_infeksi = []
    y_infeksi = []
    x_sehat = []
    y_sehat = []

    x_pos.append(random.randint(x_min, x_max))
    y_pos.append(random.randint(y_min, y_max))

    randRasio = (random.randint(1, 100))
    if randRasio <= rasio:
        status = "terinfeksi"
        statusHealth.append(status)
        x_infeksi.append(random.randint(x_min, x_max))
        y_infeksi.append(random.randint(y_min, y_max))
        jml_terinfeksi += 1
        waktuInfeksi.append(1)
    else:
        status = "sehat"
        statusHealth.append(status)
        waktuInfeksi.append(0)
        x_sehat.append(random.randint(x_min, x_max))
        y_sehat.append(random.randint(y_min, y_max))

# ITERASI #

hari_ke = 1
hari.append(hari_ke)
totalInfeksi.append(jml_terinfeksi)

while (jml_terinfeksi > 0):
    for i in range(individu):
        x_infeksi = []
        y_infeksi = []
        x_sehat = []
        y_sehat = []

      # UPDATE POSISI
        probRand = random.uniform(0, 1)
        if (probRand >= prob):
            arah = random.uniform(0, 1)
            if arah <= 0.25:  # kanan
                x_pos[i] = x_pos[i-1] + 1
                y_pos[i] = y_pos[i-1]
            elif arah <= 0.5:  # kiri
                x_pos[i] = x_pos[i-1] - 1
                y_pos[i] = y_pos[i-1]
            elif arah <= 0.75:  # atas
                x_pos[i] = x_pos[i-1]
                y_pos[i] = y_pos[i-1] + 1
            elif arah <= 1:  # bawah
                x_pos[i] = x_pos[i-1]
                y_pos[i] = y_pos[i-1] - 1

            # KOREKSI DGN PBC
            if x_pos[i] > x_max:
                x_pos[i] = x_pos[i] - 1
            elif x_pos[i] < x_min:
                x_pos[i] = x_pos[i] + 1
            elif y_pos[i] > y_max:
                y_pos[i] = y_pos[i] - 1
            elif y_pos[i] < y_min:
                y_pos[i] = y_pos[i] + 1

            # PENGECEKAN PENYEBARAN VIRUS (INDIVIDU PADA POSISI YG SAMA)
            for j in range(individu):
                if j != i:
                    if (x_pos[j] == x_pos[i]) and (y_pos[j] == y_pos[i]):
                        if statusHealth[j] != "terinfeksi" and statusHealth[j] != "imun":
                            if statusHealth[i] == "terinfeksi":
                                statusHealth[j] = "terinfeksi"
                                waktuInfeksi[j] = 1
                                jml_terinfeksi += 1
                        elif statusHealth[j] == "terinfeksi":
                            if statusHealth[i] == "sehat":
                                statusHealth[i] = "terinfeksi"
                                waktuInfeksi[i] = 1
                                jml_terinfeksi += 1

        # PENGECEKAN PERUBAHAN STATUS TERINFEKSI -> IMUN
        if statusHealth[i] == "terinfeksi":
            if waktuInfeksi[i] <= waktuPulih:
                waktuInfeksi[i] += 1
                x_infeksi.append(x_pos[i])
                y_infeksi.append(y_pos[i])
            else:
                statusHealth[i] = "imun"
                jml_terinfeksi -= 1
                x_sehat.append(x_pos[i])
                y_sehat.append(y_pos[i])
        else:
            x_sehat.append(x_pos[i])
            y_sehat.append(y_pos[i])

        plt.figure(1)
        plt.subplot(1, 2, 1)
        plt.title('Simulasi Random Walk Penyebaran Virus')
        plt.plot(x_infeksi, y_infeksi, 'ro')
        plt.plot(x_sehat, y_sehat, 'go')

    # PERUBAHAN HARI
    hari_ke += 1
    hari.append(hari_ke)

    # PERUBAHAN INFEKSI
    totalInfeksi.append(jml_terinfeksi)
    plt.subplot(1, 2, 2)
    plt.plot(totalInfeksi, color='blue')
    plt.title("Grafik Penyebaran Virus")
    plt.xlabel('Jumlah Hari')
    plt.ylabel('Jumlah Terinfeksi')
    Camera.snap()

print("Total waktu pemulihan yang diperlukan oleh komunitas: ", max(hari))

for i in range(len(totalInfeksi)):
    print("Hari ke "+str(hari[i]))
    print("Jumlah yang Terinfeksi: "+str(totalInfeksi[i]))
    print("")

# Animasi Plot
anim = Camera.animate(interval=1000)
plt.grid(True, which="both")
anim.save('plot dan grafik.mp4')
rc('animation', html='jshtml')
plt.show()
