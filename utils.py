from operator import attrgetter


def last_race_getter(racer):
    return racer.races[-1:]


def sort_racers(racers):
    racers = sorted(racers, key=last_race_getter)
    racers = sorted(racers, key=attrgetter('races_sorted'))
    racers = sorted(racers, key=attrgetter('points'))
    return racers


def get_point_str(val) -> str:
    if val in {11, 12, 13, 14}:
        point = 'очков'
    elif val % 10 == 1:
        point = 'очко'
    elif val % 10 in {2, 3, 4}:
        point = 'очка'
    else:
        point = 'очков'
    return point
