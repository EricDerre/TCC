<?php
include 'acesso_com.php';
include '../conn/connect.php';
// ! Alteração de IA - Revisar: (01/11/2026, Fase 4, pacote P4) inclui quebra.php, a variante de quebra de localizador
// ligada só por `?quebra=<modo>` ou pelo cookie `quebra`; desligada, a lista de produtos sai como sempre saiu.
// ! Motivo: ficha 29, opção c (decisão 80): a cura de seletor é medida também com a quebra feita no HTML que o PHP devolve.
include_once __DIR__ . '/../quebra.php';
$lista = $conn->query("select * from vw_tbprodutos");
$row = $lista->fetch_assoc();
$rows = $lista->num_rows;
?>

<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Produtos - Lista</title>
    <link rel="stylesheet" href="../css/bootstrap.min.css">
    <link rel="stylesheet" href="../css/estilo.css">
</head>
<body class="fundoadm"> 
    <?php include "menu_adm.php"; ?>
    <main class="container">
        <h2 class="breadcrumb alert-info" >Lista de Produtos </h2>
        <table class="table table-hover table-condensed tb-opacidade bg-info"> 
            <thead>
                <th class="hidden">ID</th>
                <th>TIPO</th>
                <th>DESCRIÇÃO</th>
                <th>RESUMO</th>
                <th>VALOR</th>
                <th>IMAGEM</th>
                <th>
                    <a href="produtos_insere.php" target="_self" class="btn btn-block btn-primary btn-xs" role="button">
                        <span class="glyphicon glyphicon-plus" aria-hidden="true"></span>
                        <span class="hidden-xs">ADICIONAR</span>
                    </a>
                </th>
            </thead>
            
            <tbody> <!-- início corpo da tabela -->
           	<!-- início estrutura repetição -->
                <?php do{?>
                    <tr>
                        <td class="hidden">
                            <?php echo $row['id_produto'];?>
                        </td>
                        <td>
                        <?php echo $row['rotulo_tipo'];?>
                            <span class="visible-xs"></span>
                            <span class="hidden-xs"></span>
                        </td>
                        <td>
                            <?php 
                                if ($row['destaque_produto']=='Sim') { 
                                    echo '<span class="glyphicon glyphicon-heart text-danger" aria-hidden="true"></span>';
                                }else{
                                    echo '<span class="glyphicon glyphicon-ok text-info" aria-hidden="true"></span>';
                                }
                            ?> 
                            <?php echo $row['descri_produto']?>    
                        </td>
                        <td> 
                            <?php echo $row['resumo_produto']?>
                        </td>
                        <td>
                        <?php echo number_format($row['valor_produto'],2,',','.');?>
                        </td>
                        <td>
                            <img src="../images/<?php echo $row['imagem_produto'];?>" width="100px">
                        </td>
                        <td >
                            <!-- ! Alteração de IA - Revisar: (01/11/2026, P4) o botão EXCLUIR sai por PHP para a variante de quebra
                                 (quebra.php): no modo id_renomeado o atributo data-id vira data-produto (a página não tem id em
                                 elemento nenhum), no classe_trocada a classe delete vira remover, no texto_alterado o botão diz
                                 "EXCLUIR ITEM" e no estrutura_alterada ele sai envolvido num div.acoes antes do link ALTERAR. Sem
                                 modo, o HTML é o de antes; o script no fim da página acompanha a classe e o atributo.
                                 ! Motivo: ficha 29, opção c (decisão 80). -->
                            <?php
                                // a quebra de linha entre os dois spans fica como no HTML original: ela entra no nome acessível do
                                // botão (o ícone, um espaço e o texto), e as duas formas de quebra precisam ter o mesmo nome
                                $quebra_botao_excluir = '<button data-nome="' . $row['descri_produto'] . '" ' . quebra_atributo('data-id', 'data-produto')
                                    . '="' . $row['id_produto'] . '" class="' . quebra_classe('delete', 'remover') . ' btn btn-xs btn-block btn-danger">' . "\n"
                                    . '<span class="glyphicon glyphicon-trash"></span>' . "\n" . '<span class="hidden-xs">' . quebra_texto('EXCLUIR', 'EXCLUIR ITEM')
                                    . '</span>' . "\n" . '</button>';
                                if (quebra_estrutura()) { echo '<div class="acoes">' . $quebra_botao_excluir . '</div>'; }
                            ?>
                            <a href="produtos_atualiza.php?id_produto=<?php echo $row['id_produto']?>" role="button" class="btn btn-warning btn-block btn-xs">
                                <span class="glyphicon glyphicon-refresh"></span>
                                <span class="hidden-xs">ALTERAR</span>
                            </a>
                            <?php if (!quebra_estrutura()) { echo $quebra_botao_excluir; } ?>
                        </td>
                    </tr>
                    <?php }while($row = $lista->fetch_assoc());?>
       
            </tbody><!-- final corpo da tabela -->
        </table>
    </main>
    <!-- inicio do modal para excluir... -->
    <div class="modal fade" id="modalEdit" role="dialog">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <button class="close" data-dismiss="modal" type="button">
                        &times;
                    </button>
                </div>
                <div class="modal-body">
                    Deseja mesmo excluir o item?
                    <h4><span class="nome text-danger"></span></h4>
                </div>
                <div class="modal-footer">
                    <a href="#" type="button" class="btn btn-success delete-yes">
                        Confirmar
                    </a>
                    <button class="btn btn-danger" data-dismiss="modal">
                        Cancelar
                    </button>
                </div>
            </div>
        </div>
    </div>
</body>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
<script src="../js/bootstrap.min.js"></script>
<script type="text/javascript">
    // ! Alteração de IA - Revisar: (01/11/2026, P4) a classe e o atributo lidos aqui acompanham a variante de quebra
    // (quebra.php): sem modo, continuam '.delete' e 'id'.
    // ! Motivo: no modo classe_trocada o botão sai como .remover e no id_renomeado o data-id vira data-produto; sem
    // acompanhar, o clique não abriria o modal e a quebra no PHP não seria comparável à armada pelo harness, em que o
    // manipulador já está ligado ao elemento quando a mutação acontece.
    $('.<?php echo quebra_classe('delete', 'remover'); ?>').on('click',function(){
        var nome = $(this).data('nome'); //busca o nome com a descrição (data-nome)
        var id = $(this).data('<?php echo quebra_atributo('id', 'produto'); ?>'); // busca o id (data-id)
        //console.log(id + ' - ' + nome); //exibe no console
        $('span.nome').text(nome); // insere o nome do item na confirmação
        $('a.delete-yes').attr('href','produtos_excluir.php?id_produto='+id); //chama o arquivo php para excluir o produto
        $('#modalEdit').modal('show'); // chamar o modal
    });
</script>

</html>