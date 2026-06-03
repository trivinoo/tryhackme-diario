# Estudo Diario de Cybersecurity

## 2026-05-28 - TryHackMe: Introduction to Cyber Security

Hoje comecei a organizar minha progressao no TryHackMe.

Progresso atual:

- Rank: Top 80%
- Badges: 1
- Streak: 1
- Rooms completos: 4
- Path: Introduction to Cyber Security, 8% completo

Rooms completos:

### What is Networking?

Aprendi os fundamentos de redes de computadores: como dispositivos se comunicam, por que redes existem e como a informacao trafega entre sistemas. Esse conteudo e base para entender internet, IP, DNS, protocolos, portas e seguranca de rede.

### Careers in Cyber

Vi que cybersecurity tem varias trilhas profissionais, nao apenas hacking. Existem areas como SOC, blue team, red team, pentest, forense digital, resposta a incidentes, governanca, cloud security e threat intelligence.

### Offensive Security Intro

Introducao ao lado ofensivo da seguranca. O foco foi entender como atacantes pensam, como vulnerabilidades podem ser encontradas e como ethical hacking e usado legalmente para testar e melhorar sistemas.

### Defensive Security Intro

Introducao ao lado defensivo. Aprendi sobre monitoramento, deteccao, analise de logs, resposta a incidentes e protecao de sistemas contra ameacas.

Resumo do dia:

Hoje eu vi a diferenca entre seguranca ofensiva e defensiva, entendi melhor as possibilidades de carreira em cyber e comecei a reforcar a base tecnica com networking. O proximo passo natural e continuar em Network Fundamentals, especialmente Intro to LAN, OSI Model, IP, DNS e protocolos.

## 2026-06-01 - TryHackMe: Network Fundamentals

Hoje continuei estudando fundamentos de rede no TryHackMe, com foco em dois assuntos importantes para entender como a internet funciona na pratica: DNS e HTTP.

Rooms estudados:

### DNS in Detail

Aprendi como o DNS ajuda a transformar nomes de sites em enderecos IP. A ideia principal e que humanos usam nomes como `tryhackme.com`, mas os computadores precisam encontrar o IP correto para se conectar ao servidor.

Pontos principais:

- DNS funciona como uma agenda da internet, traduzindo dominios para IPs.
- Existem diferentes tipos de registros DNS, como `A`, `AAAA`, `CNAME`, `MX` e `TXT`.
- A resolucao DNS pode passar por varias etapas, incluindo cache, servidor recursivo, root servers, TLD servers e authoritative name servers.
- DNS e essencial para acessar sites, enviar emails e encontrar servicos na rede.
- Entender DNS tambem ajuda em cyber, porque muitos ataques, investigacoes e configuracoes passam por dominios, subdominios e registros DNS.

### HTTP in Detail

Aprendi como o navegador pede conteudo para um servidor web usando HTTP. Esse protocolo define como cliente e servidor conversam para carregar paginas, APIs, imagens e outros recursos.

Pontos principais:

- HTTP usa um modelo de request e response.
- O cliente envia uma requisicao para o servidor, e o servidor responde com conteudo e um status code.
- Metodos HTTP comuns incluem `GET`, `POST`, `PUT` e `DELETE`.
- Status codes ajudam a entender o resultado da requisicao, como `200 OK`, `301 Redirect`, `403 Forbidden`, `404 Not Found` e `500 Internal Server Error`.
- Headers carregam informacoes extras sobre a requisicao ou resposta, como tipo de conteudo, cookies, autenticacao e cache.
- HTTPS adiciona criptografia com TLS, protegendo melhor os dados em transito.

Resumo do dia:

Hoje eu aprofundei dois conceitos que aparecem o tempo todo em cybersecurity. DNS mostra como os nomes viram destinos reais na rede, e HTTP mostra como navegadores e servidores trocam informacoes. Esses fundamentos vao ser importantes para estudar web security, analise de logs, investigacao de trafego, phishing, subdomain enumeration e testes com ferramentas como Burp Suite e Wireshark.

## 2026-06-03 - TryHackMe: Web Fundamentals

Hoje estudei um capitulo sobre como websites funcionam e comecei a conectar desenvolvimento web com seguranca. Tambem usei este video como apoio de estudo: https://www.youtube.com/watch?v=iWoiwFRLV4I

Topicos estudados:

### How websites work

Aprendi que, quando acesso um site, o navegador faz uma requisicao para um servidor web. O servidor responde com dados que o navegador interpreta e renderiza na tela.

Pontos principais:

- O navegador representa o lado do cliente.
- O servidor web representa o lado do servidor.
- O front end e a parte que o navegador renderiza para o usuario.
- O back end processa requisicoes e retorna respostas.
- A comunicacao web depende do ciclo request e response.

### HTML

Revisei que HTML e a estrutura basica de uma pagina web. Ele organiza o conteudo usando elementos e tags.

Pontos principais:

- `<!DOCTYPE html>` define o documento como HTML5.
- `<html>` e o elemento raiz da pagina.
- `<head>` guarda metadados, como o titulo da pagina.
- `<body>` contem o conteudo visivel no navegador.
- Tags como `<h1>`, `<p>`, `<button>` e `<img>` estruturam textos, botoes e imagens.
- Atributos como `class`, `id` e `src` adicionam informacoes aos elementos.

### JavaScript

Aprendi que JavaScript adiciona interatividade as paginas. Enquanto HTML cria a estrutura e CSS cuida do estilo, JavaScript controla comportamentos dinamicos.

Pontos principais:

- JavaScript pode alterar conteudo na pagina em tempo real.
- Scripts podem ser adicionados com a tag `<script>`.
- `document.getElementById()` permite selecionar um elemento da pagina.
- Eventos como `onclick` executam acoes quando o usuario interage com a pagina.
- JavaScript e essencial para sites modernos, mas tambem pode criar riscos quando usado sem cuidado.

### Sensitive Data Exposure

Vi que informacoes sensiveis podem ficar expostas quando desenvolvedores deixam dados no codigo fonte do front end, como comentarios, links escondidos ou credenciais de teste.

Pontos principais:

- O codigo enviado ao navegador pode ser visto pelo usuario.
- Comentarios HTML podem revelar informacoes que deveriam ter sido removidas.
- Credenciais, endpoints internos e links escondidos nunca devem ficar no codigo client-side.
- Uma das primeiras etapas ao analisar um site e verificar o codigo fonte.

### HTML Injection

Aprendi que HTML Injection acontece quando uma aplicacao exibe entrada do usuario sem filtrar ou sanitizar corretamente. Se o site aceitar HTML como entrada e renderizar isso na pagina, o usuario pode alterar a aparencia ou o comportamento do conteudo exibido.

Pontos principais:

- Nunca se deve confiar diretamente no input do usuario.
- Entrada sem sanitizacao pode permitir que alguem injete tags HTML.
- HTML Injection e uma vulnerabilidade client-side.
- Esse conceito ajuda a entender vulnerabilidades mais avancadas, como Cross-Site Scripting.

Resumo do dia:

Hoje conectei a base de web com seguranca. Entendi melhor como navegador, servidor, HTML e JavaScript trabalham juntos, e comecei a ver como pequenos erros no front end podem virar falhas de seguranca. Os pontos mais importantes foram: revisar o codigo fonte, nao expor dados sensiveis no cliente e sempre validar ou sanitizar entrada do usuario.
