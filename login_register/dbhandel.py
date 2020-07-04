import sqlite3

def save_project(name,project,p_title,project_content):
    connection=sqlite3.connect('db.sqlite3')
    c=connection.cursor()
    c.execute("INSERT INTO project_details (NAME,PROJECT_NAME,PROJECT_TITLE,PROJECT_CONTENT) VALUES (?,?,?,?);",(name,project,p_title,project_content))
    connection.commit()
    connection.close()

def retriveproject(name):
    connection = sqlite3.connect('db.sqlite3')
    c = connection.cursor()
    d=c.execute("SELECT PROJECT_NAME,PROJECT_TITLE,PROJECT_CONTENT FROM project_details where NAME=?",(name,))
    data_t={}
    for names in d.fetchall():
        data_t[names[0]]={"title":names[1],"body":names[2]}

    connection.close()
    return data_t