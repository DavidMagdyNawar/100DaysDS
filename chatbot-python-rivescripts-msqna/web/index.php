<?php
	session_start();
?>

<!doctype html>
<html>
<head>
<!-- Global site tag (gtag.js) - Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=UA-134156566-1"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'UA-134156566-1');
</script>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1, user-scalable=0">
<meta http-equiv="Cache-control" content="no-cache">
<title>MPF 智能助手 Smart Assistant</title>
<link href="css/clio-chatbot.css" rel="stylesheet">
<link href="css/animate.css" rel="stylesheet">
	
</head>
<body>
	<div class="container">
		<div class="leftmenu">

			<ul>
			 <li class="appl" onclick="user( wording('appl', $('.lang select').val()) ,$('.lang select').val())">強積金計劃</li>
			 <li class="contribution" onclick="user(wording('contribution', $('.lang select').val()),$('.lang select').val())">供款</li>
			 <li class="acc" onclick="user(wording('acc', $('.lang select').val()),$('.lang select').val())">整合/轉移</li>
			 <li class="claim" onclick="user(wording('claim', $('.lang select').val()), $('.lang select').val(),$('.lang select').val())">申索權益</li>
			 <li class="layoff" onclick="user(wording('layoff', $('.lang select').val()), $('.lang select').val(),$('.lang select').val())">遣散費</li>
			 <li class="service" onclick="user( wording('service', $('.lang select').val()) ,$('.lang select').val())">服務</li>
			</ul>

			<img src="img/logo.png" class="logo"/>
		</div>
		<div class="dialogue">
			<div class="info">
				<div class="profile-pic"><img src="img/jarvis-icon-20190116.png"/></div>
				<div class="name">
					Jarvis<span>MPF 智能助手</span>
				</div>
				<div class="lang">
					<select>
						<option value="ct">繁中</option>
				<?php //		<option value="en">English</option> ?>
					</select>
				</div> 
				<div class="m-faq-btn"><a>常見問題</a></div>
			</div>
			<div class="content">
				<div class="box">
					
				</div>
			</div>
			<div class="textinput">
				<input type="text" id="sendInput" placeholder="在此輸入您的問題"/>
				<a class="btn" >傳送</a>
			</div>
		</div>
	
	</div>
	
	<script src="js/jquery-3.3.1.min.js"></script>
	<script src="js/clio-chatbot.js"></script>
	<script>
		//https://api.migos.com.hk/chatbot/s1.php
		//https://api.migos.com.hk/chatbot/s2.php

		
		
		
		

	</script>

</body>
</html>
