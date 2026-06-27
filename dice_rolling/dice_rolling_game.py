import random 

while True:
  dice = input('Roll the dice? (y/n): ').lower()
  if dice == 'y':
      die1 = random.randint(1, 6)
      die2 = random.randint(1, 6)
      print(f'({die1}, {die2})')          #  f representformatted string
  elif dice == 'n':
      print('Thanks for playing!')
      break
  else:
      print('Invalid choice!')