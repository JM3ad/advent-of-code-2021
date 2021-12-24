from src.helpers.files import load_txt_file
from src.helpers.perf import add_profile

def run():
    lines = load_txt_file('./src/day_24/input.txt')
    max_monad = get_max_monad(lines)
    print(f"Day 24 Q1: max monad = {max_monad}")

    print(f"Day 24 Q2: ")

@add_profile
def get_max_monad(lines):
    instruction_blocks = parse_lines(lines)
    for monad in get_possible_monads_from_largest_first():
        if is_valid_monad(monad, instruction_blocks):
            return monad
    return 0
    raise Exception("No valid monads")

def get_possible_monads_from_largest_first():
    max_monad = 99999999999999
    min_monad = 99999991111111 # 11111111111111
    for i in range(max_monad, min_monad, -1):
        s = str(i)
        if '0' in s:
            continue
        yield s

def parse_lines(lines):
    instruction_blocks = []
    current_block = None
    for line in lines:
        if line.startswith('inp'):
            if current_block:
                instruction_blocks.append(current_block)
            current_block = []
        current_block.append(line.split())
    instruction_blocks.append(current_block)
    return instruction_blocks

cache = {}

def reset_cache():
    global cache
    cache = {}

def is_valid_monad(monad, instruction_blocks):
    w,x,y,z = 0,0,0,0
    global cache
    for i in range(len(instruction_blocks)):
        instructions = instruction_blocks[i]
        w,x,y,z = read_input(instructions[0], int(monad[i]), w, x, y, z)
        w0,x0,y0,z0 = w,x,y,z
        if (i, w, x, y, z) in cache:
            w,x,y,z = cache[(i,w,x,y,z)]
            continue

        for instruction in instructions[1:]:
            w,x,y,z = process_instruction(instruction, w, x, y, z)
        cache[(i,w0,x0,y0,z0)] = (w,x,y,z)
    return z == 0

add = lambda x, y: x + y
mul = lambda x, y: x * y
div = lambda x, y: int(x / y)
mod = lambda x, y: x % y
eql = lambda x, y: 1 if x == y else 0

def process_instruction(instruction, w, x, y, z):
    op = instruction[0]
    a = instruction[1]
    b_temp = instruction[2]
    b = read_b(b_temp, w, x, y, z)
    
    the_op = None
    if op == 'add':
        the_op = add
    elif op == 'mul':
        the_op = mul   
    elif op == 'eql':
        the_op = eql
    elif op == 'div':
        the_op = div
    elif op == 'mod':
        the_op = mod

    if a == 'w':
        w = the_op(w, b)
    elif a == 'x':
        x = the_op(x, b)
    elif a == 'y':
        y = the_op(y, b)
    elif a == 'z':
        z = the_op(z, b)
    return w,x,y,z

def read_b(b_temp, w, x, y, z):
    if b_temp == 'w':
        return w
    elif b_temp == 'x':
        return x
    elif b_temp == 'y':
        return y
    elif b_temp == 'z':
        return z
    else:
        return int(b_temp)

def read_input(instruction, num, w, x, y, z):
    var = instruction[1]
    if var == 'w':
        w = num
    elif var == 'x':
        x = num
    elif var == 'y':
        y = num
    elif var == 'z':
        z = num
    else:
        raise Exception(f"Unrecognised: {var}")
    return w,x,y,z