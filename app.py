#!/usr/bin/env python
# -*- encoding:utf8 -*-
#

__Author__  = "Yoshihiro Tanaka"
__date__    = "2014-12-15"
__version__ = "0.1.3 (Beta)"

from flask import Flask, redirect, render_template, request, url_for, send_from_directory
from werkzeug import secure_filename
application = Flask(__name__)

from wtforms import Form, BooleanField, TextField, TextAreaField, PasswordField, validators

import mysql.connector

from dataProcessing.dataProcessing import *
import os, hashlib, time

class SearchForm(Form):
    position  = TextField('Position [Ex. 1]', [validators.Length(min=1, max=15)])
    rsid      = TextField('rs [Ex. 186143557]', [validators.Length(min=1, max=15)])
    mail      = TextField('mail address', [validators.Length(min=1, max=40)])

class MySQLCursorDict(mysql.connector.cursor.MySQLCursor):
    def _row_to_python(self, rowdata, desc=None):
        row = super(MySQLCursorDict, self)._row_to_python(rowdata, desc)
        if row:
            return dict(zip(self.column_names, row))
        return None

@application.route("/", methods=['GET', 'POST'])
def index():
    mes = False
    mes = request.args.get('mes')
    form = SearchForm(request.form)
    if request.method == 'POST':
        if request.form['position']:
            return redirect(url_for('result', pos=form.position.data))
        elif request.form['rsid']:
            return redirect(url_for('result', rsid=form.rsid.data))

    return render_template('index.html', 
                            form = [form, mes])

@application.route("/result", methods=['GET', 'POST'])
def result():
    form = SearchForm(request.form)
    if request.method == 'POST':
        if request.form['position']:
            return redirect(url_for('result', pos=form.position.data))
        elif request.form['rsid']:
            return redirect(url_for('result', rsid=form.rsid.data))

    dataDict = {}
    perDict  = {}
    rsid = request.args.getlist('rsid')
    pos  = request.args.getlist('pos')

    idList = []
    if len(rsid) != 0:
        rsid = rsid[0]
        if "rs" not in rsid:
            rsid = "rs"+str(rsid)
        target = ["id",rsid]
    elif len(pos) != 0:
        pos = pos[0]
        target = ["pos",pos]

    err = 0
    try:
        conDict  = {}
        infoDict = {}
        cursor = connect.cursor(cursor_class=MySQLCursorDict)
        cursor.execute('select * from main where ' + target[0] + '="' + str(target[1]) + '"', ())
        rows = cursor.fetchall()[0]
        cursor.close()
        for k, v in rows.items():
            if k == "info":
                conStr = v
            else:
                infoDict[k] = v
        setList, dataDict  = toList(conStr)
        if target[0] == "pos":
            pingDict  = {}
        else:
            pingDict  = links(str(rsid))
        spcDict   = changeSPC(1, dataDict)
        stackList = changeSPC(2, dataDict)
    except Exception as e:
        print e
        return redirect(url_for('index', mes=True))

    markerList = setMarkers(dataDict)
    ref = infoDict["REF"]
    alt = infoDict["ALT"].split(",")

    alleles = []
    for gts in setList:
        allele = []
        gt = [int(r) for r in gts.split("|")]
        print gt
        for r in gt:
            if   r == 0:
                allele.append(ref)
            else:
                allele.append(alt[r-1])
        alleles.append("|".join(allele).encode('utf-8'))

    print spcDict
    print stackList

    #allele = [
    #        ref + "|" + ref,
    #        alt + "|" + alt,
    #        ref + "|" + alt,
    #        "-|-",
    #        "ALL"
    #        ]

    country = createList(3)

    return render_template("result.html",
                           items = [
                                    dataDict,
                                    alleles,
                                    country,
                                    markerList,
                                    stackList
                                   ],
                           form = form,
                           info = [
                                    infoDict,
                                    pingDict
                                   ],
                           spc  = spcDict)

@application.route("/pred", methods=['GET', 'POST'])
def prediction():
    return render_template('pred.html', err = -1)

@application.route("/upload", methods=['POST'])
def upload():
    data = request.files['data']
    form = SearchForm(request.form)
    if request.method == 'POST' and request.form['mail']:
        if data and data.filename.split('.')[-1] in ['txt', 'TXT']:
            filename = secure_filename(data.filename)
            sha = hashlib.sha224(str(time.time())).hexdigest()
            filepath = "uploads/" + sha
            data.save(filepath)
            with open('uploads/' + sha + '.log', "w") as f:
                f.write(form.mail.data)

        #spcDict = samplePrediction("spc", filepath)
        #pCode   = spcDict["RESULT"]
        #print pCode
        #pcDict  = samplePrediction(pCode.lower(), filepath)
        #print pcDict
            os.system('nohup python samplePrediction/samplePrediction.py "' + sha + '" > /dev/null 2> log/' + sha + '.log &')
            return render_template('pred.html', err = 0)
    return render_template('pred.html', err = 1)

@application.route('/presult/<sha>')
def showResult(sha):
    return render_template('presult/' + sha + '.html')

@application.route("/index")
def returnIndex():
    return redirect(url_for('index'))    

if __name__ == "__main__":
    connect = mysql.connector.connect(
        user     ='xxx',
        password ='xxx',
        host     ='127.0.0.1',
        database ='xxx',
        charset  ='utf8')
    application.run(host="xxx", debug=True)
