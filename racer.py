from utils import get_point_str


class RacerFinish:
    def __init__(self, text, race_num, dsq_points):
        if text.isnumeric():
            points = int(text)
        elif text in Racer.MODS:
            points = dsq_points

        self.text = text
        self.points = points
        self.race_num = race_num
        self.is_excluded = False

    def __str__(self):
        text = self.text
        if self.is_excluded:
            text = '(' + text + ')'
        return text


class Racer:
    DNF = 'dnf'
    OCS = 'ocs'
    DSQ = 'dsq'
    MODS = {DNF, OCS, DSQ}

    def __init__(self, name, races, exclude, dsq_points):
        self.name = name
        self.races_str = list(map(str, races))
        self.races = races
        for i, race in enumerate(self.races):
            if race in self.MODS:
                self.races[i] = dsq_points
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
            self.races_str[idx] = '(' + self.races_str[idx] + ')'

    def __str__(self):
        point = get_point_str(self.points)
        result = ' '.join(self.races_str)
        return(f"{self.name}: {self.points} {point}: " +
               f"{result}")
