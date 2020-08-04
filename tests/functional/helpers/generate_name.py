import random


def generate_name():
    fnames = ['Dallan', 'Billy', 'Sam', 'Russell', 'Kevin', 'James', 'Serge', 'Steven', 'Chris', 'Shai', 'Dion',
              'Dennis', 'Enes', 'Kendrick', 'Andre', 'Nick', 'Danillo', 'Nerlens', 'Victor', 'Jerami', 'Paul']
    lnames = ['Bhatti', 'Donavon', 'Presti', 'Westbrook', 'Durant', 'Harden', 'Ibaka', 'Adams', 'Paul',
              'Gilgeous-Alexander', 'Waiters', 'Schroder', 'Kanter', 'Perkins', 'Roberson', 'Collison', 'Gallinari',
              'Noel', 'Oladipo', 'Grant', 'George']
    return f'{random.choice(fnames)} {random.choice(lnames)}'
