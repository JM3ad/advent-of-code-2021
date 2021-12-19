from src.helpers.files import load_txt_file

def run():
    input = load_txt_file('./src/day_19/input.txt')
    count = count_beacons(input)
    print(f"Day 19 Q1: there are {count} beacons")

    print(f"Day 19 Q2: ")

def count_beacons(input):
    scanners = parse_input(input)
    match_scanners(scanners)
    beacons = get_actual_beacons(scanners)
    return len(beacons)

def match_scanners(scanners):
    while(any_scanner_unmatched(scanners)):
        for i in range(len(scanners)):
            for j in range(i + 1, len(scanners)):
                try_match_scanner_pair(scanners[i], scanners[j])

def any_scanner_unmatched(scanners):
    return any([not scanner.is_located() for scanner in scanners])

def try_match_scanner_pair(a, b):
    if a.is_located() == b.is_located():
        return
    known = [s for s in [a,b] if s.is_located()][0]
    unknown = [s for s in [a,b] if not s.is_located()][0]

    # theory - iterate over all pairs of beacons, and see if diff is consistent
    # if so, hypothesise and see if others match
    matched = []
    for idx_k1 in range(len(known.beacons)):
        count = 0
        matched_unknown = []
        for idx_k2 in range(len(known.beacons)):
            if idx_k1 == idx_k2:
                continue
            for idx_u1 in range(len(unknown.beacons)):
                for idx_u2 in range(idx_u1 + 1, len(unknown.beacons)):
                    kb = known.beacons
                    ub = unknown.beacons
                    success = match_beacons(known, kb[idx_k1], kb[idx_k2], ub[idx_u1], ub[idx_u2])
                    if success and count == 0:
                        matched_unknown.append(ub[idx_u1])
                        matched_unknown.append(ub[idx_u2])
                        count += 1
                    elif success and count == 1:
                        count += 1
                        if ub[idx_u1] in matched_unknown:
                            matched.append((kb[idx_k1], ub[idx_u1]))
                        else:
                            matched.append((kb[idx_k1], ub[idx_u2]))

    # for el in matched:
    #     k = el[0]
    #     u = el[1]
    #     print(f"s0: {k}")
    #     print(f"s1: {u}")
    # print(matched)
    if len(matched) >= 12:
        for x in get_coord_lambdas():
            for y in get_coord_lambdas():
                for z in get_coord_lambdas():
                    kb1 = matched[0][0]
                    ub1 = matched[0][1]
                    poss_position = (kb1.c1 - x(ub1), kb1.c2 - y(ub1), kb1.c3 - z(ub1))
                    valid = True
                    for el in matched:
                        kbi, ubi = el
                        if kbi.c1 != poss_position[0] + x(ubi):
                            valid = False
                            break
                        if kbi.c2 != poss_position[1] + y(ubi):
                            valid = False
                            break
                        if kbi.c3 != poss_position[2] + z(ubi):
                            valid = False
                            break
                    if valid:
                        print(f"Matched {unknown.id}")
                        print(f"New pos = {poss_position}")
                        unknown.rearrange(poss_position, x, y, z)
                        return

def get_coord_lambdas():
    return [
        lambda b: b.c1,
        lambda b: -b.c1,
        lambda b: b.c2,
        lambda b: -b.c2,
        lambda b: b.c3,
        lambda b: -b.c3
    ]

def match_beacons(known, k1, k2, u1, u2):
    known_diffs = [k1.c1 - k2.c1, k1.c2 - k2.c2, k1.c3 - k2.c3]
    unknown_diffs = [u1.c1 - u2.c1, u1.c2 - u2.c2, u1.c3 - u2.c3]
    return diffs_match(known_diffs, unknown_diffs)
    
def add_match(match, coord, k, unknowns):
    if k in unknown_diffs:
        index = unknown_diffs.index(k)
        match[coord] = index
    else:
        index = unknown_diffs.index((-1) * k)
        match[coord] = -index

def diffs_match(d1, d2):
    for d in d1:
        if d not in d2 and (-1 * d) not in d2:
            return False
    return True

def get_actual_beacons(scanners):
    all_beacons = {beacon for scanner in scanners for beacon in scanner.beacons}
    return all_beacons

def parse_input(input):
    scanners = []
    scanner_lines = []
    for line in input:
        if line.strip() == '':
            scanners.append(parse_scanner(scanner_lines))
            scanner_lines = []
        else:
            scanner_lines.append(line)
    scanners.append(parse_scanner(scanner_lines))
    
    return scanners

def parse_scanner(beacons):
    return Scanner(beacons)

class Beacon():
    def __init__(self, input_line):
        self.c1, self.c2, self.c3 = [int(num) for num in input_line.split(',')]

    def __eq__(self, other):
        if isinstance(other, Beacon):
            return self.c1 == other.c1 and self.c2 == other.c2 and self.c3 == other.c3
        return False

    def __hash__(self):
        return (self.c1, self.c2, self.c3).__hash__()

    def __str__(self):
        return str((self.c1, self.c2, self.c3))

class Scanner():
    def __init__(self, input_lines):
        self.id = input_lines[0].split()[2]
        self.beacons = [Beacon(input_line) for input_line in input_lines[1:]]
        ## TODO?
        if self.id == '0':
            self.position = (0,0,0)
        else:
            self.position = None

    def is_located(self):
        return self.position != None

    @property
    def x(self):
        return self.position[0]

    @property
    def y(self):
        return self.position[1]

    @property
    def z(self):
        return self.position[2]

    def rearrange(self, position, x, y, z):
        self.position = position
        for beacon in self.beacons:
            c1, c2, c3 = x(beacon) + position[0], y(beacon) + position[1], z(beacon) + position[2]
            beacon.c1, beacon.c2, beacon.c3 = c1, c2, c3