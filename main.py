import math
import numpy as np
import matplotlib.pyplot as plt
from functions import * 

MHz = pow(10, 6) # перевод из МГц в Гц
GHz = pow(10, 9) # перевод из ГГц в Гц
f = [900 * MHz, 1.9 * GHz, 28 * GHz] # массив со значениями частот

Pt = 23 # излучаемая мощность антены БС
increase = 10 # усиление на передаче и приеме
B = 400 * MHz # ширина канала
N = -174 # тепловой шум

shennon_dBm_list = [], [], []
d = 240 # значение расстояния
for i in range(len(shennon_dBm_list)):
  for j in range(1, d + 1):
    # вычисление значений скорости Шеннона для всех расстояний
    shennon_dBm_list[i].append(shennon_dBm(SNR_W(FSPL_W(f[i], j), B, N, increase, Pt), B))


fig = plt.subplots(figsize=(7, 5))

# график значения скорости Шеннона от расстояния для нескольких частот
plt.plot(shennon_dBm_list[0], label="f = $900$ МГц")
plt.plot(shennon_dBm_list[1], label="f = $1.9$ ГГц")
plt.plot(shennon_dBm_list[2], label="f = $28$ ГГц")
plt.title('Значение скорости Шеннона от расстояния', fontsize=16, fontweight="bold")
plt.xlabel('Значение расстояния', fontsize=12)
plt.ylabel('Значение скорости', fontsize=12)
plt.xlim(0, d - 1)
plt.grid()
plt.legend(loc=1)
plt.savefig('shenon_from_dist.png')


# переменные для того, чтобы посмотреть зависимость скорости от частоты, усиления на передаче и мощности передачи
increase_list = [10, 15, 20]
Pt_list = [23, 25, 30]

print('Зависимость от частоты')
for i in range(3):
  print(f"Скорость Шеннона: {round(shennon_dBm(SNR_W(FSPL_W(f[i], d), B, N, increase_list[0], Pt_list[0]), B), 3)}, f = {int(f[i])} Гц, усил = {increase_list[0]} дБ, Pt ={Pt_list[0]} дБм"))
print('Зависимость от усиления')
for i in range(3):
  print(f"Скорость Шеннона: {round(shennon_dBm(SNR_W(FSPL_W(f[0], d), B, N, increase_list[i], Pt_list[0]), B), 3)}, f = {int(f[0])} Гц, усил = {increase_list[i]} дБ, Pt = {Pt_list[0]} дБм")
print('Зависимость от Pt')
for i in range(3):
  print(f"Скорость Шеннона: {round(shennon_dBm(SNR_W(FSPL_W(f[0], d), B, N,increase_list[0], Pt_list[i]), B), 3)}, f = {int(f[0])} Гц, усил = {increase_list[0]} дБ, Pt = {Pt_list[i]} дБм")

# Task 2 

FSPL_dBm_list = []
UMaLOS_dBm_list = []
UMaNLOS_dBm_list = []
InHLOS_dBm_list = []
InHNLOS_dBm_list = []
d = 240 # значение расстояния
for i in range(10, d + 1):
  # вычисление значений скорости Шеннона для всех расстояний
  FSPL_dBm_list.append(FSPL_dBm(f[0], i))
  UMaLOS_dBm_value = UMaLOS_dBm(f[0], i)
  UMaLOS_dBm_list.append(UMaLOS_dBm_value)
  UMaNLOS_dBm_list.append(UMaNLOS_dBm(f[0], i, UMaLOS_dBm_value))
  InHLOS_dBm_value = InHLOS_dBm(f[0], i)
  InHLOS_dBm_list.append(InHLOS_dBm_value)
  InHNLOS_dBm_list.append(InHNLOS_dBm(f[0], i, InHLOS_dBm_value))

fig = plt.subplots(figsize=(7, 5))

plt.plot(FSPL_dBm_list, label="FSPL")
plt.plot(UMaLOS_dBm_list, label="UMaLOS")
plt.plot(UMaNLOS_dBm_list, label="UMaNLOS")
plt.plot(InHLOS_dBm_list, label="InHLOS")
plt.plot(InHNLOS_dBm_list, label="InHNLOS")
plt.title('Значение моделей распространения от расстояния', fontsize=14, fontweight="bold")
plt.xlabel('Значение расстояния', fontsize=12)
plt.ylabel('дБм', fontsize=12)
plt.xlim(0, d - 10)
plt.grid()
plt.legend()
plt.savefig('models_from_dist.png')


# Task 3 

FSPL_shennon_dBm_list = []
UMaLOS_shennon_dBm_list = []
UMaNLOS_shennon_dBm_list = []
InHLOS_shennon_dBm_list = []
InHNLOS_shennon_dBm_list = []
d = 120 # значение расстояния
for i in range(10, d + 1):
  # вычисление значений скорости Шеннона для всех расстояний
  FSPL_shennon_dBm_list.append(shennon_dBm(SNR_W(FSPL_W(f[0], i), B, N, increase, Pt), B))
  UMaLOS_dBm_value = UMaLOS_dBm(f[0], i)
  UMaLOS_shennon_dBm_list.append(shennon_dBm(SNR_W(dBm_to_W(UMaLOS_dBm_value), B,N, increase, Pt), B))
  UMaNLOS_shennon_dBm_list.append(shennon_dBm(SNR_W(dBm_to_W(UMaNLOS_dBm(f[0], i, UMaLOS_dBm_value)), B, N, increase, Pt), B))
  InHLOS_dBm_value = InHLOS_dBm(f[0], i)
  InHLOS_shennon_dBm_list.append(shennon_dBm(SNR_W(dBm_to_W(InHLOS_dBm_value), B, N, increase, Pt), B))
  InHNLOS_shennon_dBm_list.append(shennon_dBm(SNR_W(dBm_to_W(InHNLOS_dBm(f[0], i,InHLOS_dBm_value)), B, N, increase, Pt), B))

fig = plt.subplots(figsize=(7, 5))

# график значения скорости Шеннона от расстояния
plt.plot(UMaLOS_shennon_dBm_list, label="UMaLOS")
plt.plot(UMaNLOS_shennon_dBm_list, label="UMaNLOS")
plt.plot(InHLOS_shennon_dBm_list, label="InHLOS")
plt.plot(InHNLOS_shennon_dBm_list, label="InHNLOS")
plt.title('Значение скорости Шеннона от расстояния', fontsize=14, fontweight="bold")
plt.xlabel('Значение расстояния', fontsize=12)
plt.ylabel('Значение скорости', fontsize=12)
plt.xlim(0, d - 10)
plt.grid()
plt.savefig('shenon_model_from_dist.png')


fig = plt.subplots(figsize=(7, 5))

# график значения скорости Шеннона от расстояния для нескольких частот
plt.plot(FSPL_shennon_dBm_list, label="FSPL")
plt.title('Значение скорости Шеннона от расстояния', fontsize=14, fontweight="bold")
plt.xlabel('Значение расстояния', fontsize=12)
plt.ylabel('Скорость', fontsize=12)
plt.xlim(0, d - 10)
plt.grid()
plt.savefig('shenon_FSPL_from_dist.png')