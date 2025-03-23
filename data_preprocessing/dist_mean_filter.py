import os
import numpy as np


def dist_mean_filter(input_dir, filename, feature_output_tensor, threshold=4):
    """
    Фильтрует файлы на основе значений dist_mean.
    Удаляет файл, если все значения выходят за границы mu_dist_mean ± threshold * std_dist_mean.
    """
    file_path = os.path.join(input_dir, filename)
    
    # Проверяем, существует ли файл
    if not os.path.exists(file_path):
        print(f"Файл {filename} не найден.")
        return False
    
    # Загружаем данные
    try:
        data = np.load(file_path)
    except Exception as e:
        print(f"Ошибка загрузки файла {filename}: {e}")
        return False
    
    # Получаем канал dist_mean
    dist_mean = data[:, :, feature_output_tensor['dist_mean']].flatten()
    
    # Вычисляем статистики
    mu_dist_mean = np.mean(dist_mean)
    std_dist_mean = np.std(dist_mean)
    
    # Определяем границы
    upper_bound = mu_dist_mean + threshold * std_dist_mean
    print('max_dist_mean =',np.max(dist_mean))
    print('min_dist_mean =',np.min(dist_mean))
    print('mu+4*std =', upper_bound)
    print('==========================================')
    # Проверяем, находятся ли все значения в допустимых границах
    if np.all(np.max(dist_mean) <= 5):
        print(f"Файл {filename} сохранён.")
        return True
    else:
        os.remove(file_path)  # Удаляем файл
        print(f"Файл {filename} удалён (данные вне диапазона).")
        return False

if __name__ == "__main__":
    import config_preprocessing as cp
    import time
    
    start = time.time()
    # Пример вызова функции
    input_dir = cp.path_tensors_dist_mean_filter

    # Получаем список файлов .npy
    filenames = [f for f in os.listdir(input_dir) if f.endswith('.npy')]
    print(filenames)
    for filename in filenames:
        dist_mean_filter(input_dir, filename, cp.feature_output_tensor)
    end = time.time()
    print(round((end-start)))