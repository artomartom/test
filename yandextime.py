#!/bin/python3

 
import urllib.request, json 
import datetime

yandexurl = "https://yandex.com/time/sync.json?geo=213"

def download_json():
        with urllib.request.urlopen(yandexurl) as url:
            data = json.load(url)
            return data

def ms_to_date(ms ):
    return datetime.datetime.fromtimestamp(ms/1000.0)

 
def ajdust_timezone(date):
    return date        

def task_a():
    data = download_json()    
    print ("Задание 1.а")
    print ("    Результат в сыром виде:")
    print (data)

def task_b( ):
    data = download_json()    
    print ("Задание 1.b")
    date= ms_to_date(data['time'] ).strftime('%Y-%m-%d %H:%M:%S')[:-3]
       
    timezone = data['clocks']['213']['offsetString']
     
    print(f"  Временная зона: {timezone}")
    print(f"  Дата: {date}")



def get_delta():
    start_time = datetime.datetime.now()
    response_time = download_json()['time']
    start_time = ajdust_timezone(start_time)
    resp_time= ms_to_date(response_time)
    delta = (resp_time - start_time ).total_seconds()
    return delta

def task_c( ):

    print ("Задание 1.с")
    print ("Выводим дельту времени")
    delta = get_delta()
    print (f"   Дельта: {delta} ")

     
def task_d( ):

    print ("Задание 1.d")
    print ("среднее время 5и запросов")

    deltas =[]
    
    try:
        for i in range(5):
                delta = get_delta()
                delta=0
                if delta == 0: 
                    raise BaseException("delta cant be 0, stoping...")
                deltas.append() 
                #print (f"   Дельта: {deltas[i]} ")
    except  BaseException as e:      
        print (e)
        return 

    avrage = sum(deltas)/ len(deltas)
    print (f"   Средняя дельта: {avrage} ") 

def main():

    task_a()
    task_b()
    task_c()
    task_d()
    




if __name__ == "__main__":
    main()

 
#print(type(data))
#print(data)
#print( ms_to_date(),)
