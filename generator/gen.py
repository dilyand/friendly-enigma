import random
import io
import codecs

CHUNK_SIZE = int((1024 * 1024 * 1024) / 10)

# Define the number of chunks to generate
NUM_CHUNKS = 2 * 6


def get_random_chars(length):

    # Update this to include code point ranges to be sampled
    include_ranges = [
        ( 0x0041, 0x005A ),
        ( 0x0061, 0x007A ),
        ( 0x0030, 0x0039 ),
        ( 0x0410, 0x044F ),
    ]

    alphabet = [
        chr(code_point) for current_range in include_ranges
            for code_point in range(current_range[0], current_range[1] + 1)
    ]

    return ''.join(random.choice(alphabet) for i in range(length))

# Generate random UTF-8 characters and write to file in chunks
if __name__ == '__main__':
    with io.open('random_characters_1.txt', 'w', encoding='utf-8') as f:
        for i in range(NUM_CHUNKS):
            characters = get_random_chars(CHUNK_SIZE)
            f.write(characters)
            f.flush()
