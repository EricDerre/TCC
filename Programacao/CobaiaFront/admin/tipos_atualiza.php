<?php 
include 'acesso_com.php';
include '../conn/connect.php';

if($_POST){ 

    $id_tipo = $_POST['id_tipo'];
    $sigla_tipo = $_POST['sigla_tipo'];
    $rotulo_tipo = $_POST['rotulo_tipo'];

    $id = $_POST['id_tipo'];
    
    $updateSql = "update tbtipos
                  set id_tipo = '$id_tipo',
                  sigla_tipo = '$sigla_tipo',
                  rotulo_tipo = '$rotulo_tipo'
                  where id_tipo = $id; ";

    $resultado = $conn->query($updateSql);
    if($resultado){
        header('location: tipos_lista.php');
    }
}

if($_GET){
    $id_form = $_GET['id_tipo'];
}else{
    $id_form = 0;
}
$lista = $conn->query("select * from tbtipos where id_tipo = $id_form");
$row = $lista->fetch_assoc();
$numRows = $lista->num_rows;


?>

<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="../css/bootstrap.min.css">
    <link rel="stylesheet" href="../css/estilo.css">
    <title>Tipos - insere</title>
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
                    Alterando o Tipo
                </h2>
                <div class="thumbnail">
                    <div class="alert alert-info" role="alert">
                        <form action="tipos_atualiza.php" method="post" name="form_tipos_insere" enctype="multipart/form-data" id="form_tipos_insere" value="<?php echo $row['id_tipo'] ?>">
                            <input type="hidden" name="id_tipo" id="id_tipo" value="<?php echo $row['id_tipo']?>">
                            <label for="rotulo_tipo">Tipo:</label>
                            <div class="input-group">
                                <span class="input-group-addon">
                                    <span class="glyphicon glyphicon-tasks" aria-hidden="true"></span>
                                </span>

                                <input type="text" name="rotulo_tipo" id="rotulo_tipo" class="form-control" placeholder="Digite o tipo do produto" maxlength="100" required value="<?php echo $row['rotulo_tipo']?>">
                            </div>

                            <label for="sigla_tipo">Sigla:</label>     
                            <div class="input-group">
                                <span class="input-group-addon">
                                    <span class="glyphicon glyphicon-cutlery" aria-hidden="true"></span>
                                </span>
                                <input type="text" name="sigla_tipo" id="sigla_tipo" class="form-control" placeholder="Digite a descrição do produto" maxlength="3" required value="<?php echo $row['sigla_tipo']?>">
                            </div>
                    

                            <hr>
                            <input type="submit" id="atualizar" name="atualizar" class="btn btn-success btn-block" value="Atualizar">
                        
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