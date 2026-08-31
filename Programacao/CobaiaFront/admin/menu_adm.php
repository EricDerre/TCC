<!-- html:5 -->
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <title>Área Administrativa</title>
    <meta charset="UTF-8">
    <!-- Link arquivos Bootstrap CSS -->
    <!-- CÓDIGO DESABILITADO PARA NÃO HAVER CONFLITOS 
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link href="../css/bootstrap.min.css" rel="stylesheet">
    -->
    <!-- Link para CSS específico -->
    
</head>
<body>
<nav class="nav navbar-inverse">
<div class="container-fluid">
    <!-- Agrupamento para exibição Mobile -->
    <div class="navbar-header">
        <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#defaultNavbar" aria-expanded="false">
            <span class="sr-only"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
        </button>
        <a href="index.php" class="navbar-brand">
            <img src="../images/logo churrascaria.png" alt="">
        </a>
    </div>
    <!-- Fecha Agrupamento para exibição Mobile -->
    <!-- nav direita -->
    <div class="collapse navbar-collapse" id="defaultNavbar">
        <ul class="nav navbar-nav navbar-right">
            <li>
                <button type="button" class="btn btn-danger navbar-btn disabled">
                    Olá, <?php echo($_SESSION['login_usuario']); ?>!
                </button>
            </li>
            <li class="active"><a href="index.php">ADMIN</a></li>
            <li><a href="produtos_lista.php">PRODUTOS</a></li>
            <li><a href="tipos_lista.php">TIPOS</a></li>
            <li><a href="usuarios_lista.php">USUÁRIOS</a></li>
            <li class="active">
                <a href="../index.php">
                    <span class="glyphicon glyphicon-home"></span>
                </a>
            </li>
            <li>
                <a href="logout.php">
                    <span class="glyphicon glyphicon-log-out"></span>
                </a>
            </li>
        </ul>
    </div><!-- fecha collapse navbar-collapse -->
    <!-- Fecha nav direita -->

</div><!-- fecha container-fluid -->

</nav>

    
<!-- Link arquivos Bootstrap js -->
<!-- CÓDIGO DESABILITADO PARA NÃO HAVER CONFLITOS 
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
    <script src="../js/bootstrap.min.js"></script>
-->
</body>
</html>