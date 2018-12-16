
import urllib,time,datetime
import numpy as np
import pandas as pd
import os
import math
import csv
import pandas.io.data

class Quote(object):
  
  DATE_FMT = '%Y-%m-%d'
  TIME_FMT = '%H:%M:%S'
  
  def __init__(self):
    self.symbol = ''
    self.date,self.time,self.open_,self.high,self.low,self.close,self.volume,self.avg10,self.avg20,self.avg50,self.avg100,self.avg200,self.bollinger_high,self.bollinger_low = ([] for _ in range(14))

  def append(self,dt,open_,high,low,close,volume,avg10,avg20,avg50,avg100,avg200,bollinger_high,bollinger_low):
    self.date.append(dt.date())
    self.time.append(dt.time())
    self.open_.append(float(open_))
    self.high.append(float(high))
    self.low.append(float(low))
    self.close.append(float(close))
    self.volume.append(int(volume))
    self.avg10.append(float(avg10))
    self.avg20.append(float(avg20))
    self.avg50.append(float(avg50))
    self.avg100.append(float(avg100))
    self.avg200.append(float(avg200))
    self.bollinger_high.append(float(bollinger_high))
    self.bollinger_low.append(float(bollinger_low))
        
  def to_csv(self):
    return ''.join(["{0},{1},{2},{3:.2f},{4:.2f},{5:.2f},{6:.2f},{7},{8:.2f},{9:.2f},{10:.2f},{11:.2f},{12:.2f},{13:.2f},{14:.2f}\n".format(self.symbol,
              self.date[bar].strftime('%Y-%m-%d'),self.time[bar].strftime('%H:%M:%S'),
              self.open_[bar],self.high[bar],self.low[bar],self.close[bar],self.volume[bar],self.avg10[bar],self.avg20[bar],self.avg50[bar],self.avg100[bar],self.avg200[bar],self.bollinger_high[bar],self.bollinger_low[bar]) 
              for bar in xrange(len(self.close))])
    
  def write_csv(self,filename):
    with open(filename,'w') as f:
      f.write(self.to_csv())
        
  def read_csv(self,filename):
    self.symbol = ''
    self.date,self.time,self.open_,self.high,self.low,self.close,self.volume = ([] for _ in range(7))
    for line in open(filename,'r'):
      symbol,ds,ts,open_,high,low,close,volume = line.rstrip().split(',')
      self.symbol = symbol
      dt = datetime.datetime.strptime(ds+' '+ts,self.DATE_FMT+' '+self.TIME_FMT)
      self.append(dt,open_,high,low,close,volume)
    return True

  def __repr__(self):
    return self.to_csv()

class WeeklyQuote(Quote):
  ''' Intraday quotes from Google. Specify interval seconds and number of days '''
  def __init__(self,symbol,interval_seconds=604800,num_days=5):
    super(WeeklyQuote,self).__init__()
    self.symbol = symbol.upper()
    #url_string = "http://www.google.com/finance/getprices?q={0}".format(self.symbol)
    #url_string += "&i={0}&p={1}Y&f=d,o,h,l,c,v".format(interval_seconds,num_days)
    
    #csv = urllib.urlopen(url_string).readlines()
    csv0  =  pd.io.data.get_data_yahoo(symbol.replace('\n',''),start = datetime.datetime(2011, 1, 3), end = datetime.datetime.now())
    csv = csv0.asfreq('W-FRI', method='pad')
    #print csv['Adj Close'][len(csv)-1]
    for bar in xrange(7,len(csv)):
      #print csv['Adj Close'][bar]
      close=csv['Adj Close'][bar]
      high=csv['High'][bar]
      low=csv['Low'][bar]
      open_=csv['Open'][bar]
      volume = csv['Volume'][bar]
      open_,high,low,close = [float(x) for x in [open_,high,low,close]]
      
      dt = csv.index[bar]
      if len(self.high)>=10:
        length=len(self.high)
        avg10=sum(self.close[length-9:length],close)/10
      else:
        avg10=0
      if len(self.high)>=20:
        length=len(self.high)
        avg20=sum(self.close[length-19:length],close)/20
      else:
        avg20=0
      if len(self.high)>=50:
        length=len(self.high)
        avg50=sum(self.close[length-49:length],close)/50
      else:
        avg50=0
      if len(self.high)>=100:
        length=len(self.high)
        avg100=sum(self.close[length-99:length],close)/100
      else:
        avg100=0
      if len(self.high)>=200:
        length=len(self.high)
        avg200=sum(self.close[length-199:length],close)/200
      else:
        avg200=0

      if len(self.high)>=20:
        length=len(self.high)
        std20=np.std(np.append(self.close[length-19:length],close))
      else:
        std20=0
      bollinger_high=avg20+2*std20
      bollinger_low=avg20-2*std20
            
      #if dt.hour<>9:
      self.append(dt,open_,high,low,close,volume,avg10,avg20,avg50,avg100,avg200,bollinger_high,bollinger_low)
class DailyQuote(Quote):
  ''' Intraday quotes from Google. Specify interval seconds and number of days '''
  def __init__(self,symbol,interval_seconds=604800,num_days=5):
    super(DailyQuote,self).__init__()
    self.symbol = symbol.upper()
    #url_string = "http://www.google.com/finance/getprices?q={0}".format(self.symbol)
    #url_string += "&i={0}&p={1}Y&f=d,o,h,l,c,v".format(interval_seconds,num_days)
    
    #csv = urllib.urlopen(url_string).readlines()
    csv0  =  pd.io.data.get_data_yahoo(symbol.replace('\n',''),start = datetime.datetime(2011, 1, 3), end = datetime.datetime.now())
    csv = csv0
    for bar in xrange(7,len(csv)):
      #print csv['Adj Close'][bar]
      close=csv['Adj Close'][bar]
      high=csv['High'][bar]
      low=csv['Low'][bar]
      open_=csv['Open'][bar]
      volume = csv['Volume'][bar]
      open_,high,low,close = [float(x) for x in [open_,high,low,close]]
      dt = csv.index[bar]
      if len(self.high)>=10:
        length=len(self.high)
        avg10=sum(self.close[length-9:length],close)/10
      else:
        avg10=0
      if len(self.high)>=20:
        length=len(self.high)
        avg20=sum(self.close[length-19:length],close)/20
      else:
        avg20=0
      if len(self.high)>=50:
        length=len(self.high)
        avg50=sum(self.close[length-49:length],close)/50
      else:
        avg50=0
      if len(self.high)>=100:
        length=len(self.high)
        avg100=sum(self.close[length-99:length],close)/100
      else:
        avg100=0
      if len(self.high)>=200:
        length=len(self.high)
        avg200=sum(self.close[length-199:length],close)/200
      else:
        avg200=0

      if len(self.high)>=20:
        length=len(self.high)
        std20=np.std(np.append(self.close[length-19:length],close))
      else:
        std20=0
      bollinger_high=avg20+2*std20
      bollinger_low=avg20-2*std20
      self.append(dt,open_,high,low,close,volume,avg10,avg20,avg50,avg100,avg200,bollinger_high,bollinger_low)
def send_email(user, pwd, recipient, subject, body):
    import smtplib

    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print 'successfully sent the mail'
    except:
        print "failed to send mail"

def irrationalReverse(q,trenddirection):
  if(trenddirection==1) and q.close[len(q.close)-1]<q.bollinger_low[len(q.close)-1]:
      return True
  if(trenddirection==2) and q.close[len(q.close)-1]>q.bollinger_high[len(q.close)-1]:
      return True

def trendscore(q,trenddirection):
  score=0
  if(q.avg10[len(q.close)-1]>q.avg10[len(q.close)-2]):
    score=score+1
  else:
    score=score-1
    
  if(q.avg20[len(q.close)-1]>q.avg20[len(q.close)-2]):
    score=score+1
  else:
    score=score-1
  if(q.avg50[len(q.close)-1]>q.avg50[len(q.close)-2]):
    score=score+1
  else:
    score=score-1
    
  if(trenddirection==1) and score==1:
      return True
  if(trenddirection==2) and score==-1:
      return True

if __name__ == '__main__':
  #1 uptrend 2 downtrend 3 no trend
  filename='SP500.txt'
  listSymbol = open(filename,'r').readlines()
  #print listSymbol
  listOuput=[]
  i=1
  if(i==1):
  #for bar in xrange(0,len(listSymbol)):
    #print bar
    try:
      symbol='YUM'
    #print symbol
      q = WeeklyQuote(symbol)
      p =  DailyQuote(symbol)
      print q
      print 'check'+symbol
     
      if(len(q.close)>200):
        if(q.avg50[len(q.close)-1]>q.avg50[len(q.close)-5]):
          trenddirection=1
        else:
          trenddirection=2
        if(p.close[len(p.close)-1]<(p.avg20[len(p.close)-1]-0.875*(p.avg20[len(p.close)-1]-p.bollinger_low[len(p.close)-1])) and trenddirection==1):
          listOuput.append([symbol,'LONG'])
        if(p.close[len(p.close)-1]<(q.avg20[len(q.close)-1]-0.875*(q.avg20[len(q.close)-1]-q.bollinger_low[len(q.close)-1])) and trenddirection==1):
          listOuput.append([symbol,'LONG'])
        if(p.close[len(p.close)-1]>(p.avg20[len(p.close)-1]+0.875*(p.avg20[len(p.close)-1]-p.bollinger_low[len(p.close)-1])) and trenddirection==2):
          listOuput.append([symbol,'SHORT'])
        if(p.close[len(p.close)-1]>(p.avg20[len(p.close)-1]+0.875*(p.avg20[len(p.close)-1]-p.bollinger_low[len(p.close)-1])) and trenddirection==2):
          listOuput.append([symbol,'SHORT'])
#
    except IOError:
      print 'IO error, next one'
    else:
      print 'Unknown error, next'
#  listOuput.append(['SPY','LONG'])
#  listOuput.append(['XOM','LONG'])
    i=i-1
  print listOuput
  
    
  if(len(listOuput)>1):
    send_email('wshenstock@gmail.com','bdbd0213','wshen02@gmail.com','StocktoCheck',listOuput)

    
                               # print it out
