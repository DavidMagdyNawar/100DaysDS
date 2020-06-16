// JavaScript Document
//var jsID = document.cookie.match(/PHPSESSID=[^;]+/);
//jsID = jsID[0];
//jsID = jsID.replace("PHPSESSID=", "");

var lang;
//get lang from URL
$.urlParam = function(name){
	var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
	return results;
}

//console.log("1:"+$.urlParam("lang")[0]);
if($.urlParam("lang")!=null){ 
	lang = $.urlParam("lang")[1];
}else{ 
	window.location.replace("index.php?lang=ct");
}

console.log("lang:"+lang);

//$.getJSON("https://ipinfo.io/?format=jsonp&callback=getIP",function(json){});


function chatbot( contents, buttonlist, contente){
	
	//timelog 
	var currentTime = new Date();
	var hours = currentTime.getHours();
	var minutes = currentTime.getMinutes();
	if (minutes < 10){ minutes = "0" + minutes}
	var timelog = hours+" : "+minutes;
	
	var sumButtonlist="";
	console.log("contents: "+contents);
	if (buttonlist==null){buttonlist=""}else{
		for(i=0; i < buttonlist.length ; i++){
			sumButtonlist += '<button onclick="user('+"'"+buttonlist[i]+"'"+','+"'"+lang+"'"+')">'+buttonlist[i]+'</button>'
			}
	}
	//set rely content
	var sumcontent= '<div class="chatbot fadeInLeft animated faster"><div class="profile-pic"><img src="img/jarvis-icon-20190116.png"></div><div class="msg"><div class="db-reply">'+ contents +'</div>' + sumButtonlist + '<div class="db-reply">'+ contente +'</div>'  + '<div class="time">' + timelog + '</div></div></div>'
	$(sumcontent).appendTo(".dialogue .content .box");
	
	//animation scroll to bottom
	$(".dialogue .content ").animate({ scrollTop: $(".dialogue .content .box").height() }, 500);
	
	
}




function user(content, lang){
	//timelog add by cargo3
	var currentTime = new Date();
	var hours = currentTime.getHours();
	var minutes = currentTime.getMinutes();
	if (minutes < 10){ minutes = "0" + minutes}
	var timelog = hours+" : "+minutes;
	//set rely content
	var sumcontent= '<div class="user fadeIn animated faster"><div class="msg"><div class="db-reply">'+ content +'</div>' + '<div class="time">' + timelog + '</div></div></div>'

	var jsID = document.cookie.match(/PHPSESSID=[^;]+/);
	jsID = jsID[0];
	jsID = jsID.replace("PHPSESSID=", "");

	//var ip = user_location();

	//console.log("ip:"+ip);	
	
	if(content==="open"){}else{
	$(sumcontent).appendTo(".dialogue .content .box");
	}
	
	//animation scroll to bottom
	$(".dialogue .content ").animate({ scrollTop: $(".dialogue .content .box").height() }, 500);
	
	console.log("pass to sever: reply:"+content+", lang:"+lang+", session:"+jsID)
	
	$.ajax({
			url: "https://pepper.chinalife.com.hk/chatbot/s.php",
			type: 'POST',
			data: {s:content,lang:lang,e:jsID},
			dataType: 'json',
			cache: false,
			success: function (data) {
				console.log( "load json success" );
				console.log(data);
				if (lang==="en"){
				 chatbot( data.output.encontent.texts, data.output.enbuttonlist, data.output.encontent.texte);
				}else{
				 chatbot( data.output.ctcontent.texts, data.output.ctbuttonlist, data.output.ctcontent.texte);
				}
			},error: function(xhr, ajaxOptions, thrownError){
				 //console.log(jsID);
				 console.log( "load json fail" );
			}
		});
}


$( document ).ready(function() {
			//"open" is a opening keyword pass to sever
			user("open", lang);
			wording(lang);
			console.log("current lang="+lang)
			$(".lang select").val(lang);
		});

		
		$(".btn").click( function(){
			user($(".textinput input").val(), lang);
			document.getElementById('sendInput').value="";
		})

		
		$('.textinput input').keypress(function(e) {
		  if (e.which == '13') {
			 e.preventDefault();
			user($(".textinput input").val(), lang);
			  this.value=""
		   }
		});
		
		$(".lang select").change( function(){
			window.location.replace("index.php?lang="+$(this).val());
		});
		
		$(".m-faq-btn").click( function(){
			$(".leftmenu").addClass("m-show");
		});
		$(".leftmenu").click( function(){
			$(".leftmenu").removeClass("m-show");
			$(".leftmenu").removeClass("m-show");
		});


//wording
function wording(lang){
	
	var applText=["Application","參加強積金計劃"];
	var contributionText=["Contribution","供款"];
	var accText=["Account","離職／整合帳戶／轉移強積金"];
	var claimText=["Claim","申索累算權益"];
	var layoffText=["Layoff","長期服務金／遣散費"];
	var serviceText=["Services","服務"];
	var submitText=["Send","傳送"];
	
	if(lang==="en"){
		$(".appl").html( applText[0]);
		$(".appl").attr("onclick","user( '"+applText[0]+"' ,$('.lang select').val())");
		
		$(".contribution").html( contributionText[0]);
		$(".contribution").attr("onclick","user( '"+contributionText[0]+"' ,$('.lang select').val())");
		
		$(".acc").html( accText[0]);
		$(".acc").attr("onclick","user( '"+accText[0]+"' ,$('.lang select').val())");
		
		
		$(".claim").html( claimText[0]);
		$(".claim").attr("onclick","user( '"+claimText[0]+"' ,$('.lang select').val())");
		
		
		$(".layoff").html( layoffText[0]);
		$(".layoff").attr("onclick","user( '"+layoffText[0]+"' ,$('.lang select').val())");
		
		
		$(".service").html( serviceText[0]);
		$(".service").attr("onclick","user( '"+serviceText[0]+"' ,$('.lang select').val())");
				
		$(".textinput .btn").html( submitText[0]);
	}else {
		$(".appl").html( applText[1]);
		$(".appl").attr("onclick","user( '"+applText[1]+"' ,$('.lang select').val())");
		
		$(".contribution").html( contributionText[1]);
		$(".contribution").attr("onclick","user( '"+contributionText[1]+"' ,$('.lang select').val())");
		
		$(".acc").html( accText[1]);
		$(".acc").attr("onclick","user( '"+accText[1]+"' ,$('.lang select').val())");
		
		
		$(".claim").html( claimText[1]);
		$(".claim").attr("onclick","user( '"+claimText[1]+"' ,$('.lang select').val())");
		
		
		$(".layoff").html( layoffText[1]);
		$(".layoff").attr("onclick","user( '"+layoffText[1]+"' ,$('.lang select').val())");
		
		
		$(".service").html( serviceText[1]);
		$(".service").attr("onclick","user( '"+serviceText[1]+"' ,$('.lang select').val())");
				
		$(".textinput .btn").html( submitText[1]);
	}
	
	
	
	
} 





