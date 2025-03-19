import numpy as np
import laspy
import os

def filter_las_data(las_data, n_points):
    """
    Фильтрует данные las_data, выбирая случайную выборку из n_points точек.
    
    :param las_data: laspy.LasData, данные из las файла
    :param n_points: int, количество точек в отфильтрованном датасете
    :return: laspy.LasData, отфильтрованные данные
    """
    total_points = len(las_data.x)
    if n_points >= total_points:
        return las_data  # Если запрашиваемое количество больше доступного, возвращаем исходные данные
    
    indices = np.random.choice(total_points, n_points, replace=False)  # Выбираем случайные индексы
    
    las_data_filtered = laspy.create(point_format=las_data.header.point_format, file_version=las_data.header.version)
    las_data_filtered.header = las_data.header  # Копируем заголовок
    
    for dimension in las_data.point_format.dimensions:  # Копируем все атрибуты точек
        setattr(las_data_filtered, dimension.name, getattr(las_data, dimension.name)[indices])
    
    return las_data_filtered

def process_las_reduce_points(input_directory, output_directory, n_points=1_000_000):
    # Проход по всем файлам в директории
    for filename in os.listdir(input_directory):
        if filename.endswith(".las"):
            filepath = os.path.join(input_directory, filename)
            print(f"Обработка файла: {filepath}")
            las_data = laspy.read(filepath)
            las_file = filter_las_data(las_data, n_points)
            filepath_out = os.path.join(output_directory, filename)
            las_file.write(filepath_out)

# Пример использования
if __name__ == "__main__":
    import config_preprocessing as cp
    import time
    input_directory = cp.path_las_many_points  # Указать путь к каталогу с LAS-файлами
    output_directory = cp.path_las_reduced_points  # Указать путь к каталогу с LAS-файлами
    # Создаем выходную директорию, если она не существует
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    start = time.time()
    process_las_reduce_points(input_directory, output_directory, n_points=cp.number_of_points)
    end = time.time()
    print(round((end-start)/60,1))
