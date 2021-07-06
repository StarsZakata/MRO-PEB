import numpy as np
import matplotlib.pyplot as plt
import time
#класс ПЭБ
class PEB:
    #Исходные данные
    priceSchedule=[1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 2, 3, 5, 5, 5, 4.5, 3, 3, 3, 3, 4.5, 5, 7, 9, 11, 12, 8, 4]
    loadSchedule=[450, 300, 270, 320, 330, 345, 420, 560, 780, 720, 680, 720, 800, 820, 960, 1100, 1180, 1290, 1420, 1600, 1720, 1520, 790, 640]
    actionLoad = [-4000, -3000, -2000, -1000, 0, 1000, 2000, 3000, 4000]
    capacity=17000
    initCharge=5000
    constantLoad=350
    targetCharge=5000
    CurrentCharge = initCharge

    #Хеш-таблицы для хранения промежуточных результатов
    #+вспомогательный параметр
    book=dict()
    bookLoad = dict()
    Strategy=dict()
    CurCharge=dict()
    BestStrategy=""

    #Значения для графиков
    GraphicsStrategy=[]
    GraphicsCurrentCharge=[]
    GraphicsCurrentProfit=[]

    #Хранение конечного результата
    StrategyForPPU = []
    Charge=[]
    PriceProfit=[]

    #+вспомогательные параметры, для нахождения наилучшего действия
    MaxProfit = 0
    MaxProfitCharge = 0


    def price(self,n,m):
        for i in range(n):
            for j in range(m):
                SumLoad = self.constantLoad+self.loadSchedule[j]+self.actionLoad[i]
                Pricecalc = self.priceSchedule[j]*SumLoad
                price = "priceHour"+str(i)+"-"+str(j)
                sumload="sumload"+str(i)+"-"+str(j)
                self.book[sumload]=SumLoad
                self.book[price]=Pricecalc

    def Max(self):
        for i in range (len(self.Charge)):
            if self.Charge[i]>self.targetCharge:
                if self.PriceProfit[i]>self.MaxProfit:
                    self.MaxProfit=self.PriceProfit[i]
                    self.MaxProfitCharge=self.Charge[i]
                    self.BestStrategy=self.StrategyForPPU[i]

    def Dinamic1(self,n):
            for i in range(n):
                for k in range(n):
                    self.Strategy[str(i)+"-"+str(k)]=str(i)+"->"+str(k)
                    self.CurCharge[str(i)+"-"+str(k)] = self.initCharge - self.book["sumload" + str(i) +"-"+ str(0)]-self.book["sumload" + str(k) +"-"+ str(1)]
                    self.bookLoad[str(i)+"-"+str(k)]=self.book["priceHour" + str(i) +"-"+ str(0)]+self.book["priceHour" + str(k) +"-"+ str(1)]
                    if self.CurCharge[str(i)+"-"+str(k)]<0 or self.CurCharge[str(i)+"-"+str(k)]>self.capacity:
                        del self.CurCharge[str(i)+"-"+str(k)]
                        del self.bookLoad[str(i)+"-"+str(k)]
                        del self.Strategy[str(i)+"-"+str(k)]
                    try:
                        for key,value in self.CurCharge.items():
                            if value==self.CurCharge[str(i)+"-"+str(k)]:
                                if self.bookLoad[key]>self.bookLoad[str(i)+"-"+str(k)]:
                                    print(self.bookLoad[key])
                                    print(self.bookLoad[str(i)+"-"+str(k)])
                                    del self.CurCharge[str(i) +"-"+ str(k)]
                                    del self.bookLoad[str(i) +"-"+ str(k)]
                                    del self.Strategy[str(i) + "-" + str(k)]
                                if self.bookLoad[key]<self.bookLoad[str(i)+"-"+str(k)]:
                                    del self.CurCharge[key]
                                    del self.bookLoad[key]
                                    del self.Strategy[key]
                    except:
                        pass
            self.Charge=list(self.CurCharge.values())
            self.PriceProfit=list(self.bookLoad.values())
            self.StrategyForPPU=list(self.Strategy.values())
    def Dinamic2(self,m,n):
        for r in range (2,m):
            for i in range(len(self.CurCharge)):
                for k in range(n):
                    self.CurCharge[str(i) +"-"+ str(k)] = self.Charge[i]-self.book["sumload" + str(k) +"-"+ str(r)]
                    self.bookLoad[str(i) +"-"+ str(k)] = self.PriceProfit[i]+self.book["priceHour" + str(k) +"-"+ str(r)]
                    self.Strategy[str(i)+"-"+str(k)]=self.StrategyForPPU[i]+"->"+str(k)
                    if self.CurCharge[str(i) +"-"+ str(k)] < 0 or self.CurCharge[str(i) +"-"+ str(k)] > self.capacity:
                        del self.CurCharge[str(i) +"-"+ str(k)]
                        del self.bookLoad[str(i) +"-"+ str(k)]
                        del self.Strategy[str(i)+"-"+str(k)]
                    try:
                        count=0
                        for key,value in self.CurCharge.items():
                            if value==self.CurCharge[str(i)+"-"+str(k)]:
                                if self.bookLoad[key]>self.bookLoad[str(i)+"-"+str(k)]:
                                    del self.CurCharge[str(i) +"-"+ str(k)]
                                    del self.bookLoad[str(i) +"-"+ str(k)]
                                    del self.Strategy[str(i) + "-" + str(k)]
                                if self.bookLoad[key]<self.bookLoad[str(i)+"-"+str(k)]:
                                    del self.CurCharge[key]
                                    del self.bookLoad[key]
                                    del self.Strategy[key]
                                else:
                                     count=count+1
                                     if count>=2:
                                         del self.CurCharge[str(i) + "-" + str(k)]
                                         del self.bookLoad[str(i) + "-" + str(k)]
                                         del self.Strategy[str(i) + "-" + str(k)]
                    except:
                        pass
            self.Charge = list(self.CurCharge.values())
            self.PriceProfit = list(self.bookLoad.values())
            self.StrategyForPPU=list(self.Strategy.values())
    def Graphics(self):
        self.GraphicsStrategy=self.BestStrategy.split("->")
        index=[]

        for i in range (len(self.GraphicsStrategy)):
            index.append(i+1)
            if self.GraphicsStrategy[i]=="0":
                self.GraphicsStrategy[i]=-4000
            elif self.GraphicsStrategy[i]=="1":
                self.GraphicsStrategy[i] = -3000
            elif self.GraphicsStrategy[i]=="2":
                self.GraphicsStrategy[i] = -2000
            elif self.GraphicsStrategy[i]=="3":
                self.GraphicsStrategy[i] = -1000
            elif self.GraphicsStrategy[i]=="4":
                self.GraphicsStrategy[i] = 0
            elif self.GraphicsStrategy[i] =="5":
                self.GraphicsStrategy[i] = 1000
            elif self.GraphicsStrategy[i]=="6":
                self.GraphicsStrategy[i] = 2000
            elif self.GraphicsStrategy[i]=="7":
                self.GraphicsStrategy[i] = 3000
            elif self.GraphicsStrategy[i]=="8":
                self.GraphicsStrategy[i]= 4000
            else:
                print("Что-то не так в начальных данных")
        print("Стратегия по продаже энергии в сеть:",self.GraphicsStrategy)
        plt.figure(figsize=(8, 5))
        plt.title("Стратегия по продаже энергии в сеть",fontsize=20)
        plt.xlabel("Час",fontsize=15)
        plt.ylabel("Вт",fontsize=15)
        plt.xticks(index)
        plt.bar(index, self.GraphicsStrategy,color="green")
        ax = plt.gca()
        ax.axhline(color='k')
        plt.show()

        for k in range (len(self.GraphicsStrategy)):
            if k==0:
                self.GraphicsCurrentCharge.append(self.initCharge-self.constantLoad-self.loadSchedule[k]-self.GraphicsStrategy[k])
            else:
                self.GraphicsCurrentCharge.append(self.GraphicsCurrentCharge[k-1]-self.constantLoad-self.loadSchedule[k]-self.GraphicsStrategy[k])
        print("Заряд батиареи по часам:",self.GraphicsCurrentCharge)
        plt.figure(figsize=(8, 5))
        plt.title("Заряд батареи по часам",fontsize=20)
        plt.xlabel("Час",fontsize=15)
        plt.ylabel("Вт/ч",fontsize=15)
        plt.xticks(index)
        plt.plot(index,self.GraphicsCurrentCharge, color="red",linewidth=4)
        plt.scatter(index, self.GraphicsCurrentCharge, color="orange", s=100)
        ax = plt.gca()
        ax.axhline(color='k')
        plt.show()

        for r in range (len(self.GraphicsStrategy)):
            if r==0:
                self.GraphicsCurrentProfit.append(self.priceSchedule[r]*(self.constantLoad+self.loadSchedule[r]+self.GraphicsStrategy[r]))
            else:
                self.GraphicsCurrentProfit.append(self.GraphicsCurrentProfit[r-1]+self.priceSchedule[r] * (self.constantLoad + self.loadSchedule[r] + self.GraphicsStrategy[r]))
        print("Прибыль по часам: ",self.GraphicsCurrentProfit)
        plt.figure(figsize=(8, 5))
        plt.title("Прибыль по часам",fontsize=20)
        plt.xlabel("Час",fontsize=15)
        plt.ylabel("Прибыль (рубли)",fontsize=15)
        plt.xticks(index)
        plt.plot(index,self.GraphicsCurrentProfit, color="black",linewidth=4)
        plt.scatter(index, self.GraphicsCurrentProfit, color="blue", s=100)
        ax = plt.gca()
        ax.axhline(color='k')
        plt.show()

start_time = time.time()
peb = PEB()
peb.price(9,24)
peb.Dinamic1(9)
peb.Dinamic2(24,9)
peb.Max()
peb.Graphics()
print("--- %s seconds ---" % (time.time() - start_time))
