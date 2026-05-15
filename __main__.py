HYDRO = "Hydro"
PYRO = "Pyro"

class Gauge:
    def __init__(self, element, units):
        self.element = element
        self.units = units

    def __sub__(self, units):
        self.units = max(0, self.units - units)

        return self

    def __str__(self):
        return f"({self.units} {self.element})"

    element = None
    units = 0

class Pyro(Gauge):
    def react(self, incoming):
        match (incoming.element):
            case HYDRO:
                prev = f"{incoming}, {self}"

                coef = 2

                temp = self.units
                self -= coef * incoming.units
                incoming -= temp / coef

                print(f"VAPE: {prev} -> {incoming}, {self};", end = " ")

        return self, incoming

    def __str__(self):
        return f"({self.units} {self.element})"

class Aura:
    existing = []

    def __str__(self):
        return "[" + ",".join(str(e) for e in self.existing) + "]"

    def manageGauges(self, existing, incoming):

        for e in existing:
            e, remaining = e.react(incoming)
            if remaining.units == 0:
                break

        for e in existing:
            if e.units == 0:
                existing.remove(e)

        return existing, remaining


    def apply(self, incoming: Gauge):
        prev = str(self)

        if not self.existing:
            self.existing.append(incoming)
        else:
            self.existing, remaining = self.manageGauges(self.existing, incoming)
            #if remaining.units > 0:
            #    self.apply(existing, remaining)
        
        print(f"[{prev} -> {self}]")
       


def main():
    aura = Aura()
    hydro = Gauge(HYDRO, 2)
    pyro = Pyro(PYRO, 2)

    print(hydro)

    aura.apply(pyro)
    aura.apply(hydro)

if __name__ == "__main__":
    main()

