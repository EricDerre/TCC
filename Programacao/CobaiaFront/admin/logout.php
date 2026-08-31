<?php 
session_name('chulettaaa');
session_start();
session_destroy();
header('location: ../index.php');
exit;
?>