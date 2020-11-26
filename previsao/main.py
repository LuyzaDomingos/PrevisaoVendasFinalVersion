from Preprocessor import preProcessing
import matplotlib.pyplot as plt
from trend import Trend
from seasonal import Seasonal
import numpy as np

vendas = preProcessing('13')
vendasM = vendas.resample('M').sum()

numMeses = 12
ate = len(vendasM)-6

trend = Trend()
seasonal = Seasonal();

#for i in range(0 , 31):    
#    coef = trend.spearman_coef(np.log(vendasM.iloc[a_partir:, i]))
#    print('Prod ' + str(i)+': '+str(coef))

pUP = vendasM.iloc[12:ate, 0]
pDOWN = vendasM.iloc[12:ate, 26]
time = [i for i in range(1, len(pUP)+1)]
#print(time)

plt.plot(time, pUP, 'b-')
if seasonal.seasonality_test(pUP) :
  print('pUP Tem sazonalidade')
  seasonal.regression(pUP, 12)
  S = [seasonal.S(t-1) for t in time]
  Z_S = [d - s for d, s in zip(pUP,S)]
  plt.plot(time, Z_S, 'b--')
  plt.plot(time, S, 'r--')
  if seasonal.seasonality_test(Z_S) :
    print('pUP-S Tem sazonalidade')
  else:
    print('pUP-S NAO tem sazonalidade')


#plt.plot(time, pDOWN, 'r-')
if seasonal.seasonality_test(pDOWN) :
  print('pDown Tem sazonalidade')
  seasonal.regression(pDOWN, 12)
  S = [seasonal.S(t-1) for t in time]
  Z_S = [d - s for d, s in zip(pDOWN,S)]
  #plt.plot(time, S, 'r--')


maxData = np.amax(pUP) + 1
minData = np.amin(S) - 1
for t in range(12, len(pUP), + 12):
  plt.plot([t,t],[minData, maxData], 'k--')





#plt.plot(time, pDOWN, 'r-')
#plt.plot(time, trend.getT_polinomial(time, pDOWN), 'r--')
plt.savefig('plot.png')
