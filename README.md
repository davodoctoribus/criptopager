# criptopager
Dinamica II do PS PET

O Criptopager é um projeto para a parte II do processo seletivo do Programa de Educação Tutorial de Engenharia de Computação (PET Eng Comp), essa fase do processo seletivo consiste num core project de cibersegurança.

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
1. Abstração da comunicação
2. Implementação de criptografia
3. Interceptação das mensagens

Aqui nesse repositório, temos apenas a implementação de duas das três etapas, pois a terceira consiste apenas em usar programas que possam capturar e analisar pacotes de dados (para esse trabalho usamos o [Wireshark](https://gitlab.com/wireshark/wireshark))

### Etapa 1: Abstração da comunicação
Fizemos uma abstração do sistema de comunicação usado por pagers utilizando o modelo Transmissor-Receptor feito, em python, com Protocolo TCP para enviar e receber mensagens de forma a replicar uma aplicação real de seu funcionamento.
Ela foi feita em duas partes, um código que é a central, que envia as mensagens, sendo esse o 'modelado/Transmissor.py'; e outro que é responsável por receber esses dados, esse sendo o 'modelado/Receptor.py'

### Etapa 2: Implementação de criptografia
Para a implementação da criptografia nos baseamos nos códigos abstraídos da etapa anterior e, a partir da implementação da biblioteca cryptography, utilizamos o módulo Fernet para fazer uma criptografia simétrica e garantir a segurança da mensagem, para que, ao pacote ser interceptado, a mensagem não possa ser lida.

## Como usar e testar

### Pré-requisitos
Antes de rodar o projeto, é necessário ter instalado:
- [Python 3.8 ou superior](https://www.python.org/downloads/)
- A biblioteca `cryptography`, usada apenas na versão com criptografia. Para instalá-la, rode:
  ```bash
  pip install cryptography
  ```
- (Opcional, apenas para reproduzir a etapa de interceptação) [Wireshark](https://www.wireshark.org/download.html) instalado na máquina.

Não é necessário instalar mais nada além disso: a versão sem criptografia (`modelado/`) usa apenas bibliotecas nativas do Python (`socket`, `json`, `threading`, `time`).

### Rodando a versão sem criptografia (`modelado/`)
Essa versão simula a comunicação original dos pagers, sem nenhuma proteção — é a que evidencia o problema descrito na seção "Fundamentação".

1. Abra um terminal e inicie a central (Transmissor):
   ```bash
   cd modelado
   python Transmissor.py
   ```
2. Abra um ou mais terminais adicionais e inicie um pager (Receptor) em cada um:
   ```bash
   cd modelado
   python Receptor.py
   ```
   Ao rodar, será pedido um capcode — esse é o identificador daquele pager (ex: `001`, `002`). Pode-se abrir vários receptores com capcodes diferentes para simular vários pagers recebendo o mesmo broadcast.
3. De volta ao terminal do Transmissor, informe o capcode de destino e a mensagem. Todos os pagers conectados recebem os dados transmitidos, mas apenas o pager cujo capcode corresponde exibe a mensagem — os demais a descartam silenciosamente, assim como um pager real faria.

### Rodando a versão com criptografia (`criptografado/`)
O funcionamento é o mesmo da versão anterior, mudando apenas que agora a mensagem é cifrada antes de ser transmitida.

1. Inicie a central:
   ```bash
   cd criptografado
   python Transmissor.py
   ```
2. Inicie um ou mais pagers em terminais separados:
   ```bash
   cd criptografado
   python Receptor.py
   ```
3. Envie mensagens normalmente pelo Transmissor. O conteúdo agora trafega cifrado pela rede, e só é decifrado no pager de destino, que possui a mesma chave simétrica usada para a criptografia.

> A chave usada está fixa diretamente no código (variável `CHAVE`), o que é suficiente para os fins de demonstração deste projeto. Em uma aplicação real, essa chave precisaria ser gerada e distribuída de forma segura entre os dispositivos, e não deixada exposta no código-fonte.

### Reproduzindo a etapa de interceptação (Wireshark)
Essa etapa não depende de nenhum código adicional — o Wireshark captura o tráfego diretamente da rede.

1. Abra o Wireshark e selecione a interface de rede correspondente (use a interface `Loopback`/`lo` caso esteja testando tudo na mesma máquina).
2. Aplique um filtro para focar apenas no tráfego do projeto, por exemplo:
   ```
   tcp.port == 5060
   ```
3. Inicie a captura antes de rodar o Transmissor e o Receptor.
4. Envie uma mensagem pelo Transmissor.
5. No Wireshark, clique com o botão direito sobre o pacote TCP capturado e selecione **Follow → TCP Stream** para visualizar o conteúdo transmitido.

**Resultado esperado em cada versão:**
- Rodando a partir da pasta `modelado/`: o conteúdo da mensagem aparece em texto legível dentro do JSON capturado.
- Rodando a partir da pasta `criptografado/`: o campo da mensagem aparece como uma sequência de caracteres cifrados, sem forma de ler o conteúdo original sem a chave.

## Estrutura do projeto
```
.
├── criptografado/
│   ├── Receptor.py
│   └── Transmissor.py
├── modelado/
│   ├── Receptor.py
│   └── Transmissor.py
└── README.md
```

## Equipe
Amanda de Lima e Oliveira, Francisco Davi Moreira e Kaio Lopes Vieira Luz
