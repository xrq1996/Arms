# coding:utf-8

import sqlite3
import time
import unit
import datetime
import threading
R = threading.Lock()

def data_creat():
    try:
        conn = sqlite3.connect('logs.db')
        cursor = conn.cursor()
        cursor.execute("create table domaintable(ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,domain TEXT,is_crawl Int DEFAULT 0, status Int DEFAULT 0,add_time datetime,des TEXT DEFAULT '',title TEXT DEFAULT '',steps Int DEFAULT 0)")
        cursor.close()
        conn.commit()
        conn.close()
        return True
    except:
        return False

def data_select(domain):
    try:
        R.acquire()
        conn = sqlite3.connect("logs.db")
        cursor = conn.cursor()
        configsql = "select * from domaintable where  domain = '%s' " % domain
        cursor.execute(configsql)
        configmodel = cursor.fetchone()
        R.release()
        if configmodel:
            return True
        else:
            return False
    except:
        return None

def data_insert(domain):
    try:
        #R.acquire()
        conn = sqlite3.connect('logs.db')
        cursor = conn.cursor()
        domain = domain
        conn.execute("insert or ignore into domaintable (domain) values ('" + domain + "')")
        cursor.close()
        conn.commit()
        #R.release()
        conn.close()
        return True
    except:
        return False

def data_getlist(where):
    R.acquire()
    try:
        conn = sqlite3.connect("logs.db")
        cursor = conn.cursor()
        configsql = "select * from domaintable where %s" % where
        cursor.execute(configsql)
        list = cursor.fetchall()
        for data in list:
            cursor.execute("update domaintable set is_crawl = 1 where id ="+ str(data[0]))
            conn.commit()
        cursor.close()
        conn.close()
        R.release()
        return list
    except Exception as e:
        try:
            conn.close()
        except Exception as e:
            pass
        try:
            cursor.close()
        except Exception as e:
            pass
        print(e)
        R.release()
        return False

def start_getlist(where):
    R.acquire()
    try:
        conn = sqlite3.connect("logs.db")
        cursor = conn.cursor()
        configsql = "select * from domaintable where %s" % where
        cursor.execute(configsql)
        list = cursor.fetchone()
        R.release()
        return list
    except Exception as e:
        print(e)
        R.release()
        return False

def data_update(doamin, sqlstr):
    R.acquire()
    try:
        conn = sqlite3.connect("logs.db")
        cursor = conn.cursor()
        cursor.execute("update domaintable set %s where domain ='%s' "% (sqlstr,doamin))
        conn.commit()
        cursor.close()
        conn.close()
        R.release()
        return False
    except Exception as e:
        print(e)
        R.release()
        return False


def logs_insert(self, current_domain, uri):
    try:
        conn = sqlite3.connect('logs.db')
        cursor = conn.cursor()
        cursor.execute(
            "create table logstable(ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,current_domain TEXT, uri TEXT,add_time TEXT)")
        current_domain = current_domain
        uri = uri
        vla = (1, current_domain, uri)
        sql2 = "insert into logstable values(?,?,?);"
        cursor.execute(sql2, vla)
        cursor.close()
        conn.commit()
        conn.close()
        return 1
    except:
        conn = sqlite3.connect('logs.db')
        cursor = conn.cursor()
        current_domain = current_domain
        uri = uri
        add_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn.execute(
            "insert into logstable(current_domain,uri,add_time) values ('" + current_domain + "', '" + uri + "','" + add_time + "')")
        cursor.close()
        conn.commit()
        conn.close()
        return 0


def logs_search(self, current_domain, uri):
    try:
        conn = sqlite3.connect("logs.db")
        cursor = conn.cursor()
        configsql = "select * from logstable where current_domain = '%s' and uri = '%s'" % (current_domain, uri)
        cursor.execute(configsql)
        configmodel = cursor.fetchone()
        if configmodel:
            return True
        else:
            return False
    except:
        return False
