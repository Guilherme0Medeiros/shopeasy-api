from rest_framework import serializers
from shop.models import Produto, Carrinho, ItemCarrinho, Pedido



class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = '__all__'


class ItemCarrinhoSerializer(serializers.ModelSerializer):
    produto_nome = serializers.CharField(source='produto.nome', read_only=True)

    class Meta:
        model = ItemCarrinho
        fields = '__all__'
        extra_kwargs = {
            'carrinho': {'required': False}
        }

class CarrinhoSerializer(serializers.ModelSerializer):
    itens = ItemCarrinhoSerializer(many=True, required=False)

    class Meta:
        model = Carrinho
        fields = '__all__'

    def create(self, validated_data):
        itens_data = validated_data.pop('itens', [])
        carrinho = Carrinho.objects.create(**validated_data)

        for item in itens_data:
            ItemCarrinho.objects.create(carrinho=carrinho, **item)

        carrinho.atualizar_preco_total()
        return carrinho

    def update(self, instance, validated_data):
        itens_data = validated_data.pop('itens', [])
        instance.itens.all().delete()

        for item in itens_data:
            ItemCarrinho.objects.create(carrinho=instance, **item)

        instance = super().update(instance, validated_data)
        instance.atualizar_preco_total()
        return instance



class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'
        read_only_fields = ['preco_total']  

    def create(self, validated_data):
        usuario = validated_data['usuario']

       
        carrinho, _ = Carrinho.objects.get_or_create(usuario=usuario)

        
        preco_total = sum(item.produto.preco * item.quantidade for item in carrinho.itens.all())
  
        for item in carrinho.itens.all():
            produto = item.produto
            if produto.estoque < item.quantidade:
                raise serializers.ValidationError(
                    f"Estoque insuficiente para o produto: {produto.nome}"
                )
            produto.estoque -= item.quantidade
            produto.save()



        
        pedido = Pedido.objects.create(
            usuario=usuario,
            preco_total=preco_total,
            status="pendente"
        )

        return pedido

