import json
import sys
import itertools

def generate_versions(template, count=2):
    """Генерирует несколько версий на основе шаблона"""
    parts = template.split('.')
    generated = []
    
    # Генерируем все возможные комбинации для звездочек
    star_indices = [i for i, part in enumerate(parts) if part == '*']
    if not star_indices:
        return [template]  # если нет звездочек, возвращаем сам шаблон
    
    # Генерируем 2 случайных варианта для каждой звездочки
    for _ in range(count):
        new_parts = parts.copy()
        for i in star_indices:
            new_parts[i] = str(random.randint(0, 9))  # генерируем цифру 0-9
        generated.append('.'.join(new_parts))
    
    return generated

def version_to_tuple(version_str):
    """Преобразует строку версии в кортеж чисел для сравнения"""
    return tuple(map(int, version_str.split('.')))

def main():
    if len(sys.argv) != 3:
        print("Использование: python script.py <версия> <конфиг файл>")
        sys.exit(1)
    
    input_version = sys.argv[1]
    config_file = sys.argv[2]
    
    try:
        # Чтение конфигурационного файла
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        # Генерация всех версий
        all_versions = []
        for template in config.values():
            all_versions.extend(generate_versions(template))
        
        # Удаляем дубликаты и сортируем
        unique_versions = list(set(all_versions))
        sorted_versions = sorted(unique_versions, key=version_to_tuple)
        
        print("Все сгенерированные версии (отсортированные):")
        for version in sorted_versions:
            print(version)
        
        # Фильтрация версий старше входной
        input_tuple = version_to_tuple(input_version)
        older_versions = [
            v for v in sorted_versions 
            if version_to_tuple(v) < input_tuple
        ]
        
        print(f"\nВерсии старше {input_version}:")
        for version in older_versions:
            print(version)
            
    except FileNotFoundError:
        print(f"Ошибка: файл {config_file} не найден")
    except json.JSONDecodeError:
        print("Ошибка: неверный формат JSON в конфигурационном файле")
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")

if __name__ == "__main__":
    import random
    random.seed()  # Инициализация генератора случайных чисел
    main()