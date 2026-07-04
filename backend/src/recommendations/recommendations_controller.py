from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated

from .recommendations_service import RecommendationsService
from .recommendations_models import AiAutocompleteRequest, AiProductPredictionResponse

from ..products.products_models import ProductsPreviewModel
from ..users.users_models import UserResponseModel
from ..auth.auth_dependencies import get_current_user
from ..recommendations.recommendations_dependencies import get_rec_service

router = APIRouter(prefix='/recommendations', tags=["Recommendations"])

@router.get('/for-you', response_model=list[ProductsPreviewModel])
async def get_for_you_recommendations(
    rec_service: Annotated[RecommendationsService, Depends(get_rec_service)],
    current_user: UserResponseModel = Depends(get_current_user)
):
    return await rec_service.get_personalized_recommendations_async(current_user.id)

@router.post('/autofill', response_model=AiProductPredictionResponse)
async def autocomplete_product_fields(
    payload: AiAutocompleteRequest,
    rec_service: Annotated[RecommendationsService, Depends(get_rec_service)],
    current_user: UserResponseModel = Depends(get_current_user)
):
    try:
        return await rec_service.autocomplete_product_fields_async(payload.user_prompt)
    except ValueError as ex:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(ex)
        )