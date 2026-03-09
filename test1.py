import multiprocessing

def process_file(file_path, result_queue):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            line_count = sum(1 for line in file)
        result_queue.put((file_path, line_count))
    except FileNotFoundError:
        result_queue.put((file_path, "Файл не найден"))
    except Exception as e:
        result_queue.put((file_path, f"Ошибка: {e}"))


def main():
    file_paths = ["file1.txt", "file2.txt", "file3.txt"]
    result_queue = multiprocessing.Queue()
    processes = []

    for file_path in file_paths:
        process = multiprocessing.Process(
            target=process_file,
            args=(file_path, result_queue)
        )
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    while not result_queue.empty():
        file_path, line_count = result_queue.get()
        print(f"Количество строк в файле: {file_path}: {line_count}.")

if __name__ == "__main__":
    main()