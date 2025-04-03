from rest_framework.routers import DefaultRouter
from .viewsets import ProdutoViewSet, CarrinhoViewSet, ItemCarrinhoViewSet, PedidoViewSet

router = DefaultRouter()
router.register(r'produtos', ProdutoViewSet)
router.register(r'carrinhos', CarrinhoViewSet)
router.register(r'itens-carrinho', ItemCarrinhoViewSet)
router.register(r'pedidos', PedidoViewSet)
