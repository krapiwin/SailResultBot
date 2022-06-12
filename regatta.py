from pprint import pprint as pp

from racer import Racer
from utils import sort_racers


class Regatta:
    DNF = 'dnf'
    MOD_DIVIDER = '-'

    def __init__(self, name='', divider=',', exclude=0):
        self.name = name
        self.races = []
        self.races_dsq = []
        self.participants = set()
        self.divider = divider
        self.exclude = exclude

    def get_dsq_points(self) -> int:
        '''
        Получает очки за dsq. Количество участников + 1.
        '''
        return(len(self.participants) + 1)

    def create_race(self, race):
        race = race.split(self.divider)
        race_dsq = {}
        race_finishers = []

        for racer in race:
            if self.MOD_DIVIDER in racer:
                racer, mod = (racer.split(self.MOD_DIVIDER))
                race_dsq[racer] = mod  # str to dict
            else:
                race_finishers.append(racer)  # str to list
            self.participants.add(racer)  # str to set

        self.races.append(race_finishers)  # list of lists
        self.races_dsq.append(race_dsq)  # list of dicts

    def create_results(self):
        racers = self.participants
        racer_objs = []
        dsq_points = self.get_dsq_points()

        for racer in racers:
            racer_res = []
            for race, race_dsq in zip(self.races, self.races_dsq):
                if racer in race:
                    result = (race.index(racer) + 1)
                    racer_res.append(result)
                elif racer in race_dsq:
                    dsq = race_dsq[racer]
                    racer_res.append(dsq)
                else:
                    racer_res.append(self.DNF)

            args = (racer, racer_res, self.exclude, dsq_points)
            racer_objs.append(Racer(*args))

        results = sort_racers(racer_objs)
        return results


def get_result_data(racers):
    '''
    Cюда планируется прикрутить PrettyTable.

    либо pandas + tabulate
    '''
    data = []
    for racer in racers:
        line = [racer.name, racer.points] + racer.races_str
        data.append(line)
    pp(data)
    return data


def main():
    divider = ' '
    exclude = 1
    name = 'Чемпионат Вселенной'

    regatta = Regatta(name, divider, exclude)
    regatta.create_race('р2 р27 р13 р18 р4 пл2-dsq пл1 пл4 р8 пл3')
    regatta.create_race('р2 р18 пл2 р13 пл4 р8 р27 р4 р13')
    regatta.create_race('пл4 р4 р27 пл2 пл1 р8 пл3')

    results = regatta.create_results()
    results_str = (list(map(str, results)))
    pp(results_str)


if __name__ == "__main__":
    main()
