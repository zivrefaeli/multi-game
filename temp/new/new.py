def numbersInPi(pi: str, numbers: list):
    ranges = []
    map = {}
    
    for number in numbers:
        start = 0
        while True:
            try:
                index = pi.index(number, start)
                start = index + 1
            except ValueError:
                break
            else:
                length = len(number)
                ranges.append({"start": index, "end": index + length})

    for range in ranges:
        key = range['start']
        if key in map:
            map[key].append(range)
        else:
            map[key] = [range]

    array = []
    find(map, 0, len(pi), 0, array)
    if len(array) == 0:
        return -1
    return min(array)

def find(map, targetIndex, targetLength, count, counters):
    array = map.get(targetIndex)
    if not array:
        return
    for range in array:
        end = range['end']
        if end == targetLength:
            counters.append(count)
            return
        find(map, end, targetLength, count + 1, counters)

PI = "3141592653589793238462643383279"
NUMBERS = ["314159265358979323846", "26433", "8", "3279", "314159265", "35897932384626433832", "79"]

print(numbersInPi(PI, NUMBERS))