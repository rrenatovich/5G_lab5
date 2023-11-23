import math 
import numpy as np

c = 299792458 # константа скорости света
# функция для модели FSPL в шкале дБм
def FSPL_dBm(f, d):
  return 20 * math.log10(d) + 20 * math.log10(f) - 147.55

# функция для модели FSPL в шкале Ватт
def FSPL_W(f, d):
  return pow((4 * math.pi * d * f) / c, 2)

# функция для перевода дБм в ваты
def dBm_to_W(value):
  return 0.001 * pow(10, value / 10)

# функция для расчета отношения сигнал шум в шкале Ватт
def SNR_W(model, B, N, increase, Pt):
  return (dBm_to_W(Pt) * dBm_to_W(increase) * dBm_to_W(increase) / model) / (B * dBm_to_W(N))

# функция для расчета отношения сигнал шум в шкале дБм
def SNR_dBm(model, B, N, increase, Pt):
  return 10 * math.log10(1000 * (Pt * increase * increase / model) / (B * N))

def shennon_dBm(SNR, B):
  return B * math.log2(1 + SNR)


h_BS = 25 # высота антенны BS
h_UT = 15 # высота антенны UT

# функция для расчета расстояния между вершинами двух антенн
def d_3D_value(h_BS, h_UT, d):
  return math.sqrt(pow(h_BS - h_UT, 2) + pow(d, 2))

def d_break_value(h_BS, h_UT, d, f):
  if d <= 18:
    g = 0
  else:
    g = 5 / 4 * pow(d / 100, 3) * math.exp(-d / 150)

  if h_UT < 13:
    C = 0
  elif h_UT <= 23 and h_UT >= 13:
    C = pow((h_UT - 13) / 10, 1.5) * g
  else:
    return "Значение h_UT слишком большое"

  p = np.random.random()
  prob = 1 / (1 + C)
  if p < prob:
    h_E = 1  # эффективная высота окружающей среды
  else:
    h_E = np.random.randint(low=12, high=h_UT-1.5)

  return 4 * (h_BS - h_E) * (h_UT - h_E) * f / c

# функция для модели UMaLOS в шкале дБм
def UMaLOS_dBm(f, d):
  d_break = d_break_value(h_BS, h_UT, d, f)
  if d >= 10 and d <= d_break:
    return 28 + 22 * math.log10(d_3D_value(h_BS, h_UT, d)) + 20 * math.log10(f)
  elif d >= d_break and d <= 5000:
    return 28 + 40 * math.log10(d_3D_value(h_BS, h_UT, d)) + 20 * math.log10(f) - 9 * math.log10(pow(d_break, 2) + pow(h_BS - h_UT, 2))
  else:
    return 0

# функция для модели UMaNLOS в шкале дБм
def UMaNLOS_dBm(f, d, PL_UMaLOS):
  PL_UMaNLOS = 13.54 + 39.08 * math.log10(d_3D_value(h_BS, h_UT, d)) + 20 * math.log10(f) - 0.6 * (h_UT - 1.5)
  if d >= 10 and d <= 5000:
    return max(PL_UMaNLOS, PL_UMaLOS)
  else:
    return 0

# функция для модели InHLOS в шкале дБм
def InHLOS_dBm(f, d):
  d_3D = d_3D_value(h_BS, h_UT, d)
  if 1 <= d_3D and d_3D <= 150:
    return 32.4 + 17.3 * math.log10(d_3D_value(h_BS, h_UT, d)) + 20 * math.log10(f)
  else:
    return 0

# функция для модели InHNLOS в шкале дБм
def InHNLOS_dBm(f, d, PL_InHLOS):
  PL_InHNLOS = 17.3 + 38.3 * math.log10(d_3D_value(h_BS, h_UT, d)) + 24.9 * math.log10(f)
  if d >= 10 and d <= 5000:
    return max(PL_InHNLOS, PL_InHLOS)
  else:
    return 0