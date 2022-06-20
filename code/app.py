from flask import Flask, render_template, request
import pyodbc, time

app = Flask(__name__)

# Connecting to database

host = ""
db = ""
user = ""
pwd ="@CSE6331"
driver= '{SQL Server}'
# driver= '{ODBC Driver 17 for SQL Server}'
connection = pyodbc.connect('DRIVER='+driver+';PORT=1433;SERVER='+host+';PORT=1443;DATABASE='+db+';UID='+user+';PWD='+ pwd)
# connection_string = "Server=" + host + ",1433;Initial Catalog=" + db + ";Persist Security Info=False;User ID=" + user + ";Password=" + pwd + ";MultipleActiveResultSets=False;Encrypt=True;TrustServerCertificate=False;Connection Timeout=30;"
cursor = connection.cursor()

@app.route('/')
def landing_page():
    select_top_10_query = "SELECT TOP (5) * FROM [dbo].[ni]"
    cursor.execute(select_top_10_query)
    response = cursor.fetchall()
    return render_template("base.html", rows = response, count = 5)

@app.route('/id_range', methods=["GET", "POST"])
def id_range():
    id_start = int(request.form['id_start'])
    id_end = int(request.form['id_end'])
    select_top_n_query_get_count = "SELECT COUNT(*) FROM [dbo].[ni] WHERE id BETWEEN " + str(id_start) + " AND " + str(id_end)
    cursor.execute(select_top_n_query_get_count)
    count = cursor.fetchall()
    select_top_n_query = "SELECT * FROM [dbo].[ni] WHERE id BETWEEN " + str(id_start) + " AND " + str(id_end)
    cursor.execute(select_top_n_query)
    response = cursor.fetchall()
    return render_template("base.html", rows = response, count = count[0][0], time = 0)

@app.route('/id_range_inner_join', methods=["GET", "POST"])
def id_range_inner_join():
    id_start = int(request.form['id_start_inner_join'])
    id_end = int(request.form['id_end_inner_join'])
    start_time = time.time()
    select_top_n_query_get_count = "SELECT COUNT(*) FROM [dbo].[ni] INNER JOIN [dbo].[di] ON [dbo].[di].[id] = [dbo].[ni].[id] WHERE [dbo].[ni].[id] BETWEEN " + str(id_start) + " AND " + str(id_end)
    cursor.execute(select_top_n_query_get_count)
    count = cursor.fetchall()
    select_top_n_query = "SELECT [dbo].[ni].[name], [dbo].[di].* FROM [dbo].[ni] INNER JOIN [dbo].[di] ON [dbo].[di].[id] = [dbo].[ni].[id] WHERE [dbo].[ni].[id] BETWEEN " + str(id_start) + " AND " + str(id_end) + ";"
    cursor.execute(select_top_n_query)
    response = cursor.fetchall()
    # time_diff_query = ""
    # cursor.execute(time_diff_query)
    # time = cursor.fetchall()
    return render_template("base.html", rows = response, count = count[0][0], time = time.time() - start_time)

@app.route('/matching_code', methods=["GET", "POST"])
def matching_code():
    n = int(request.form['number_of_codes'])
    code = int(request.form['code'])
    start_time = time.time()
    select_top_n_query = "SELECT TOP ("+ str(n) +") [dbo].[ni].[name], [dbo].[di].* FROM [dbo].[ni] INNER JOIN [dbo].[di] ON [dbo].[di].[id] = [dbo].[ni].[id] WHERE [dbo].[di].[code] = " + str(code)
    cursor.execute(select_top_n_query)
    response = cursor.fetchall()
    return render_template("base.html", rows = response, count = n, time = time.time() - start_time)

@app.route('/operations')
def operations():
    return render_template("operations.html")

if __name__ == '__main__':
    app.run()
