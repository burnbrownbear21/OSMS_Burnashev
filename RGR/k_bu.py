import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import correlate

#CRC
def calculate_crc(array):
    G = [0, 1, 1, 1, 1, 1, 1, 1]
    length_array = len(array)
    array += [0] * 7  # добавление 7 нулей
    for i in range(length_array-1):
        if array[i] == 1:
            for j in range(8):
                array[i+j] ^= G[j]
    
    return array[length_array:]

#Проверка CRC
def check_crc(array):
    G = [0, 1, 1, 1, 1, 1, 1, 1]
    length_array = len(array)
    for i in range(length_array-8):
        if array[i] == 1:
            for j in range(8):
                array[i+j] ^= G[j]
    
    return array[-7:]
#Последовательность голда. Генерация псевдослучайных последовательностей используем ибо он имеет хорошее автокорреляционные свойства
def calculate_gold_pos():
    x = [0, 1, 0, 0, 0] # 8
    y = [0, 1, 1, 1, 1] # 8+7=15
    gold = []
    for i in range(31):
        gold.append(x[4] ^ y[4])
        xx = x[3] ^ x[4]
        del x[-1]
        x.insert(0, xx)
        yy = y[1] ^ y[4]
        del y[-1]
        y.insert(0, yy)
        
    return list(gold)

def cor_priem(array, posl_g):
    posl_g_x10 = [bit for bit in posl_g for i in range(10)]
    
    index = correlate(array, posl_g_x10)
    index = index / (len(posl_g_x10)/1.5)
    plt.figure(9)
    plt.title("Автокорреляция")
    plt.plot(index)

    indexm = []
    indexm.append(np.argmax(index))
    indexm.append(np.argmax(index[indexm[0]+50:]) + indexm[0]+50)
    print(indexm)
    return array[indexm[0]:indexm[1]]


    
def decoding(array):
    decod_bit = []
    for i in range(0, len(array), 10):
        sred = sum(array[i:i+10])
        sred = int(sred) / 10
        if sred > 0.5:
            decod_bit.append(1)
        else:
            decod_bit.append(0)
    
    return decod_bit

# Ввод имени и фамилии
name = input("Введите имя: ")
sname = input("Введите фамилию: ")

# Кодирование в ASCII и запись в массив, преобразование в int
# Шифруем полученные данные в ASCII после преобразуем в 8 битное бинарное представление
bposl = list(''.join(format(ord(char), '08b') for char in name + sname))
bposl = [int(bit) for bit in bposl]

print('Бит.послед. ', bposl)

bposl_copy = bposl.copy()
crc = calculate_crc(bposl_copy)
print('crc', crc)
posl_g = calculate_gold_pos()
print('gold', posl_g)

bposl_Nx = [bit for bit in posl_g + bposl + crc + posl_g for i in range(10)]  # повторение каждого бита 10 раз

print('max index', len(bposl_Nx))
index = int(input("Введите номер для вставки: "))

# Вставка в удвоенный массив
bposl_Nx_2 = [0] * (len(bposl_Nx)*2) # создание пустого массива
bposl_Nx_2[index:index+len(bposl_Nx)] = bposl_Nx 

noice = np.random.uniform(-0.3, 0.3, len(bposl_Nx_2)) # 0.3 размер шума

bposl_Nx_2_noice = bposl_Nx_2 + noice

singal = cor_priem(bposl_Nx_2_noice, posl_g) # сигнал без лишнего в начале
signal_decod = decoding(singal)
#signal_decod = signal_decod[:len(bposl)+len(crc)]
signal_decod = signal_decod[:-len(posl_g)]

check = check_crc(signal_decod.copy())
print("Check crc: ", check)
if 1 in check:
    print("ОШИБКА")
else:
    signal_decod = signal_decod[:-7]

print("Получено", signal_decod)

# Преобразуем массив бит в строку
bstr = ''.join(str(bit) for bit in signal_decod)

# Разделим строку на байты и преобразуем каждый байт в символ ASCII
text = ''.join([chr(int(bstr[i:i+8], 2)) for i in range(0, len(bstr), 8)])

print(text)

plt.figure(1)
plt.title("2 задание")
plt.plot(bposl)

plt.figure(2)
plt.title("вместе с Голдом и crc")
plt.plot(bposl_Nx)

plt.figure(3)
plt.title("удвоенная")
plt.plot(bposl_Nx_2)

plt.figure(4)
plt.title("удвоенная с шумом")
plt.plot(bposl_Nx_2_noice)

plt.figure(5)
plt.title("полученный сигнал")
plt.plot(singal)

plt.figure(6)
plt.title("декодированный")
plt.plot(signal_decod)

# 13 
fft_otpr = np.fft.fftshift(abs(np.fft.fft(bposl_Nx_2))) + 100
fft_pol = np.fft.fftshift(abs(np.fft.fft(bposl_Nx_2_noice)))
t = np.arange(-(len(fft_otpr)/2), len(fft_otpr)/2)
plt.figure(7)
plt.title('Спектры полученного и переданного')
plt.plot(t,fft_otpr)
plt.plot(t,fft_pol)

# Разной длительности
x05 = np.repeat(bposl, 5)
x1 = np.repeat(bposl, 10)
x2 = np.repeat(bposl, 20)

# Удлинение короткого и укорочение длинного
x05 = np.concatenate((x05, x05))
x2 = x2[:len(x1)]

fft_05 = np.fft.fftshift(abs(np.fft.fft(x05)/len(x05)))+0.4
fft_1 = np.fft.fftshift(abs(np.fft.fft(x1)/len(x1)))+0.2
fft_2 = np.fft.fftshift(abs(np.fft.fft(x2)/len(x2)))

t = np.arange(-(len(fft_05)/2), len(fft_05)/2)
plt.figure(8)
plt.title('Спектры 3 разных по длительности сигналов')
plt.plot(t,fft_05) 
plt.plot(t,fft_1)
plt.plot(t,fft_2)

plt.show()