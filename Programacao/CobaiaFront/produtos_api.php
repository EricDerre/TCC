<?php ?>
<!-- ! Alteração de IA - Revisar -->
<!--
Página nova (não substitui nenhuma existente): mesma estrutura/layout do
resto do CobaiaFront (menu_publico.php/rodape.php, mesmo Bootstrap), mas o
grid de produtos é populado via fetch() na CobaiaAPI (Python/FastAPI, porta
8000) em vez de consulta SQL direta — é o alvo "sistema moderno" (JSON real
via HTTP) do agente, complementar ao restante do site (que fica intocado).
-->
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="css/bootstrap.min.css">
    <link rel="stylesheet" href="css/estilo.css">
    <link rel="shortcut icon" type="imagex/png" href="../Chuleta/images/logo churrascaria.png">
    <title>Churrascaria Fornalha - Produtos (API)</title>
</head>
<body class="fundofixo">

    <!-- Area de menu -->
    <?php include 'menu_publico.php'; ?>
    <main class="container">

        <h2 class="breadcrumb alert-danger"><strong>Produtos via API</strong></h2>

        <div id="produtos-api-status" class="text-center text-muted">Carregando produtos da CobaiaAPI...</div>
        <div id="produtos-api-grid" class="row"></div>

        <!-- rodapé -->
        <footer class="panel-footer" style="background: none;">
            <?php include 'rodape.php'; ?>
            <a name="contato"></a>
        </footer>
    </main>

    <!-- Modal de detalhes (populado via fetch em /api/produtos/{id}) -->
    <div class="modal fade" id="modalDetalhe" role="dialog">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <button class="close" data-dismiss="modal" type="button">&times;</button>
                    <h4 id="modalDetalheTitulo"></h4>
                </div>
                <div class="modal-body" id="modalDetalheCorpo"></div>
            </div>
        </div>
    </div>
</body>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
<script src="js/bootstrap.min.js"></script>
<script>
    // ! Alteração de IA - Revisar
    var COBAIA_API_BASE = "http://localhost:8000";

    function formatarPreco(preco) {
        var n = Number(preco);
        return isNaN(n) ? String(preco) : "R$ " + n.toFixed(2).replace(".", ",");
    }

    function cartaoProduto(p) {
        var destaqueTexto = (p.destaque === true) ? "Sim" : (p.destaque === false ? "Não" : String(p.destaque));
        return (
            '<div class="col-sm-6 col-md-4">' +
                '<div class="thumbnail">' +
                    (p.imagem ? '<img src="images/' + p.imagem + '" class="img-responsive img-rounded">' : '') +
                    '<div class="caption text-right">' +
                        '<h3 class="text-danger"><strong>' + (p.nome || '(sem nome)') + '</strong></h3>' +
                        '<p class="text-warning"><strong>' + (typeof p.tipo === "object" ? JSON.stringify(p.tipo) : p.tipo) + '</strong></p>' +
                        '<p class="text-left">' + (p.resumo || '') + '</p>' +
                        '<p class="text-left"><small>destaque: ' + destaqueTexto + '</small></p>' +
                        '<p>' +
                            '<button class="btn btn-default disable" style="cursor: default">' + formatarPreco(p.preco) + '</button> ' +
                            '<button class="btn btn-info btn-xs saiba-mais" data-id="' + p.id + '">Saiba Mais...</button>' +
                        '</p>' +
                    '</div>' +
                '</div>' +
            '</div>'
        );
    }

    function carregarProdutos() {
        var status = document.getElementById("produtos-api-status");
        var grid = document.getElementById("produtos-api-grid");
        fetch(COBAIA_API_BASE + "/api/produtos")
            .then(function (resp) {
                if (!resp.ok) { throw new Error("HTTP " + resp.status); }
                return resp.json();
            })
            .then(function (produtos) {
                if (!Array.isArray(produtos) || produtos.length === 0) {
                    status.textContent = "Nenhum produto retornado pela API.";
                    return;
                }
                status.textContent = "";
                grid.innerHTML = produtos.map(cartaoProduto).join("");
            })
            .catch(function (err) {
                status.textContent = "Erro ao carregar produtos da CobaiaAPI: " + err.message;
                status.className = "text-center text-danger";
            });
    }

    document.addEventListener("click", function (ev) {
        if (!ev.target.classList.contains("saiba-mais")) { return; }
        var id = ev.target.getAttribute("data-id");
        fetch(COBAIA_API_BASE + "/api/produtos/" + id)
            .then(function (resp) {
                if (!resp.ok) { throw new Error("HTTP " + resp.status); }
                return resp.json();
            })
            .then(function (p) {
                document.getElementById("modalDetalheTitulo").textContent = p.nome || ("Produto #" + id);
                document.getElementById("modalDetalheCorpo").textContent = p.resumo || "(sem descrição)";
                $("#modalDetalhe").modal("show");
            })
            .catch(function (err) {
                document.getElementById("modalDetalheTitulo").textContent = "Erro";
                document.getElementById("modalDetalheCorpo").textContent = err.message;
                $("#modalDetalhe").modal("show");
            });
    });

    carregarProdutos();
</script>
</html>
