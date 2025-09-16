# Data_Structures_Lab

# Weather Data Storage System 🌦️

## 📌 Project Overview
This project implements a **Weather Data Storage System** as part of the **Data Structures course (ENCS205 / ENCA201)** in the **3rd Semester, B.Tech (CSE - Data Science)**.  
The system is designed to **collect, store, and manage temperature records** for different cities and years. It uses **2D arrays** and **Abstract Data Types (ADTs)** to organize data efficiently and allows for insertion, deletion, retrieval, and analysis of records.  

The focus is on understanding:
- How to design and implement **ADTs**.
- Storing tabular data in **2D arrays**.
- Comparing **row-major vs. column-major** access.
- Handling **sparse data** using sentinel values.
- Performing **time and space complexity analysis**.

---

## 🎯 Assignment Objectives
- Build a strong foundation in Python and Data Structures.  
- Work with **2D arrays and ADTs** in a practical scenario.  
- Implement real-world style **data storage and retrieval**.  
- Learn to handle **sparse data efficiently**.  
- Analyze and explain **time/space complexity** of operations.  

---

## 🏗️ Features Implemented
1. **Weather Record ADT**
   - Attributes:  
     - `Date` (DD/MM/YYYY)  
     - `City` (String)  
     - `Temperature` (Float in °C)  
   - Operations:  
     - `INSERT()` → Add new record  
     - `DELETE()` → Remove a record (city + date)  
     - `RETRIEVE()` → Get all records for a given city & year  

2. **2D Array Storage**
   - Rows = Years  
   - Columns = Cities  
   - Each cell stores a list of weather records (or sentinel if empty).  

3. **Data Access Methods**
   - `ROW_MAJOR()` → Traverse records row by row (year-wise).  
   - `COLUMN_MAJOR()` → Traverse records column by column (city-wise).  
   - `SPARSE()` → Show only non-empty records in sparse representation.  

4. **Utility Functions**
   - `POPULATE()` → Load demo records for quick testing.  
   - `POPULATE_ARRAY()` → User-defined years & cities with manual input.  
   - `DISPLAY_RECORDS()` → View all records in flat list form.  
   - `PRINT_TABLE()` → Tabular summary (years × cities).  

5. **Complexity Analysis**
   - `COMPLEXITY()` → Prints time & space complexity of key operations.  

---

## ⚙️ How It Works
- Data is stored in a **global matrix (2D list)** with years as rows and cities as columns.  
- Each cell either contains a **list of records** or a **sentinel value (`None`)** for empty.  
- Operations dynamically adjust the matrix size when new years or cities are added.  
- Sparse representation extracts only non-empty cells for memory-efficient reporting.  

---

## 📊 Complexity Analysis
- **Insert:** O(R + C) in worst case (matrix resize), typically O(1) per record.  
- **Delete:** O(R + C + M), where M = records in a cell.  
- **Retrieve:** O(R + C + M).  
- **Row/Column Traversal:** O(R × C).  
- **Space:** O(R × C) for matrix + O(K) for total records.
