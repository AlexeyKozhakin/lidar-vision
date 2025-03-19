import numpy as np
import laspy
import os


def global_filter_iterative(las_data, z_sigma_threshold, max_iter=100):
    """
    Итерационная глобальная фильтрация выбросов по оси Z.
    Фильтрация останавливается, если выбрасываемых точек больше нет или если достигнут предел итераций.
    
    :param las_data: Лас-объект с данными
    :param z_sigma_threshold: Порог по сигмам для фильтрации
    :param max_iter: Максимальное количество итераций
    :return: Отфильтрованные данные
    """
    z = las_data.z
    for iteration in range(max_iter):
        # Рассчитываем среднее и стандартное отклонение
        mu_z = np.mean(z)
        std_z = np.std(z)

        # Определяем диапазон
        lower_bound = mu_z - z_sigma_threshold * std_z
        upper_bound = mu_z + z_sigma_threshold * std_z

        # Индексы точек, попадающих в диапазон
        valid_indices = np.where((z >= lower_bound) & (z <= upper_bound))[0]

        # Если все точки в пределах диапазона, завершаем фильтрацию
        if len(valid_indices) == len(z):
            print(f'Количество итераций для фильтрации: {iteration}')
            break

        # Применяем фильтрацию
        las_data.points = las_data.points[valid_indices]
        z = las_data.z  # Обновляем массив z после удаления точек

    else:
        # Если цикл завершился, но количество итераций достигло максимума
        raise Exception(f"Достигнуто максимальное количество итераций ({max_iter}) при фильтрации.")

    return las_data

def process_las_filter_global(input_directory, output_directory, z_sigma_threshold, max_iter=100):
    # Проход по всем файлам в директории
    for filename in os.listdir(input_directory):
        if filename.endswith(".las"):
            filepath = os.path.join(input_directory, filename)
            print(f"Обработка файла: {filepath}")
            las_data = laspy.read(filepath)
            las_file = global_filter_iterative(las_data, z_sigma_threshold, max_iter=100)
            filepath_out = os.path.join(output_directory, filename)
            las_file.write(filepath_out)

if __name__ == "__main__":
    import config_preprocessing as cp
    import time
    input_directory = cp.path_las_noise  # Указать путь к каталогу с LAS-файлами
    output_directory = cp.path_las_clean  # Указать путь к каталогу с LAS-файлами
    # Создаем выходную директорию, если она не существует
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    start = time.time()
    z_sigma_threshold = cp.filter_params['global_filter']['z_sigma_threshold']
    process_las_filter_global(input_directory, output_directory, z_sigma_threshold, max_iter=100)
    end = time.time()
    print(round((end-start)/60,1))