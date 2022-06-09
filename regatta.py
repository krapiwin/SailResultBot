from pprint import pprint as pp
from racer.py import Racer, sort_racers


class Regatta:
    def __init__(self, name):
        self.name = name
        self.races = []
        self.races_dsq = []
        self.participants = set()

    def get_dsq_points(self, mod, race):
        if mod is None:
            return(len(self.races[race]) + 1)
        else:
            return(len(self.participants) + 1)

    def create_race(self, race, ):
        race = race.split(' ')
        race_dsq = {}
        race_finishers = []

        for racer in race:
            try:
                racer, mod = (racer.split('-'))
                race_dsq[racer] = mod
            except ValueError:
                race_finishers.append(racer)
            self.participants.add(racer)

        self.races.append(race_finishers)
        self.races_dsq.append(race_dsq)

    def create_results(self, exclude):
        racers = self.participants

        race_results = {}
        racer_objs = []

        for racer in racers:
            racer_res = []

            for i in range(len(self.races)):
                race = self.races[i]
                race_dsq = self.races_dsq[i]
                if racer in race:
                    result = (race.index(racer) + 1)
                    racer_res.append(result)
                    continue
                if racer in race_dsq:
                    dsq = race_dsq[racer]
                    racer_res.append(dsq)
                    continue
                else:
                    racer_res.append('dnf')
            racer_objs.append(Racer(racer, racer_res, exclude, self))
            race_results[racer] = racer_res
        return(sort_racers(racer_objs))


def main():
    regatta = Regatta('корпорат 3000')
    n = int(input())
    for _ in range(n):
        regatta.create_race(input())
    exclude = 1
    results = regatta.create_results(exclude)
    print(regatta.name)
    pp(results)


if __name__ == "__main__":
    main()
