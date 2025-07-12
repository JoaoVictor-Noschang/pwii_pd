# ➕💚 PlusLife Web

O PlusLife é um site web desenvolvido para auxiliar usuários a monitorar e manter um estilo de vida saudável, registrando atividades físicas, alimentação e hidratação. Ele oferece as seguintes funcionalidades (Requisitos Funcionais):
- [RF1] O sistema deve manter usuários.
- [RF2] O sistema deve manter registros de bem estar mental do usuário.
- [RF3] O sistema deve manter registros de refeições do usuário.
- [RF4] O sistema deve manter registros de tipos de refeições.
- [RF5] O sistema deve manter registros de hidratação do usuário.
- [RF6] O sistema deve manter registros de exercícios do usuário.
- [RF7] O sistema deve manter registros de tipos de exercícios.
- [RF8] O sistema deve calcular IMC (Indice de massa corporal).
- [RF9] O sistema deve manter um histórico de IMCs (Indice de massa corporal).

<br>

## Utilizou-se o seguinte DER (Diagrama Entidade Relacionamento)

<p align="center">
  <img src="./der/der_pluslife.jpg" alt="Login" />
  
</p>

<br>

# 🤓 Como rodar o projeto?

Para executar o *PlusLife* em sua máquina, siga os passos abaixo:

1.  *Clone o Repositório:*
    Abra seu terminal ou prompt de comando e execute:
    bash
    git clone [https://github.com/JoaoVictor-Noschang/pdmii_projeto_disciplina.git](https://github.com/JoaoVictor-Noschang/pdmii_projeto_disciplina.git)
    
<br>

2.  *Instale as Dependências:*
    Navegue até o diretório do projeto clonado e instale todas as dependências necessárias com:

    Abrindo a página do projeto
    bash
    cd pdmii_projeto_disciplina
    

    Instalando as dependências
    bash
    npm install
    

<br>

3.  *Inicie o Aplicativo:*
    Após a instalação das dependências, você pode iniciar o projeto com:
    bash
    npx expo start
    
    Este comando abrirá o Metro Bundler no seu terminal, onde você poderá escanear o QR code com o aplicativo Expo Go no seu celular ou usar um emulador.

<br>


# 💾 Tecnologia em Análise e Desenvolvimento de Sistemas

5° Semestre - IFMT Campus Campo Verde.  
Projeto para a Disciplina de *Programação de Dispositivos Móveis II*

---

### 💡 Autores
- [João Victor](https://github.com/JoaoVictor-Noschang)


<br>

## 🔧 Features mínimas

Além disso o sistema deve cumprir os seguinte requisitos:
- Possuir 5 telas;

    - ✅ Projeto possui 8 telas: Login, cadastro, home, registro de refeições, de hidratação, de exercícios, calculadora de IMC e perfil do usuário.

- Possuir pelo menos 1 microsserviço;

    - ✅ A lógica do IMC é feita por uma API externa que recebe os dados e retorna o resultado do calculo e a informação de acordo com o resultado.

- Possuir Persistência de dados (local, BD, nuvem, ou outro).

    - ✅ Utiliza persistência de dados local com o SQLite.

<br>

# 🖥 Tecnologias Utilizadas

Este projeto foi construído utilizando as seguintes tecnologias e bibliotecas:

* *React Native:* Framework para desenvolvimento de aplicativos móveis multiplataforma.
* *Expo Go:* Ferramenta que facilita o desenvolvimento, teste e implantação de aplicativos React Native.
* *Expo Router:* Biblioteca de roteamento baseada em arquivos para navegação entre as telas do aplicativo.
* *Expo SQLite:* Biblioteca que oferece acesso a um banco de dados local SQLite, utilizado para persistência de dados.
* *Figma:* Ferramenta de design utilizada para prototipagem e criação das interfaces do usuário.

<br>

## Bibliotecas do Expo

Foram utilizadas algumas bibliotecas nativas do Expo Go, os quais foram necessárias a instalação de suas dependências, estão descritas a seguir.


### Iniciando um projeto Expo GO em branco com JS

1. Para iniciar o projeto em branco utilizando JavaScript, utilizou-se o comando de criação de projeto do Expo a partitr de um template em branco:

   <pre><code>npx create-expo-app@latest --template</code></pre>
   
   Após o comando o terminar solicita que escolha qual template será usado, e então escolheu-se o tamplate:

   <pre><code>blank</code></pre>

   Ao escolher, irá finalizar a instalação e configuração dos arquivos do Expo Go com um projeto em branco.

2. Após, o projeto foi iniciado, para verificar se tudo foi instalado corretamente, e para configurar aplicativo do celular para a renderização do projeto.

   <pre><code>npx expo start</code></pre>

<br>

### Incluindo a biblioteca Expo Router ao projeto

É uma biblioteca de roteamento baseada em arquivos para React Native.
Será a biblioteca resposável por mapear e lidar com a navegação entre as páginas do projeto.

1. Para intalar no projeto utiliza-se o seguinte comando:

   <pre><code>npx expo install expo-router react-native-safe-area-context react-native-screens expo-linking expo-constants expo-status-bar</code></pre>

<br>

### Incluindo a biblioteca Expo SQLite ao projeto

Uma biblioteca que fornece acesso a um banco de dados que pode ser consultado por meio de uma API SQLite.
Responsável por fazer a comunicação entre aaplicação e um banco de dado local utilizando SQLite.

1. Para intalar no projeto utiliza-se o seguinte comando:

   <pre><code>npx expo install expo-sqlite</code></pre>

<br>

---