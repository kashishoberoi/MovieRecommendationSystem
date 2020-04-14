import sqlite3

def connect_userRegister():
    conn=sqlite3.connect("movieRecommenderSystem.db")
    cur=conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY, username text PRIMARY KEY, password text, genre text)")
    conn.commit()
    conn.close()

def insert_userRegister(username,password,genre):
    conn=sqlite3.connect("movieRecommenderSystem.db")
    cur=conn.cursor()
    cur.execute("INSERT INTO user VALUES (NULL,?,?,?)",(username,password,genre))
    conn.commit()
    conn.close()

def view_userRegister():
    conn=sqlite3.connect("movieRecommenderSystem.db")
    cur=conn.cursor()
    cur.execute("SELECT * FROM user")
    rows=cur.fetchall()
    conn.close()
    return rows

def search_userRegister(username,password):
    conn=sqlite3.connect("movieRecommenderSystem.db")
    cur=conn.cursor()
    cur.execute("SELECT * FROM user WHERE username = ? AND password = ?", (username,password))
    rows=cur.fetchall()
    conn.close()
    return rows

def delete_userRegister(username,password):
    conn=sqlite3.connect("movieRecommenderSystem.db")
    cur=conn.cursor()
    cur.execute("DELETE FROM user WHERE username = ? AND password = ?",(username,password))
    conn.commit()
    conn.close()

def update_userRegister(username,genre):
    conn=sqlite3.connect("movieRecommenderSystem.db")
    cur=conn.cursor()
    cur.execute("UPDATE user SET genre = ? WHERE username=?",(genre,username))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    connect_userRegister()
    insert_userRegister('kashish','oberoi','0000001010101011001')
    print(view_userRegister())
