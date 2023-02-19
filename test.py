import heapq
import io
import os
import unittest

from sys import getsizeof
from tempfile import NamedTemporaryFile

from sort import read_substr, save_str_to_file, sort_and_write, sort_chunks, cleanup, push, min_heap_sort



class TestSaveStrToFile(unittest.TestCase):
    def test_file_saved_correctly(self):
        # create a temporary file
        with NamedTemporaryFile(delete=False) as f:
            file_name = f.name
            text = "Hello, world!"
            
            # save text to file
            save_str_to_file(file_name, text)

            # read the saved file
            with open(file_name, 'r', encoding='utf-8') as saved_file:
                saved_text = saved_file.read()

            # check that the text matches the saved text
            self.assertEqual(text, saved_text)
        
        # cleanup: delete the temporary file
        os.unlink(file_name)



class TestSortAndWrite(unittest.TestCase):
    def test_sort_and_write(self):
        # create a temporary file
        with NamedTemporaryFile(delete=False) as f:
            file_name = f.name
            chars = ["b", "a", "c"]

            # call the function to sort and write characters to the file
            sort_and_write(file_name, chars)

            # read the saved file
            with open(file_name, 'r', encoding='utf-8') as saved_file:
                saved_text = saved_file.read()

            # check that the saved text is the sorted string of characters
            self.assertEqual(saved_text, "abc")

        # cleanup: delete the temporary file
        os.unlink(file_name)



class TestReadSubstr(unittest.TestCase):
    def test_returns_empty_list_when_max_size_is_zero(self):
        # Arrange
        file = io.StringIO('hello')
        max_size = 0

        # Act
        result = read_substr(file, max_size)

        # Assert
        self.assertEqual(result, [])

    def test_returns_empty_list_when_max_size_is_negative(self):
        # Arrange
        file = io.StringIO('hello')
        substr_size = -1

        # Act
        result = read_substr(file, substr_size)

        # Assert
        self.assertEqual(result, [])

    def test_reads_no_more_bytes_than_allowed(self):
        # Arrange
        file = io.StringIO('helloworld')
        max_size = 55

        # Act
        result = read_substr(file, max_size)

        # Assert
        self.assertTrue(getsizeof(''.join(result)) <= max_size)

    def test_returns_all_characters_when_file_is_smaller_than_max_size(self):
        # Arrange
        file = io.StringIO('hello')
        max_size = getsizeof(['h', 'e', 'l', 'l', 'o']) + 1

        # Act
        result = read_substr(file, max_size)

        # Assert
        self.assertEqual(result, ['h', 'e', 'l', 'l', 'o'])



class TestCleanup(unittest.TestCase):
    def test_cleanup(self):
        # create a tmp directory and a file in it
        os.mkdir('./tmp/')
        with open('./tmp/test_file', 'w', encoding='utf-8') as file:
            file.write('test')

        # call the cleanup function
        cleanup()

        # check that the tmp directory and file are deleted
        self.assertFalse(os.path.exists('./tmp/'))
        self.assertFalse(os.path.exists('./tmp/test_file'))



class TestSortChunks(unittest.TestCase):
    def test_sort_chunks(self):
        try:
            # create a temporary file
            with NamedTemporaryFile(delete=False) as f:
                file_name = f.name
                text = "edcbaxag"

                # write text to the file
                with open(file_name, 'w', encoding='utf-8') as file:
                    file.write(text)

                # call the function to sort chunks of the file
                max = 120
                sort_chunks(file_name, max)

                # check that the tmp directory was created and contains the expected number of files
                self.assertTrue(os.path.exists('./tmp/'))
                self.assertEqual(len(os.listdir('./tmp/')), 2)  # 3 files: sorted_1, sorted_2

                # check the contents of each sorted file
                with open('./tmp/sorted_1', 'r', encoding='utf-8') as file:
                    self.assertEqual(file.read(), 'abcde')
                with open('./tmp/sorted_2', 'r', encoding='utf-8') as file:
                    self.assertEqual(file.read(), 'agx')

        finally:
            # cleanup: delete the temporary file and tmp directory
            os.unlink(file_name)
            cleanup()



class TestPush(unittest.TestCase):
    def test_push(self):
        # create a heap and a counters dictionary
        heap = []
        heapq.heapify(heap)
        counters = {}

        # push a character onto the heap
        file = io.StringIO()
        char = 'a'
        push(char, heap, counters, file)

        # check that the heap and counters are updated correctly
        expected_heap = [('a', 1, file)]
        self.assertEqual(heap, expected_heap)
        self.assertEqual(counters[char], 1)

        # push the same character onto the heap again
        push(char, heap, counters, file)

        # check that the heap and counters are updated correctly again
        expected_heap = [('a', 1, file), ('a', 2, file)]
        self.assertEqual(heap, expected_heap)
        self.assertEqual(counters[char], 2)



class TestMinHeapSort(unittest.TestCase):
    def test_min_heap_sort(self):
        # create some temporary files with characters in them
        os.mkdir('./tmp/')
        with open('./tmp/file1', 'w', encoding='utf-8') as file:
            file.write('abc')
        with open('./tmp/file2', 'w', encoding='utf-8') as file:
            file.write('abc')

        # call the min_heap_sort function to sort the characters in the files
        min_heap_sort('./sorted_output')

        # check that the sorted output file contains the correct characters
        with open('./sorted_output', 'r', encoding='utf-8') as file:
            sorted_chars = file.read()
            self.assertEqual(sorted_chars, 'aabbcc')

        # cleanup
        cleanup()
        os.remove('./sorted_output')



if __name__ == '__main__':
    unittest.main()
