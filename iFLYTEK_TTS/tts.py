#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import time
from ctypes import *
from io import BytesIO
import wave
import platform
import logging
from pydub import AudioSegment
import shutil


class convertTTS(object):
	logging.basicConfig(level=logging.DEBUG)
	BASEPATH=os.path.split(os.path.realpath(__file__))[0]

	plat = platform.architecture()
	if plat[0] == '32bit':
		cur = cdll.LoadLibrary(BASEPATH + '/x86/libmsc.so')
	else:
		cur = cdll.LoadLibrary(BASEPATH + '/x64/libmsc.so')
	
	def login(self,str_txt='appid = 539feff8, work_dir = .'):
		MSPLogin = self.cur.MSPLogin
		ret = 0
		ret = MSPLogin(None,None,str_txt) 
		
		if ret != 0:
			logging.error("MSPLogin failed, error code: " + str(ret))
		else:
			logging.info("MSPLogin")

		return ret

	def logout(self):
		MSPLogout = self.cur.MSPLogout
		MSPLogout()
		logging.info("MSPLogout")

	def saveWave(self, raw_data, _tmpFile = 'test.wav'):
		f = wave.open(_tmpFile,'w')
		f.setparams((1, 2, 16000, 262720, 'NONE', 'not compressed'))
		f.writeframesraw(raw_data)
		f.close()
		return _tmpFile

	def text_to_speech(self,src_text,voicename,speed,volumn,pitch,mp3,file_name=None):
		logging.info (str(voicename) + " " + str(speed) + " " + str(volumn) + " " + str(pitch))

		encoding = 'utf8'
		sample_rate = 16000
		rdn = 2

		QTTSSessionBegin = self.cur.QTTSSessionBegin
		QTTSTextPut = self.cur.QTTSTextPut

		QTTSAudioGet = self.cur.QTTSAudioGet
		QTTSAudioGet.restype = c_void_p
		
		QTTSSessionEnd = self.cur.QTTSSessionEnd

		ret_c = c_int(0)

		session_begin_params="voice_name=" + str(voicename) + ",text_encoding=" + str(encoding) + ",sample_rate=" + str(sample_rate) +",speed=" + str(speed) + ",volume=" + str(volumn) + ",pitch=" + str(pitch) + ",rdn=" + str(rdn)

		sessionID = QTTSSessionBegin(session_begin_params, byref(ret_c))

		if ret_c.value != 0 :
			logging.error("QTTSSessionBegin failed, error code: " + ret_c.value)
			return
		
		ret = QTTSTextPut(sessionID, src_text, len(src_text),None)

		if ret != 0:
			logging.error("QTTSTextPut failed, error code: " + str(ret))
			QTTSSessionEnd(sessionID, "TextPutError")
			return

		logging.info("正在合成: " + (src_text))

		audio_len = c_uint(0)
		synth_status = c_int(0)

		f = BytesIO()

		while True:
			p = QTTSAudioGet(sessionID, byref(audio_len), byref(synth_status), byref(ret_c))
			
			if ret_c.value != 0:
				logging.error("QTTSAudioGet failed, error code: " + str(ret_c))
				QTTSSessionEnd(sessionID, "AudioGetError")
				break

			if p != None:
				buf = (c_char * audio_len.value).from_address(p)
				f.write(buf)

			if synth_status.value == 2 :
				self.saveWave(f.getvalue(),file_name)
				break

			time.sleep(1)

		logging.info('合成完成！【' + file_name  + '】\n')
		ret = QTTSSessionEnd(sessionID, "Normal")

		if ret != 0:
			logging.error("QTTSTextPut failed, error code: " + str(ret))

def clear(text):
	text = text.replace('《', '')
	text = text.replace('》','')

	return text

def joinwav(fn, num_of_file):
	infiles =[]
	outfile = fn + ".wav"

	for num in range(1,num_of_file):
		filename = fn + "-" + str(num) + ".wav"
		logging.info(filename)
		infiles.append (AudioSegment.from_wav(filename))
		infiles.append (AudioSegment.from_wav("silentFix.wav"))
	
	combined = infiles[0]
	
	for wavcombined in infiles[1:]:
		combined = combined.append(wavcombined)

	combined.export(outfile, format="wav")
	logging.info(' 連結語音檔完成！【' + outfile  + '】')

def wav2mp3(filename):
	fn = os.path.splitext(filename)[0]
	#ext = os.path.splitext(filename)[1]
	AudioSegment.from_wav(filename).export(fn + ".mp3", format="mp3")
	logging.info(' 輸出 MP3 語音檔完成！【' + fn + ".mp3"  + '】')

def main(filename, voicename, speed, volumn, pitch, mp3, joinfile):
	lineno = 0
        fpath = os.path.dirname(os.path.abspath(__file__))

	fh = open(fpath + "/" + filename)
	fn = os.path.splitext(filename)[0]

	tts = convertTTS()
	tts.login()

	while True:	
		content = fh.readline()

		if (content <> ''):
			if not content.strip(): continue
			content = clear(content)

			lineno = lineno + 1
			
			targetfilename = fn + "-" + str(lineno) + ".wav"
			
			tts.text_to_speech(content,voicename,speed,volumn,pitch,mp3,targetfilename)

			#if (1 == mp3):
			#	wav2mp3(targetfilename)

		if not content:
			break
	fh.close()
	
	tts.logout()
	
	if (1 == joinfile):
		joinwav(fn, lineno+1)

	        if (1 == mp3):
			wav2mp3(fn + ".wav")


if __name__ == "__main__":
    nfn = sys.argv[1]

    main(nfn, 'xiaoyan', 50, 50, 50, 1, 1)


