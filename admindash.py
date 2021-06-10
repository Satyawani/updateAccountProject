from dbasefile import *
def adash():
    cn,cur = dbfun()
    cur.execute("select count(Active) from rule where Active=1")
    for i in cur:
        alen = i[0]
    cur.execute("select count(Active) from rule where Active=0")
    for i in cur:
        delen = i[0]
    cur.execute("select count(Active) from rule")
    for i in cur:
        tlen = i[0]

    a = []
    cur.execute('desc rule')
    for i in cur:
        a.append(i[0])

    rq1 = " select * from rule"
    cur.execute(rq1)

    rcont = []
    for i in cur:
        rcont.append(i)

    cn.commit()
    cn.close()
    return alen, delen, tlen, a, rcont

def rulenamef():
    cn,cur = dbfun()
    cur.execute('select RuleName  from rule')
    a1 = ['Select the Rulename']
    for i in cur:
        a1.append(i[0])
    return a1

