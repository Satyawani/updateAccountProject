from flask import Flask, render_template, request, jsonify
from admindash import *
from dbasefile import *
from datetime import *
from pymysql import *
import sqlite3

app = Flask(__name__, template_folder='templates')
app.static_folder = 'static'
app.template_folder = "templates"

th = (
    "Invoice_No", "d_date", "c_supp_code", "c_name", "n_taxable_amt", "c_bill_no", "n_total", "c_br_code",
    "c_item_code",
    "act_name", "c_cat_code", "itm_name", "c_mfac_code", "manu_name", "n_qty", "n_sch_qty", "n_mrp", "n_pur_rate",
    "n_eff_pur_rate")

def timedatef():
    now = str(date.today())
    dtime = datetime.now()
    time2 = dtime.strftime("%H:%M:%S")
    return now, time2, dtime
def adminconfig():
    rn = request.form.get('id_rulename')
    rdis = request.form.get('id_dis')
    rflat = request.form.get('id_flat')
    rqty = request.form.get('id_qty')
    ramt = request.form.get('id_amt')
    rtrans = request.form.get('id_trans')
    rbranch = request.form.get('id_branch')
    rbrand = request.form.get('id_brand')
    rmanu = request.form.get('id_manu')
    rsupp = request.form.get('id_supplier')
    rcate = request.form.get('id_category')
    rprod = request.form.get('id_product')
    rstatus = request.form.get('rstatus')
    rfreq = request.form.get('rf')
    rprice = request.form.get("gender12")
    rstart=request.form.get('rstartdate')
    cn,cur = dbfun()
    a, b, rcreate = timedatef()
    adq = f"insert into rule(RuleName,Active,TransType,FromDate,ToDate,BranchCode,BrandCode,ProductCode,ManufCode,SupplierCode,CategoryCode,QtyThreshold,ValueThreshold,Frequency,StartDate,PriceType,Discount,FlatPrice,createdate) values('{rn}',{rstatus},'{rtrans}',Null,null,'{rbranch}','{rbrand}','{rprod}','{rmanu}','{rsupp}','{rcate}',{rqty},{ramt},{rfreq},'{rstart}',{rprice},{rdis},{rflat},'{rcreate}')"
    cur.execute(adq)

    cn.commit()

    cn.close()


def rulemodify():
    sl = request.form.get("id_selected")
    endis = request.form.get("rm")
    sqrm = f"update rule set Active={endis} where rulename='{sl}'"
    cn,cur = dbfun()
    cur.execute(sqrm)
    cn.commit()
    cn.close()


def fetchdata():
    global qt,dt
    qt = []
    dt = []
    cn,cur=dbfun()
    print(rbrand,rmanu,rsupp,rcate)
    if rbrand != "All" and rmanu != 'All' and rsupp != 'All' and rcate != 'All':
        print('')
        a = f"select sum(n_qty),sum(n_mrp),sum(n_eff_pur_rate) from livedata where c_brand='{rbrand}' and  c_mfac_code='{rmanu}' and  c_cat_code='{rcate}' and c_supp_code='{rsupp}'"
        cur.execute(a)
        for i in cur:
            for j in i:
                qt.append(j)

        b = f" select * from livedata where c_brand='{rbrand}' and  c_mfac_code='{rmanu}' and  c_cat_code='{rcate}' and c_supp_code='{rsupp}'"

        cur.execute(b)
        for i in cur:
            for j in i:
                dt.append(j)

        mq4 = f"insert into rulelog(uid,rid,rulename,rtime,fromdate,todate,mrptax,effrate ) values('{uname}','{rid[0]}','{rn}','{ctime}','{sdate}','{edate}',{qt[1]},{qt[2]})"
        cur.execute(mq4)
        cn.commit()



    elif rbrand != "All" and rmanu != 'All' and rsupp != 'All' and rcate == 'All':
        a = f"select sum(n_qty),sum(n_mrp),sum(n_eff_pur_rate) from livedata where c_brand='{rbrand}' and  c_mfac_code='{rmanu}' and c_supp_code='{rsupp}' "
        cur.execute(a)
        for i in cur:
            for j in i:
                qt.append(j)

        b = f"select * from livedata where c_brand='{rbrand}' and  c_mfac_code='{rmanu}' and c_supp_code='{rsupp}' "
        cur.execute(b)
        for i in cur:
            for j in i:
                dt.append(j)

        mq4 = f"insert into rulelog(uid,rid,rulename,rtime,fromdate,todate,mrptax,effrate ) values('{uname}','{rid[0]}','{rn}','{ctime}','{sdate}','{edate}',{qt[1]},{qt[2]})"
        cur.execute(mq4)
        cn.commit()


    elif rbrand != "All" and rmanu != 'All' and rsupp == 'All' and rcate == 'All':
        a = f"select sum(n_qty),sum(n_mrp),sum(n_eff_pur_rate) from livedata where c_brand='{rbrand}' and  c_mfac_code='{rmanu}' "
        cur.execute(a)
        for i in cur:
            for j in i:
                qt.append(j)

        b = f"select *  from livedata where c_brand='{rbrand}' and  c_mfac_code='{rmanu}' "
        cur.execute(b)
        for i in cur:
            for j in i:
                dt.append(j)

        mq4 = f"insert into rulelog(uid,rid,rulename,rtime,fromdate,todate,mrptax,effrate ) values('{uname}','{rid[0]}','{rn}','{ctime}','{sdate}','{edate}',{qt[1]},{qt[2]})"
        cur.execute(mq4)
        cn.commit()

    elif rbrand != "All" and rmanu == 'All' and rsupp == 'All' and rcate == 'All':
        a = f"select sum(n_qty),sum(n_mrp),sum(n_eff_pur_rate) from livedata where c_brand='{rbrand}' "
        cur.execute(a)
        for i in cur:
            for j in i:
                qt.append(j)

        b = f"select * from livedata where c_brand='{rbrand}' "
        cur.execute(b)
        for i in cur:
            for j in i:
                dt.append(j)

        mq4 = f"insert into rulelog(uid,rid,rulename,rtime,fromdate,todate,mrptax,effrate ) values('{uname}','{rid[0]}','{rn}','{ctime}','{sdate}','{edate}',{qt[1]},{qt[2]})"
        cur.execute(mq4)
        cn.commit()

    elif rbrand == "All" and rmanu != 'All' and rsupp == 'All' and rcate == 'All':

        a = f"select sum(n_qty),sum(n_mrp),sum(n_eff_pur_rate) from reckitttable where c_mfac_code='{rmanu}' "
        cur.execute(a)
        for i in cur:
            for j in i:
                qt.append(j)

        b = f"select * from reckitttable where  c_mfac_code='{rmanu}' "
        cur.execute(b)
        dt=cur.fetchall()
        print(dt)
        mq4 = f"insert into rulelog(uid,rid,rulename,rtime,fromdate,todate,mrptax,effrate ) values('{uname}','{rid[0]}','{rn}','{ctime}','{sdate}','{edate}',{qt[1]},{qt[2]})"
        print("instered data",mq4)
        cur.execute(mq4)
        cn.commit()

    else:
        print('not support')
    return dt,qt

def fun12():
    global rprod,rsupp,rmanu,rbrand,rcate,rn,ctime,sdate,edate, rid,dt,qt,msg
    sdate=request.form.get('id_sdate')
    edate=request.form.get('id_edate')
    rn = request.form.get('id_selected')
    rdis = request.form.get('id_dis')
    rflat = request.form.get('id_flat')
    rqty = request.form.get('id_qty')
    ramt = request.form.get('id_amt12')
    rtrans = request.form.get('id_trans')
    rbranch = request.form.get('id_branch')
    rbrand = request.form.get('id_brand')
    rmanu = request.form.get('id_manu')
    rsupp = request.form.get('id_supp')
    rcate = request.form.get('id_cate')
    rprod = request.form.get('id_prod')
    rfreq = request.form.get('id_freq')
    rprice = request.form.get("id_price")
    rstart=request.form.get("id_start")

    print(rstart,type(rstart))
    rstart= datetime.strptime(rstart, '"%Y-%m-%d"')
    rfrom=request.form.get('id_sdate')
    rto=request.form.get('id_edate')
    print(rfrom,rto)





    ctime = datetime.now()
    ntime = str(datetime.today() + timedelta(days=30))

    mq1 = f"update rule set FromDate='{sdate}', ToDate='{edate}' where rulename='{rn}'"
    mq2 = f"select id,QtyThreshold,ValueThreshold from rule where rulename='{rn}'"

    print(mq1)
    print(mq2)
    cn,cur = dbfun()
    cur.execute(mq1)
    cur.execute(mq2)

    rid = []
    for i in cur:
        for j in i:
            rid.append(j)
    print(rfreq,rid)

    if rfreq == 'Monthly':
        cdate = datetime.today()

        delta = cdate - rstart
        dt,qt=fetchdata()
        print(delta,cdate,rstart)
        if delta == 30:
            pass
        else:
            msg = f"Still {30-delta.days}  more days  r there to pass the DC  note  "

    elif rfreq =='Quarterly':
        cdate = datetime.today()
        delta = cdate - rstart
        dt,qt=fetchdata()
        print(dt, qt)
        if delta == 90:
            pass
        else:
            msg = f"Still {delta}  more days  r there to pass the DC  note  "

    elif rfreq == 'Yearly':
        cdate = datetime.today()
        delta = cdate - rstart
        dt,qt=fetchdata()
        print(dt, qt)
        if delta == 365:
            pass
        else:
            msg= f"Still {delta}  more days  r there to pass the DC  note "

    else:
        pass


@app.route("/file123",methods=["POST","GET"])
def ajaxlivesearch():
    alen, delen, tlen, rh, rcont = adash()
    cn,cur=dbfun()
    if request.method == 'POST':
        query = "SELECT * from  rule where Active=1"
        cur.execute(query)
        numrows = int(cur.rowcount)
        employee = cur.fetchall()
        print(employee[0])
        print('no data',numrows)
        emplo=employee[0]
        return jsonify({'htmlresponse': render_template('activehtml.html', employee=employee, numrows=numrows,rh=rh)})


@app.route('/ruleform')
def hello_world1():
    return render_template("ruleform.html")

@app.route('/signup')
def hello_world3():
    return render_template("signuppage.html")

@app.route('/uform')
def hello_world12():
    return render_template("uform.html")

@app.route('/admindash')
def hello_world4():
    global rh
    alen, delen, tlen, rh, rcont = adash()

    return render_template('admindash.html', alen=alen, delen=delen, tlen=tlen, rh=rh, rcont=rcont)
@app.route('/uf', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        fun12()

        return render_template('table1.html' , th=th, tqty=qt[0], tamt=qt[1], ruid=rid[0], thrqty=rid[1],
                               thramt=rid[2], rqty=5000 - qt[0], ramt=rid[1] - qt[1],msg=msg,dt=dt)


@app.route('/rulemodify')
def hello_world2():
    cn,cur = dbfun()
    cur.execute('select RuleName  from rule')
    a = ['Select the Rulename']
    for i in cur:
        a.append(i[0])

    return render_template("rulemodify.html", rname=a)

@app.route('/alogin', methods=['POST', 'GET'])
def adminlogin():
    if request.method == 'POST':
        adminconfig()
        alen, delen, tlen, rh, rcont = adash()

        return render_template('admindash.html', alen=alen, delen=delen, tlen=tlen, rh=rh, rcont=rcont)


@app.route('/rulem', methods=['POST', 'GET'])
def rmdo():
    if request.method == 'POST':
        rulemodify()
        alen, delen, tlen, rh, rcont = adash()

        return render_template('admindash.html', alen=alen, delen=delen, tlen=tlen, rh=rh, rcont=rcont)




@app.route("/fetchrecords",methods=["POST","GET"])
def fetchrecords13():
    cn,cur = dbfun()
    if request.method == 'POST':
        query = request.form.get('query')
        print(type(query))
        if query=='Select the Rulename':

           e2=('','','','','','','','','','','','','','','','','','')


        else:
            search_text = request.form['query']
            print(search_text)
            cur.execute(f"SELECT * FROM  rule where rulename='{search_text}'")
            employeelist = cur.fetchall()
            print(employeelist)
            employeelist=list(employeelist[0])
            employeelist[15]=str(employeelist[15])
            print(type(employeelist[15]))
            e2=employeelist
    return jsonify(e2)

@app.route('/signup', methods=['POST', 'GET'])
def signup1():
    if request.method == 'POST':
        cn, cur = dbfun()
        global uname
        email=request.form.get('email_id')
        uname = request.form.get('uname')
        passw = request.form.get('upassd')


        q1 = f"insert into userdetail(uname,passd,email) values('{uname}','{passw}','{email}')"
        cur.execute(q1)
        cn.commit()
        cn.close()

        return render_template('index.html')


@app.route('/form', methods=['POST', 'GET'])
def fuct():
    if request.method == 'POST':
        cn,cur = dbfun()
        global uname
        uname = request.form.get('uname')
        passw = request.form.get('pname')
        if uname=='admin':

            q1 = f"select * from userdetail where uname='{uname}' and passd='{passw}'"
            b = cur.execute(q1)
            print(b)

            if b == 1:
                alen, delen, tlen, rh, rcont = adash()
                return render_template('admindash.html', alen=alen, delen=delen, tlen=tlen, rh=rh, rcont=rcont)
            else:
                return render_template('index.html')
        else:
            q1 = f"select * from userdetail where uname='{uname}' and passd='{passw}'"
            b = cur.execute(q1)
            a = rulenamef()

            if b == 1:
                return render_template('uform.html',rname=a)
            else:
                return render_template('index.html')


@app.route('/')
def hello_world():
    return render_template("index.html")


if __name__ == '__main__':
    app.run()
