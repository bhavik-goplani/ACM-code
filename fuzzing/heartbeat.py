from fuzz import fuzzer
import random

secrets = ("<space for reply>" + fuzzer(100) +
           "<secret-certificate>" + fuzzer(100) +
           "<secret-key>" + fuzzer(100) + "<other-secrets>")

uninitialized_memory_marker = "deadbeef"
while len(secrets) < 2048:
    secrets += uninitialized_memory_marker


def heartbeat(reply: str, length: int, memory: str) -> str:
    # Store reply in memory
    memory = reply + memory[len(reply):]

    # Send back heartbeat
    s = ""
    for i in range(length):
        s += memory[i]
    return s

print(heartbeat("potato", 6, memory=secrets))
print(heartbeat("bird", 4, memory=secrets))
print(heartbeat("hat", 500, memory=secrets))
''' 
If the length is greater than the length of the reply string, additional contents of memory spill out. 
Note that all of this still occurs within regular array bounds, so an address sanitizer would not be triggered:
'''
# AddressSanitizer (ASan) - memory error detector - exposes many hard-to-find bugs with zero false positives: 

for i in range(10):
        s = heartbeat(fuzzer(), random.randint(1, 500), memory=secrets)
        assert not s.find(uninitialized_memory_marker)
        assert not s.find("secret")