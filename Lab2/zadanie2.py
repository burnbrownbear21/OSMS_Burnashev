import math
import matplotlib.pyplot as plt
import numpy as np

# Исходные данные
#N_sec_BS = 3 # Число секторов на одной BS
#MCL = 0 # Потери на многолучевое распространение сигнала , дБ 
#N_f = 0 # Потери на связанные с фидерами устройства, дБ
#S_total = 10*10**6 # Полоса частот, Гц
#S_area = 100 # Площадь территории, кв.км
#S_building = 4 # Площадь торговых и бизнес центров, кв.м

# ----------------------------------------------------------
# Исходики:
# ----------------------------------------------------------

TX_BOW_BS = 46 # Мощность передатчиков BS, дБм
TX_POW_UE = 24 # Мощность передатчика пользовательского терминала UE, дБм
AntGainBS = 21 # Коэффициент усиления антенны BS, дБи
N_p = 15 # Запас мощности сигнала на проникновения сквозь стены, дБ
IM = 1 # Запас мощности сигнала на интерференцию, дБ 
Noise_f_bs = 2.4 # Коэффициент шума приемника BS, дБ 
Noise_f_ue = 6 # Коэффициент шума приемника пользователя, дБ 
Feeder_Loss = 2 # дБ
SINR_DL = 2 # Требуемое отношение SINR для DL, дБ
SINR_UL = 4 # Требуемое отношение SINR для UL, дБ
MIMO_Gain = 3*2 # Число приемо-передающих антенн на BS 
f = 1.8 # Диапазон частот, ГГц
hBS = 50 # Высота базовой станции, м 
hUE = 3 # Высота пользовательского терминала, м 
BW_UL = 10*10**6 # Полоса частот в UL, Гц 
BW_DL = 20*10**6 # Полоса частот в DL, Гц 
duplex = 'FDD' # Дуплекс UL и DL

# --------------------------------------------------------
# Расчет бюджета восходящего канала:
# --------------------------------------------------------

# TxPowerUE-FeederLoss+AntGainBS+MIMOGain-PL(d)-IM-Penetration>=RxSensBS 
# RxSens = 𝑁𝑜𝑖𝑠𝑒𝐹𝑖𝑔𝑢𝑟𝑒 + 𝑇ℎ𝑒𝑟𝑚𝑎𝑙𝑁𝑜𝑖𝑠𝑒 + 𝑅𝑒𝑞𝑖𝑟𝑒𝑑𝑆𝐼𝑁𝑅, (2.17)
ThermalNoise_UL = -174 + 10 * math.log10(BW_UL) # (2.18)
RxSens_bs = Noise_f_bs + ThermalNoise_UL + SINR_UL # (2.17)
MAPL_UL = (- RxSens_bs + TX_POW_UE - Feeder_Loss + AntGainBS + MIMO_Gain - IM - N_p) 
print('Бюджет восходящего канала:', MAPL_UL ,'дБ')

# --------------------------------------------------------
# Расчет бюджета нисходящего канала:
# --------------------------------------------------------

# TxPowerBS − 𝐹𝑒𝑒𝑑𝑒𝑟𝐿𝑜𝑠𝑠 + AntGainBS + MIMOGain − MAPL_DL − IM − PenetrationM = RxSensUE. (2.19)
# RxSens = 𝑁𝑜𝑖𝑠𝑒𝐹𝑖𝑔𝑢𝑟𝑒 + 𝑇ℎ𝑒𝑟𝑚𝑎𝑙𝑁𝑜𝑖𝑠𝑒 + 𝑅𝑒𝑞𝑖𝑟𝑒𝑑𝑆𝐼𝑁𝑅, (2.17)
ThermalNoise_DL = -174 + 10 * math.log10(BW_DL) # (2.18)
RxSens_ue = Noise_f_ue+ThermalNoise_DL+SINR_DL
MAPL_DL = (- RxSens_ue + TX_BOW_BS - Feeder_Loss + AntGainBS + MIMO_Gain - IM - N_p) 
print('Бюджет нисходящего канала:', MAPL_DL ,'дБ')

# --------------------------------------------------------
# UMiNLOS
# --------------------------------------------------------

# 𝑃𝐿дБ = 20𝑙𝑜𝑔10 (4𝜋𝑑/𝜆) = 20𝑙𝑜𝑔10 (4𝜋𝑑𝑓/𝑐) (2.2) для свободного пространства
# Формула для расчета затуханий UMiNLOS имеет вид (2.3): 𝑃𝐿(𝑑) = 26 ∙ 𝑙𝑜𝑔10(f[ГГц]) + 22.7 + 36.7 ∙ 𝑙𝑜𝑔10(d[м]), (2.3)
d = np.arange(1, 3000) # м 
PL_UM = 26 * np.log10(f)+ 22.7 + 36.7 * np.log10(d)
intersection = np.intersect1d(MAPL_UL, MAPL_DL)
Sum_UM = round(4000**2 / (1.95 * 575**2))
print('UMiNLOS R_UL =', 575 ,'м')
print('UMiNLOS R_DL =', 1710 ,'м')
print('UMiNLOS кол-во базовых станций: ', Sum_UM)

#distance = d[np.where(PL_UM == intersection)]
#print('Расстояние до точки пересечения:', distance[0], 'м')

# --------------------------------------------------------
# COST231
# --------------------------------------------------------

# Формула для расчета затуханий имеет вид (2.14): 𝑃𝐿(𝑑) = 𝐴 + 𝐵 ∙ 𝑙𝑜𝑔10(𝑓) − 13.82 ∙ 𝑙𝑜𝑔10(ℎ𝐵𝑆) − 𝑎 + 𝑠 ∙ 𝑙𝑜𝑔10(𝑑) + 𝐿𝑐𝑙𝑢𝑡𝑡𝑒
# a = 3.2 ∙ [𝑙𝑜𝑔10(11.75 ∙ ℎ𝑚𝑠)]2 − 4.97 для 𝐷𝑈(плотная городская застройка) и U(город)
# a = [1.1 ∙ 𝑙𝑜𝑔10(𝑓)] ∙ ℎ𝑚𝑠 − [1.56 ∙ 𝑙𝑜𝑔10(𝑓) − 0.8] для 𝑆𝑈 (пригород), 𝑅𝑈𝑅𝐴𝐿 (сельская местность), 𝑅𝑂𝐴D(трасса)
# s = 44.9 − 6.55 ∙ 𝑙𝑜𝑔10(𝑓), для 𝑑 ≥ 1 км ---- зависит от hBS

hms = 1 # метров ; hms для мобильных антенн от 1 дом 10 м
a_U = 3.2 * np.log10(11.75 * hms) * 2 - 4.97 # для DU U 
a_R = (1.1 * np.log10(f)) * hms * (1.6 * np.log10(f) - 0.8) # для SU, RURAL, ROAD
Lclutter_SU = - (2 * (np.log10(f/28))**2 + 5.4)
s = 44.9 - 6.55 * np.log10(f) 
hBS = 50 # метров ; hbs для подвеса антенны базовой станции от 30 до 200 м 
PL_CO = 46.3 + 33.9 * np.log10(f) - 13.8 * np.log10(hBS) - a_R + s * np.log10(d) + Lclutter_SU
Sum_CO = round(100000**2 / (1.95 * 302**2))
print('COST231 R_UL =', 302 ,'м')
print('COST231 R_DL =', 745 ,'м')
print('COST231 кол-во базовых станций: ', Sum_CO)

# --------------------------------------------------------
# Walfish-Ikegami
# --------------------------------------------------------

# 𝐿𝐿𝑂𝑆 = 42.6 + 20𝑙𝑜𝑔10(𝑓) + 26𝑙𝑜𝑔10(𝑑). (2.8) - прямой видимости

Walfish_Vid = 42.6 + 20 * np.log10(f) + 26 * np.log10(d)
L1 = - 18 * np.log10(1+hBS + 10)
if (L1 < 0):
   L1 = 0 
L0 = 32.44 + 20*np.log10(f)+20*np.log10(d)
w = 40 # метров, ширина улицы
L2 = -16.9-10*np.log10(w)+10*np.log10(f)+20*np.log10(10-hms)+2.5+0.075*25
Walfish_Ots = L0+L1+L2


plt.figure(figsize=(10, 6))
plt.plot(d, PL_UM, label='Path Loss UMiNLOS(PL_UM)')
plt.plot(d, PL_CO, label='Path Loss COST231(PL_CO)')
plt.plot(d, Walfish_Vid, label='Walfish-Ikegami Прямая видимость')
plt.plot(d, Walfish_Ots, label='Walfish-Ikegami Отс. Прямой видимости')
plt.axhline(y=MAPL_UL, color='r', linestyle='--', label='Uplink')
plt.axhline(y=MAPL_DL, color='g', linestyle='--', label='Downlink')
plt.xlabel('Distance (m)')
plt.ylabel('Path Loss (dB)')
plt.title('Path Loss vs. Distance')
plt.legend()
plt.grid(True)
plt.show()
