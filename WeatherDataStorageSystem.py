# WEATHER DATA STORAGE SYSTEM 

YEARS = []      # list of years (rows)
CITIES = []     # list of cities (columns)
MATRIX = []     # 2D array: MATRIX[row][col] stores list of record dicts or None
RECORDS = []    # flat list of all records (date, city, temperature)
SENTINEL = None # sentinel for sparse cells


# Helpers
def YEAR_INDEX(y):
    try:
        return YEARS.index(y)
    except ValueError:
        return -1

def CITY_INDEX(c):
    try:
        return CITIES.index(c)
    except ValueError:
        return -1

def MAKE_RECORD(date, city, temperature):
    return {"date": date, "city": city, "temperature": float(temperature)}


# 1. INSERT
def INSERT():
    date = input("Enter Date (DD/MM/YYYY): ").strip()
    city = input("Enter City: ").strip()
    temp_s = input("Enter Temperature: ").strip()
    try:
        temp = float(temp_s)
    except ValueError:
        print("Invalid temperature!")
        return
    parts = date.split("/")
    if len(parts) != 3:
        print("Invalid Date Format! Use DD/MM/YYYY")
        return
    year = int(parts[2])

    # Update YEARS and CITIES
    if year not in YEARS:
        YEARS.append(year)
        YEARS.sort()
    if city not in CITIES:
        CITIES.append(city)

    # Matrix size
    rows = len(YEARS)
    cols = len(CITIES)
    while len(MATRIX) < rows:
        MATRIX.append([SENTINEL for _ in range(cols)])
    for r in range(len(MATRIX)):
        while len(MATRIX[r]) < cols:
            MATRIX[r].append(SENTINEL)

    r = YEAR_INDEX(year)
    c = CITY_INDEX(city)
    if MATRIX[r][c] == SENTINEL:
        MATRIX[r][c] = []
    rec = MAKE_RECORD(date, city, temp)
    MATRIX[r][c].append(rec)
    RECORDS.append(rec)
    print("Record Inserted Successfully!")


# 2. CREATE BATCH 
def CREATE_RECORDS():
    try:
        n = int(input("Enter number of weather records to create: ").strip())
    except ValueError:
        print("Invalid number.")
        return
    for i in range(n):
        print("\nEnter details for weather record " + str(i+1) + ":")
        date = input("Enter date (DD/MM/YYYY): ").strip()
        city = input("Enter city name: ").strip()
        temp_s = input("Enter temperature (in Celsius): ").strip()
        try:
            temp = float(temp_s)
        except ValueError:
            print("Invalid temperature - skipping this record.")
            continue
        
        parts = date.split("/")
        if len(parts) != 3:
            print("Invalid date format - skipping this record.")
            continue
        year = int(parts[2])
        if year not in YEARS:
            YEARS.append(year)
            YEARS.sort()
        if city not in CITIES:
            CITIES.append(city)
        rows = len(YEARS)
        cols = len(CITIES)
        while len(MATRIX) < rows:
            MATRIX.append([SENTINEL for _ in range(cols)])
        for r in range(len(MATRIX)):
            while len(MATRIX[r]) < cols:
                MATRIX[r].append(SENTINEL)
        r = YEAR_INDEX(year)
        c = CITY_INDEX(city)
        if MATRIX[r][c] == SENTINEL:
            MATRIX[r][c] = []
        rec = MAKE_RECORD(date, city, temp)
        MATRIX[r][c].append(rec)
        RECORDS.append(rec)
    print("Batch creation complete.")


# 3. DELETE (by date and city)
def DELETE():
    date = input("Enter Date (DD/MM/YYYY) to delete: ").strip()
    city = input("Enter City: ").strip()
    parts = date.split("/")
    if len(parts) != 3:
        print("Invalid Date Format!")
        return
    year = int(parts[2])
    if year not in YEARS or city not in CITIES:
        print("Record Not Found!")
        return
    r = YEAR_INDEX(year)
    c = CITY_INDEX(city)
    if MATRIX[r][c] == SENTINEL:
        print("No Records Found!")
        return
    before = len(MATRIX[r][c])
    # Remove matching date entries in that cell
    MATRIX[r][c] = [rec for rec in MATRIX[r][c] if rec["date"] != date]
    after = len(MATRIX[r][c])
    # Update RECORDS list to remove matching entries
    RECORDS[:] = [rec for rec in RECORDS if not (rec["date"] == date and rec["city"] == city)]
    if after == 0:
        MATRIX[r][c] = SENTINEL
    if before == after:
        print("No Record Found for Given Date.")
    else:
        print("Record Deleted Successfully!")


# 4. RETRIEVE (by city and year)
def RETRIEVE():
    city = input("Enter City: ").strip()
    year_s = input("Enter Year (YYYY): ").strip()
    try:
        year = int(year_s)
    except ValueError:
        print("Invalid Year!")
        return
    if year not in YEARS or city not in CITIES:
        print("No Records Found!")
        return
    r = YEAR_INDEX(year)
    c = CITY_INDEX(city)
    if MATRIX[r][c] == SENTINEL:
        print("No Data Available!")
        return
    print(f"Records for {city} in {year}:")
    for rec in MATRIX[r][c]:
        print(f"Date: {rec['date']}  Temp: {rec['temperature']}°C")


# 5. POPULATE DEMO DATA
def POPULATE():
    demo = [
        ("01/01/2024", "Delhi", 15.5),
        ("02/01/2024", "Delhi", 16.0),
        ("01/01/2024", "Mumbai", 24.0),
        ("15/02/2023", "Delhi", 20.2),
        ("10/03/2025", "Chennai", 29.0)
    ]
    for d, c, t in demo:
        if c not in CITIES:
            CITIES.append(c)
        if int(d.split("/")[2]) not in YEARS:
            YEARS.append(int(d.split("/")[2]))
    YEARS.sort()
    rows, cols = len(YEARS), len(CITIES)
    while len(MATRIX) < rows:
        MATRIX.append([SENTINEL for _ in range(cols)])
    for r in range(rows):
        while len(MATRIX[r]) < cols:
            MATRIX[r].append(SENTINEL)
    for d, c, t in demo:
        y = int(d.split("/")[2])
        r = YEAR_INDEX(y)
        col = CITY_INDEX(c)
        if MATRIX[r][col] == SENTINEL:
            MATRIX[r][col] = []
        rec = MAKE_RECORD(d, c, t)
        MATRIX[r][col].append(rec)
        RECORDS.append(rec)
    print("Demo Data Populated!")


# 6. ROW-MAJOR ACCESS
def ROW_MAJOR():
    print("ROW-MAJOR ACCESS:")
    for r in range(len(YEARS)):
        for c in range(len(CITIES)):
            if MATRIX[r][c] == SENTINEL:
                print(f"Year {YEARS[r]} City {CITIES[c]}: No Data")
            else:
                print(f"Year {YEARS[r]} City {CITIES[c]}: {MATRIX[r][c]}")


# 7. COLUMN-MAJOR ACCESS
def COLUMN_MAJOR():
    print("COLUMN-MAJOR ACCESS:")
    for c in range(len(CITIES)):
        for r in range(len(YEARS)):
            if MATRIX[r][c] == SENTINEL:
                print(f"City {CITIES[c]} Year {YEARS[r]}: No Data")
            else:
                print(f"City {CITIES[c]} Year {YEARS[r]}: {MATRIX[r][c]}")


# 8. SPARSE REPRESENTATION
def SPARSE():
    print("SPARSE REPRESENTATION:")
    sparse_list = []
    for r in range(len(YEARS)):
        for c in range(len(CITIES)):
            if MATRIX[r][c] != SENTINEL:
                for rec in MATRIX[r][c]:
                    sparse_list.append((YEARS[r], CITIES[c], rec["date"], rec["temperature"]))
    if not sparse_list:
        print("No Data Available!")
    else:
        for item in sparse_list:
            print(item)


# 9. DISPLAY RECORDS (flat list)
def DISPLAY_RECORDS():
    if not RECORDS:
        print("No weather records found.")
        return
    print("\nWeather Record Details:")
    for rec in RECORDS:
        print("Date: " + rec['date'] + ", Temperature: " + str(rec['temperature']) + " °C, City: " + rec['city'])


# 10. POPULATE ARRAY FROM USER
def POPULATE_ARRAY():
    years_input = input("Enter years separated by commas (e.g. 2023,2024): ").strip()
    cities_input = input("Enter cities separated by commas (e.g. Delhi,Mumbai): ").strip()
    years = [int(y.strip()) for y in years_input.split(",") if y.strip() != ""]
    cities = [c.strip() for c in cities_input.split(",") if c.strip() != ""]
    # Set globals
    global YEARS, CITIES, MATRIX, RECORDS
    YEARS = years
    CITIES = cities
    MATRIX = []
    RECORDS = []
    rows = len(YEARS)
    cols = len(CITIES)
    for i in range(rows):
        row = []
        for j in range(cols):
            val = input(f"Enter temperature for {CITIES[j]} in {YEARS[i]} (or press Enter to skip): ").strip()
            if val == "":
                row.append(SENTINEL)
            else:
                try:
                    t = float(val)
                except ValueError:
                    print("Invalid numeric input, storing as SENTINEL.")
                    row.append(SENTINEL)
                    continue
                rec_date = "01/01/" + str(YEARS[i])  # approximate date when only year given
                rec = MAKE_RECORD(rec_date, CITIES[j], t)
                row.append([rec])  # store as list of records
                RECORDS.append(rec)
        MATRIX.append(row)
    print("User-populated matrix created.")


# 11. COMPLEXITY ANALYSIS
def COMPLEXITY():
    print("\nTIME COMPLEXITY:")
    print("Insert: O(R + C) worst case (search + resize), typically O(1) for appending to cell list")
    print("Delete: O(R + C + M) where M = records in cell")
    print("Retrieve: O(R + C + M)")
    print("Row/Col Major Access: O(R * C)")
    print("\nSPACE COMPLEXITY:")
    print("Matrix: O(R * C) + Records: O(K)")


# 12. PRINT TABLE
def PRINT_TABLE():
    if not YEARS or not CITIES:
        print("No table to print.")
        return
    header = "Year/City".ljust(12)
    for city in CITIES:
        header += city.ljust(12)
    print(header)
    for i in range(len(YEARS)):
        row_str = str(YEARS[i]).ljust(12)
        for j in range(len(CITIES)):
            val = MATRIX[i][j]
            if val is None or val == SENTINEL:
                row_str += "None".ljust(12)
            else:
                # Show number of records in cell
                row_str += (str(len(val)) + " rec").ljust(12)
        print(row_str)


# MAIN MENU
def MAIN():
    while True:
        print("\n--- WEATHER DATA STORAGE SYSTEM ---")
        print("1. Insert Record")
        print("2. Create Multiple Records")
        print("3. Delete Record (by date & city)")
        print("4. Retrieve Records (by city & year)")
        print("5. Populate Demo Data")
        print("6. Populate Matrix (user input years & cities)")
        print("7. Row-Major Access")
        print("8. Column-Major Access")
        print("9. Sparse Representation")
        print("10. Display Flat Records")
        print("11. Print Table Summary")
        print("12. Complexity Analysis")
        print("13. Exit")

        choice = input("Enter Choice (1-13): ").strip()

        if choice == '1':
            INSERT()
        elif choice == '2':
            CREATE_RECORDS()
        elif choice == '3':
            DELETE()
        elif choice == '4':
            RETRIEVE()
        elif choice == '5':
            POPULATE()
        elif choice == '6':
            POPULATE_ARRAY()
        elif choice == '7':
            ROW_MAJOR()
        elif choice == '8':
            COLUMN_MAJOR()
        elif choice == '9':
            SPARSE()
        elif choice == '10':
            DISPLAY_RECORDS()
        elif choice == '11':
            PRINT_TABLE()
        elif choice == '12':
            COMPLEXITY()
        elif choice == '13':
            print("Exiting Weather System... Good luck!")
            break
        else:
            print("Invalid Choice! Please enter 1-13.")


if __name__ == "__main__":
    MAIN()