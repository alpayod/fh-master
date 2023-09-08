import csv

def check_csv():
    with open('Result/ergebnis_gas.csv', 'r') as file:
        csv_data = list(csv.reader(file, delimiter=';'))
        last_value = float(csv_data[-1][1])
        second_last_value = float(csv_data[-2][1])
        difference = abs(last_value - second_last_value)
        
        if difference >= 12:
            print("ALERT")
        else:
            print("OK")

check_csv()

