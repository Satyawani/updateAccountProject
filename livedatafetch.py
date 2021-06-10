from apscheduler.schedulers.background import BackgroundScheduler
from pymysql import *
import pyodbc
from datetime import *
cn = connect(host="localhost", user="root", passwd="tiger", db="nproject")
c = cn.cursor()


host = "UAT_04m00021_cl"
database = "04M00021"
username = "data"
password = "D@1@<>3"

print("DB CONNECT ATTEMPT")
sq1 = "SELECT d.c_br_code+'/'+d.c_year+'/'+d.c_prefix+'/'+string(d.n_srno) as Invoice_No,d.d_date,d.c_supp_code,a.c_name,p.n_taxable_amt,p.c_bill_no,p.n_total,d.c_br_code,d.c_item_code,m.c_name,m.c_cat_code,c.c_name,m.c_mfac_code,f.c_name, d.n_qty,d.n_sch_qty,d.n_mrp,d.n_pur_rate,d.n_eff_pur_rate FROM dba.pur_det d inner join dba.Item_mst m on m.c_code = d.c_item_code inner join dba.pur_mst p on d.c_br_code = p.c_br_code and d.c_year=p.c_year and d.c_prefix=p.c_prefix and d.n_srno=p.n_srno left join dba.mfac_mst f on f.c_code =m.c_mfac_code left join dba.Item_category_mst c on c.c_code =m.c_cat_code left join dba.act_mst a on d.c_supp_code =a.c_code"
sq2 = "insert into livedata(Invoice_No,d_date,c_supp_code,c_name,n_taxable_amt,c_bill_no,n_total,c_br_code,c_item_code,act_name,c_cat_code,itm_name,c_mfac_code,manu_name,n_qty,n_sch_qty,n_mrp,n_pur_rate,n_eff_pur_rate) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"


def timedatef():
    now = str(date.today())
    time1 = datetime.now()
    global ntime
    ntime = str(date.today() + timedelta(days=7))
    time2 = time1.strftime("%H:%M:%S")
    return time1, ntime


def ldata():
    e = []
    cs = 'DSN=%s;UID=%s;PWD=%s;DATABASE=%s;' % (host, username, password, database)
    cnxn = pyodbc.connect(cs)
    print(cnxn)
    cur = cnxn.cursor()
    cur.execute(sq1)
    #  cur.execute("select top 1 * from item_mst")

    for i in cur:
        l = []

        for j in range(19):
            if j == 1:
                l.append(str(i[j]))
            elif j == 4 or j == 6 or j == 14 or j == 15 or j == 16 or j == 17 or j == 18:
                l.append(float(i[j]))
            else:
                l.append(i[j])

        e.append(tuple(l))

    cnxn.commit()
    cnxn.close()
    print(len(e))
    c.executemany(sq2, e)
    cn.commit()
    cn.close()



ldata()
'''if __name__ == '__main__':
    try:
        sched = BackgroundScheduler()
        sched.start()
        sched.add_job(ldata, 'interval', hours=10)
        input("Press enter to exit.")
        sched.shutdown()
    except Exception as e:
        print("Error: " + str(e))'''
