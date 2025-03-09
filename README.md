# lidar-vision
# LiDAR-Vision-ML (Скриптовая часть)

## 📌 Описание

Этот раздел документации описывает, как использовать скрипты для обработки LiDAR данных, обучения модели, инференса (предсказаний) и визуализации результатов. Все операции выполняются через командную строку, что позволяет гибко настроить работу с данными и моделью.

## 📌 Установка

1. **Клонировать репозиторий**:
    ```bash
    git clone https://github.com/username/lidar2image-ml.git
    cd lidar2image-ml
    ```

2. **Установить зависимости**:
    Для начала установите все необходимые библиотеки:
    ```bash
    pip install -r requirements.txt
    ```

## 📌 Конфигурационные файлы

В конфигурационных файлах (`configs/`) содержатся параметры, которые настраивают каждый этап обработки. Вы можете изменять эти файлы, чтобы изменить поведение скриптов:

- `configs/preprocess_config.yaml` — настройки для предобработки LiDAR данных.
- `configs/train_config.yaml` — параметры для обучения модели.
- `configs/inference_config.yaml` — параметры для инференса.

## 📌 Шаги пайплайна

### 1. **Обработка данных**:
   Преобразует данные LiDAR в 3-канальные изображения.

   Запустите:
   ```bash
   python scripts/preprocess.py --config configs/preprocess_config.yaml
```

### 2. **Обучение модели**:
Обучает модель для классификации или сегментации на основе обработанных данных.

Запустите:
```bash
python scripts/train.py --config configs/train_config.yaml
```
### 3. **Инференс (предсказания)**:
Применяет обученную модель к новым данным для предсказания объектов.

Запустите:
```bash
python scripts/inference.py --config configs/inference_config.yaml
```
### 4. **Визуализация результатов**:
Визуализирует результаты классификации или сегментации.

Запустите:
```bash
python scripts/visualize.py --input data/results/
```
📌 **Запуск всего пайплайна**
Для автоматического запуска всего пайплайна можно использовать скрипт run_pipeline.sh, который последовательно выполнит все этапы обработки:
```bash
#!/bin/bash
echo "📌 Запуск обработки данных..."
python scripts/preprocess.py --config configs/preprocess_config.yaml

echo "📌 Обучение модели..."
python scripts/train.py --config configs/train_config.yaml

echo "📌 Инференс..."
python scripts/inference.py --config configs/inference_config.yaml

echo "📌 Визуализация результатов..."
python scripts/visualize.py --input data/results/
```
