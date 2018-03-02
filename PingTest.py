#!/usr/bin/env python3

from flask import Flask, render_template, request, redirect
from utils import DoPing
from tinydb import TinyDB, Query
from socket import gethostbyname

app = Flask(__name__)


@app.route('/')
def index():
    db = TinyDB('ips.json')
    ips = db.all()
    db.close()
    if len(ips) != 0:
        targets = [i['target'] for i in ips]
        results = DoPing(targets)
        addrs = []
        rtts =[]
        names = []
        print(ips)
        for addr, rtt in results.items():
            addrs.append(addr)
            rtts.append(rtt)
        for addr in addrs:
            for i in ips:
                if  i["target"] == addr:
                    names.append(i["name"])
        # if len(addrs) == 1:
        #     addrs = '["'+addrs[0]+'"]'
        # else:
        #     temp = addrs
        #     addrs = '[' + "".join(['"'+i+'",' for i in temp[:-1]])
        #     addrs += '"'+temp[-1]+'"]'
        print(addrs)
        print(names)
        print(rtts)
        return render_template("index.html", addrs="#".join(names), rtts=str(rtts))
    else:
        return render_template("index.html", addrs='没有', rtts=[12])

@app.route('/add', methods=['POST'])
def postadd():
    ip = request.form['addip']
    name = request.form['name']
    db = TinyDB('ips.json')
    Target = Query()
    sd = db.search(Target.name  == name)
    if len(sd) == 0:
        db.insert({'target':ip, 'name':name})
        db.close()
    return redirect('/')

if __name__ == "__main__":
    app.run()


