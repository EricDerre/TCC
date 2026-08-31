<?php 
include 'conn/connect.php';
$lista = $conn->query("select * from vw_tbprodutos where destaque_produto = 'Sim';");
$row_destaque =  $lista->fetch_assoc();
$num_linhas = $lista->num_rows;

?>

<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="css/bootstrap.min.css">
    <link rel="stylesheet" href="css/estilo.css">
    <title>Destaques</title>
</head>
<body>
        <!-- mostrar se a consulta retornar vazia -->
        <?php if($num_linhas == 0){?>
            <h2 class="breadcrumb alert-danger">
                Não há produtos em Destaque
            </h2>
        <?php }?>

        <!-- mostrar se a consulta retornou produtos -->
        <?php if($num_linhas>0){?>
            <h2 class="breadcrumb alert-danger">
                <strong>Destaques</strong>
            </h2>
            <div class="row">
                <?php do{?>
                    <div class="col-sm-6 col-md-4">
                        <div class="thumbnail">
                            <a href="produto_detalhes.php?id_produto=<?php echo $row_destaque ['id_produto']?>">
                                <img src="images/<?php echo $row_destaque ['imagem_produto']?>" class="img-responsive img-rounded">
                            </a>
                            <div class="caption text-right">
                                <h3 class="text-danger">
                                    <strong><?php echo $row_destaque ['descri_produto']?></strong>
                                </h3>
                                <p class="text-warning">
                                    <strong><?php echo $row_destaque ['rotulo_tipo']?></strong>
                                </p>
                                <p class="text-left">
                                    <?php echo mb_strimwidth($row_destaque ['resumo_produto'],0,42,'...');?>
                                </p>
                                <p>
                                    <button class="btn btn-default disable" role="button" style="cursor: default">
                                        <?php echo "R$ ".number_format($row_destaque['valor_produto'],2,",",".");?>
                                    </button>
                                    <a href="produto_detalhes.php?id_produto=<?php echo $row_destaque['id_produto']?>">
                                        <span class="hidden-xs">Saiba Mais...</span>
                                        <span class="hidden-xs glyphicon glyphicon-eye-open" aria-hidden="true"></span>
                                    </a>
                                </p>
                            </div>
                        </div>
                    </div>
                <?php }while($row_destaque = $lista->fetch_assoc());?>
            </div>
        <?php }?>

</body>
</html>