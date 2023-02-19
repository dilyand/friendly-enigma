# friendly-enigma

Read a very large file, containing a single continuous string of UTF-8 characters, and sort the string using little memory.

## Algo

1.) Read the string in chunks, sort each chunk and write it to a tmp file.

2.) Read the tmp files one char at a time, pushing the read chars onto a heap. Since the tmp files contain sorted strings, we are always reading the 'lowest' char from each tmp file.

3.) Pop the min value from the heap and write it to the output file.

4.) Read a new char from the same file where the popped min value originated.

5.) Loop until all chars are read from all tmp files.

## Run tests

```
python3 test.py
```

## Run program

This program creates a very large number of temporary files. You may need to increase the limit for open file handles your OS allows before you can run it. Eg, on MacOS: `ulimit -Sn 10000`.

```
python3 sort.py 'path/to/input_file'
```

Find the sorted string in './out.txt'.

## Memory usage reports

During the read and sort chunks phase, the program prints the memory usage of the current process after writing every sorted chunk to a tmp file.

During the heap sort phase, the program prints the memory usage of the current process after every 10m elements handled.
