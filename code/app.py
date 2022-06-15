from datetime import datetime, timedelta
from flask import Flask, render_template, request
import pyodbc

app = Flask(__name__)

# Connecting to database

host = "tcp:cse6331.database.windows.net"
db = "cse6331assignment2"
user = "kjtcse6331"
pwd ="AzureSQL@CSE6331"
driver= '{SQL Server}'
# driver= '{ODBC Driver 17 for SQL Server}'
connection = pyodbc.connect('DRIVER='+driver+';PORT=1433;SERVER='+host+';PORT=1443;DATABASE='+db+';UID='+user+';PWD='+ pwd)
# connection_string = "Server=" + host + ",1433;Initial Catalog=" + db + ";Persist Security Info=False;User ID=" + user + ";Password=" + pwd + ";MultipleActiveResultSets=False;Encrypt=True;TrustServerCertificate=False;Connection Timeout=30;"
cursor = connection.cursor()

@app.route('/')
def landing_page():
    select_top_10_query = "SELECT TOP (5) * FROM [dbo].[earthquakes]"
    cursor.execute(select_top_10_query)
    response = cursor.fetchall()
    return render_template("base.html", earthquakes = response, count = 10)

@app.route('/greater_than_magnitude', methods=["GET", "POST"])
def greater_than_magnitude():
    n = float(request.form['magnitude'])
    select_top_n_query_get_count = "SELECT COUNT(*) FROM [dbo].[earthquakes] WHERE magnitude > " + str(n)
    cursor.execute(select_top_n_query_get_count)
    count = cursor.fetchall()
    select_top_n_query = "SELECT * FROM [dbo].[earthquakes] WHERE magnitude > " + str(n)
    cursor.execute(select_top_n_query)
    response = cursor.fetchall()
    return render_template("base.html", earthquakes = response, count = count[0][0])

@app.route('/top_n_quakes', methods=["GET", "POST"])
def top_n_quakes():
    n = int(request.form['number'])
    select_top_n_query = "SELECT TOP (" + str(n) + ") * FROM [dbo].[earthquakes]"
    cursor.execute(select_top_n_query)
    response = cursor.fetchall()
    return render_template("base.html", earthquakes = response, count = n)

@app.route('/split_over_last_n_days', methods=["GET", "POST"])
def split_over_last_n_days():
    n = int(request.form['days'])
    date_format = "%Y-%m-%dT%H-%M-%S"
    last_quake_in_data = datetime.strptime("2022-02-15T01:37:36.356", date_format)
    past_date = last_quake_in_data - timedelta(days = n)
    past_date_str = past_date.strftime(date_format)
    select_top_n_query_get_count = "SELECT COUNT(*) FROM [dbo].[earthquakes] WHERE time > " + past_date_str
    cursor.execute(select_top_n_query_get_count)
    count = cursor.fetchall()
    return render_template("splits.html", days = n, count = count[0][0], one_two = count[0][0], two_three = count[0][0], three_four = count[0][0], four_seven = count[0][0])

@app.route('/operations')
def operations():
    return render_template("operations.html")

if __name__ == '__main__':
    app.run()