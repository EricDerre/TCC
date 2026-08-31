<?php 
include 'acesso_com.php';
include '../conn/connect.php';

if($_POST){

    $id_tipo = $_POST['id_tipo'];
    $sigla_tipo = $_POST['sigla_tipo'];
    $rotulo_tipo = $_POST['rotulo_tipo'];


    $inseretipo ="INSERT INTO tbtipos
                  (id_tipo, sigla_tipo, rotulo_tipo)
                  VALUES
                  ('$id_tipo','$sigla_tipo','$rotulo_tipo');
                  ";

    $resultado = $conn->query($inseretipo);

    // Após a gravação bem sucedida do produto, volta (Atualiza) lista

    if(mysqli_insert_id($conn)){
        header('location: tipos_lista.php');
    }
}
    // Selecionar os dados de chave estrangeira (lista de tipos de produtos)
    
    $consulta_fk = "select * from tbtipos order by rotulo_tipo asc";
    $lista_fk = $conn->query($consulta_fk);
    $row_fk = $lista_fk->fetch_assoc();
    $nlinhas = $lista_fk->num_rows;


?>

<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="../css/bootstrap.min.css">
    <link rel="stylesheet" href="../css/estilo.css">
    <title>Tipos - Insere</title>
</head>
<body class="fundoadm">
    <?php include 'menu_adm.php';?>

    <main class="container">
        <div class="row">
            <div class="col-xs-12 col-sm-offset-2 col-sm-6 col-md-8">
                <h2 class="breadcrumb text-info">
                    <a href="tipos_lista.php">
                        <button class="btn btn-info">
                            <span class="glyphicon glyphicon-chevron-left"></span>
                        </button>
                    </a>
                    Inserindo o Tipo
                </h2>
                <div class="thumbnail">
                    <div class="alert alert-info" role="alert">
                        <form action="tipos_insere.php" method="post" name="form_produto_insere" enctype="multipart/form-data" id="form_produto_insere">
                            <label for="id_tipo">Tipo:</label>
                            <div class="input-group">
                                <span class="input-group-addon">
                                    <span class="glyphicon glyphicon-tasks" aria-hidden="true"></span>
                                </span>

                                <input type="text" name="rotulo_tipo" id="rotulo_tipo" class="form-control" placeholder="Digite o tipo do produto" maxlength="20" required>
                            </div>

                            <label for="sigla_tipo">Sigla:</label>     
                            <div class="input-group">
                                <span class="input-group-addon">
                                    <span class="glyphicon glyphicon-cutlery" aria-hidden="true"></span>
                                </span>
                                <input type="text" name="sigla_tipo" id="sigla_tipo" class="form-control" placeholder="Digite a sigla do tipo" maxlength="3" required>
                            </div>

                           
                            <br>
                            <hr>
                            <input type="submit" id="enviar" name="enviar" class="btn btn-success btn-block" value="Cadastrar">
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </main>

    <!-- Script para imagem -->
<script>
document.getElementById("imagem_produto").onchange = function(){
    var reader = new FileReader();
    if(this.files[0].size>528385){
        alert("A imagem deve ter no máximo 500KB");
        $("#imagem").attr("src", "blank");
        $("#imagem").hide();
        $("#imagem_produto").wrap('<form>').closest('form').get(0).reset();
        $("#imagem_produto").unwrap();
        return false
    }

    if(this.files[0].type.indexOf('image')== 1){
        alert("Formato inválido, escolha uma imagem!");
        $("#imagem").attr("src", "blank");
        $("#imagem").hide();
        $("#imagem_produto").wrap('<form>').closest('form').get(0).reset();
        $("#imagem_produto").unwrap();
        return false
    }

    reader.onload = function(e){
        document.getElementById("imagem").src = e.target.result
        $("#imagem").show();
    }

    reader.readAsDataURL(this.files[0]);
}
</script>
</body>
</html>
