import csv

def read_csv(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            instruments = row[5].split(';')
            instruments_info = []
            for instrument in instruments:
                name, years, hours = instrument.split(':')
                instruments_info.append({
                    'name': name,
                    'years': int(years),
                    'hours': int(hours)
                })
            print(f"Nom: {row[0]}, Prénom: {row[1]}, Instruments: {instruments_info}")

read_csv("participants.csv")


#A tester 