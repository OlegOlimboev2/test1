from multiprocessing import Process, Lock, shared_memory
import array

def process_element(shm_name, array_length, index, lock):
    shm = shared_memory.SharedMemory(name=shm_name)
    shared_buffer = shm.buf

    with lock:
        start = index * 4
        num = int.from_bytes(shared_buffer[start:start + 4], byteorder='little')
        result = num ** 2
        shared_buffer[start:start + 4] = result.to_bytes(4, byteorder='little')
        current_state = []
        for i in range(array_length):
            pos = i * 4
            current_state.append(int.from_bytes(shared_buffer[pos:pos + 4], byteorder='little'))
        print(f'Процесс изменил массив: {current_state}')

    shm.close()

if __name__ == '__main__':
    data = array.array('i', [1, 4, 9])
    array_length = len(data)
    buffer_size = array_length * 4

    shm = shared_memory.SharedMemory(create=True, size=buffer_size)

    shared_buffer = shm.buf
    for i, val in enumerate(data):
        shared_buffer[i * 4:(i + 1) * 4] = val.to_bytes(4, byteorder='little')

    lock = Lock()
    processes = []

    for i in range(array_length):
        p = Process(
            target=process_element,
            args=(shm.name, array_length, i, lock)
        )
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    final_array = []
    for i in range(array_length):
        pos = i * 4
        final_array.append(
            int.from_bytes(shared_buffer[pos:pos + 4], byteorder='little')
        )
    print(f'\nИсходный массив после изменений: {final_array}')

    shm.close()
    shm.unlink()