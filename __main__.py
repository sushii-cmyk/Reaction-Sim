
class Gauge:
    HYDRO = "Hydro"
    PYRO = "Pyro"
    ELECTRO = "Electro"
    
    def __init__(self, element, units):
        self.element = element
        self.units = units

    def __sub__(self, units):
        self.units = max(0, self.units - units)

        return self

    def __str__(self):
        return f"({self.units} {self.element})"

    def __bool__(self):
        return bool(self.units)

    element = None
    units = 0

class Pyro(Gauge):
    def react(self, incoming):
        prev = f"{incoming}, {self}"
        reaction = "()"
        match (incoming.element):
            case Gauge.HYDRO:
                reaction = "hV"
                coef = 2
                temp = self.units
                self -= coef * incoming.units
                incoming -= temp / coef
                
            case Gauge.ELECTRO:
                reaction = "eO"
                coef = 1
                temp = self.units
                self -= coef * incoming.units
                incoming -= temp


        print(f"{reaction}: {prev} > {self}{f' +> {incoming}' if incoming else ''}")

        return self, incoming

    def __str__(self):
        return f"({self.units} {self.element})"

    def __bool__(self):
        return self.units

class Aura:
    existing = []

    def __str__(self):
        return "[" + ",".join(str(e) for e in self.existing) + "]"

    def manageGauges(self, existing, incoming):
        print(f"resolving {incoming} > [{self}]")
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
            if remaining.units > 0:
                self.apply(remaining)
        
        print(f"previously: {prev} -> now: {self}")
       


def main():
    aura = Aura()
    hydro = Gauge(Gauge.HYDRO, 2)
    electro = Gauge(Gauge.ELECTRO, 1)
    pyro_aura = Pyro(Gauge.PYRO, 2)

    #print(hydro)

    aura.apply(pyro_aura)
    aura.apply(electro)

if __name__ == "__main__":
    main()

