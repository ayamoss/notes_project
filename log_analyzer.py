import re
from collections import Counter
import time


def analyze_logs_fast(file_path):
    ip_counter = Counter()
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            match = re.search(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', line)
            if match:
                ip_counter[match.group(0)] += 1
    return ip_counter.most_common(3)


if __name__ == "__main__":
    log_file_name = "server_demo.log"
    print("Генерация тестового файла логов...")
    with open(log_file_name, "w", encoding="utf-8") as f:
        for i in range(50000):
            f.write("192.168.1.15 - [23/Jun/2026] \"GET /api/notes HTTP/1.1\" 200\n")
            f.write("10.0.0.42 - [23/Jun/2026] \"POST /api/notes HTTP/1.1\" 201\n")
        for i in range(10000):
            f.write("172.16.254.1 - [23/Jun/2026] \"GET /favicon.ico HTTP/1.1\" 404\n")

    print(f"Файл {log_file_name} успешно создан.\n" + "-" * 40)

    start_time = time.time()
    result = analyze_logs_fast(log_file_name)
    end_time = time.time()

    print("Результат анализа (Топ-3 IP-адреса):")
    for ip, count in result:
        print(f"IP: {ip} | Запросов: {count}")

    print("-" * 40)
    print(f"Время выполнения алгоритма O(N): {end_time - start_time:.4f} сек.")
