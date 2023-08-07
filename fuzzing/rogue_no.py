'''
With fuzzing, it is easy to generate uncommon values in the input, 
causing all kinds of interesting behavior. 
Consider the following code, again in the C language, 
which first reads a buffer size from the input, and then allocates a buffer of the given size:

char *read_input() {
    size_t size = read_buffer_size();
    char *buffer = (char *)malloc(size);
    // fill buffer
    return (buffer);
}
What happens if size is very large, exceeding program memory? 
What happens if size is less than the number of characters following? 
What happens if size is negative? 
By providing a random number here, fuzzing can create all kinds of damages.
'''

from fuzz import fuzzer

def collapse_if_too_large(s):
    if int(s) > 1000:
        raise ValueError

long_number = fuzzer(100, ord('0'), 10)
print(long_number)

collapse_if_too_large(long_number)