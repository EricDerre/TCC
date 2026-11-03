<?php
// ! Alteração de IA - Revisar: arquivo novo (01/11/2026, Fase 4, pacote P4): a variante de quebra de localizador do
// front legado (ficha 29, opção c, decisão 80). O modo vem do parâmetro de URL `?quebra=<modo>` (que também grava o
// cookie `quebra`, para as páginas seguintes do mesmo roteiro) ou do cookie `quebra`, e `quebra_pagina` (parâmetro ou
// cookie) restringe o modo a uma página do site; sem um dos dois, ou com um valor
// fora dos quatro modos, toda função devolve o valor normal e o front se comporta exatamente como antes. Modos:
// id_renomeado (o id ou o atributo identificador do alvo muda de nome), classe_trocada (a classe que o localizador usa
// é trocada), texto_alterado (o texto, o valor ou o placeholder ganha uma palavra) e estrutura_alterada (o alvo é
// envolvido num contêiner novo e trocado de posição). Páginas que usam estas funções: menu_publico.php (campo de busca),
// admin/login.php (campo de login e botão Entrar), admin/produtos_lista.php (botão EXCLUIR) e
// cliente/registrar_reserva.php (botão Reservar). O harness da Fase 4 arma as mesmas quebras pelo navegador
// (Programacao/AgenteCore/experimentos/cenarios_fase4.py, QUEBRAS) e o relatório da fase compara as duas formas.
// ! Motivo: o Eric decidiu (ficha 29, opção c) que a cura de seletor fosse medida com a quebra armada no navegador E
// com uma mudança real no HTML que o PHP devolve, mantendo o front legado intocado quando a variante está desligada;
// concentrar a leitura do modo e as trocas num arquivo só deixa cada página com uma troca de uma linha por atributo.
function quebra_modo() {
    static $modo = null;
    if ($modo !== null) {
        return $modo;
    }
    $modos = array('id_renomeado', 'classe_trocada', 'texto_alterado', 'estrutura_alterada');
    $pedido = '';
    if (isset($_GET['quebra'])) {
        $pedido = $_GET['quebra'];
        if (!headers_sent()) {
            setcookie('quebra', $pedido, 0, '/');
        }
    } elseif (isset($_COOKIE['quebra'])) {
        $pedido = $_COOKIE['quebra'];
    }
    // `quebra_pagina` (parâmetro ou cookie) restringe o modo a uma página: o harness da Fase 4 manda os dois cookies,
    // porque a mutação armada no navegador só alcança a página do alvo e as duas formas precisam ser comparáveis
    // (sem ele, o modo id_renomeado da lista de produtos renomeava também o campo de login, que o roteiro atravessa)
    $pagina = '';
    if (isset($_GET['quebra_pagina'])) {
        $pagina = $_GET['quebra_pagina'];
        if (!headers_sent()) {
            setcookie('quebra_pagina', $pagina, 0, '/');
        }
    } elseif (isset($_COOKIE['quebra_pagina'])) {
        $pagina = $_COOKIE['quebra_pagina'];
    }
    $atual = isset($_SERVER['SCRIPT_NAME']) ? ltrim(str_replace('\\', '/', $_SERVER['SCRIPT_NAME']), '/') : '';
    if ($pagina !== '' && $pagina !== $atual) {
        $modo = '';
        return '';
    }
    if (in_array($pedido, $modos, true)) {
        $modo = $pedido;
        return $modo;
    }
    $modo = '';
    return '';
}

// O id (ou o nome do atributo identificador) no modo id_renomeado; senão o normal.
function quebra_id($normal, $renomeado) {
    return quebra_modo() === 'id_renomeado' ? $renomeado : $normal;
}

function quebra_atributo($normal, $renomeado) {
    return quebra_id($normal, $renomeado);
}

// A classe no modo classe_trocada; senão a normal.
function quebra_classe($normal, $trocada) {
    return quebra_modo() === 'classe_trocada' ? $trocada : $normal;
}

// O texto, o valor ou o placeholder no modo texto_alterado; senão o normal.
function quebra_texto($normal, $alterado) {
    return quebra_modo() === 'texto_alterado' ? $alterado : $normal;
}

// Verdadeiro só no modo estrutura_alterada: a página envolve o alvo num contêiner novo e o emite em outra posição.
function quebra_estrutura() {
    return quebra_modo() === 'estrutura_alterada';
}
