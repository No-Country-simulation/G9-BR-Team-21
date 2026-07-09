# Guia de Boas Práticas — Git & GitHub
### EnergiAI · Hackathon ONE G9

Este guia existe para evitar os erros mais comuns de quem está começando a trabalhar em equipe com Git: perder alterações, gerar conflitos de merge desnecessários e subir código na branch errada. Siga essa rotina e a maioria dos problemas nem vai acontecer.

---

## A estrutura de branches do projeto

```
main                    ← versão estável/final, só recebe merge de "develop"
 └── develop             ← branch de integração dos dois times
      ├── develop-backend       ← só o time de Back-End trabalha aqui
      └── develop-datascience   ← só o time de Data Science trabalha aqui
```

**Regra de ouro:** ninguém trabalha direto na `main` nem na `develop`. Cada pessoa trabalha na branch do seu time (`develop-backend` ou `develop-datascience`), e o merge para `develop` acontece via Pull Request, não direto.

---

## Feature branches (uma branch por entregável)

Além das branches fixas do time, use **feature branches temporárias** para desenvolver uma parte específica e delimitada do sistema (um endpoint, uma etapa do modelo, uma integração). Ela nasce da branch do seu time, vive só enquanto essa parte está sendo feita, e é apagada depois de mesclada:

```
develop-backend
     │
     ├─── cria ───► feature/endpoint-analise-energetica
     │                        │
     │                        │ (trabalha, commita)
     │                        │
     │◄─── PR + merge ────────┘
     │
     └─── (branch da feature é apagada)
```

**1. Parta sempre da branch do seu time atualizada**

```bash
git checkout develop-backend
git pull origin develop-backend
```

**2. Crie a feature branch**

```bash
git checkout -b feature/endpoint-analise-energetica
```

O `-b` cria e já troca para ela. Padrão de nome: `feature/nome-descritivo-curto`, minúsculo, hífen no lugar de espaço.

**3. Trabalhe e commite normalmente nela**

```bash
git add .
git commit -m "Implementa validação de entrada do endpoint"
git push -u origin feature/endpoint-analise-energetica
```

**4. Quando terminar, abra PR de volta pra `develop-backend`** (veja a seção de Pull Request abaixo)

**5. Depois do merge, apague a feature branch**

```bash
git checkout develop-backend
git pull origin develop-backend
git branch -d feature/endpoint-analise-energetica
```

Ela já cumpriu o papel — manter ela viva só polui a lista de branches (aquele monte de branch velha que aparece na aba "Stale" do GitHub).

**Quando abrir uma nova feature branch:** pergunte "isso é uma unidade de trabalho que faz sentido revisar e mesclar de uma vez só?". Se sim, é uma feature nova. Se for só uma etapa dentro de algo maior, ela entra na feature que já existe — não é necessário (nem recomendado) criar uma branch para cada tarefa pequena do board.

---

## A rotina de todo dia (decore esses 4 passos)

Antes de começar a mexer em qualquer coisa, **sempre**, nessa ordem:

### 1. Verifique em qual branch você está

```bash
git branch
```

A branch atual aparece com um `*` na frente. Se não for a sua (ex: `develop-backend`), troque:

```bash
git checkout develop-backend
```

### 2. Atualize a branch local antes de mexer em qualquer coisa

```bash
git pull origin develop-backend
```

Isso traz para o seu computador tudo que os colegas já subiram, **antes** de você começar a escrever código em cima. É o passo que mais evita conflito de merge — se você programa em cima de uma versão desatualizada, quando for subir depois seu código pode "brigar" com o que os outros já mudaram.

> ⚠️ Se pular esse passo com frequência, é praticamente garantido que em algum momento vai dar conflito.

### 3. Trabalhe e commit com frequência

Não acumule um dia inteiro de trabalho em um commit só. Prefira commits pequenos e frequentes, cada um representando uma mudança que faz sentido sozinha:

```bash
git add .
git commit -m "Adiciona endpoint de análise energética"
```

**Mensagens de commit boas:**
- Comece com um verbo no presente: "Adiciona", "Corrige", "Remove", "Ajusta"
- Seja específico: `"Corrige validação do campo consumo_kwh"` é melhor que `"fix"` ou `"ajustes"`

### 4. Suba suas alterações

```bash
git push origin develop-backend
```

Se for a primeira vez que essa branch é enviada para o GitHub, pode ser necessário:

```bash
git push -u origin develop-backend
```

(o `-u` só precisa ser usado uma vez; depois disso, `git push` sozinho já basta)

---

## Antes de dar push, dê pull de novo

Se você ficou um tempo trabalhando sem sincronizar, é bem possível que um colega tenha subido algo enquanto isso. Antes do `push`, rode o `pull` de novo:

```bash
git pull origin develop-backend
git push origin develop-backend
```

Se aparecer conflito nesse `pull`, resolva ele **antes** de subir (veja a seção de conflitos abaixo).

---

## Como integrar o trabalho na `develop` (ou de uma feature branch)

Quando uma parte do trabalho estiver pronta e estável, o caminho correto **não é** dar merge direto pelo terminal — é abrir um **Pull Request (PR)** no GitHub. O `git push` sozinho não cria PR automaticamente; é uma funcionalidade da plataforma GitHub, não do Git em si, então precisa de um passo extra.

### Passo a passo pra abrir o PR

Depois do `git push`, existem duas formas fáceis de chegar na tela de criar o PR:

**Opção 1 — link direto que aparece no terminal**

Na maioria das vezes, logo depois do `git push` de uma branch nova, o próprio terminal já mostra um link pronto:

```
remote: Create a pull request for 'feature/endpoint-analise-energetica' on GitHub by visiting:
remote:      https://github.com/seu-usuario/energiai/pull/new/feature/endpoint-analise-energetica
```

Basta clicar (ou colar) esse link no navegador.

**Opção 2 — pelo site do GitHub**

1. Entre no repositório no GitHub
2. Vá na aba **"Pull requests"**
3. Clique em **"New pull request"**
4. Em **base**, escolha para onde o código vai (`develop-backend`, `develop-datascience`, ou `develop` no caso de merge entre times)
5. Em **compare**, escolha de onde o código vem (sua feature branch, ou a branch do seu time)
6. Escreva um título e uma descrição curta do que foi feito
7. Clique em **"Create pull request"**

### Depois de criado

O PR fica aberto esperando revisão. Alguém do time olha o código (aba "Files changed" mostra o diff), comenta se achar algo, e só depois de aprovado é que alguém clica em **"Merge pull request"** — aí sim o código entra oficialmente na branch de destino.

Isso dá uma chance de alguém revisar o código antes dele entrar na branch de integração, e fica um histórico claro de quando cada parte foi incorporada.

> 💡 Existe automação para criar PR direto do terminal sem passar pelo navegador (GitHub CLI, comando `gh pr create`), mas é um recurso extra e opcional. Para quem está começando, vale pegar o jeito pelo site primeiro — é visual, dá pra ver o diff e comentar com mais clareza.

---

## Como evitar conflitos de merge (na prática)

Conflito acontece quando duas pessoas alteram **a mesma linha do mesmo arquivo** em branches diferentes. Formas de reduzir isso ao mínimo:

- **Sempre dê `pull` antes de começar a trabalhar** (passo 2 da rotina acima) — é a causa nº 1 de conflito evitável
- **Respeite as fronteiras de pasta**: quem está em `develop-backend` só mexe em `backend/`; quem está em `develop-datascience` só mexe em `datascience/`. Times diferentes não devem editar os mesmos arquivos
- **Commits pequenos e frequentes** geram menos divergência acumulada do que um commit gigante uma vez por semana
- **Combine no grupo** antes de mexer em arquivos compartilhados, como o `README.md` da raiz ou o `.gitignore`

### Se mesmo assim der conflito

O Git vai marcar o arquivo com algo assim:

```
<<<<<<< HEAD
sua versão do código
=======
versão do colega
>>>>>>> develop-backend
```

Não entre em pânico — abra o arquivo, decida junto com quem gerou o conflito qual trecho deve ficar (ou combine os dois), apague as marcações (`<<<<<<<`, `=======`, `>>>>>>>`) manualmente, depois:

```bash
git add .
git commit -m "Resolve conflito entre X e Y"
```

Se travar, é melhor chamar alguém do time para resolver junto do que tentar sozinho sob pressão — resolver conflito errado pode apagar trabalho de um colega sem querer.

---

## Erros comuns de quem está começando

| Erro | Consequência | Como evitar |
|---|---|---|
| Trabalhar direto na `main` ou `develop` | Código instável vai para a branch principal sem revisão | Sempre trabalhe na branch do seu time |
| Não dar `pull` antes de começar | Conflitos de merge desnecessários | Sempre `pull` antes de codar (passo 2) |
| Commits gigantes, uma vez por semana | Difícil revisar, difícil resolver conflito, difícil reverter se algo quebrar | Commits pequenos e frequentes |
| Mensagem de commit tipo `"mudanças"` ou `"asdasd"` | Ninguém entende o histórico depois | Mensagens curtas mas descritivas |
| Editar arquivo de outro time sem avisar | Conflito e retrabalho | Respeitar a divisão `backend/` vs `datascience/` |
| Resolver conflito sem entender o que está apagando | Perda de código de um colega | Chamar quem fez a outra parte antes de resolver |

---

## Comandos essenciais — cola rápida

```bash
git branch                              # ver em qual branch você está
git checkout nome-da-branch             # trocar de branch
git pull origin nome-da-branch          # atualizar do GitHub antes de trabalhar
git status                              # ver o que foi alterado
git add .                               # preparar tudo que foi alterado
git commit -m "mensagem descritiva"     # salvar as alterações localmente
git push origin nome-da-branch          # enviar para o GitHub
git log --oneline                       # ver histórico resumido de commits
```

---

## Resumo em uma frase

**Antes de mexer:** confira a branch certa e dê `pull`. **Depois de mexer:** commit pequeno e descritivo, `pull` de novo, depois `push`, e integre via Pull Request — nunca merge direto na `develop` ou `main`.