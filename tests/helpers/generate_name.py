import random


def generate_name():
    fnames = ['Dallan', 'Billy', 'Sam', 'Russell', 'Kevin', 'James', 'Serge', 'Steven', 'Chris', 'Shai', 'Dion',
              'Dennis', 'Enes', 'Kendrick', 'Andre', 'Nick', 'Danillo', 'Nerlens', 'Victor', 'Jerami', 'Paul', 'LeBron',
              'Anthony', 'Karl-Anthony', 'Dwyane', 'Chris', 'Charles', 'Michael', 'Greg', 'Steph', 'Klay', 'Jimmy',
              'Javale', 'Kawhi', 'Giannis']
    lnames = ['Bhatti', 'Donavon', 'Presti', 'Westbrook', 'Durant', 'Harden', 'Ibaka', 'Adams', 'Paul',
              'Gilgeous-Alexander', 'Waiters', 'Schroder', 'Kanter', 'Perkins', 'Roberson', 'Collison', 'Gallinari',
              'Noel', 'Oladipo', 'Grant', 'George', 'James', 'Davis', 'Towns', 'Wade', 'Bosh', 'Barkley', 'Jordan',
              'Oden', 'Curry', 'Thompson', 'Butler', 'McGee', 'Leonard', 'Antetekuonmpo']
    return f'{random.choice(fnames)} {random.choice(lnames)}'
