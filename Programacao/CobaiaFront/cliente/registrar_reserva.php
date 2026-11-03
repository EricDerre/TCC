<?php
include '../conn/connect.php';
// ! Alteração de IA - Revisar: (01/11/2026, Fase 4, pacote P4) inclui quebra.php, a variante de quebra de localizador
// ligada só por `?quebra=<modo>` ou pelo cookie `quebra`; desligada, o formulário de reserva sai como sempre saiu.
// ! Motivo: ficha 29, opção c (decisão 80): a cura de seletor é medida também com a quebra feita no HTML que o PHP devolve.
include_once __DIR__ . '/../quebra.php';

$lista = $conn->query("select * from vw_tbpedidos where cpf like '%" . $_GET["cliente"] . "%';");
$row = $lista->fetch_assoc();
$rows = $lista->num_rows;

if ($_POST) {
    $id_cliente = $_POST['id_clientes'];
    $pessoas = $_POST['pessoas'];
    $data_pedido = $_POST ['data_pedido'];

    $inserepedido ="INSERT INTO tbpedido_reserva
    (id_clientes, pessoas, data_pedido, status)
    VALUES
    ('$id_cliente','$pessoas','$data_pedido', 'Em Análise');
    ";

    $resultado = $conn->query($inserepedido);
}

// Fazendo a limitação da data da reserva
// Obtém a data atual
$min = new DateTime();
$max = new DateTime();

// Adiciona dois dias
$min->add(new DateInterval('P2D'));

// Adicionar 90 dias à data atual
$max->add(new DateInterval('P90D'));

// Formata a data para o padrão
$minDate = $min->format('Y-m-d');
$maxDate = $max->format('Y-m-d');

?>

<div ng-show="Registrar">
    <section>
        <article>
            <div class="row">
                <div class="col-xs-6 col-sm-6 col-sm-offset-3">
                    <h1 class="breadcrumb text-info text-center">Faça sua Reserva</h1>
                        <div class="thumbnail">
                        <br>
                            <div class="alert alert-info" role="alert">
                                <!-- ! Alteração de IA - Revisar: (01/11/2026, P4) o botão Reservar sai por PHP para a variante de
                                     quebra (quebra.php): no modo id_renomeado o id enviar vira enviar_reserva, no classe_trocada a
                                     classe btn-danger vira btn-reservar, no texto_alterado o valor vira "Reservar mesa" e no
                                     estrutura_alterada o botão sai envolvido num div.acoes no começo do formulário. Sem modo, o
                                     HTML é o de antes; o name=enviar nunca muda.
                                     ! Motivo: ficha 29, opção c (decisão 80). -->
                                <?php
                                    $quebra_enviar = '<input type="submit" id="' . quebra_id('enviar', 'enviar_reserva') . '" name="enviar" class="btn '
                                        . quebra_classe('btn-danger', 'btn-reservar') . ' btn-block" value="' . quebra_texto('Reservar', 'Reservar mesa') . '">';
                                ?>
                                <form action="registrar_reserva.php" name="reserva_login" id="reserva_login" method="POST" enctype="multipart/form-data">
                                    <?php if (quebra_estrutura()) { echo '<div class="acoes">' . $quebra_enviar . '</div>'; } ?>

                                    <label for="id_pedido">Número de Pessoas:</label>
                                    <p class="input-group">
                                        <span class="input-group-addon">
                                            <span class="glyphicon glyphicon-user text-info" aria-hidden="true"></span>
                                        </span>    
                                        <input type="number" min="1" name="pessoas" id="pessoas" class="form-control" required>
                                    </p>

                                    <label for="data_pedido">Data da Reserva:</label>     
                                    <p class="input-group">
                                        <span class="input-group-addon">
                                            <span class="glyphicon glyphicon-cutlery text-info" aria-hidden="true"></span>
                                        </span>
                                    <input type="date" name="data_pedido" id="data_pedido" class="form-control" required min="<?php echo $minDate; ?>" max="<?php echo $maxDate; ?>">
                                    </p>

                                    <label for="id_clientes">id do cliente:</label>     
                                    <p class="input-group">
                                        <input type="text" name="id_clientes" id="id_clientes" class="form-control" value="<?php echo $row['id_clientes'];?>"required>
                                    </p>

                                    <br>
                                    <hr>
                                    <?php if (!quebra_estrutura()) { echo $quebra_enviar; } ?>
                                </form>
                            </div><!-- fecha alert -->
                        </div><!-- fecha thumbnail -->
                </div><!-- fecha dimensionamento -->
            </div><!-- fecha row -->
        </article>
    </section>
</div>