#!/usr/bin/php
<?php
$s = stream_socket_client('unix:///tmp/TelldusEvents');
while(1){
    echo stream_socket_recvfrom($s,1024)."\n";
}
?>
