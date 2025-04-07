from rest_framework import viewsets
from shop.models import Produto, Carrinho, ItemCarrinho, Pedido
from .serializers import ProdutoSerializer, CarrinhoSerializer, ItemCarrinhoSerializer, PedidoSerializer
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.filter(excluido=False)
    serializer_class = ProdutoSerializer

    def destroy(self, request, *args, **kwargs):
        produto = self.get_object()
        produto.excluido = True
        produto.save()
        return Response({"detail": "Produto excluído com sucesso."}, status=status.HTTP_204_NO_CONTENT)


class ItemCarrinhoViewSet(viewsets.ModelViewSet):
    queryset = ItemCarrinho.objects.filter(excluido=False)
    serializer_class = ItemCarrinhoSerializer


class CarrinhoViewSet(viewsets.ModelViewSet):
    queryset = Carrinho.objects.all()
    serializer_class = CarrinhoSerializer

    @action(detail=False, methods=['post'], url_path='adicionar-item')
    def adicionar_item(self, request):
        carrinho = Carrinho.objects.first()

        if not carrinho:
            return Response({"error": "Nenhum carrinho encontrado."}, status=status.HTTP_404_NOT_FOUND)

        dados = request.data
        produto_id = dados.get("produto")
        quantidade = dados.get("quantidade", 1)

        if not produto_id:
            return Response({"error": "Produto é obrigatório."}, status=status.HTTP_400_BAD_REQUEST)

        #verifica se o item ja esta no carrinho
        item, created = ItemCarrinho.objects.get_or_create(
            carrinho=carrinho, produto_id=produto_id,
            defaults={"quantidade": quantidade}
        )
        #aumenta a quantidade se ja existir
        if not created:
            
            item.quantidade += quantidade
            item.save()

        carrinho.atualizar_preco_total()

        return Response({"message": "Item adicionado ao carrinho."}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['delete'], url_path='remover-item')
    def remover_item(self, request):
        produto_id = request.data.get("produto")
        quantidade = request.data.get("quantidade", 1)

        if not produto_id:
            return Response({"error": "ID do produto é obrigatório."}, status=status.HTTP_400_BAD_REQUEST)

        carrinho = Carrinho.objects.first()  
        if not carrinho:
            return Response({"error": "Nenhum carrinho encontrado."}, status=status.HTTP_404_NOT_FOUND)

        item = carrinho.itens.filter(produto_id=produto_id).first()

        if not item:
            return Response({"error": "Item não encontrado no carrinho."}, status=status.HTTP_404_NOT_FOUND)

        if item.quantidade > quantidade:
            item.quantidade -= quantidade
            item.save()
        else:
            item.delete()

        carrinho.atualizar_preco_total()

        return Response({"message": "Item removido do carrinho."}, status=status.HTTP_200_OK)






class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.filter(excluido=False)
    serializer_class = PedidoSerializer

    @action(detail=True, methods=['post'])
    def pagar(self, request, pk=None):
        pedido = get_object_or_404(Pedido, pk=pk)
        
        if pedido.status == "pago":
            return Response({'mensagem': 'Este pedido já foi pago.'}, status=status.HTTP_400_BAD_REQUEST)
        
        pedido.status = "pago"
        pedido.save()
        
        #excluir o carrinho dps do pedido
        Carrinho.objects.filter(usuario=pedido.usuario).delete()
        
        return Response({'mensagem': 'Pagamento confirmado! Pedido marcado como pago.'}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        pedido = self.get_object()
        pedido.excluido = True
        pedido.save()
        return Response({"detail": "Pedido excluído com sucesso."}, status=status.HTTP_204_NO_CONTENT)