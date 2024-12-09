import random
import string
from time import time
from threading import Thread
from multiprocessing import Process, Manager

def create_large_text_file(filename, num_words=1000000):
    with open(filename, 'w') as file:
        for _ in range(num_words):
            word = ''.join(random.choices(string.ascii_lowercase, k=random.randint(3, 10)))
            file.write(word + ' ')

def count_words_sequential(filename):
    with open(filename, 'r') as file:
        text = file.read()
    word_freq = {}
    for word in text.split():
        word_freq[word] = word_freq.get(word, 0) + 1
    return word_freq

def count_words_threading(filename):
    def worker(text_chunk, word_freq):
        for word in text_chunk.split():
            word_freq[word] = word_freq.get(word, 0) + 1
    
    with open(filename, 'r') as file:
        text = file.read()
    
    chunks = [text[i:i + len(text) // 4] for i in range(0, len(text), len(text) // 4)]
    word_freq = {}
    threads = []
    
    for chunk in chunks:
        thread = Thread(target=worker, args=(chunk, word_freq))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    return word_freq

def count_words_multiprocessing(filename):
    def worker(text_chunk, return_dict, idx):
        word_freq = {}
        for word in text_chunk.split():
            word_freq[word] = word_freq.get(word, 0) + 1
        return_dict[idx] = word_freq
    
    with open(filename, 'r') as file:
        text = file.read()
    
    chunks = [text[i:i + len(text) // 4] for i in range(0, len(text), len(text) // 4)]
    manager = Manager()
    return_dict = manager.dict()
    processes = []
    
    for idx, chunk in enumerate(chunks):
        process = Process(target=worker, args=(chunk, return_dict, idx))
        processes.append(process)
        process.start()
    
    for process in processes:
        process.join()
    
    word_freq = {}
    for chunk_freq in return_dict.values():
        for word, count in chunk_freq.items():
            word_freq[word] = word_freq.get(word, 0) + count
    
    return word_freq

if __name__ == "__main__":
    create_large_text_file("large_text.txt")

    start = time()
    sequential_result = count_words_sequential("large_text.txt")
    print(f"Sequential: {time() - start:.2f} seconds")
    
    start = time()
    threading_result = count_words_threading("large_text.txt")
    print(f"Threading: {time() - start:.2f} seconds")
    
    start = time()
    multiprocessing_result = count_words_multiprocessing("large_text.txt")
    print(f"Multiprocessing: {time() - start:.2f} seconds")

