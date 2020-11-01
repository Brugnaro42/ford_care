# ford_care

## 1. Introdução
  O projeto *Ford Care* tem como objetivo automatizar a verificação das condições do automóvel utilizando dados gerados pelo veículo, dessa maneira, atuais donos de veículos Ford conseguiriam acompanhar a saúde do seu veículo e receberiam *insights* para prolongar a vida útil do automóvel e, consequentemente, aumentar o valor de revenda do mesmo.
  Em suma, o projeto servirá para impulsionar o valor de revenda dos produtos da Ford, aumentar a vida útil dos automóveis e proporcionar que as condições de um veículo autônomo estejam seguras mesmo sem uma averiguação humana. Portanto, nos próximos 5 anos com a ajuda da inteligência artificial e do aprendizado de máquina, a Ford poderá construir uma base para continuar garantindo a qualidade das experiências e sentimentos que cria em seus clientes por mais 100 anos. 
  

## 2. Estrutura do Projeto
  O desenvolvimento foi pensado em dois núcleos, a parte de *maintenance* e do atendimento das requisições do *app*.
  
## 2.1 Maintenance
  Esse núcleo tem como objetivo cuidar do tratamento, limpeza dos dados e treinamento dos modelos. Há de ser executado periodicamente de acordo com a frequência de atualização dos dados. Os modelos são abastecidos por dados OBD2, gerados pelos próprios veículos. Inicialmente, os treinamentos foram efetuados com dados oferecidos em um repositório do *Kaggle* (https://www.kaggle.com/cephasax/obdii-ds3), no entanto, no futuro usaremos os dados dos dispositivos que farão as requisições para a aplicação.
  Todos os modelos são devidamente treinados e exportados para a biblioteca ford_care, que conterá todas as funcionalidades para as requisições. Ainda há uma função que retorna a porcentagem de desgaste de componentes julgados como importantes (motor, transmissão, filtro de óleo e filtro de combustível). As ferramentas usadas são:

- **Ford Guesser (KNN)**: É o modelo a ser requisitado, que responde se o veículo tem o risco de criar um alerta para algum componente do trem de força;
- **Ford Classifier (KNN)**: Responsável por mostrar o alarme que provavelmente será retornado;
- **Ford Tear**: Retorna a porcentagem de desgaste dos componentes citados anteriormente, baseando-se na distância total percorrida pelo carro e vida média (em km) de cada um deles.

## 2.2 App
  Essa segunda parte cuida de receber os dados via *pymongo*, usar os modelos em *pickle* e a função *Ford Tear* para retornar os resultados para o usuário. Essa parte há de ser descrita de maneira mais detalhada futuramente.
