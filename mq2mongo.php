<?php

// Mosquitto details
$appEUI = "70B3D57ED000010A";
$client = new Mosquitto\Client();
$client->onConnect('connect');
$client->onDisconnect('disconnect');
$client->onSubscribe('subscribe');
$client->onMessage('message');
$client->setCredentials('70B3D57ED000010A', 'S5i//oLLLv/TMcW8iODdWVv4oKIG/KAL/Y56u4l0soo=');
$client->connect("staging.thethingsnetwork.org", 1883, 60);
$client->subscribe("$appEUI/devices/+/up", 1);

while (true) {
        $client->loop();
        sleep(2);
}
 
$client->disconnect();
unset($client);
 
function connect($r) {
        echo "I got code {$r}\n";
}
 
function subscribe() {
        echo "Subscribed to a topic\n";
}
 
// must return "custom";

function message($message) {
	// Mongodb Configuration
	$dbhost = 'localhost';
	$dbname = 'ttnWorkshop';
	
	// Connect to test database
	$m = new Mongo("mongodb://$dbhost");
	$db = $m->$dbname;
	$c_senseData = $db->senseData;
        printf("\nGot a message on topic %s with payload:%s", 
          $message->topic, $message->payload);
	$readableJson=json_decode($message->payload, true);
        foreach ($readableJson as $k => $v) {
          echo $k, " : ", $v, "\n";
	  switch ($k) {
	    case "dev_eui":
	      $node =$v;
	      break;
	    case "payload":
              $msgData=base64_decode($v);
              echo "\nmsgData is ", $msgData, "\n";
	      $msgDataJson=json_decode($msgData, true);
	      break;
	    case "metadata":
	      print_r($v[0]);
	      $msgTime=$v[0]['gateway_time'];
	      echo "\nTime is $msgTime \n";
	      break;
	  }
	}
	if($msgDataJson!="") {
	  $senserec = array( 
	    'node' => $node,
	    'time' => $msgTime,
    	    'msgData' => $msgDataJson
	  );
	} else {
	  $senserec = array( 
	    'node' => $node,
	    'time' => $msgTime,
    	    'msgData' => $msgData
	  );
	}

	$c_senseData->save($senserec);
	$m->close();
}
 
function disconnect() {
        echo "Disconnected cleanly\n";
}

