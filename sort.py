import argparse
import heapq
import os
import psutil
import shutil

from sys import getsizeof



MAX = 1024 * 1024 * 5
OUTPUT = "./out.txt"

# to report memory usage
process = psutil.Process(os.getpid())



def save_str_to_file(file_name, str):
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(str)



def sort_and_write(file_name, chars):
    # chars is a list of characters
    chars.sort()
    str = ''.join(chars)
    save_str_to_file(file_name, str)



def read_substr(file, max_size):
    """
    Read a substring from an open file containing a single line.
    Returns the chars of the substring as a list.
    max_size sets the limit for the size of the chars list.
    """
    chars = []
    
    if max_size <= 0:
        return chars
    
    read_size = getsizeof(chars)

    while read_size < max_size:
        char = file.read(1)
        if not char:
            # EOF
            break
        chars.append(str(char))
        read_size = getsizeof(chars)
        
    return chars



def cleanup():
    if os.path.exists('./tmp/'):
        shutil.rmtree('./tmp/')



def sort_chunks(file_name, max_size):
    print("Reading the input file in chunks and sorting each chunk. Reporting memory usage after each sorted chunk is saved to a tmp file.")

    chunk = 1

    cleanup()
    os.mkdir('./tmp/')

    with open(file_name, 'r', encoding='utf-8') as file:
        chars = read_substr(file, max_size)
        while (len(chars) > 0):
            sort_and_write('./tmp/sorted_' + str(chunk), chars)
            chars = read_substr(file, max_size)
            chunk = chunk + 1

            print("Memory usage: {} MB.".format(process.memory_full_info().uss / 1024 / 1024))



def push(char, heap, counters, file):
    """
    Push a value onto a heap.
    The value has three elements: (char, counter, file).
    char is a character that we want to sort.
    file is an open file handle for the file from which the char was read. 
    If char is the min element in the heap and gets popped, we use file to read a new char from the same file.
    counter is used to break ties between chars, since file handles can't be compared.
    """
    current_counter = counters.get(char, 0)
    heapq.heappush(heap, (str(char), current_counter + 1, file))
    counters[char] = current_counter + 1


def min_heap_sort(output_file):
    print("Merging the sorted chunks.")

    sorted_file = open(output_file, 'w+')

    # initialise a heap
    min_heap = []
    heapq.heapify(min_heap)
    
    # we'll store open file handles here
    open_files = []
    # we'll store counters for each char here
    counters = {}

    for f in os.listdir('./tmp/'):
        # read all files in the tmp folder one char at a time and push the char onto the heap
        if os.path.isfile('./tmp/' + f):
            file = open('./tmp/' + f)
            open_files.append(file)
            char = file.read(1)
            push(char, min_heap, counters, file)

    cycle_count = 0

    while(len(min_heap) > 0):
        cycle_count += 1
        # report memory usage every 10000000 elements
        if cycle_count % 10000000 == 0:
            print("Processed {} elements. Memory usage: {} MB.".format(cycle_count, process.memory_full_info().uss / 1024 / 1024))

        # pop the min element from the heap, write it to the sorted file, and push a new element onto the heap from the file where this element originated
        min_element = heapq.heappop(min_heap)
        sorted_file.write(str(min_element[0]))
        sorted_file.flush()
        next = min_element[2].read(1)
        if next:
            push(next, min_heap, counters, min_element[2])
        else:
            min_element[2].close()

    sorted_file.close()



def external_sort(input_file, output_file = OUTPUT, max_size = MAX):
    sort_chunks(input_file, max_size)
    min_heap_sort(output_file)
    cleanup()
    print('Sorted values are written to' , str(output_file))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Sort a lage file using little memory.')
    parser.add_argument('input_file', type=str, help='path to input file, eg ./in.txt')
    args = parser.parse_args()
    input = args.input_file
    
    external_sort(input)
