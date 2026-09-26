# criptopager
Dinamica II do PS PET

O Criptopager é um projeto para a parte II do processo seletivo do Programa de Educação Tutorial de Engenharia de Computação (PET Eng Comp), essa fase do processo seletivo consiste num core project de cibersegurança.

## Índice


## Sobre o projeto
O projeto baseia-se na modelagem em código (na linguagem python) e redes da comunicação que ocorre entre dois pagers, como ela pode ser facilmente interceptada e como o uso de uma criptografia simples pode tornar esse sistema mais seguro.

## Fundamentação:
### O que são pagers:
Pagers são equipamentos que fazem comunicação por ondas de rádio em estilo broadcast, usado em hospitais como transmissor particular, que pode enviar e receber mensagens mesmo com obstáculos e paredes.
### O problema:
Pela natureza da comunicação entre pagers, a interceptação dessa comunicação pode ser feita facilmente, e esse fator unido à ausência de criptografia (dados enviados em texto bruto) resulta em mensagens facilmente interceptáveis, pois só é necessário decodificar o procolo dos dados.
### Como a criptografia ajuda:
Apesar do uso do broadcast permitir a recepção dos dados enviados da central de forma fácil, o uso da criptografia impede que o conteúdo enviado por meio dos pagers seja interceptado, ou seja, ao decodificar o protocolo haverá apenas uma mensagem criptografada, sem que seja possível visualizar seu conteúdo. 

## Funcionamento:
O projeto baseia-se em 3 etapas:
