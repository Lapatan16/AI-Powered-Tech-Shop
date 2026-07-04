import json
import os
from google import genai
from google.genai import types

from .recommendations_models import AiProductPredictionResponse

from ..database.unit_of_work import UnitOfWork
from ..products.products_models import ProductsPreviewModel 
from ..products.products_query import ProductQueryParams  

class RecommendationsService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        self.ai_client = genai.Client(api_key=os.getenv("OPENAI_API_KEY"))

    async def get_personalized_recommendations_async(self, user_id: int) -> list[ProductsPreviewModel]:
        products = await self.uow.recommendations.get_recommended_products_by_user_id_async(user_id)
        
        if not products:
            fallback_params = ProductQueryParams(
                category_id=None,
                sub_category_id=None,
                sort_by_price=None,
                page=1, 
                limit=8
            )
            
            products, _ = await self.uow.products.find_all_products_async(fallback_params)
            
        return [ProductsPreviewModel.from_entity(p) for p in products]
    
    async def autocomplete_product_fields_async(self, user_prompt: str) -> AiProductPredictionResponse:
        categories = await self.uow.products.find_product_categories_and_subcategories_async()
        
        taxonomy_guide = []
        for cat in categories:
            sub_cats = [{"sub_category_id": sc.id, "name": sc.name} for sc in cat.sub_categories]
            taxonomy_guide.append({
                "category_id": cat.id,
                "category_name": cat.name,
                "allowed_subcategories": sub_cats
            })
            
        taxonomy_json_str = json.dumps(taxonomy_guide, indent=2)

        system_instruction = (
            "You are an expert e-commerce product manager. Analyze the user's raw text description "
            "and extract structured listing fields. You MUST map the product to one correct 'sub_category_id' "
            "found within the allowed taxonomy tree below. If price or stock are not specified, estimate a logical retail value.\n\n"
            f"ALLOWED TAXONOMY TREE:\n{taxonomy_json_str}"
        )

        try:
            response = await self.ai_client.aio.models.generate_content(
                model="gemini-2.5-flash",
                contents=f"Extract fields from this description: {user_prompt}",
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.2,
                    response_mime_type="application/json",
                    response_schema=AiProductPredictionResponse,
                ),
            )
            
            return response.parsed
            
        except Exception as e:
            raise ValueError(f"AI Autofill processing failed: {str(e)}")