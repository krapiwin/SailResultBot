from pprint import pprint as pp
from operator import attrgetter


def last_race_getter(racer):
    return racer.races[-1:]


class Racer:
    def __init__(self, name, races, exclude, regatta):
        self.name = name
        self.regatta = regatta
        self.races_final = list(map(str, races))
        self.races = races
        for i in range(len(self.races)):
            mod = self.races[i]
            if mod in {'dnf', 'ocs', 'dsq'}:
                val = self.regatta.get_dsq_points(mod, i)
                print(val)
                self.races[i] = val
        self.races_sorted = sorted(self.races)

        self.sum = sum(self.races_sorted)
        if exclude <= 0:
            self.excluded = []
            exclude = 0
        else:
            self.excluded = self.races_sorted[-1*exclude:]

        excluded_id = []

        for i in range(exclude):
            value = self.excluded[i]
            index = self.races.index(value)
            self.races[index] = 0
            excluded_id.append(index)

        exclude_sum = sum(self.excluded)
        self.points = self.sum - exclude_sum

        for idx in excluded_id:
            self.races_final[idx] = '(' + self.races_final[idx] + ')'

    def __str__(self):
        if self.points in {11, 12, 13, 14}:
            point = 'очков'
        elif self.points % 10 == 1:
            point = 'очко'
        elif self.points % 10 in {2, 3, 4}:
            point = 'очка'
        else:
            point = 'очков'
        result = ' '.join(self.races_final)
        return(f"{self.name}: {self.points} {point}: " +
               f"{result}")


def sort_racers(racers):
    racers = sorted(racers, key=last_race_getter)
    racers = sorted(racers, key=attrgetter('races_sorted'))
    racers = sorted(racers, key=attrgetter('points'))
    racers = (list(map(str, racers)))
    return racers


def input_data():
    exclude = int(input('введите количество выбросов: '))
    with open('input.txt') as f:
        lines = f.readlines()
    racers = []
    for line in lines:
        line = line.strip()
        name, races = line.split()
        races = races.split(',')
        races = list(map(int, races))
        racer = Racer(name, races, exclude)
        racers.append(racer)
    return(racers, exclude)


def main():
    racers, exclude = input_data()
    racers = sort_racers(racers)
    pp(racers)


if __name__ == "__main__":
    main()
