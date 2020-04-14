import sqlite3
def view_userRegister():
    conn=sqlite3.connect("movieRecommenderSystem.db")
    cur=conn.cursor()
    cur.execute("SELECT * FROM userRatings")
    rows=cur.fetchall()
    conn.close()
    print(rows)

if __name__ == "__main__":
    view_userRegister()