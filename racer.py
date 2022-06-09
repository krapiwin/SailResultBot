from utils import get_point_str


class Racer:
    def __init__(self, name, races, exclude, dsq_points):
        self.name = name
        self.races_final = list(map(str, races))
        self.races = races
        for i in range(len(self.races)):
            mod = self.races[i]
            if mod in {'dnf', 'ocs', 'dsq'}:
                val = dsq_points
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
        point = get_point_str(self.points)
        result = ' '.join(self.races_final)
        return(f"{self.name}: {self.points} {point}: " +
               f"{result}")
