from flask import Flask,render_template,url_for,redirect,request,flash
from flask_mysqldb import MySQL
app=Flask(__name__)

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='2002'
app.config['MYSQL_DB']='smarket'
app.config['MYSQL_CURSORCLASS']='DictCursor'
mysql=MySQL(app)


@app.route('/')
def home():
    con=mysql.connection.cursor()
    sql="select * from employee"
    con.execute(sql)
    res=con.fetchall()
    return render_template("home.html",datas=res)


@app.route("/adduser",methods=['GET','POST'])
def adduser():
    if request.method =='POST':
        name=request.form['name']
        city=request.form['city']
        age=request.form['age']
        con=mysql.connection.cursor()
        sql="insert into employee(Name,City,Age) value (%s,%s,%s)"
        con.execute(sql,[name,city,age])
        mysql.connection.commit()
        con.close()
        flash('Employee Details Added')
        return redirect(url_for("home"))
    return render_template("adduser.html")
    
    
@app.route("/edituser/<string:id>",methods=['GET','POST'])
def edituser(id):
    con=mysql.connection.cursor()
    if request.method=='POST':
        name=request.form['name']
        city=request.form['city']
        age=request.form['age']
        sql="update employee set NAME=%s,CITY=%s,AGE=%s where ID=%s"
        con.execute(sql,[name,city,age,id])
        mysql.connection.commit()
        con.close()
        flash('Employee Details Updated')
        return redirect(url_for('home'))
        con=mysql.connection.cursor()
    sql="select * from employee where ID=%s "
    con.execute(sql,[id])
    res=con.fetchone()
    return render_template('edituser.html',datas=res)



@app.route("/deleteuser/<string:id>",methods=['GET','POST'])
def deleteuser(id):
    con=mysql.connection.cursor()
    sql="delete from employee where ID=%s "
    con.execute(sql,[id])
    mysql.connection.commit()
    con.close()
    flash('Employee Details Deleted')
    return redirect(url_for('home'))
  
if(__name__=='__main__'):
    app.secret_key='abc123'
    app.run(debug=True)