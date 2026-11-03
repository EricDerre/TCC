<?php
    include '../conn/connect.php';
    // ! Alteração de IA - Revisar: (01/11/2026, Fase 4, pacote P4) inclui quebra.php, a variante de quebra de localizador
    // ligada só por `?quebra=<modo>` ou pelo cookie `quebra`; desligada, o formulário de login sai como sempre saiu.
    // ! Motivo: ficha 29, opção c (decisão 80): a cura de seletor é medida também com a quebra feita no HTML que o PHP devolve.
    include_once __DIR__ . '/../quebra.php';
    // Iniciar a verificação do login
    if($_POST){
        $login = $_POST['login_usuario'];
        $senha = $_POST['senha_usuario'];
        $loginRes = $conn->query("select * from tbusuarios where login_usuario = '$login' and senha_usuario = '$senha';");
        $rowLogin = $loginRes->fetch_assoc();
        $numRow = mysqli_num_rows($loginRes);

        // Se a sessão não existir
        if(!isset($_SESSION)){
            $sessaoAntiga = session_name('chulettaaa');
            session_start();
            $session_name_new = session_name();
        }
        if($numRow>0){
            $_SESSION['login_usuario'] = $login;
            $_SESSION['nivel_usuario'] = $rowLogin['nivel_usuario'];
            $_SESSION['nome_da_sessao'] = session_name();
            if($rowLogin['nivel_usuario']=='sup'){
                echo "<script>window.open('index.php','_self')</script>";
            }
            else{
                echo "<script>window.open('../cliente/index.php?cliente=".$login."','_self')</script>";
            }
        }else{
            echo "<script>window.open('invasor.php','_self')</script>";
        }
    }
?>
<!DOCTYPE html>
<html lang="pt-BR">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="30;URL=../index.php">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="../css/bootstrap.min.css">
    <script src="https://kit.fontawesome.com/2495680ceb.js" crossorigin="anonymous"></script>
    <!-- Link para CSS específico -->
    <link rel="stylesheet" href="../css/estilo.css" type="text/css">
    <link rel="stylesheet" href="../css/estilo-login.css">
    
    <title>Chuleta Quente - Login</title>
</head>

<body class="fundofixo">
    <div class="login-container">
        <div class="login-form">
             <p class="text-danger text-center" role="alert">
                <i><img src="../images/logo churrascaria maior.png" class="tamanho_img" style="width: 190px;"></i>
                     </p>
                <!-- ! Alteração de IA - Revisar: (01/11/2026, P4) o id do campo de login e o botão Entrar passam pela variante de
                     quebra (quebra.php): no modo id_renomeado o id login_usuario vira usuario (com o for do rótulo), no
                     classe_trocada a classe btn-primary vira btn-entrar, no texto_alterado o botão diz "Entrar agora" e no
                     estrutura_alterada o botão sai envolvido num div.acoes antes dos campos. Sem modo, o HTML é o de antes;
                     o name dos campos nunca muda, porque o POST acima lê $_POST['login_usuario'] e $_POST['senha_usuario'].
                     ! Motivo: ficha 29, opção c (decisão 80). -->
                <?php
                    $quebra_id_login = quebra_id('login_usuario', 'usuario');
                    $quebra_botao = '<button type="submit" class=" btn ' . quebra_classe('btn-primary', 'btn-entrar') . '">'
                        . quebra_texto('Entrar', 'Entrar agora') . '</button>';
                ?>
                <form action="login.php" method="POST">
                    <?php if (quebra_estrutura()) { echo '<div class="acoes">' . $quebra_botao . '</div>'; } ?>
                      <div class="input-group">
                    <label  for="<?php echo $quebra_id_login; ?>">Login</label>
                 <input type="text" name="login_usuario" id="<?php echo $quebra_id_login; ?>" autofocus required autocomplete="off" placeholder="Digite seu login.">
             </div>
            <div class="input-group">
        <label for="senha_usuario">Senha</label>
    <input  type="password" name="senha_usuario" id="senha_usuario" required autocomplete="off" placeholder="Digite sua senha.">
</div>
    <?php if (!quebra_estrutura()) { echo $quebra_botao; } ?>
        </form>
    </div>
</div>


    <!-- Link arquivos Bootstrap js -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
    <script src="../js/bootstrap.min.js"></script>
</body>

</html>