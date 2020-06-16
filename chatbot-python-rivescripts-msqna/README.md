# chatbot-python-rivescripts-msqna
Python Chatbot with rivescripts and Microsoft QnaMaker

# Prerequisite
1. Register Microsoft QnA Services

# Dependencies
OS
1. Apache
2. MySQL
3. Php

Python
1. numpy
2. rivescripts
3. MySQLdb

# Installation
1. Move web folder to your www root, other files and folder don't put it to web root
2. MySQL DB <br/>
CREATE TABLE `Chatbot` (
  `id` int(11) NOT NULL,
  `ipaddress` varchar(15) DEFAULT NULL,
  `sessionid` varchar(50) DEFAULT NULL,
  `msg` text,
  `reply` text,
  `score` float DEFAULT '0',
  `msgdatetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

3. Change the Microsoft QnA Account and kb in chatbot.py

# To-do
1. Add thumb-up and thumb-down.

# Screen
<img src='https://github.com/kindersham/chatbot-python-rivescripts-msqna/blob/master/screen1.png' width='80%'>
<img src='https://github.com/kindersham/chatbot-python-rivescripts-msqna/blob/master/screen2.png' width='80%'>

# Live Demo
<a href="http://chatbot.chinalifetrustees.com.hk">http://chatbot.chinalifetrustees.com.hk</a>

# License
Copyright (c) 2017-present, <a href="mailto:kinder.sham@gmail.com">Kinder Sham</a>
