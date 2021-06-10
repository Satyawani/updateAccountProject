from pymysql import *

def dbfun():
    global cn
    cn = connect(host="localhost", user="root", passwd="tiger", db="nproject")
    c = cn.cursor()
    return cn,c

