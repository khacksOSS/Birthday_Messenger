# imports necessary for functionality
import requests
import psycopg2 as pg
def make_api_list(user_number,message,api_username,api_password):
    # list of api we are using may change in futher also
    api_list = ["https://enterprise.smsgupshup.com/GatewayAPI/rest?method=SendMessage&send_to="+str(user_number)+"&msg="+message+"&msg_type=TEXT&userid="+api_username+"&auth_scheme=plain&password="+api_password+"&v=1.1&format=text"]
    return api_list

# reading the config file
file = open("creden.config",'r')
text = file.readlines()
d={}
for j in text:
    if j[0] != "#":
        l=j.split(' = ')
        if len(l)==2:
            d[l[0].strip()]=l[1].strip()
api_id,user,password,host,port,database= d['api_id'],d['user'],d['password'],d['host'],d['port'],d['database']
api_username,api_password = d['api_username'],d['api_password']
del d



# Creating a Session for the Api Request 
sess = requests.Session()


# Connect to the Database
connection = pg.connect(user=user,
                        password=password,
                        host=host,
                        port=port,
                        database=database)

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
    req = make_api_list(user_number,message, api_username,api_password)[int(api_id)]
    a = sess.get(req)        
    sql1 = "insert into log(date,time,regno,name,status,phone_no) values(current_date"\
                ",current_time,'%s','%s','%s','%s')"%(str(details[i][1]), str(details[i][0]),\
                str(a.content.split()[0]).replace("b","")[1:-1],details[i][4])
    cur.execute(sql1)


connection.commit()
connection.close()