from flask import Blueprint, render_template, request, redirect, url_for
from flask.wrappers import Request
import time
import operator

views = Blueprint(__name__, 'views')

chartdata = {"A":0, "B":0, "C":0, "D":0}

order_index = 0

class order:
    def __init__(self, order_no, meal_set, take_time, method):
        self.order_no = order_no
        self.meal_set = meal_set
        self.take_time = take_time
        self.method = method

order_list = []


def timestr(tm):
    return str(time.localtime(tm).tm_hour).zfill(2)+":"+str(time.localtime(tm).tm_min).zfill(2)+":"+str(time.localtime(tm).tm_sec).zfill(2)

@views.route('/')
def index():
    title = "Home"
    return render_template('index.html', title = title)

@views.route('/mc', methods=["GET"])
def mc():
    title = "Multiple choice"
    return render_template('mc.html', title = title)

@views.route('/form', methods=["POST","GET"])
def form():
    title = "FORM"
    global chartdata
    mcinput = request.form.get("mcinput")
    if mcinput:
        chartdata[mcinput] += 1
    print(chartdata)
    return render_template('form.html', title = title, mcinput=mcinput)

@views.route('/result', methods=["GET","POST"])
def result():
    title = "RESULT"
    global chartdata
    A = chartdata["A"]
    B = chartdata["B"]
    C = chartdata["C"]
    D = chartdata["D"]
    reset = "False"
    reset = request.form.get("reset")
    if reset == "True":
        chartdata = {"A":0, "B":0, "C":0, "D":0}
        print(chartdata)
        reset = "False"
    return render_template('result.html', title = title, A=A, B=B, C=C, D=D)


@views.route('/app', methods=["POST","GET"])
def app():
    title = "App"
    size = len(order_list)
    return render_template('app.html', title = title, size=size)

@views.route('/kiosk', methods=["POST","GET"])
def kiosk():
    title = "Kiosk"
    return render_template('kiosk.html', title = title)

@views.route('/order_no', methods=["POST","GET"])
def order_no():
    title = "order_no"
    global order_list
    global order_index

    order_index += 1
    mcinput = request.form.get("mcinput")
    method = request.form.get("method")
    
    take_time = time.time()+int(request.form.get("arr_time"))*60
    order_list.append(order(order_index+100, mcinput, take_time, method))
    return render_template('order_no.html', title = title, mcinput=mcinput, order=order_index+100, method=method, taketime=timestr(take_time))

@views.route('/monitor', methods=["POST","GET"])
def monitor():
    title = "monitor"
    shown_no1 = []
    shown_no2 = []
    order_list.sort(key=operator.attrgetter('take_time'))
    for i in order_list:
        if i.take_time+30 < time.time():
            shown_no1.append(i.order_no)
        else:
            shown_no2.append(i.order_no)
    return render_template("monitor.html", title=title, shown_no1=shown_no1, shown_no2=shown_no2)

@views.route('/server', methods=["POST","GET"])
def server():
    title = "server"
    shown_no = []
    order_list.sort(key=operator.attrgetter('take_time'))

    for i in order_list:
        shown_no.append([i.order_no, i.meal_set, i.method, timestr(i.take_time)])

    reset = "False"
    reset = request.form.get("reset")
    if reset == "True":
        order_list.clear()
        reset = "False"
    return render_template("server.html", title=title, data=shown_no)

@views.route('/user', methods=["POST","GET"])
def user():
    title = "User"
    return render_template('user.html', title = title)

@views.route('/userchanged', methods=["POST","GET"])
def userchanged():
    title = "Changed"
    order_no1 = int(request.form.get("order_no"))
    take_time1 = time.time()+int(request.form.get("arr_time"))*60
    meal_set = "NULL"
    order_no2 = str(order_no1)+" cannot found"
    method = "NULL"
    take_time = "NULL"

    for i in order_list:
        if i.order_no == order_no1:
            i.take_time = take_time1
            take_time = timestr(take_time1)
            meal_set = i.meal_set
            method = i.method
            order_no2 = i.order_no
            break

    return render_template('userchanged.html', title = title, mcinput=meal_set, order=order_no2, method=method, taketime=take_time)
    
@views.route('/staff_monitor', methods=["POST","GET"])
def staff_monitor():
    title = "For staff only"
    shown_no = []
    #order_list.sort(key=operator.attrgetter('take_time'))
    #j = 0
    # for i in order_list:
    #     if j < 20:
    #         shown_no.append([i.order_no, i.meal_set, i.method, timestr(i.take_time)])
    #     j = j+1
    shown_no.append([113, "Big Mac Pro", "app", timestr(1683172800+16*60)])

    shown_no.append([112, "Big Mac Plus", "app", timestr(1683172800+20*60)])


    reset = "False"
    reset = request.form.get("reset")
    if reset == "True":
        order_list.clear()
        reset = "False"
    return render_template("staff_monitor.html", title=title, data=shown_no)


@views.route('/app_1', methods=["POST","GET"])
def app_1():
    title = "App"
    size = len(order_list)
    return render_template('app_1.html', title = title, size=size)

@views.route('/new_order_no', methods=["POST","GET"])
def new_order_no():
    title = "order_no"
    global order_list
    global order_index

    order_index += 1
    mcinput = request.form.get("mcinput")
    method = "app"
    
    take_time = time.time()+int(request.form.get("arr_time"))*60
    order_list.append(order(order_index+100, mcinput, take_time, method))
    return render_template('new_order_no.html', title = title, mcinput=mcinput, order=order_index+100, method=method, taketime=timestr(take_time+300))

@views.route('/user_1', methods=["POST","GET"])
def user_1():
    title = "Modify Arrival Time"
    return render_template('user_1.html', title = title)

@views.route('/userchanged_1', methods=["POST","GET"])
def userchanged_1():
    title = "Changed"
    order_no1 = int(request.form.get("order_no"))
    take_time1 = time.time()+int(request.form.get("arr_time"))*60
    meal_set = 'NULL'
    order_no2 = str(order_no1)+" cannot found"
    method = "NULL"
    take_time = "NULL"

    for i in order_list:
        if i.order_no == order_no1:
            i.take_time = take_time1
            #i.meal_set = meal_set
            take_time = timestr(take_time1)
            method = i.method
            order_no2 = i.order_no
            meal_set = i.meal_set
            break

    return render_template('userchanged_1.html', title = title, mcinput=meal_set, order=order_no2, method=method, taketime=take_time)

@views.route('/monitor_3', methods=["POST","GET"])
def monitor_3():
    title = "monitor"
    shown_no1 = []
    shown_no2 = []
    order_list.sort(key=operator.attrgetter('take_time'))
    for i in order_list:
        if i.take_time+30 < time.time():
            shown_no1.append(i.order_no)
        elif i.take_time < time.time()+30*60:
            shown_no2.append(i.order_no)
    
    shown_no1 = [112]
    shown_no2 = []
    return render_template("monitor_3.html", title=title, shown_no1=shown_no1, shown_no2=shown_no2)