import csv

def check_csv_file(filepath):
    with open(filepath, "r") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            email = row.get("email")
            if not email:
                return False
    return True


filepath = "assets/people.csv"
result = check_csv_file(filepath)
if result:
    print("O arquivo CSV contém valores válidos para a coluna 'email'.")
else:
    print("O arquivo CSV não contém valores válidos para a coluna 'email'.")