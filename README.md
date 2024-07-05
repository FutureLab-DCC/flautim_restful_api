# Flautim: um tutorial

Flautim é uma plataforma que facilita a realiação de experimentos em Aprendizado Federado. Neste tutorial, vamos te mostrar como a plataforma te auxilia a treinar modelos colaborativamente sem abrir mão da privacidade dos dados.

## O que você vai precisar:

- Um conjunto de dados no formato adequado e a=uma classe Dataset para sua leitura.
- Um arquivo .py com o código da API para seu modelo.
- Um arquivo .py contendo os hiperparâmetros do seu modelo.

Para realizar seu treino federado em nossa plataforma, faça o seguinte:

## Passo a passo

1) Acesse a plataforma: Entre na sua conta e navegue até a página de Experimentos dentro de seu projeto e clique em "Adicionar modelo" para começar.

2) Preencha os dados do experimento: Escolha um nome para o experimento e selecione seu modelo e dataset. Você deverá implementar uma classe Dataset para a leitura dos seus dados. Você também pode, opcionalmente, adicionar uma descrição sobre o que será feito.

3) Envie seu código API: Adicione seu código da API. Este código define como o modelo irá interagir com os dados distribuídos e realizar o treinamento colaborativo, a partir de uma biblioteca qbaseada em PyTorch e Flower.

4) Envie o arquivo de hiperparâmetros: Clique no botão "Adicionar" nessa seção e escolha o arquivo .py que contém os hiperparâmetros do seu modelo.

5) Treine seu modelo: Revise as informações inseridas e, quando tudo estiver certo, clique no botão "Executar experimento". A plataforma irá iniciar o processo, treinando seu modelo de forma distribuída e segura.

6) Monitore o progresso: Acompanhe o progresso do treinamento na página do seu modelo. Você poderá ver o tempo restante, a acurácia do modelo e outras métricas importantes na aba "Saídas". A plataforma também possibilita um acompanhamento mais detalhado com os logs de treino na aba "Logs". 

7) Avalie e utilize: Uma vez que o treinamento for concluído, você poderá baixar o modelo treinado na aba "Modelos". Além disso, avalie o desempenho do seu modelo e utilizá-lo para fazer previsões ou tomar decisões, com base na duração total do treinamento e na loss e acurácia do modelo ao longo desse treino.

Seguindo esses simples passos, você poderá treinar seus modelos com colaboração, mantendo a privacidade dos seus dados. Confira nossos exemplos, como a implementação para o dataset MNIST para ver na prática como a plataforma funciona!


# FAQ

- *O que é a Flautim?*
    A Flautim é uma plataforma poderosa que facilita a realização de experimentos em Aprendizado Federado, permitindo que você treine modelos de machine learning de forma colaborativa sem abrir mão da privacidade dos dados.

- *Quais são os benefícios de usar a Flautim?*
    - Treinamento colaborativo: Treine modelos com dados de diferentes fontes sem compartilhar os dados brutos, preservando a privacidade.
    - Simplicidade: Interface amigável e intuitiva facilita o uso da plataforma, mesmo para iniciantes em Aprendizado Federado. Se você já treinou algum modelo de Aprendizado de M´quina, você consegue utilizar a plataforma sem problemas!
    - Flexibilidade: Suporta diversos modelos de machine learning e permite personalização do processo de treinamento.
    - Escalabilidade: Treine modelos em larga escala de forma eficiente e segura.
    - Segurança: Proteja seus dados e modelos com recursos de segurança robustos.

- *Como posso entrar em contato com o suporte do Flautim?*
    Se você tiver dúvidas ou precisar de ajuda, entre em contato com a equipe de suporte do Flautim através do email placeholder@email.com.

##  Erros comuns
1. Sincronização de Pesos:
    Problema: Inconsistência na atualização dos pesos dos modelos locais e globais.
    Solução: Garantir que os pesos dos modelos locais sejam corretamente enviados ao servidor e que o servidor os agregue adequadamente antes de enviar os pesos globais atualizados de volta aos clientes.

2. Heterogeneidade de Dados:
    Problema: Diferenças significativas na distribuição de dados entre os clientes podem levar a modelos globais que não generalizam bem.
    Solução: Implementar técnicas de balanceamento de dados ou ajuste de amostragem para garantir que os dados sejam mais uniformemente distribuídos entre os clientes.

3. Configuração de Hiperparâmetros:
    Problema: Escolha inadequada de hiperparâmetros pode resultar em convergência lenta ou sobreajuste/subajuste do modelo.
    Solução: Realizar validação cruzada e ajuste de hiperparâmetros para encontrar as configurações ótimas para o treinamento federado.

4. Incompatibilidade de Tamanho de Tensor:
    Problema: Geralmente, diferença na arquitetura do modelo esperada ou nas dimensões de entrada entre as duas rodadas.
    Solução: Garantir que todos os clientes no setup de aprendizado federado usem exatamente a mesma arquitetura de modelo e etapas de pré-processamento de dados, com processos consistentes de carregamento do modelo em todas as rodadas de treinamento. Garantir tamanhos de entrada e as configurações do modelo sejam idênticos ao inicializar o modelo para cada rodada.

- Links para os exemplos
