class TagDAO:

    def ajouter_tag(self, tag: str, schema: str):
        pass

    def supprimer_tag(self, tag: str, schema: str):
        pass

    def consulter_tags(self, schema: str):
        pass

    def rechercher_tags_par_son(self, id_freesound: str, schema: str):
        pass

    def ajouter_association_son_tag(self, id_freesound: str, tag: str, schema: str):
        pass

    def supprimer_association_son_tag(self, id_freesound: str, tag: str, schema: str):
        pass

    def check_if_son_has_tag(self, id_freesound: str, tag: str, schema: str):
        pass
