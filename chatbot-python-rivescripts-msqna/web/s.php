<?php
 header('Access-Control-Allow-Origin: *');
 header("Content-type: application/json; charset=utf-8"); 


 $msg = @$_REQUEST['s'];
 #$msg = str_replace('&#92;','?',$msg);
 $msg = preg_replace("/[\'\"]+/" , '' ,$msg);
 $msg = strtolower(str_replace(' ', ',', $msg));

 $e = @$_REQUEST['e'];

 $ip = $_SERVER['REMOTE_ADDR'];

echo $msg;
echo $ip;

 //echo $sess;

 $handle = popen("python /chatbot/chinalifetrustees/chatbot.py $msg $e $ip","r");

 $outputs = fread($handle, 4096);
 pclose($handle);


 //$mysqli = new mysqli("localhost", "root", "Chinalife2017", "CLIOHK");
 //$mysqli->query("SET NAMES 'utf8'");

 echo $outputs;

?>
