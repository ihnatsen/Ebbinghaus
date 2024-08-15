from scripts.DataBase.DataBaseSQLity import SQLite
import os

name_file = input('Enter file name: ')
name_rule = input('Enter rule name: ')

with open(name_file, 'r') as file:
    rule = file.read()
    SQLite().save_rule(name_rule, rule)
    print('Rules saved successfully!')

os.remove(name_file)
