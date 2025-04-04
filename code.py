import requests
import json
import datetime
import time

def get_time_data():
    # a) Выполняем запрос и выводим сырой ответ
    url = "https://yandex.com/time/sync.json?geo=213"
    print("Выполняем запрос к ресурсу...")
    
    start_time = datetime.datetime.now()  # Фиксируем время перед запросом
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверяем на ошибки HTTP
        raw_data = response.text
        print("\na) Сырой ответ от сервера:")
        print(raw_data)
        
        # b) Парсим JSON и выводим понятное время и временную зону
        data = json.loads(raw_data)
        timestamp = data['time'] / 1000  # Конвертируем из мс в секунды
        time_str = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        timezone = data['clocks'][0]['name']
        
        print("\nb) Человекочитаемое время и временная зона:")
        print(f"Время: {time_str}")
        print(f"Временная зона: {timezone}")
        
        # c) Вычисляем дельту времени
        server_time = datetime.datetime.fromtimestamp(timestamp)
        delta = (server_time - start_time).total_seconds()
        
        return delta
        
    except requests.exceptions.RequestException as e:
        print(f"\nОшибка при выполнении запроса: {e}")
        return None

def main():
    deltas = []
    
    # d) Выполняем серию из 5 запросов
    for i in range(5):
        print(f"\n--- Запрос {i+1} из 5 ---")
        delta = get_time_data()
        if delta is not None:
            deltas.append(delta)
            print(f"\nc) Дельта времени: {delta:.3f} секунд")
        
        if i < 4:  # Не ждем после последнего запроса
            time.sleep(1)  # Пауза между запросами
    
    if deltas:
        avg_delta = sum(deltas) / len(deltas)
        print(f"\nd) Средняя дельта по 5 запросам: {avg_delta:.3f} секунд")
    else:
        print("\nНе удалось получить данные ни по одному запросу")

if __name__ == "__main__":
    main()