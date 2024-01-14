def rest(*args):
    energy, value = args
    if energy + value > 100:
        gained = 100 - energy
        energy = 100
    else:
        energy += value
        gained = value

    print(f"You gained {gained} energy.")
    print(f"Current energy: {energy}.")
    return energy


def order(*args):
    energy, coins, value = args

    if energy >= 30:
        energy -= 30
        coins += value
        print(f"You earned {value} coins.")
    else:
        print("You had to rest!")

    return energy, coins


initial_energy = 100
initial_coins = 100

working_day = input().split('|')

for task in working_day:
    event, number = task.split('-')

    if event == 'rest':
        initial_energy = rest(initial_energy, int(number))

    elif event == 'order':
        initial_energy, initial_coins = order(initial_energy, initial_coins, int(number))

    else:
        if initial_coins >= int(number):
            initial_coins -= int(number)
            print(f"You bought {event}.")
        else:
            print(f"Closed! Cannot afford {event}.")
            raise SystemExit

print(f"Day completed!\nCoins: {initial_coins}\nEnergy: {initial_energy}")
