from app.data.usuarios_mock import USUARIOS


class Usuario:
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
        return self._senha == senha

    def mostrar_perfil(self):
        raise NotImplementedError('cada perfil define o seu proprio nome')

    def pode_ver_ofertas(self):
        return False

    def pode_publicar_oferta(self):
        return False

    def pode_moderar_ofertas(self):
        return False

    def listar_permissoes(self):
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
    def mostrar_perfil(self):
        return 'visitante'

    def pode_ver_ofertas(self):
        return True


class Contribuidor(Visitante):
    def mostrar_perfil(self):
        return 'contribuidor'

    def pode_publicar_oferta(self):
        return True


class Moderador(Contribuidor):
    def mostrar_perfil(self):
        return 'moderador'

    def pode_moderar_ofertas(self):
        return True


PERFIS = {
    'visitante': Visitante,
    'contribuidor': Contribuidor,
    'moderador': Moderador,
}


def carregar_usuarios():
    return [PERFIS[u['perfil']](u['id'], u['nome'], u['senha'])
            for u in USUARIOS]
