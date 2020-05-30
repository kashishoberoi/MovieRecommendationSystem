from flask import Flask, redirect, url_for, request,render_template
from flask import session, flash
#DATABASE USER
import sqlite3

def connect_userRegister():
    conn=sqlite3.connect("movieRecommenderSystem.db")
    cur=conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS user (userid INTEGER PRIMARY KEY, username text, password text, genre text)")
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

def search_userRegister_userOnly(username):
    conn=sqlite3.connect("movieRecommenderSystem.db")
    cur=conn.cursor()
    cur.execute("SELECT * FROM user WHERE username = ?", (username,))
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
    
#FETCH GENRE MOVIES

def fetch_genre_movies(genre):
    genre = genre.split('|')
    conn=sqlite3.connect("movieRecommenderSystem.db")
    cur=conn.cursor()
    gen_dict = dict()
    for gen in genre:
        cur.execute("SELECT * FROM moviesGenre WHERE genre = ?", (gen,))
        rows=cur.fetchall()
        gen_dict[gen] = rows
    conn.close()
    return gen_dict

def fetch_cluster_movies(genre):
    genre = genre.split('|')
    gen_list = ['Comedy','IMAX','Sci-Fi','Children','Mystery','Musical','Drama','Adventure','War','Western','Animation','Thriller','Crime','Documentary','Fantasy','Horror','Romance','Action','Film-Noir']
    gen_dict = dict()
    for i in range(len(gen_list)):
        gen_dict[gen_list[i]] = i
    x = [0 for i in range(19)]
    for gen in genre:
        x[gen_dict[gen]] = 1
    centre =[[ 1.99840144e-14,  7.88436268e-04,  2.12877792e-02,
         2.70696452e-02,  2.39159001e-02,  1.07752957e-02,
         1.00000000e+00,  2.58431888e-02,  6.48269820e-02,
         9.02321507e-03,  9.54883925e-03, -3.77475828e-14,
         1.89570581e-14,  1.57687254e-02,  1.76084100e-02,
         1.29479760e-14, -3.21270788e-14, -2.41334730e-14,
         5.16863776e-03],
       [ 8.43450479e-01,  3.99361022e-04,  1.95686901e-02,
         2.83546326e-02,  1.43769968e-02,  7.46805112e-02,
        -1.18238752e-14,  2.03674121e-02,  1.07827476e-02,
         8.78594249e-03,  8.78594249e-03,  1.35782748e-02,
         2.31629393e-02,  1.99680511e-03,  4.87220447e-02,
         8.78594249e-03,  1.00000000e+00,  3.35463259e-02,
        -3.06178694e-16],
       [ 1.85407245e-14,  7.17257208e-04,  7.15822694e-02,
         2.76861282e-02,  2.45301965e-02,  1.29106298e-02,
         5.96189764e-14,  5.66213743e-15,  1.44885956e-02,
         3.33066907e-16,  1.27815235e-01, -2.60069744e-14,
         8.32667268e-16,  2.77555756e-15,  3.09855114e-02,
         4.16333634e-17,  2.86902883e-04, -1.11577414e-14,
         2.29522307e-03],
       [ 5.53379040e-02,  1.12634672e-02,  3.36434868e-01,
         8.32517140e-03,  3.03623898e-02,  1.95886386e-03,
        -1.17683641e-14,  1.85962357e-15,  4.11361410e-02,
         5.87659158e-03,  6.61116552e-02,  3.88834476e-01,
         6.36630754e-03,  9.79431929e-04,  5.58276200e-02,
         7.24779628e-02,  4.26052889e-02,  1.00000000e+00,
         1.46914789e-03],
       [ 1.00000000e+00,  4.72366556e-04,  2.45630609e-02,
         3.99149740e-02,  1.35805385e-02,  2.45630609e-02,
         6.67244038e-14,  2.14926783e-02,  8.85687293e-03,
         1.98452366e-15,  3.58998583e-02,  9.91969769e-03,
         4.44024563e-02,  1.96032121e-02,  3.15304676e-02,
         5.72744450e-02, -2.50355292e-14,  5.52668871e-02,
         2.36183278e-04],
       [ 5.54465162e-02,  4.90677134e-04,  1.09421001e-01,
         2.94406281e-03,  2.16388616e-01,  1.96270854e-03,
         1.87929342e-01,  1.37389598e-02,  4.41609421e-03,
         1.96270854e-03,  3.43473994e-03,  1.00000000e+00,
         5.10304220e-02,  1.96270854e-03,  5.00490677e-02,
         1.00000000e+00,  2.06084396e-02,  6.08439647e-02,
         1.96270854e-03],
       [ 1.72639680e-14,  5.61362756e-03,  4.06504065e-03,
         3.48432056e-03,  2.90360046e-03,  1.68408827e-02,
         4.56301663e-14,  8.32365467e-03,  1.99380565e-02,
         7.74293457e-04,  5.80720093e-03,  2.12930701e-03,
         9.67866822e-03,  1.00000000e+00,  9.67866822e-04,
         4.83933411e-03,  1.74216028e-03,  1.54858691e-03,
        -3.70363462e-16],
       [ 3.99436090e-02,  8.92857143e-03,  4.55827068e-02,
         1.12781955e-02,  3.47744361e-02,  2.81954887e-03,
         1.00000000e+00,  1.77161654e-01,  1.23120301e-01,
         3.85338346e-02,  1.40977444e-02,  3.12030075e-01,
         2.71616541e-01,  4.69924812e-03,  2.44360902e-02,
         2.16165414e-02,  3.94736842e-02,  1.00000000e+00,
         1.40977444e-03],
       [ 1.51534126e-01,  2.81778334e-02,  2.71133375e-01,
         3.38134001e-02,  2.69254853e-02,  6.26174076e-03,
         1.31496556e-02,  1.00000000e+00,  4.69630557e-02,
         2.44207890e-02,  8.20288040e-02,  1.23356293e-01,
         3.69442705e-02,  4.38321853e-03,  1.48403256e-01,
         3.56919224e-02,  7.63932373e-02,  7.32623669e-01,
         1.25234815e-03],
       [ 1.42108547e-14,  6.30119723e-04,  1.57529931e-02,
         1.76433522e-02,  2.20541903e-02,  2.96156270e-02,
         1.00000000e+00,  3.84373031e-02,  6.39571519e-02,
         1.44927536e-02,  9.45179584e-03,  3.65469439e-02,
         4.37933207e-02,  2.83553875e-03,  4.06427221e-02,
         8.50661626e-03,  1.00000000e+00,  3.87523629e-02,
         5.98613737e-03],
       [ 3.06498545e-01,  2.03685742e-02,  1.16391853e-01,
         7.66246363e-01,  2.23084384e-02,  4.17070805e-02,
         1.35790495e-01,  7.60426770e-01,  2.90979631e-03,
         7.75945684e-03,  1.71677983e-01,  5.81959263e-03,
         5.81959263e-03,  5.81959263e-03,  7.41028128e-01,
         1.84287100e-02,  4.75266731e-02,  3.10378274e-02,
         1.93986421e-03],
       [ 2.89017341e-02, -7.97972799e-17,  6.74373796e-03,
         4.33526012e-03,  1.74373796e-01,  1.92678227e-03,
         1.00000000e+00,  1.68593449e-02,  5.78034682e-03,
         4.81695568e-03,  2.40847784e-03,  3.95953757e-01,
         1.00000000e+00,  3.85356455e-03,  5.29865125e-03,
         3.56454721e-02,  3.27552987e-02,  4.81695568e-04,
         6.84007707e-02],
       [ 4.39442658e-01,  2.03644159e-02,  4.50160772e-02,
         9.49624866e-01,  2.25080386e-02,  6.21650589e-02,
         3.75133976e-02,  2.88317256e-01,  1.07181136e-03,
         6.43086817e-03,  1.00000000e+00,  3.21543408e-03,
         8.57449089e-03, -6.93889390e-17,  1.08252947e-01,
         2.14362272e-03,  3.00107181e-02,  5.03751340e-02,
        -9.62771529e-17],
       [ 1.62761241e-01,  3.16656111e-03,  2.02659911e-02,
         1.89993667e-03,  1.91260291e-01,  1.89993667e-03,
        -1.11022302e-14,  4.11652945e-02,  3.79987334e-03,
         6.33312223e-03,  1.58328056e-02,  5.61114630e-01,
         1.00000000e+00,  1.89993667e-03,  1.26662445e-02,
         1.26662445e-02,  3.35655478e-02,  4.78784041e-01,
         3.03989867e-02],
       [ 2.73556231e-02,  1.68861871e-03,  1.75616346e-01,
         2.70178994e-03,  9.69267139e-02,  2.70178994e-03,
         1.21580547e-01,  1.51975684e-02,  4.72813239e-03,
         2.02634245e-03,  1.68861871e-02,  6.93889390e-16,
         2.12765957e-02,  1.68861871e-03,  6.38297872e-02,
         1.00000000e+00,  9.79398852e-03,  3.71496116e-02,
         6.75447484e-04],
       [ 4.61847390e-02,  1.33868809e-03,  7.36278447e-02,
         3.34672021e-03,  1.86077644e-01,  2.00803213e-03,
         1.00000000e+00,  2.81124498e-02,  3.34672021e-02,
         4.01606426e-03,  4.01606426e-03,  1.00000000e+00,
         1.88737914e-15,  5.35475234e-03,  1.87416332e-02,
         2.24820162e-15,  2.20883534e-02,  2.48412402e-15,
         2.00803213e-02],
       [ 1.00000000e+00,  6.48088140e-04,  1.19896306e-02,
         3.95333765e-02,  1.16655865e-02,  1.87945561e-02,
         1.00000000e+00,  2.07388205e-02,  1.62022035e-02,
         5.18470512e-03,  7.45301361e-03,  6.48088140e-04,
         5.05508749e-02,  6.80492547e-03,  3.07841866e-02,
         1.19896306e-02,  3.42781359e-15,  2.49513934e-02,
         6.48088140e-04],
       [ 1.54375615e-01,  3.33934269e-17,  8.84955752e-03,
         4.91642085e-03,  8.84955752e-03,  1.96656834e-02,
         1.86823992e-02,  8.45624385e-02,  2.45821042e-02,
         1.00000000e+00,  3.93313668e-03,  6.88298918e-03,
         7.86627335e-03,  9.83284169e-04,  2.94985251e-03,
         2.16322517e-02,  8.06293019e-02,  1.32743363e-01,
        -1.24032729e-16],
       [ 1.77111717e-02,  2.04359673e-03,  1.28746594e-01,
         2.04359673e-03,  1.95504087e-01,  6.81198910e-04,
        -1.09356968e-14,  2.65667575e-02,  1.22615804e-02,
         1.36239782e-03,  4.76839237e-03,  1.00000000e+00,
         1.83186799e-15, -1.58206781e-15,  2.17983651e-02,
         2.20656826e-15,  5.31335150e-02,  2.30371278e-15,
         1.22615804e-02],
       [ 1.00000000e+00,  5.59448321e-17,  9.41176471e-03,
         1.41176471e-02,  1.56862745e-02,  3.37254902e-02,
         1.00000000e+00,  1.64705882e-02,  1.25490196e-02,
         4.70588235e-03,  7.84313725e-03,  2.19607843e-02,
         3.60784314e-02,  3.13725490e-03,  3.37254902e-02,
         4.70588235e-03,  1.00000000e+00,  3.37254902e-02,
         7.84313725e-04]]
    final = [sum([abs(c[i]-x[i]) for i in range(19)])for c in centre]
    clusterNumber = final.index(min(final))
    return search_movieCluster(clusterNumber)

def make_home_page(genre):
    gen_dict = fetch_genre_movies(genre)
    gen_cluster_movie_list = fetch_cluster_movies(genre)
    return gen_dict,gen_cluster_movie_list
    
#API CALLS
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Kashishsagarvivek'  
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/takemeto',methods = ['POST','GET'])
def toakemeto():
    if request.method == 'POST':
        if request.form['submit_button'] == 'LOGIN':
            return render_template('login.html')
        if request.form['submit_button'] == 'SIGNUP':
            return render_template('signup.html')



# Searching Movies
def search_userRatingsMovieName(search_string):
    conn=sqlite3.connect("movieRecommenderSystem.db")
    cur=conn.cursor()
    cur.execute("SELECT * FROM movies WHERE lower(movieName) LIKE ?", (search_string.lower()+'%',))
    rows=cur.fetchall()
    conn.close()
    return rows

@app.route('/searchmovie',methods = ['POST','GET'])
def searchmovie():
    searchBool = True
    username = request.form['username'] #search_string
    search_string = request.form['search_string']
    if search_string=='':
        movies = []
        searchBool= False
    movies = search_userRatingsMovieName(search_string)
    if searchBool == False or len(movies) == 0:
        return render_template('searchpage.html',username = username,movies=movies,search_string = search_string,searchBool=searchBool),204
    else:
        return render_template('searchgenrepage.html',username = username,movies=movies,search_string = search_string,searchBool=searchBool)

# Searching Genre

def search_genre(genre):
    conn=sqlite3.connect("movieRecommenderSystem-base-2.db")
    cur=conn.cursor()
    cur.execute("SELECT * FROM movie_genre WHERE lower(genre) LIKE ?", (genre.lower()+'%',))
    rows=cur.fetchall()
    conn.close()
    return rows

@app.route('/searchgenre',methods = ['POST','GET'])
def searchgenre():
    searchBool = True
    username = request.form['username'] #search_string
    search_string = request.form['search_string']
    if search_string=='':
        movies = []
        searchBool= False
    movies = search_genre(search_string)
    if searchBool == False or len(movies) == 0:
        return render_template('searchgenrepage.html',username = username,movies=movies,search_string = search_string,searchBool=searchBool),204
    else:
        return render_template('searchgenrepage.html',username = username,movies=movies,search_string = search_string,searchBool=searchBool)
@app.route('/login',methods = ['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if len(search_userRegister(username,password)) == 1:
            genre = search_userRegister(username,password)[0][3]
            genre_dict,gen_cluster_movies = make_home_page(genre)
            return render_template('main.html',username = username,gen_dict = genre_dict,gen_cluster_movies = gen_cluster_movies)
        else:
            return render_template('login.html',message = 'user not found'),401

@app.route('/signup',methods = ['POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if len(search_userRegister_userOnly(username))==0 and username!='' and password!='':
            genre_fetch = request.form.getlist('genre')
            genre = '|'.join(genre_fetch)
            genre_dict,gen_cluster_movies = make_home_page(genre)
            insert_userRegister(username,password,genre)
            print(genre_fetch)
            return render_template('main.html',username = username,gen_dict = genre_dict,gen_cluster_movies = gen_cluster_movies,status = 200)
        else:
            return render_template('signup.html',message = 'user already there',status = 300),401
#RATING and USERS
def connect_userRatings():
    conn=sqlite3.connect("movieRecommenderSystem.db")
    cur=conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS userRatings (id INTEGER PRIMARY KEY,userid INTEGER, username text, movieId INTEGER, rating REAL)")
    conn.commit()
    conn.close()

def insert_userRatings(userId,username,movieId,rating):
    conn=sqlite3.connect("movieRecommenderSystem.db")
    cur=conn.cursor()
    cur.execute("INSERT INTO userRatings VALUES (NULL,?,?,?,?)",(userId,username,movieId,rating))
    conn.commit()
    conn.close()

def search_userRatings(username,movieId):
    conn=sqlite3.connect("movieRecommenderSystem.db")
    cur=conn.cursor()
    cur.execute("SELECT * FROM userRatings WHERE username = ? AND movieId = ?", (username,movieId))
    rows=cur.fetchall()
    conn.close()
    return rows

def update_userRatings(username,movieId,rating):
    conn=sqlite3.connect("movieRecommenderSystem.db")
    cur=conn.cursor()
    cur.execute("UPDATE userRatings SET rating = ? WHERE username=? AND movieId= ?",(rating,username,movieId))
    conn.commit()
    conn.close()

def search_userRatings_onlyUsername(username):
    conn=sqlite3.connect("movieRecommenderSystem.db")
    cur=conn.cursor()
    cur.execute("SELECT movieId,rating FROM userRatings WHERE username = ?", (username,))
    rows=cur.fetchall()
    conn.close()
    return rows

def search_movie_bymovieId(movieId):
    conn=sqlite3.connect("movieRecommenderSystem.db")
    cur=conn.cursor()
    cur.execute("SELECT movieName FROM movies WHERE movieId = ?", (movieId,))
    rows=cur.fetchall()
    conn.close()
    if len(rows)==0:
        return []
    return rows

def get_user_rating_details(username):
    movieId_rating = search_userRatings_onlyUsername(username)
    if len(movieId_rating)==0:
        return []
    for itr in range(len(movieId_rating)):
        movieId_rating[itr] = list(movieId_rating[itr])
        movieId_rating[itr].append(search_movie_bymovieId(movieId_rating[itr][0]))
    return movieId_rating

@app.route('/userratingpage',methods=['POST'])
def userratingpage():
    if request.method == 'POST':
        username = request.form['username']
        movies = get_user_rating_details(username)
        if len(movies)==0:
            return render_template('userRatings.html',username = username,movie_list = movies,userRatingBool = False)
    return render_template('userRatings.html',username = username,movie_list = movies,userRatingBool = True)


# Genre Cluster Data
def connect_movie_cluster():
    conn=sqlite3.connect("movieRecommenderSystem.db")
    cur=conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS moviesCluster (id INTEGER PRIMARY KEY,clusterNumber INTEGER ,movieId INTEGER, movieName text)")
    conn.commit()
    conn.close()

def insert_movie_cluster(clusterNumber,movieId,movieName):
    conn=sqlite3.connect("movieRecommenderSystem.db")
    cur=conn.cursor()
    cur.execute("INSERT INTO moviesCluster VALUES (NULL,?,?,?)",(clusterNumber,movieId,movieName))
    conn.commit()
    conn.close()

def view_movieCluster():
    conn=sqlite3.connect("movieRecommenderSystem.db")
    cur=conn.cursor()
    cur.execute("SELECT * FROM moviesCluster")
    rows=cur.fetchall()
    conn.close()
    print(rows)

def search_movieCluster(clusterNumber):
    conn=sqlite3.connect("movieRecommenderSystem.db")
    cur=conn.cursor()
    cur.execute("SELECT movieId,movieName FROM moviesCluster WHERE clusterNumber= ?", (clusterNumber,))
    rows=cur.fetchall()
    conn.close()
    return rows

@app.route('/updaterating',methods=['POST'])
def updaterating():
    if request.method == 'POST':
        username = request.form['username']
        movieId = request.form['movieId']
        rating = request.form['user_rating']
        print(username)
        user_details = search_userRegister_userOnly(username)
        if len(user_details) == 0:
            return 'INVALID USER',401
        user_id = user_details[0][0]
        print(search_userRatings(username,movieId))
        if len(search_userRatings(username,movieId)) == 0:
            insert_userRatings(user_id,username,movieId,rating)
        else:
            update_userRatings(username,movieId,rating)
    return 'UPDATED',200

#Logout user and clear session

@app.route('/userlogout',methods=['POST'])
def userlogout():
    session.clear()
    flash('You have been logged out!', 'success')
    return render_template('index.html')
    
if __name__ == '__main__':
    connect_userRegister()
    connect_userRatings()
    app.run(debug = False)