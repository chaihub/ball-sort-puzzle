""" Debug class composition issue """

from dataclasses import dataclass

@dataclass
class Pen:
    color: str
    def set_color(self, newcolor):
        self.color = newcolor
        return self.color

@dataclass
class PenSet:
    pens: list[Pen]

@dataclass
class Inventory:
    items: list[PenSet]

def main():
    pen1 = Pen("white")
    pen2 = Pen("blue")
    pen3 = Pen("orange")
    penset1 = PenSet([pen1])
    penset2 = PenSet([pen1, pen3])
    inventory = Inventory([penset1, penset2])
    #print(pen1, penset2, inventory)

    # pentest = Pen("red")
    # pentest.set_color("green")
    # print(pentest)

    pentest2 = Pen("beige")
    #pentest2 = penset2.pens[1]
    # The above assignment makes pentest2 point to penset2.pens[1], it does not create a copy like it does for var2 below. Probably because the target (LHS) is bound to the object (or expression result) on the RHS.
    var1 = 5
    var2 = var1
    var2 = 7
    print(f'var1={var1}, var2={var2}')
    print(pentest2)
    pentest2.set_color(penset2.pens[1].color)
    print(pentest2)
    pentest2.set_color("black")
    print(pentest2, penset2)

if __name__ == '__main__':
    main()