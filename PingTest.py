#!/usr/bin/env python3

from flask import Flask, render_template, request, redirect
from utils import DoPing
from tinydb import TinyDB, Query


app = Flask(__name__)


@app.route('/')
def index():
    db = TinyDB('ips.json')
    ips = db.all()
    db.close()
    if len(ips) != 0:
        targets = [i['ip'] for i in ips]
        results = DoPing(targets)
        addrs = []
        rtts =[]
        for addr, rtt in results.items():
            addrs.append(addr)
            rtts.append(rtt)
        
        # if len(addrs) == 1:
        #     addrs = '["'+addrs[0]+'"]'
        # else:
        #     temp = addrs
        #     addrs = '[' + "".join(['"'+i+'",' for i in temp[:-1]])
        #     addrs += '"'+temp[-1]+'"]'
        print(addrs)
        print(rtts)
        return render_template("index.html", addrs="#".join(addrs), rtts=str(rtts))
    else:
        return render_template("index.html", addrs='没有', rtts=[12])

@app.route('/add', methods=['POST'])
def postadd():
    ip = request.form['addip']
    db = TinyDB('ips.json')
    db.insert({'ip':ip})
    db.close()
    print(db)
    return redirect('/')

if __name__ == "__main__":
    app.run()


