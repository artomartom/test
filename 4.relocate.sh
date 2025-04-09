#!/bin/bash 





# Проверяем, что скрипт запущен от root
if [ "$(id -u)" -ne 0 ]; then
    echo "Этот скрипт должен быть запущен с правами root" >&2
    exit 1
fi

 
# get list of foobar-* services 
mapfile -t services < <(systemctl list-units --no-legend --no-pager  --type=service --state=running   "foobar-*" | awk '{print $1}')


for service in "${services[@]}"; do
    echo "Обработка сервиса: $service"
    
    # Получаем название сервиса (часть после foobar-)
    service_name=${service#foobar-}
    service_name=${service_name%.service}  # Удаляем .service если есть
    
    # Определяем пути
    old_dir="/opt/misc/${service_name}"
    new_dir="/srv/data/${service_name}"
    old_service_path="${old_dir}/foobar-daemon"
    
    # Получаем текущие параметры из юнита
    unit_path="/etc/systemd/system/${service}"
    if [ ! -f "$unit_path" ]; then
        echo "Файл юнита $unit_path не найден, пропускаем"
        continue
    fi
    
    # Останавливаем сервис
    echo "Останавливаем сервис $service"
    systemctl stop "$service" || {
        echo "Не удалось остановить $service, пропускаем"
        continue
    }
    
    # Переносим файлы
    echo "Переносим файлы из $old_dir в $new_dir"
    mkdir -p "$new_dir" || {
        echo "Не удалось создать директорию $new_dir"
        systemctl start "$service"
        continue
    }
    
    cp -a "${old_dir}/." "$new_dir/" || {
        echo "Не удалось скопировать файлы"
        systemctl start "$service"
        continue
    }
    
    # Редактируем юнит
     
    echo "Обновляем пути в $unit_path"
    sed -i.bak \
        -e 's/[[:space:]]//g' \  # убрать пробелы 
        -e "s|WorkingDirectory=${old_dir}|WorkingDirectory=${new_dir}|g" \
        -e "s|ExecStart=${old_dir}|ExecStart=${new_dir}|g" \
        "$unit_path" || {
        echo "Не удалось обновить пути в юните"
        systemctl start "$service"
        continue
    }
done
    # Перечитываем конфигурацию systemd
    systemctl daemon-reload
    
for service in "${services[@]}"; do   
    
    # Запускаем сервис
    echo "Запускаем сервис $service"
    systemctl start "$service" || {
        echo "Не удалось запустить $service"
        continue
    }
    
    echo "Сервис $service успешно перенесен и запущен"
    echo

done
 
 

