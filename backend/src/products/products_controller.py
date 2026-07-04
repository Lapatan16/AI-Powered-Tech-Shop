from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status, Response
from typing import Annotated, List
import math
import os
import uuid

from .products_query import PaginatedEnvelope, ProductQueryParams
from .products_models import ProductsMinimalModel, ProductsPreviewModel
from .products_exceptions import ProductNotFoundError
from .products_dependencies import get_products_service
from .products_service import ProductsService

from ..users.users_models import UserResponseModel
from ..auth.auth_dependencies import get_current_user

router = APIRouter(
    prefix='/products',
    tags=["Products"]
)

@router.get(
    '/all', 
    response_model=PaginatedEnvelope[ProductsPreviewModel],
    status_code=status.HTTP_200_OK
)
async def get_all_products(
    service: Annotated[ProductsService, Depends(get_products_service)],
    params: ProductQueryParams = Depends()
):
    items, total_records = await service.get_all_products_async(params)
    total_pages = math.ceil(total_records / params.limit) if total_records > 0 else 1

    return PaginatedEnvelope(
        items=items,
        total_records=total_records,
        page=params.page,
        limit=params.limit,
        total_pages=total_pages
    )

@router.get('/{product_id}')
async def get_product_by_id(
    product_id: int,
    service: Annotated[ProductsService, Depends(get_products_service)]
):
    try:
        product = await service.get_product_by_id_async(product_id)
        return product
    except ProductNotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail={
            "error": str(e)
        })
    
UPLOAD_DIR = "static/uploads"

@router.post('/', response_model=ProductsMinimalModel)
async def create_product(
    name: Annotated[str, Form()],
    sub_category_id: Annotated[int, Form()],
    service: Annotated[ProductsService, Depends(get_products_service)],
    current_user: Annotated[UserResponseModel, Depends(get_current_user)],
    description: Annotated[str, Form()] = "",
    price: Annotated[float, Form()] = 0.0,
    stock: Annotated[int, Form()] = 0,
    discount: Annotated[float, Form()] = 0.0,
    images: List[UploadFile] = File(description="At least one product image is required")
):
    try:
        saved_image_urls = []
        
        for image in images:
            if not image.filename or image.filename.strip() == "":
                continue
                
            file_extension = os.path.splitext(image.filename)[1]
            if not file_extension:
                file_extension = ".jpg"
                
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            file_path = os.path.join(UPLOAD_DIR, unique_filename)
            
            with open(file_path, "wb+") as buffer:
                buffer.write(await image.read())
            
            saved_image_urls.append(f"/static/uploads/{unique_filename}")

        product = await service.create_product_async(
            name=name,
            description=description,
            sub_category_id=sub_category_id,
            user_id=current_user.id,
            price=price,
            stock=stock,
            discount=discount,
            image_src_list=saved_image_urls
        )
        return product
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail={"error": f"Failed to create product listing: {str(e)}"}
        )

@router.get('/categories/all')
async def get_product_categories_and_subcategories(
    service: Annotated[ProductsService, Depends(get_products_service)]
):
    return await service.get_product_categories_and_subcategories_async()

@router.delete('/{product_id}')
async def delete_product(
    product_id: int,
    service: Annotated[ProductsService, Depends(get_products_service)]
):
    await service.delete_product_async(product_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)