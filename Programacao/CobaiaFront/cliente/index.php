<?php
include '../conn/connect.php';

$lista = $conn->query("select * from vw_tbpedidos where cpf like '%" . $_GET["cliente"] . "%';");
$row = $lista->fetch_assoc();
$rows = $lista->num_rows;

?>

<!DOCTYPE html>
<html lang="pt-BR">
<head>
   <meta charset="UTF-8">
   <meta name="viewport" content="width=device-width, initial-scale=1.0">
   <link rel="stylesheet" href="../css/bootstrap.min.css">
   <link rel="stylesheet" href="../css/estilo.css">
   <script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.6.9/angular.min.js"></script>
   <title>Área do cliente - <?php echo $row['nome']; ?></title>
</head>
<body class="fundofixo">

   <main class="container" ng-app="App" ng-controller="Controlador">

      <h2 class="breadcrumb">
         <a href="../index.php" class="btn btn-info">
            <span class="glyphicon glyphicon-chevron-left"></span>
         </a>
         Olá, <strong><?php echo $row['nome']; ?></strong>!
      </h2>

      <div class="text-center">
         <span class="text-info btn btn-info" ng-click="FuncaoRegistro()">Faça uma nova reserva </span>
      </div>

      <?php include 'reserva_cli.php'; ?>    
      
      <?php include 'registrar_reserva.php'; ?>   
      
   </main>
</body>

<!-- Script de Angular para registrar nova reserva -->
<script>
    var app = angular.module('App', []);
    app.controller ('Controlador', function($scope){
        $scope.Registrar = false;

        $scope.FuncaoRegistro = function(){
            $scope.Registrar = !$scope.Registrar;
        }
    })
</script>
</html>
