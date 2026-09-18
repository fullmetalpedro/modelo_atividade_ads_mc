from app.models.usuario import carregar_usuarios


class LoginController:
    def __init__(self):
        self._usuarios = carregar_usuarios()

    def autenticar(self, nome, senha):
        for usuario in self._usuarios:
            if usuario.chama_se(nome) and usuario.conferir_senha(senha):
                return self._para_dicionario(usuario)
        return None

    def _para_dicionario(self, usuario):
        # Nenhum if de perfil aqui: cada objeto responde por si mesmo.
        return {
            'id': usuario.mostrar_id(),
            'nome': usuario.mostrar_nome(),
            'perfil': usuario.mostrar_perfil(),
            'permissoes': usuario.listar_permissoes(),
            'pode': {
                'ver_ofertas': usuario.pode_ver_ofertas(),
                'publicar_oferta': usuario.pode_publicar_oferta(),
                'moderar_ofertas': usuario.pode_moderar_ofertas(),
            },
        }
