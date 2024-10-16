# Sistema de Gestão de Pizzaria

Este projeto foi desenvolvido para modernizar o processo de gestão de pedidos da Pizzaria do Carlos, integrando soluções que tornam o dia a dia da operação mais eficiente e acessível. O sistema permite a integração de pedidos feitos via WhatsApp e ligação, além de oferecer uma série de funcionalidades que otimizam o fluxo de trabalho.


FUNCIONALIDADES PRINCIPAIS

1. Integração de Pedidos via WhatsApp
O sistema permite o recebimento de pedidos feitos diretamente pelo WhatsApp. Para isso, utiliza o link wa.me, com automação realizada pelo Selenium, que acessa a sessão do Mozilla armazenada no sistema. Isso garante agilidade e eficiência no processo de comunicação.

2. CRUD Completo de Clientes, Pizzas e Pedidos
O sistema oferece um CRUD (Create, Read, Update, Delete) completo para gerenciar clientes, pizzas e pedidos. O front-end foi desenvolvido utilizando o framework Flet, garantindo uma interface amigável e moderna.

3. Relatórios no Power BI
Relatórios interativos são gerados no Power BI, proporcionando uma visão detalhada do desempenho da pizzaria, incluindo métricas de pedidos e vendas.

4. Exportação de Dados para Excel
A exportação de dados é feita utilizando as bibliotecas Pandas e Openpyxl, permitindo que todas as informações relevantes sejam exportadas diretamente para planilhas Excel para análise adicional.

5. Acessibilidade e Inclusão
Preocupado com a acessibilidade, o sistema foi desenvolvido para ser totalmente compatível com leitores de tela, permitindo o uso por pessoas com deficiência visual. Além disso, há otimizações de cores para garantir que a interface seja acessível para pessoas com daltonismo.

6. Emissão de Recibos
O sistema também conta com a funcionalidade de emissão de recibos para cada pedido realizado, facilitando o controle e a documentação das transações.


TECNOLOGIAS UTILIZADAS

1. Flet: Framework para o desenvolvimento do front-end.
2. Python: Utilizado no desenvolvimento do back-end.
3. SQLite: Banco de dados leve e eficiente para armazenamento das informações.
4. Pandas & Openpyxl: Para exportação e manipulação de dados em Excel.
5. Selenium: Para automação do envio de mensagens via WhatsApp, utilizando a sessão salva do Mozilla.


CONCLUSÃO
Este projeto combina tecnologia, acessibilidade e automação para entregar uma solução completa de gestão para pizzarias, facilitando o processo de pedidos e oferecendo uma integração completa com o WhatsApp, relatórios interativos e exportação para Excel.
