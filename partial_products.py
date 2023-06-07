def print_signals(file, width):
    name = "bw_mult"
    file.write(f'entity {name} is\n'
               f'   port(a, x : in std_logic_vector({width-1} downto 0);\n'
               f'        is_signed : in std_logic;\n'
               f'        p, c : out std_logic_vector({width * 2 - 1} downto 0)\n'
               f');\n'
               f'end {name};\n\n'
               f'architecture behaviour of {name} is\n')
    
    file.write('--partial product signals\n')

    for i in range(width):
        file.write(f'   signal pp{i} : std_logic_vector({width-1} downto 0);\n')


def print_behaviour(file, width):
    file.write('begin\n')
    for i in range(width - 1):
        for j in range(width):
            file.write(f'    pp{i}({j}) <= (a({j}) and x({i})){" xor is_signed" if j == width-1 else ""};\n')

    for j in range(width):
        file.write(f'    pp{width - 1}({j}) <= (a({j}) and x({width - 1})){" xor is_signed" if j != width - 1 else ""};\n')
