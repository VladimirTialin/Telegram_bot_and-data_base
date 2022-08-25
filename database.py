import sqlite3 as dbe
import os.path
def OpenDataBase():
    try:
        if os.path.exists("C:/Users/Владимир/Desktop/HomeWork10/database.db"):
            return dbe.connect("C:/Users/Владимир/Desktop/HomeWork10/database.db")
        else:
            raise
    except:
        db = dbe.connect("C:/Users/Владимир/Desktop/HomeWork10/database.db")
        cur = db.cursor()
        cur.execute(
            "CREATE TABLE departments (id INTEGER PRIMARY KEY AUTOINCREMENT, department TEXT NOT NULL)")
        cur.execute(
            "CREATE TABLE positions (id INTEGER PRIMARY KEY AUTOINCREMENT, position TEXT NOT NULL);")
        cur.execute('''CREATE TABLE persons (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                             name TEXT NOT NULL,
                                             birth TEXT NOT NULL,
                                             tel  TEXT  NOT NULL,
                                             department INTEGER NOT NULL REFERENCES departments (id),
                                             position   INTEGER NOT NULL REFERENCES positions (id));''')
        db.commit()
        return db

def SaveDataBase(database: dbe.Connection):
    database.commit()


def CloseDataBase(database: dbe.Connection):
    database.close()


def GetDepartmentID(database: dbe.Connection, department: str):
    cur = database.cursor()
    cur.execute(
        f"SELECT id FROM departments WHERE department = '{department}';")
    result = cur.fetchall()
    if len(result) != 0:
        return result[0][0]
    else:
        return None

def AddDepartment(database: dbe.Connection, department: str):
    departmentID = GetDepartmentID(database, department)
    if departmentID is None:
        cur = database.cursor()
        cur.execute(
            f"INSERT INTO departments (department) VALUES('{department}');")
    departmentID = GetDepartmentID(database, department)
    return departmentID

def GetAllDepartments(database):
    cur = database.cursor()
    cur.execute("SELECT * FROM departments;")
    result = cur.fetchall()
    return result

def GetPositionstID(database: dbe.Connection, position: str):
    cur = database.cursor()
    cur.execute(
        f"SELECT id FROM positions WHERE position = '{position}';")
    result = cur.fetchall()
    if len(result) != 0:
        return result[0][0]
    else:
        return None

def AddPosition(database: dbe.Connection, position: str):
    positionID = GetPositionstID(database, position)
    if positionID is None:
        cur = database.cursor()
        cur.execute(
            f"INSERT INTO positions (position) VALUES('{position}');")
    positionID = GetPositionstID(database, position)
    return positionID

def GetAllPositions(database):
    cur = database.cursor()
    cur.execute("SELECT * FROM positions;")
    result = cur.fetchall()
    return result

def AddPerson(database: dbe.Connection, name: str, birth: str, tel: str, department: str, position: str):
    departmentID = AddDepartment(database, department)
    positionID = AddPosition(database, position)
    cur = database.cursor()
    cur.execute(f''' INSERT 
                     INTO persons (name, birth, tel, department, position) 
                     VALUES('{name}','{birth}', '{tel}', {departmentID}, {positionID}); ''')

def GetPerson(database: dbe.Connection, id: int):
    cur = database.cursor()
    cur.execute(f'''SELECT persons.id, persons.name, persons.birth, persons.tel, departments.department, positions.position
                    FROM  persons
                    LEFT JOIN departments ON persons.department=departments.id
                    LEFT JOIN positions ON persons.position=positions.id
                    WHERE persons.id={id};
                 ''')
    result = cur.fetchall()
    return result[0] if len(result) != 0 else None

def GetAllPersons(database: dbe.Connection):
    cur = database.cursor()
    cur.execute(f'''SELECT persons.id, persons.name, persons.birth, persons.tel, departments.department, positions.position
                    FROM  persons
                    LEFT JOIN departments ON persons.department=departments.id
                    LEFT JOIN positions ON persons.position=positions.id;
                 ''')
    result = cur.fetchall()
    return result

def GetFilterPerson(database: dbe.Connection, search: str):
    data = GetAllPersons(database)
    result = [item for item in data if search.lower() in search.lower()
              in item[1].lower()]
    return result

def RemovePerson(database: dbe.Connection, id: int):
    cur = database.cursor()
    cur.execute(f"DELETE FROM persons WHERE id={id};")

def CangeName(database: dbe.Connection,name: str,id:int):
    cur = database.cursor()
    data=(name,id)
    updateName="""UPDATE persons SET name = ? WHERE id = ?"""
    cur.execute(updateName,data)
    database.commit()
def CangeBirth(database: dbe.Connection,birth: str,id:int):
    cur = database.cursor()
    data=(birth,id)
    updateName="""UPDATE persons SET birth = ? WHERE id = ?"""
    cur.execute(updateName,data)
    database.commit()   
    
def CangeTel(database: dbe.Connection,tel: str,id:int):
    cur = database.cursor()
    data=(tel,id)
    updateName="""UPDATE persons SET tel = ? WHERE id = ?"""
    cur.execute(updateName,data)
    database.commit()    
    
def CangeDep(database: dbe.Connection,department: str,id:int):
    departmentID = AddDepartment(database, department)
    cur = database.cursor()
    data=(departmentID,id)
    updateName="""UPDATE persons SET department = ? WHERE id = ?"""
    cur.execute(updateName,data)
    database.commit() 
def CangePos(database: dbe.Connection,positions: str,id:int):
    positionID = AddPosition(database, positions)
    cur = database.cursor()
    data=(positionID,id)
    updateName="""UPDATE persons SET position = ? WHERE id = ?"""
    cur.execute(updateName,data)
    database.commit() 