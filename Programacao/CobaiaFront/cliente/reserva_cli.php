<?php 
include '../admin/acesso_com.php';
include '../conn/connect.php';

?>

<h2 class="breadcrumb alert-info texto-negrito"><strong>Suas Reservas</strong></h2>
<table class="table table-hover table-condensed tb-opacidade bg-info"> 
    <thead>
        <th class="hidden">ID</th>
        <th class="text-center">DATA DO PEDIDO</th>
        <th class="text-center">N° PESSOAS</th>
        <th class="text-center">STATUS</th>
    </thead>
            
    <tbody> <!-- início corpo da tabela -->
    <!-- início estrutura repetição -->
        <?php do{?>
            <tr>
                <td class="hidden">
                    <?php echo $row['id_pedido'];?>
                </td>

                <td class="text-center">
                    <?php  echo $row['data_pedido'] ?> 
                </td>

                <td class="text-center">
                    <?php echo $row['pessoas'];?>
                </td>

                <td class="text-center">
                    <?php  echo $row['status'] ?> 
                </td>
                       
                <td>
                    <button 
                        data-nome="<?php echo $row['pessoas'];?>" 
                        data-id="<?php echo $row['id_pedido'];?>"
                        class="cancela btn btn-xs btn-block btn-danger">
                        <span class="glyphicon glyphicon-trash"></span>
                        <span class="hidden-xs">CANCELAR</span>
                    </button>
                </td>
            </tr>
        <?php }while($row = $lista->fetch_assoc());?>
       
    </tbody><!-- final corpo da tabela -->
</table>



<!-- inicio do modal para excluir -->
<div class="modal fade" id="modalEdit" role="dialog">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <button class="close" data-dismiss="modal" type="button">
                    CANCELAMENTO DE RESERVA
                </button>
            </div>
            <div class="modal-body">
                Deseja mesmo cancelar essa reserva?
                <h4><span class="nome text-danger"></span></h4>
            </div>
            <div class="modal-footer">
                <a href="#" type="button" class="btn btn-success cancela-yes">
                    Confirmar
                </a>
                <button class="btn btn-danger" data-dismiss="modal">
                    Cancelar
                </button>
            </div>
        </div>
    </div>
</div>
<!-- fim do modal para excluir -->


<!-- inicio do modal de Excluir -->

<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
<script src="../js/bootstrap.min.js"></script>
<script type="text/javascript">
    $('.cancela').on('click',function(){
        var nome = $(this).data('nome'); //busca o nome com a descrição (data-nome)
        var id = $(this).data('id'); // busca o id (data-id)
        //console.log(id + ' - ' + nome); //exibe no console
        $('span.nome').text(nome); // insere o nome do item na confirmação
        $('a.cancela-yes').attr('href','cliente_cancelar.php?id_pedido='+id); //chama o arquivo php para excluir o produto
        $('#modalEdit').modal('show'); // chamar o modal
    });
</script>


