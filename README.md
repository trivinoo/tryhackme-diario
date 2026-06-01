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
