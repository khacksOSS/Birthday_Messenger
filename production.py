# imports necessary for functionality
import requests
import psycopg2 as pg

# Creating a Session for the Api Request 
sess = requests.Session()

# IMPORTANT : mention the Authentication credentials for gupshup api
# In future it may change
userid = "#####"
password = "#####"

# Connect to the Database
connection = pg.connect(user="#####",
                        password="####",
                        host="#.#.#.#",
                        port="####",
                        database="####")

# Create the cursor to execute statements 
cur = connection.cursor()

# The Following code is required to fetch the details of the birthday on current day
sql1 = "select * from student where date_part('day', current_date) = date_part('day', dob)"\
           "and date_part('month', current_date) = date_part('month', dob);"

# Execute and store it
cur.execute(sql1)
details = cur.fetchall()

# The Loop is for sending message to everyone on particular day 
for i in range(len(details)):
    user_number=details[i][4]
    message = "Happy Birthday, dear "+ details[i][0]+'.\n\n'+ "May God bless you abundantly and "\
        "make you a blessing for many. \n"+"With wishes and prayers,\n\n"+"From Karunya Family." 
    
    # requesting to gupshup for sending messages
    req = "https://enterprise.smsgupshup.com/GatewayAPI/rest?method=SendMessage&send_to="\
        +str(user_number)+"&msg="+message+"&msg_type=TEXT&userid="+userid+"&auth_scheme="\
        "plain&password="+password+"&v=1.1&format=text"
    a = sess.get(req)        
    sql1 = "insert into log(date,time,regno,name,status,phone_no) values(current_date"\
                ",current_time,'%s','%s','%s','%s')"%(str(details[i][1]), str(details[i][0]),\
                str(a.content.split()[0]).replace("b","")[1:-1],details[i][4])
    cur.execute(sql1)


connection.commit()
connection.close()

