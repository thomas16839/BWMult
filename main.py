import header
import partial_products
import adders

width = 32
f = open('multiplier.vhd', 'w')

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

print(fa.grid)
