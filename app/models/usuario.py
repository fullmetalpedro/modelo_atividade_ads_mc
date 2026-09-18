from app.data.usuarios_mock import USUARIOS


class Usuario:
    """Classe base: o que todo usuário do KiOferta tem.

    Guarda os dados encapsulados e, por padrão, não libera nada.
    Quem libera cada permissão são as classes filhas.
    """

    def __init__(self, id, nome, senha):
        self._id = id
        self.alterar_nome(nome)
        self.alterar_senha(senha)

    def mostrar_id(self):
        return self._id

    def mostrar_nome(self):
        return self._nome

    def alterar_nome(self, novo_nome):
        if novo_nome.strip() == '':
            raise ValueError('nome não pode ser vazio')
        self._nome = novo_nome.strip()

    def alterar_senha(self, nova_senha):
        if len(nova_senha) < 4:
            raise ValueError('senha precisa ter pelo menos 4 caracteres')
        self._senha = nova_senha

    def chama_se(self, nome):
        return self._nome.lower() == nome.strip().lower()

    def conferir_senha(self, senha):
        # A senha nunca sai da classe: de fora só dá para perguntar se confere.
        return self._senha == senha

    # --- permissões ---
    # A base é a mais restrita: não pode nada.
    # Cada filha sobrescreve só o que ela ganha a mais.

    def mostrar_perfil(self):
        return 'usuario'

    def pode_ver_ofertas(self):
        return False

    def pode_publicar_oferta(self):
        return False

    def pode_moderar_ofertas(self):
        return False

    def listar_permissoes(self):
        # Escrito uma vez aqui e herdado por todos.
        # Não pergunta o perfil: pergunta o que o objeto pode fazer.
        permissoes = []
        if self.pode_ver_ofertas():
            permissoes.append('ver_ofertas')
        if self.pode_publicar_oferta():
            permissoes.append('publicar_oferta')
        if self.pode_moderar_ofertas():
            permissoes.append('moderar_ofertas')
        return permissoes

    def __repr__(self):
        return f'{type(self).__name__}({self._nome})'


class Visitante(Usuario):
    """Só olha: vê as ofertas que os outros publicaram."""

    def mostrar_perfil(self):
        return 'visitante'

    def pode_ver_ofertas(self):
        return True


class Contribuidor(Visitante):
    """Herda tudo do visitante e ganha o direito de publicar oferta."""

    def mostrar_perfil(self):
        return 'contribuidor'

    def pode_publicar_oferta(self):
        return True


class Moderador(Contribuidor):
    """Herda tudo do contribuidor e ainda modera as ofertas dos outros."""

    def mostrar_perfil(self):
        return 'moderador'

    def pode_moderar_ofertas(self):
        return True


# Em Python a própria classe é um objeto: dá para guardar num dicionário.
PERFIS = {
    'visitante': Visitante,
    'contribuidor': Contribuidor,
    'moderador': Moderador,
}


def carregar_usuarios():
    # Único lugar que olha o texto do perfil: a hora de criar o objeto.
    return [PERFIS[u['perfil']](u['id'], u['nome'], u['senha'])
            for u in USUARIOS]
