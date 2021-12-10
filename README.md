# Task3 for LeverX courses

## About The Script

Given 2 files:
* students.json (available fields: id, name, birthday, room, sex)
* rooms.json (available fields: id, name)


* Create schema with MySQL by relations in 2 files above (One-to-many relation)


* Create script to load 2 files into database


* Create queries to get:
* List of rooms and amount of students in every room
* Top 5 rooms with the smallest average age of students
* Top 5 rooms with the biggest difference between age of students
* List of rooms with students of different sexes


* Create necessary indexes 


* Save result in JSON/XML format


* CLI has to have the next arguments:
* students - path to file with students
* rooms - path to file with rooms
* format - output format (XML/JSON)

## Installation
1. Clone the repo
    ```sh
    git clone https://github.com/yuramorozov01/leverx_task3.git
    cd leverx_task3/
    ```
2. Create virtual environment
    ```sh
    python3 -m venv venv
    ```
3. Activate virtual environment
    ```sh
    source venv/bin/activate
    ```
4. Install dependencies
    ```sh
    pip3 install -r requirements.txt
    ```

## Exectuting
1. Run script (format argument is case insensitive):
    * JSON output format 
    ```sh
    python3 main.py path/to/students.json path/to/rooms.json JSON path/to/save.json
    ```
    * XML output format
    ```sh
    python3 main.py path/to/students.xml path/to/rooms.xml XML path/to/save.xml
    ```
