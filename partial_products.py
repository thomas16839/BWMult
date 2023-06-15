def print_signals(file, width):
    name = "baughwooley"
    file.write(f'entity {name} is\n'
               f'   port(a, b : in std_logic_vector({width-1} downto 0);\n'
               f'        is_signed : in std_logic;\n'
               f'        x, y : out std_logic_vector({width * 2 - 1} downto 0)\n'
               f');\n'
               f'end {name};\n\n'
               f'architecture behaviour of {name} is\n')

    for i in range(width):
        file.write(f'   signal pp{i} : std_logic_vector({width-1} downto 0);\n')


def print_behaviour(file, width):
    file.write('begin\n')
    for i in range(width - 1):
        for j in range(width):
            file.write(f'    pp{i}({j}) <= (a({j}) and b({i})){" xor is_signed" if j == width-1 else ""};\n')

    for j in range(width):
        file.write(f'    pp{width - 1}({j}) <= (a({j}) and b({width - 1})){" xor is_signed" if j != width - 1 else ""};\n')
