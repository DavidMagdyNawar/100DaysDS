#!/usr/bin/python
# -*- coding: utf-8 -*- #

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import time
import re
import json
import requests
import urllib
import re
import MySQLdb
from rivescript import RiveScript
from datetime import datetime

msg = sys.argv[1]
e = sys.argv[2]
#ipaddress = sys.argv[3]

bot = RiveScript(utf8=True,debug=False)
bot.unicode_punctuation = re.compile(r'[.,!?;:]')
bot.load_directory("eg/brain")
bot.sort_replies()

def response(text):
        text = text.encode("utf-8")
        reply = bot.reply("localuser", text)
        reply_text = reply.encode("utf-8").strip()

        return reply_text

def msbot(text):
        text = text.encode("utf-8")
        host = "https://cliohk.azurewebsites.net/qnamaker"
        endpoint_key = "XXXX"

        kb = "XXXX"

        method = "/knowledgebases/" + kb + "/generateAnswer"
        question = {'question': text,'top': 1}
        content = json.dumps(question)

        headers = {'Authorization': 'EndpointKey ' + endpoint_key,'Content-Type': 'application/json','Content-Length': str(len(content))}
        r = requests.post(host + method, headers=headers, data=content, verify=False)

        #print (r)

        return r.content


def addToMySQL(sid,it,rt,rs):
	try:
		db = MySQLdb.connect(host="localhost", user="X", passwd="X", db="X", charset="utf8")
        	cursor = db.cursor()

		sql = "INSERT INTO CLTChatbotMessages (sessionid,msg,reply,score) VALUES ('" + sid + "','" + it + "','" + rt + "','" + str(rs) + "')"
	        cursor.execute(sql)
	        db.commit()
	except Exception as Error:
                print "Error=",Error
                return 400,Error
        finally:
               db.close()
	
	#insert = ("INSERT INTO Chatbot(sessionid) VALUES (%s)")
	#data = (sid)

	#cursor.execute(insert, data)
        #con.commit()
	#con.close()
	#return 1
	
def clearFailureLog(sid):
	try:
		db = MySQLdb.connect(host="localhost", user="root", passwd="Chinalife2017", db="CLIOHK", charset="utf8")
                cursor = db.cursor()

		sql = "DELETE FROM CLTChatbotFailure WHERE sessionid = '" + sid + "'"
		cursor.execute(sql)
		db.commit()
	except Exception as Error:
		print "Error=",Error
		return 400,Error
	finally:
		db.close()
		
def addToFailureCount(sid):
	try:
		db = MySQLdb.connect(host="localhost", user="root", passwd="Chinalife2017", db="CLIOHK", charset="utf8")
		cursor = db.cursor()

		sql = "INSERT INTO CLTChatbotFailure (sessionid) VALUES ('" + sid + "')"
		cursor.execute(sql)
		db.commit()
	except Exception as Error:
		print "Error=",Error
		return 400,Error
	finally:
		db.close()
		
def searchFailureCount(sid):
        try:
                import datetime
                rcount = 0

                snow = datetime.datetime.now()
                sbefore = datetime.datetime.now() - datetime.timedelta(minutes = 15)
                snext = datetime.datetime.now() + datetime.timedelta(minutes = 15)

                db = MySQLdb.connect(host="localhost", user="root", passwd="Chinalife2017", db="CLIOHK", charset="utf8")
                cursor = db.cursor()

                #print snow
                #print sbefore
                #print snext

                sql = "SELECT * FROM `CLTChatbotFailure` WHERE sessionid = '" + sid + "' AND failuredatetime BETWEEN '" + str(sbefore) + "' AND '" + str(snext) + "'"
                rcount = cursor.execute(sql)

                #print rcount

                return rcount
        except Exception as Error:
                print "Error=",Error
                return 400,Error
        finally:
                db.close()		

def main():
        input_text = msg
        input_text = input_text.encode("utf8")
	rscore = 100

        reply_text = response(input_text)

        if reply_text == "[ERR: No reply matched]":
                ms_bot_reply_text = msbot(input_text)
               #print ms_bot_reply_text

                item_dict2 = json.loads(ms_bot_reply_text)
		#print (item_dict2)
                answer = item_dict2['answers'][0]['answer']
		rscore = float(item_dict2['answers'][0]['score'])
                #print (answer)
		#print score

		if (rscore < 25):
			reply_text = "[ERR: No reply matched]"
		else:
	                reply_text = response(answer)

                #print reply_text
                if reply_text == "[ERR: No reply matched]":
			addToFailureCount(e)
			f = searchFailureCount(e)
			
			if (f < 3):
				reply_text = '{"status":1,"topic":"pepper","type":"wav","output":{"ctbuttonlist":["參加強積金計劃","供款","離職／整合帳戶／轉移強積金","申索累算權益","長期服務金／遣散費","服務"],"ctcontent":{"texts":"我很樂意為您效勞，但我無法完全理解您的問題。<br/>請問您是否想查詢以下的事情？","texte":""},"enbuttonlist":[],"encontent":{"texts":"","texte":""}}}'
			else:
				reply_text = '{"status":1,"topic":"pepper","type":"wav","output":{"ctbuttonlist":[],"ctcontent":{"texts":"我很樂意為您效勞，但我無法完全理解您的問題。<br/>請您致電中壽強積金熱線：3999-5555查詢。","texte":""},"enbuttonlist":[],"encontent":{"texts":"","texte":""}}}'
		else:
			clearFailureLog(e)
	else:
		clearFailureLog(e)

	creply_text = reply_text.replace("'","")

	addToMySQL(e,input_text,creply_text,rscore)
        print reply_text
	#print sessionid

if __name__ == "__main__":
        main()
