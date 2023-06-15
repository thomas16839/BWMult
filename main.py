import header
import partial_products
import adders
import sys

if __name__ == '__main__':
    f = open('baughwooley.vhd', 'w')

    try:
        width = int(sys.argv[1])
    except:
        print('Please specify (integer) width, defaulting to 32')
        width = 32

    # Write the header part (fixed) and the partial product signals (trivial)
    header.write_header(f)
    partial_products.print_signals(f, width)

    # initialise the grid and solve it
    fa = adders.Matrix(width)
    fa.solve()

    # now use the results to finish the vhdl
    fa.print_signals(f)
    partial_products.print_behaviour(f, width)
    fa.print_behaviour(f)
    fa.print_result(f)

    f.close()
