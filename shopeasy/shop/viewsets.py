from rest_framework import viewsets
from .models import Produto, Carrinho, ItemCarrinho, Pedido
from .serializers import ProdutoSerializer, CarrinhoSerializer, ItemCarrinhoSerializer, PedidoSerializer
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.filter(excluido=False)
    serializer_class = ProdutoSerializer


class ItemCarrinhoViewSet(viewsets.ModelViewSet):
    queryset = ItemCarrinho.objects.filter(excluido=False)
    serializer_class = ItemCarrinhoSerializer


class CarrinhoViewSet(viewsets.ModelViewSet):
    queryset = Carrinho.objects.all()
    serializer_class = CarrinhoSerializer

    @action(detail=False, methods=['post'], url_path='adicionar-item')
    def adicionar_item(self, request):
        # Busca sempre o primeiro carrinho
        carrinho = Carrinho.objects.first()

        if not carrinho:
            return Response({"error": "Nenhum carrinho encontrado."}, status=status.HTTP_404_NOT_FOUND)

        # Obtém os dados da requisição
        dados = request.data
        produto_id = dados.get("produto")
        quantidade = dados.get("quantidade", 1)

        if not produto_id:
            return Response({"error": "Produto é obrigatório."}, status=status.HTTP_400_BAD_REQUEST)

        # Verifica se o item já está no carrinho
        item, created = ItemCarrinho.objects.get_or_create(
            carrinho=carrinho, produto_id=produto_id,
            defaults={"quantidade": quantidade}
        )

        if not created:
            # Se já existe, apenas aumenta a quantidade
            item.quantidade += quantidade
            item.save()

        # ✅ Atualiza o preço total após adicionar
        carrinho.atualizar_preco_total()

        return Response({"message": "Item adicionado ao carrinho."}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['delete'], url_path='remover-item/(?P<produto_id>\d+)')
    def remover_item(self, request, produto_id=None):
        # Busca sempre o primeiro carrinho
        carrinho = Carrinho.objects.first()

        if not carrinho:
            return Response({"error": "Nenhum carrinho encontrado."}, status=status.HTTP_404_NOT_FOUND)

        # Tenta encontrar o item no carrinho
        item = carrinho.itemcarrinho_set.filter(produto_id=produto_id).first()

        if not item:
            return Response({"error": "Item não encontrado no carrinho."}, status=status.HTTP_404_NOT_FOUND)

        # Se a quantidade for maior que 1, apenas reduz 1
        if item.quantidade > 1:
            item.quantidade -= 1
            item.save()
        else:
            # Se a quantidade for 1, remove o item do carrinho
            item.delete()

        # ✅ Atualiza o preço total após remover
        carrinho.atualizar_preco_total()

        return Response({"message": "Item removido do carrinho."}, status=status.HTTP_200_OK)




class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

    @action(detail=True, methods=['post'])
    def pagar(self, request, pk=None):
        pedido = get_object_or_404(Pedido, pk=pk)
        
        if pedido.status == "pago":
            return Response({'mensagem': 'Este pedido já foi pago.'}, status=status.HTTP_400_BAD_REQUEST)
        
        pedido.status = "pago"
        pedido.save()
        
        # Excluir o carrinho associado ao pedido
        Carrinho.objects.filter(usuario=pedido.usuario).delete()
        
        return Response({'mensagem': 'Pagamento confirmado! Pedido marcado como pago.'}, status=status.HTTP_200_OK)

