<?php
include "conn/connect.php";
// ! Alteração de IA - Revisar: (01/11/2026, Fase 4, pacote P4) inclui quebra.php, a variante de quebra de localizador
// ligada só por `?quebra=<modo>` ou pelo cookie `quebra`; desligada, o campo de busca sai como sempre saiu.
// ! Motivo: ficha 29, opção c (decisão 80): a cura de seletor é medida também com a quebra feita no HTML que o PHP devolve.
include_once __DIR__ . '/quebra.php';
$lista_tipos = $conn->query("select * from tbtipos order by rotulo_tipo;");
$row_tipos = $lista_tipos->fetch_all();
?>
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="css/bootstrap.min.css">
    <link rel="shortcut icon" type="imagex/png" href="../Chuleta/images/logo churrascaria.png">
    <title>Menu público</title>
</head>
<body>
    <!-- abre a barra de navegação -->
    <nav class="fixed navbar fixed-top navbar-light navbar-inverse bg-light">
        <div class="container-fluid">

            <!-- agrupamento mobile -->
            <div class="navbar-header">
                <button class="navbar-toggle collapsed" type="button" data-toggle="collapse" data-target="#menupublico" aria-expanded="false">
                    <span class="sr-only">Toggle Navigation</span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                </button>
                <a href="index.php" class="navbar-brand">
                    <img src="images/logo churrascaria.png" alt="Logotipo Fornalha">
                </a>
            </div>
            <!-- fecha agrupamento mobile  -->
            
            <!-- nav direita -->
            <div class="collapse navbar-collapse" id="menupublico">
                <ul class="nav navbar-nav navbar-right">
                    <li class="active">
                        <a href="index.php">
                            <span class="glyphicon glyphicon-home"></span>
                        </a>
                    </li>
                    <li><a href="index.php#destaques">DESTAQUES</a></li>
                    <li><a href="index.php#produtos">PRODUTOS</a></li>
                    <!-- ! Alteração de IA - Revisar: acrescenta o item de menu "PRODUTOS (API)". -->
                    <!-- ! Motivo: é a ÚNICA alteração feita em arquivo pré-existente do CobaiaFront
                         (o resto do site legado é mantido intocado de propósito). A aba nova precisa
                         ser alcançável pelo mesmo menu para que o agente exercite o alvo moderno
                         (produtos_api.php, que busca dados por HTTP na CobaiaAPI) dentro do mesmo
                         layout e da mesma navegação do site legado. -->
                    <li><a href="produtos_api.php">PRODUTOS (API)</a></li>

                    <!-- dropdown -->
                    <li class="dropdown">
                        <a class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">
                            TIPOS
                            <span class="caret"></span>
                        </a>
                        <ul class="dropdown-menu">
                            <?php foreach($row_tipos as $row){?>
                                <li><a href="produtos_por_tipo.php?id_tipo=<?php echo $row[0] ?>"><?php echo $row[2] ?></a></li>
                            <?php }?>
                        </ul>
                    </li>
                    <!-- fim do dropdown -->
                    
                    <li><a href="index.php#contato">CONTATO</a></li>
                    
                    <!-- inicio formulario de busca -->
                    <form action="produtos_busca.php" method="get" name="form-busca" id="form-busca" class="navbar-form navbar-left" role="search">
                        <div class="input-group">
                                <!-- ! Alteração de IA - Revisar: (01/11/2026, P4) o campo e o botão da busca saem por PHP para a
                                     variante de quebra (quebra.php): no modo id_renomeado o id vira buscar_v2, no classe_trocada
                                     a classe form-control vira campo-busca, no texto_alterado o placeholder vira "Buscar produtos"
                                     e no estrutura_alterada o campo é envolvido num span.envoltorio e sai depois do botão. Sem
                                     modo, o HTML é o de antes, caractere a caractere nos atributos; o name=buscar nunca muda.
                                     ! Motivo: ficha 29, opção c (decisão 80); o name é lido por produtos_busca.php e por isso
                                     fica fora da quebra. -->
                                <?php
                                    $quebra_campo = '<input type="search" name="buscar" id="' . quebra_id('buscar', 'buscar_v2') . '" size="10" class="'
                                        . quebra_classe('form-control', 'campo-busca') . '" aria-label="search" placeholder="'
                                        . quebra_texto('Buscar produto', 'Buscar produtos') . '" required>';
                                    $quebra_botao = '<div class="input-group-btn"><button class="btn btn-default" type="submit">'
                                        . '<span class="glyphicon glyphicon-search"></span></button></div>';
                                    if (quebra_estrutura()) {
                                        echo $quebra_botao . '<span class="envoltorio">' . $quebra_campo . '</span>';
                                    } else {
                                        echo $quebra_campo . $quebra_botao;
                                    }
                                ?>
                        </div>
                    </form>
                    <!-- fim do formulario de busca -->

                    <li>
                        <a href="admin/index.php">
                            <span class="glyphicon glyphicon-user">&nbsp;</span>
                        </a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
</body>
</html>