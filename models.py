from database import db


class Contato(db.Model):
    __tablename__ = "contatos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    telefone = db.Column(db.String, nullable=False, unique=True)
    
    def __repr__(self):
        return f"<{self.nome}>"