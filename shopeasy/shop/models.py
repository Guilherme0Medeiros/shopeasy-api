from django.db import models
from django.db.models import Sum, F
class ModeloBase(models.Model):
    id = models.BigAutoField(primary_key=True)  
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    excluido = models.BooleanField(default=False)

    class Meta:
        abstract = True  


#soft delete
    def excluir(self):
        
        self.excluido = True
        self.save()


#produto
class Produto(ModeloBase):
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.PositiveIntegerField()

    def __str__(self):
        return self.nome


class Carrinho(ModeloBase):
    usuario = models.OneToOneField("auth.User", on_delete=models.CASCADE, unique=True)
    produtos = models.ManyToManyField("Produto", through="ItemCarrinho")
    preco_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Carrinho de {self.usuario.username}"

    def atualizar_preco_total(self):
        total = ItemCarrinho.objects.filter(carrinho=self).aggregate(
            total=Sum(F('quantidade') * F('produto__preco'))
        )['total'] or 0
        self.preco_total = total
        self.save()

class ItemCarrinho(ModeloBase):
    carrinho = models.ForeignKey(Carrinho, on_delete=models.CASCADE, related_name="itens")
    produto = models.ForeignKey("Produto", on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome} no carrinho"

class Pedido(ModeloBase):
    usuario = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    preco_total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[
            ("pendente", "Pendente"),
            ("pago", "Pago"),
            ("enviado", "Enviado"),
            ("entregue", "E/ntregue"),
        ],
        default="pendente",
    )

    def __str__(self):
        return f"Pedido {self.id} - {self.usuario.username}"