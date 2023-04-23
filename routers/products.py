from fastapi import APIRouter, status

router = APIRouter(prefix="/products",
                   tags=["products"],  # sirve para agrupar la documentacion
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})

products_list = ["Producto 1", "Producto 2", "Producto 3", "Producto 4", "Producto 5"]


@router.get("/")  # como el router tiene un prefix /products, al indicar '/' vamos a esa ruta.
async def products():
    return products_list


@router.get("/{id}")
async def products(id: int):
    return products_list[id-1]
