import os


def get_file_sizes(directory):
    """Возвращает список файлов с их размерами в указанном каталоге."""
    file_sizes = []
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        if os.path.isfile(file_path):
            file_sizes.append((file_name, os.path.getsize(file_path)))
    return file_sizes


def check_file_count(directory, expected_count):
    """Проверяет количество файлов в каталоге и выбрасывает исключение при нехватке."""
    actual_count = len(os.listdir(directory))
    if actual_count < expected_count:
        raise ValueError(f"Количество файлов ({actual_count}) меньше ожидаемого ({expected_count}).")
    return actual_count


def remove_extra_files(directory, expected_count):
    """Удаляет лишние файлы с наименьшими размерами до достижения ожидаемого количества."""
    file_sizes = get_file_sizes(directory)
    if len(file_sizes) <= expected_count:
        return

    # Сортировка файлов по размеру (от меньшего к большему)
    file_sizes.sort(key=lambda x: x[1])
    files_to_remove = file_sizes[:len(file_sizes) - expected_count]

    for file_name, size in files_to_remove:
        os.remove(os.path.join(directory, file_name))
        print(f"Удален файл: {file_name} (размер: {size} байт)")


def cleanup_directory(input_directory, true_amount_of_files):
    """Основная функция очистки каталога от лишних файлов."""
    try:
        check_file_count(input_directory, true_amount_of_files)
        remove_extra_files(input_directory, true_amount_of_files)
        print("Очистка завершена.")
    except ValueError as e:
        print(e)


if __name__ == "__main__":
    import config_preprocessing as cp
    import time
    input_directory = cp.path_las_sliced  # Указать путь к каталогу с LAS-файлами
    start = time.time()
    true_amount_of_files = cp.true_amount_of_files
    cleanup_directory(input_directory, true_amount_of_files)
    end = time.time()
    print(round((end-start)/60,1))
