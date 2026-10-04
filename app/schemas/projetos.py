from pydantic import BaseModel, Field

class InformacoesProjeto(BaseModel):
    titulo: str = Field(description='O título do projeto')
    link: str = Field(description='O link do projeto')
    conteudo: str = Field(description='A descrição do projeto')
    qnt_propostas: int = Field(description='A quantidade de propostas que foram enviadas')
    valor: str = Field(description='Valor do projeto')
    analise: str = Field(description='Análise do projeto de acordo com as capacidades técnicas do usuário')


class ListaProjetos(BaseModel):
    projetos: list[InformacoesProjeto] = Field(
        description="Uma lista contendo as informações detalhadas de cada projeto"
    )
