<?php 
include 'acesso_com.php';
include '../conn/connect.php';

if($_POST){

    $id_usuario = $_POST['id_usuario'];
    $login_usuario = $_POST['login_usuario'];
    $senha_usuario = $_POST ['senha_usuario'];
    $nivel_usuario = $_POST['nivel_usuario'];


    $insereusuario ="INSERT INTO tbusuarios
                  (id_usuario, login_usuario, senha_usuario, nivel_usuario)
                  VALUES
                  ('$id_usuario','$login_usuario','$senha_usuario', '$nivel_usuario');
                  ";

    $resultado = $conn->query($insereusuario);

    // Após a gravação bem sucedida do produto, volta (Atualiza) lista

    if(mysqli_insert_id($conn)){
        header('location: usuarios_lista.php');
    }
}

$consulta_fk = "select * from tbusuarios order by login_usuario asc";
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
    <title>Usuarios - Insere</title>
</head>
<body class="fundoadm">
    <?php include 'menu_adm.php';?>

    <main class="container">
        <div class="row">
            <div class="col-xs-12 col-sm-offset-2 col-sm-6 col-md-8">
                <h2 class="breadcrumb text-info">
                    <a href="usuarios_lista.php">
                        <button class="btn btn-info">
                            <span class="glyphicon glyphicon-chevron-left"></span>
                        </button>
                    </a>
                    Inserindo o Usuario
                </h2>
                <div class="thumbnail">
                    <div class="alert alert-info" role="alert">
                        <form action="usuario_insere.php" method="post" name="form_usuario_insere" enctype="multipart/form-data" id="form_usuario_insere">
                            <label for="id_usuario">LOGIN:</label>
                            <div class="input-group">
                                <span class="input-group-addon">
                                    <span class="glyphicon glyphicon-tasks" aria-hidden="true"></span>
                                </span>

                                <input type="text" name="login_usuario" id="login_usuario" class="form-control" placeholder="Digite o tipo do produto" maxlength="10" required>
                            </div>

                            <label for="senha_usuario">SENHA:</label>     
                            <div class="input-group">
                                <span class="input-group-addon">
                                    <span class="glyphicon glyphicon-cutlery" aria-hidden="true"></span>
                                </span>
                                <input type="password" name="senha_usuario" id="senha_usuario" class="form-control" placeholder="Digite a descrição do produto" maxlength="10" required>
                            </div>

                            <label for="nivel_usuario">NIVEL:</label>
                            <div class="input-group">
                                <span class="input-group-addon">
                                    <span class="glyphicon glyphicon-tasks" aria-hidden="true"></span>
                                </span>
                                <select name="nivel_usuario" id="nivel_usuario" class="form-control" required>
                                    <option value="sup">Superior</option>
                                </select>
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
