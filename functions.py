import math 


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
