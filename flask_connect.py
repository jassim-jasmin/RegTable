from flask import Flask, render_template, request, url_for, jsonify
import PyRegexpExtract

app = Flask(__name__)

ob = None
submitStatus = None

@app.route('/')
def submit():
    # obj = PyRegexpExtract.DB("local")
    # obj.connect()

    return render_template('main.html')

@app.route('/main',methods = ['POST', 'GET'])#####################
def index():
    if request.form['submit_button']=='zillow':
        submitStatus='zillow'

    if request.form['submit_button'] == 'local':
        submitStatus='local'
    print(submitStatus)

    return render_template('local_interface.html', result=None)

submitStatus = 'zillow'
@app.route('/process',methods = ['POST', 'GET'])
def main_connect():
    print(submitStatus)
    if submitStatus == 'local':
            ob = PyRegexpExtract.DB("local")
            print("Button local")
            return render_template('local_interface.html', result=None)
    elif submitStatus == 'zillow':
            print("Button zillow")
            zillowConnect()
    else:
        print("Nothing happend")
    print("Return status \n\n")
    #print(request.form['firstName'])
    #return jsonify({'output':'Full Name: exit'})
    return render_template('local_interface.html', result=None)

def zillowConnect():

    sql_schema=request.form['sql_schema']
    sql_table_name=request.form['sql_table_name']
    sql_idColumnName=request.form['sql_idColumnName']
    sql_columnName=request.form['sql_columnName']
    sql_eColumnName=request.form['sql_eColumnName']
    sql_condition=request.form['sql_condition']
    regexp=request.form['regexp']
    group=request.form['group']
    op=request.form['op']
    rstring=request.form['rstring']
    print(sql_schema)
    ob = PyRegexpExtract.DB('zillow',sql_schema)
    ob.reSearchInsertRow(sql_table_name, sql_idColumnName, sql_columnName, sql_eColumnName,sql_condition , regexp, group, op, rstring)
    print("Complete")


@app.route('/main/local',methods = ['POST'])
def local_connect():
    # Assume data comes from somewhere else
    data = {"output": "Full Name:John Q Public"}
    #name = request.form('firstName')
    print("hai")
    #if name:
     #   print("The value from ajax")
      #  print(name)
      #  return jsonify({'output':'Full Name: jassim'})
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug = True, host='192.168.15.63',port='3225')
    #return render_template('framework_updatepg.html', result=None)