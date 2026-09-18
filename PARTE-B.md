# Parte B — Onde aplicamos encapsulamento e herança no KiOferta

## 1. Encapsulamento

Encapsular é esconder o dado e obrigar quem está de fora a passar por um método
que valida. No KiOferta isso aparece em todas as models.

### O atributo nunca é público

Todas as models usam `_` no atributo e dão dois métodos: um para mostrar e outro
para alterar.

| Classe | Atributos protegidos | Métodos de acesso |
|---|---|---|
| `Produto` | `_id`, `_nome`, `_categoria`, `_preco` | `mostrar_*` / `alterar_nome`, `alterar_preco` |
| `Mercado` | `_id`, `_nome`, `_lat`, `_lng` | `mostrar_*` / `alterar_nome`, `alterar_localizacao` |
| `Oferta` | `_id`, `_produto`, `_mercado`, `_novo_preco` | `mostrar_*` / `alterar_preco` |
| `Usuario` | `_id`, `_nome`, `_senha` | `mostrar_id`, `mostrar_nome` / `alterar_nome`, `alterar_senha` |

### A validação mora dentro da classe

`app/models/produto.py` — não existe produto com nome vazio nem preço negativo:

```python
def alterar_preco(self, novo_preco):
    if novo_preco < 0:
        raise ValueError('preço não pode ser negativo')
    self._preco = novo_preco
```

E o `__init__` chama o próprio `alterar_preco` em vez de fazer `self._preco = preco`.
Assim a regra vale também na hora de criar o objeto — não dá para nascer errado.

`app/models/mercado.py` — latitude entre -90 e 90, longitude entre -180 e 180.

`app/models/oferta.py` — a regra de negócio do app: oferta tem que ser mais barata
que o preço normal do produto.

```python
if novo_preco >= self._produto.mostrar_preco():
    raise ValueError('oferta precisa ser mais barata que o preço normal')
```

Repare que a `Oferta` pergunta o preço ao `Produto` pelo método `mostrar_preco()`.
Ela não vai lá pegar `produto._preco`. Um objeto conversa com o outro pela porta
da frente.

### O caso mais forte: a senha (`app/models/usuario.py`)

A senha é o único atributo que **não tem getter nenhum**. Não existe
`mostrar_senha()`. De fora só dá para fazer uma pergunta:

```python
def conferir_senha(self, senha):
    # A senha nunca sai da classe: de fora só dá para perguntar se confere.
    return self._senha == senha
```

O `LoginController` compara a senha sem nunca ter a senha na mão. É encapsulamento
resolvendo um problema real de segurança, não só arrumação de código.

### Encapsulamento também nos controllers

`self._produtos` e `self._usuarios` são protegidos, e `_para_dicionario()` é um
método interno: quem usa o controller chama `listar()` ou `autenticar()`, e não
precisa saber como a lista está guardada por dentro.

---

## 2. Herança — o módulo de login

A pergunta que o app faz é "o que esse usuário pode fazer?". Quem responde é a
classe do objeto.

```
Usuario            (base: não pode nada)
   └── Visitante          + ver ofertas
         └── Contribuidor       + publicar oferta
               └── Moderador         + moderar ofertas
```

É uma corrente: cada filha herda tudo da anterior e **sobrescreve só o método da
permissão que ela ganha a mais**. O `Moderador` tem três permissões e escreveu
uma linha.

```python
class Usuario:
    def pode_ver_ofertas(self):
        return False
    def pode_publicar_oferta(self):
        return False
    def pode_moderar_ofertas(self):
        return False

class Visitante(Usuario):
    def pode_ver_ofertas(self):
        return True          # só isso muda

class Contribuidor(Visitante):
    def pode_publicar_oferta(self):
        return True          # só isso muda

class Moderador(Contribuidor):
    def pode_moderar_ofertas(self):
        return True          # só isso muda
```

**A base é a mais restrita de propósito.** Se amanhã alguém criar um perfil novo e
esquecer de configurar, ele nasce sem poder nada. O erro é seguro.

### Código escrito uma vez e herdado por todos

`listar_permissoes()` está só na classe `Usuario` e funciona para as três filhas,
porque pergunta *o que o objeto pode*, e não *qual é o perfil dele*:

```python
def listar_permissoes(self):
    permissoes = []
    if self.pode_ver_ofertas():
        permissoes.append('ver_ofertas')
    ...
```

### Polimorfismo: o controller não pergunta o perfil

```python
def _para_dicionario(self, usuario):
    return {
        'perfil': usuario.mostrar_perfil(),
        'permissoes': usuario.listar_permissoes(),
        ...
    }
```

O controller trata `bia`, `ana` e `caio` exatamente igual. Cada objeto responde
diferente porque é de uma classe diferente. **Não existe nenhum `if perfil ==` no
controller nem nas rotas.**

### O único lugar que olha o texto do perfil

O mock guarda `'moderador'` como texto. A conversão de texto para classe acontece
em um lugar só, na hora de criar o objeto:

```python
PERFIS = {
    'visitante': Visitante,
    'contribuidor': Contribuidor,
    'moderador': Moderador,
}

def carregar_usuarios():
    return [PERFIS[u['perfil']](u['id'], u['nome'], u['senha'])
            for u in USUARIOS]
```

Depois que o objeto existe, ninguém mais pergunta o perfil.

---

## 3. Como a herança aparece na resposta da API

Mesma rota, mesmo controller, três respostas diferentes — a diferença é só a classe:

| Login | Classe | `permissoes` |
|---|---|---|
| bia / bia123 | `Visitante` | `["ver_ofertas"]` |
| ana / ana123 | `Contribuidor` | `["ver_ofertas", "publicar_oferta"]` |
| caio / caio123 | `Moderador` | `["ver_ofertas", "publicar_oferta", "moderar_ofertas"]` |
