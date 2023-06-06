def write_header(file):
    file.write(f'----------------------------------------------\n'
               f'-- AUTOMATICALLY GENERATED, DO NOT EDIT     --\n'
               f'-- in case of mistakes, edit the            --\n'
               f'-- generator script                         --\n'
               f'--                                          --\n'
               f'-- TITLE: Baugh Wooley Multiplier Reduction --\n'
               f'-- AUTHOR: Thomas Pouwels                   --\n'
               f'----------------------------------------------\n'
               f'\n'
               f'library ieee;\n'
               f'use ieee.std_logic_1164.all;\n'
               f'use ieee.numeric_std.all;\n\n')
