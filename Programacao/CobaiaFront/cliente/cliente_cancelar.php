<?php 

include '../conn/connect.php';

if(isset($_GET['id_pedido'])){
    $lista = $conn->query("update tbpedido_reserva set status = 'Cancelado' where id_pedido = ".$_GET['id_pedido'].";");
header('location: reserva_cli.php');
}
?>