<?php 
    session_name('chulettaaa');
    if(!isset($_SESSION)){
        session_start();
    }
    // Segurança digital


    // Verificiar se o usuario está logado na sessão
    if(!isset($_SESSION['login_usuario'])){
        // Se não existir, redirecionamos a sessão por segurança
        header('location: login.php');
        exit;
    }

    $nome_da_sessao = session_name();
    if(!isset($_SESSION['nome_da_sessao'])
        OR ($_SESSION['nome_da_sessao']!=$nome_da_sessao)
    ){
        session_destroy();
        header('location: login.php');
        exit;
    }
  
?>