import numpy as np


class FullAdder:
    def __init__(self, layer_id, sig_id, inputs):
        self.layer = layer_id
        self.id = sig_id
        self.inputs = inputs

    def print_signal(self):
        return f"   signal sum_{self.layer}_{self.id}, car_{self.layer}_{self.id} : std_logic;\n"

    def print_assignment(self):
        return f"   sum_{self.layer}_{self.id} <= {self.inputs[0]} xor {self.inputs[1]} xor {self.inputs[2]};\n" \
               f"   car_{self.layer}_{self.id} <= (({self.inputs[0]} xor {self.inputs[1]}) and {self.inputs[2]}) or " \
               f"({self.inputs[0]} and {self.inputs[1]});\n"

    def as_input(self):
        return f"sum_{self.layer}_{self.id}", f"car_{self.layer}_{self.id}"


class HalfAdder:
    def __init__(self, layer_id, sig_id, inputs):
        self.layer = layer_id
        self.id = sig_id
        self.inputs = inputs

    def print_signal(self):
        return f"   signal ha_sum_{self.layer}_{self.id}, ha_car_{self.layer}_{self.id} : std_logic;\n"

    def print_assignment(self):
        return f"   ha_sum_{self.layer}_{self.id} <= {self.inputs[0]} xor {self.inputs[1]};\n" \
               f"   ha_car_{self.layer}_{self.id} <= {self.inputs[0]} and {self.inputs[1]};\n"

    def as_input(self):
        return f"ha_sum_{self.layer}_{self.id}", f"ha_car_{self.layer}_{self.id}"


class Matrix:
    def __init__(self, width):
        self.grid, self.width, self.height = self.init_grid(width)
        self.cur_layer = 0
        self.full_adders = []
        self.half_adders = []

    @staticmethod
    def init_grid(width):
        h = width * 2 + 1
        w = width * 2 + 1
        matrix = np.full((h, w), "", dtype=object)
        k = width + 1
        for j in range(width):
            for i in range(k, k + width):
                matrix[j, i] = f"pp{j}({width - i + k - 1})"
            k -= 1
        # baugh wooley:
        matrix[width, width] = f"is_signed"
        matrix[width, 1] = f"is_signed"
        return matrix, w, h

    def shift_grid(self):
        """Shifts all elements in the grid towards the top, such that there are no more empty spaces there.
        This makes life a lot easier when trying to find spots for full adders :)"""
        for w in range(self.width):
            for h in range(self.height):
                rolls = 0
                while self.grid[h, w] == "" and rolls < self.height - h:
                    self.grid[h:, w] = np.roll(self.grid[h:, w], -1)
                    rolls += 1

    def find_adders(self):
        locations = []
        for w in range(self.width):
            adders_in_column = 0
            for h in range(0, self.height - 2, 3):
                if (self.grid[h, w] != "") & (self.grid[h+1, w] != "") & (self.grid[h+2, w] != ""):
                    adders_in_column += 1
                    locations.append((w, h, adders_in_column))
        return locations

    def place_adders(self):
        locations = self.find_adders()
        locations.sort()

        new_adders = []
        adder_id = 0
        for (w, h, x) in locations:
            new_adders.append(FullAdder(self.cur_layer, adder_id, [self.grid[h, w], self.grid[h+1, w], self.grid[h+2, w]]))
            s, c = new_adders[-1].as_input()
            self.grid[h, w] = s
            self.grid[-x, w - 1] = c
            self.grid[h + 1, w] = ""
            self.grid[h + 2, w] = ""
            adder_id += 1

        self.full_adders.extend(new_adders)

    def finished(self):
        count = 0
        loc = 0
        for (item, x) in zip(self.grid[2, :], range(self.width)):
            if item != "":
                count += 1
                loc = x
                if count == 2:
                    return False

        # if the third row is empty, we do not need to place any more adders
        if count == 0:
            return True
        # if there is only one full adder, we need to check that we propagate it properly instead of cascading full adders
        self.place_half_adders(loc)
        return True

    def place_half_adders(self, loc):
        empty_carry = []
        for i in range(self.width):
            if self.grid[1, i] == "":
                empty_carry.append(i)

        closest = empty_carry[0]
        for c in empty_carry:
            if c < loc:
                closest = c
            else:
                break

        # now we know where the Half Adders need to be placed:
        adder_id = 0
        new_ha = []
        for i in range(closest + 1, loc):
            inputs = [self.grid[0, i], self.grid[1, i]]
            new_ha.append(HalfAdder(self.cur_layer, adder_id, inputs))
            s, c = new_ha[-1].as_input()
            self.grid[0, i] = s
            self.grid[1, i - 1] = c
            adder_id += 1
        self.half_adders.extend(new_ha)

        # and now place the final full adder
        self.full_adders.append(FullAdder(self.cur_layer, 0, [self.grid[0, loc], self.grid[1, loc], self.grid[2, loc]]))
        s, c = self.full_adders[-1].as_input()
        self.grid[0, loc] = s
        self.grid[1, loc - 1] = c
        self.grid[2, loc] = ""

    def solve(self):
        self.shift_grid()
        while not self.finished():
            self.place_adders()
            self.shift_grid()
            self.cur_layer += 1
        print("done")

    def print_signals(self, file):
        layer = 0
        file.write(f"\n   --full_adder signals for layer {layer}\n")

        for fa in self.full_adders:
            if fa.layer != layer:
                layer = fa.layer
                file.write(f"\n   --full_adder signals for layer {layer}\n")
            file.write(fa.print_signal())

        file.write(f"\n   --half_adder signals for layer {layer}\n")
        for ha in self.half_adders:
            file.write(ha.print_signal())
        file.write("\n")

    def print_behaviour(self, file):
        layer = 0
        file.write(f"\n   --layer {layer}\n")

        for fa in self.full_adders:
            if fa.layer != layer:
                layer = fa.layer
                file.write(f"\n   --layer {layer}\n")
            file.write(fa.print_assignment())
        file.write("\n")

        for ha in self.half_adders:
            file.write(ha.print_assignment())

    def print_result(self, file):
        prod = self.grid[0, 1:]
        carry = self.grid[1, 1:]
        zero = "'0'"
        file.write("    --product\n")
        for (p, i) in zip(prod, range(len(prod) - 1, -1, -1)):
            file.write(f"   x({i}) <= {p};\n")
        file.write("    --carry\n")
        for (c, i) in zip(carry, range(len(carry) - 1, -1, -1)):
            file.write(f"   y({i}) <= {c if c != '' else zero};\n")

        file.write("end behaviour;\n")
