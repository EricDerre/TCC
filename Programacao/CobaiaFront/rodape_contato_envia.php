<?php 
require 'PHPMailer/PHPMailerAutoload.php';

$Mail = new PHPMailer;
$Mail->isSMTP();

// CONFIGURANDO O SERVIDOR DE EMAIL

$Mail->Host       = "smtp.office365.com";
$Mail->Port       = "587";
$Mail->SMTPSecure = "STARTTLS";
$Mail->SMTPAuth   = "true";
$Mail->Username   = 'churrascariafornalha@outlook.com';
$Mail->Password   = '1234churras';
 // Define o remetente
$Mail->setFrom('churrascariafornalha@outlook.com', 'Churrascaria Fornalha');

// Define o destinatário
$Mail->addAddress('churrascariafornalha@outlook.com', 'Churrascaria Fornalha');

 // Conteúdo da mensagem
$Mail->Subject = "Email de ". $_POST['email_contato']. " Nome: " .$_POST['nome_contato'];
$Mail->Body    = $_POST['comentario_contato'];

$Mail->IsHTML (true);

if($Mail->send()){

echo "O email foi enviado com sucesso";

}
else{
    echo "falha no email" .$Mail->ErrorInfo;

}

?>