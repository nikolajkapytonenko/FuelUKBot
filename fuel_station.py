class FuelStation:
    def __init__(self, name, prises_list):
        self.name = name
        self.prises = dict()
        self.prises["A95+"] = prises_list[0]
        self.prises["A95"] = prises_list[1]
        self.prises["A92"] = prises_list[2]
        self.prises["ДТ"] = prises_list[3]
        self.prises["ГАЗ"] = prises_list[4]

    def __str__(self):
        return self.name

    def get_station_name(self):
        return self.name

    def get_fuel(self):
        keys = []
        [keys.append(key) for key in self.prises]
        return keys

    def get_fuel_price(self):
        text = "\n" + self.name + ":\n"
        i = 0
        for fuel in self.prises:
            if self.prises[fuel] != "-":
                text += f"{fuel}: {self.prises[fuel]};   "
                i += 1
            else:
                pass
        return text
