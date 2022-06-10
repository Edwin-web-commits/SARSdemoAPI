import email
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def db_connection():
    conn = None
    try:
        conn = sqlite3.connect("users.sqlite")

    except sqlite3.error as e:
        print(e)    
    return conn    


@app.route('/users', methods=['GET', 'POST'])
def users():
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == 'GET':
        cursor = conn.execute("SELECT * FROM user")
        users = [
            dict(user_id=row[0], full_name=row[1], email=row[2], company=row[3], position=row[4], south_african_id=row[5])
         
            for row in cursor.fetchall()
        ]
        if users is not None:
            return jsonify(users)
          

    if request.method == 'POST':
        
        new_full_name = request.json['full_name']
        new_email = request.json['email']
        new_company = request.json['company']
        new_position = request.json['position']
        new_south_african_id = request.json['south_african_id']

        sql = """INSERT INTO user (full_name, email, company, position, south_african_id) VALUES(?, ?, ?, ?, ?)"""
        
        #user tabe
        cursor = cursor.execute(sql, (new_full_name, new_email, new_company, new_position, new_south_african_id))  
        
       
        conn.commit()     
        return f"User with the id: {cursor.lastrowid} created successfully",201



@app.route('/user/<int:id>',methods=['GET','PUT','DELETE'])
def single_user(id):

    conn =db_connection()
    cursor = conn.cursor()

    user = None

    if request.method == 'GET':
        cursor = cursor.execute("SELECT * FROM user WHERE user_id=?", (id,))
        rows = cursor.fetchall()
        for r in rows:
            user = r
        if user is not None:
            return jsonify(user), 200
        else:
            return "Something went wrong", 404      
        

    if request.method == 'PUT':
        sql ="""UPDATE user SET full_name=?, email=?,company=?, position=?, south_african_id=?  WHERE user_id=?"""

            
        full_name = request.json['full_name']
        email = request.json['email']
        company = request.json['company']
        position = request.json['position']
        south_african_id = request.json['south_african_id']
        updated_user = {
                    'user_id': id,
                    'full_name': full_name,
                    'email': email,
                    'company':company,
                    'position':position,
                    'south_african_id':south_african_id
                }
        conn.execute(sql,(full_name, email, company, position, south_african_id, id)) 
        conn.commit()       
        return jsonify(updated_user)



    if request.method == 'DELETE':
        sql ="""DELETE FROM user WHERE user_id=?"""
        conn.execute(sql,(id,))
        conn.commit()
        return "The user with id:{} has been deleted".format(id), 200


#AUTHENTICATION ENDPOINTS
@app.route('/auth/register', methods=['POST'])
def register():
    conn = db_connection()
    cursor = conn.cursor()

    new_username = request.json['username']
    new_password = request.json['password']

    sql = """INSERT INTO auth (username, password) VALUES(?, ?)"""

    #auth tabe
    cursor = cursor.execute(sql, (new_username, new_password))  
        
    
    conn.commit()     
    return f"User with the id: {cursor.lastrowid} created successfully",201


@app.route('/auth/user/<string:username>', methods=['GET'])
def registeredUser(username):
    conn = db_connection()
    cursor = conn.cursor()

    userAuth = None
    cursor = cursor.execute("SELECT * FROM auth WHERE username=?", (username,))
    rows = cursor.fetchall()
    for r in rows:
            userAuth = r
    if userAuth is not None:
            return jsonify(userAuth), 200
    else:
            return "Something went wrong", 404


@app.route('/auth/login/<string:username>', methods=['GET'])
def login(username):
    conn = db_connection()
    cursor = conn.cursor()

    userAuth = None
    cursor = cursor.execute("SELECT * FROM auth WHERE username=?", (username,))
    rows = cursor.fetchall()
    for r in rows:
            userAuth = r
    if userAuth is not None:
            return jsonify(userAuth), 200
    else:
            return "Something went wrong", 404 

#COMPLIANCE ENDPOINTS

#Submission Period ENDPOINTS
@app.route('/submissionperiod',methods=['POST'])
def submissionperiod():
    conn = db_connection()
    cursor = conn.cursor()

    
    new_submit_from_date = request.json['submit_from_date']
    new_submit_to_date = request.json['submit_to_date']
    new_financial_year = request.json['financial_year']
        

    sql = """INSERT INTO submissionPeriod (submit_from_date, submit_to_date, financial_year) VALUES(?, ?, ?)"""
        
    cursor = cursor.execute(sql, (new_submit_from_date, new_submit_to_date, new_financial_year))
        
   
    conn.commit()     
    return f"Period with the id: {cursor.lastrowid} created successfully",201


@app.route('/submissionperiod/<int:id>', methods=['GET'])
def getSubmitionPeriod(id):
    conn = db_connection()
    cursor = conn.cursor()

    period = None
    cursor = cursor.execute("SELECT * FROM submissionPeriod WHERE sub_id=?", (id,))
    rows = cursor.fetchall()
    for r in rows:
        period = r
    if period is not None:
        return jsonify(period), 200
    else:
        return "Something went wrong", 404

#Submission For Tax return ENDPOINTS
@app.route('/returnsubmittedon',methods=['POST'])
def returnSubmittedDate():
    conn = db_connection()
    cursor = conn.cursor()

    new_date_submitted = request.json['dateSubmitted']
    new_submission_period= request.json['submission_period']
    new_user_id = request.json['user_id']
        

    sql = """INSERT INTO returnSubmittedOn (dateSubmitted, submission_period, user_id) VALUES(?, ?, ?)"""
        
    cursor = cursor.execute(sql, (new_date_submitted, new_submission_period, new_user_id))
        
    
    conn.commit()     
    return f"Sumbision for Returns with the id: {cursor.lastrowid} created successfully",201


@app.route('/returnsubmittedon/<int:id>', methods=['GET'])
def getReturnSubmittedDate(id):
    conn = db_connection()
    cursor = conn.cursor()

    #dateSubmitted = None
    cursor = cursor.execute("SELECT * FROM returnSubmittedOn WHERE user_id=?", (id,))
    userSubmissions = [
            dict(id=row[0], dateSubmitted=row[1], submission_period=row[2], user_id=row[3])
         
            for row in cursor.fetchall()
        ]
    if users is not None:
        return jsonify(userSubmissions)
    

#User Compliance Status ENDPOINTS
@app.route('/usercompliancestatus',methods=['POST'])
def userComplianceStatus():
    conn = db_connection()
    cursor = conn.cursor()

    new_user_id = request.json['user_id']
    new_compliance_status_code = request.json['compliance_status_code']

    sql = """INSERT INTO userComplianceStatus (user_id,compliance_status_code) VALUES(?,?)"""
        
    cursor = cursor.execute(sql, (new_user_id,new_compliance_status_code))
        
    
    conn.commit()     
    return f"User Compliance Status with the id: {cursor.lastrowid} created successfully",201


@app.route('/usercompliancestatus/<int:id>', methods=['GET','PUT'])
def getUserComplianceStatus(id):
    conn = db_connection()
    cursor = conn.cursor()

    complianceStatus = None

    if request.method == 'GET':
        cursor = cursor.execute("SELECT * FROM userComplianceStatus WHERE user_id=?", (id,))
        rows = cursor.fetchall()
        for r in rows:
           complianceStatus = r
        if complianceStatus is not None:
              return jsonify(complianceStatus), 200
        else:
            return "Something went wrong", 404

    
    if request.method == 'PUT':
        sql ="""UPDATE userComplianceStatus SET compliance_status_code=?  WHERE user_id=?"""

            
        new_compliance_status_code = request.json['compliance_status_code']
        
        updated_user_compliance = {
                    'user_id': id,
                    'compliance_status_code': new_compliance_status_code
                }
        conn.execute(sql,(new_compliance_status_code, id)) 
        conn.commit()       
        return jsonify(updated_user_compliance)

       

if __name__ == '__main__':
   app.run(debug=True)
