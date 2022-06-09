races = []
i = 1
big_string = ''
while True:
    race = input('введите приходы: ')
    if race == '':
        break
    else:
        big_string += race
    races = race.split()
racers = set(big_string.split())
print(races)
print(racers)
