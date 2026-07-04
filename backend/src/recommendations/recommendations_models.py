from pydantic import BaseModel, Field

class AiAutocompleteRequest(BaseModel):
    user_prompt: str = Field(..., description="The raw natural language description provided by the user.")

class AiProductPredictionResponse(BaseModel):
    name: str = Field(..., description="A concise, optimized marketing title for the e-commerce listing.")
    description: str = Field(..., description="A professional, descriptive retail listing summary.")
    parent_category_id: int = Field(..., description="The matching main category database identifier.")
    sub_category_id: int = Field(..., description="The matching subcategory database identifier.")
    price: str = Field(..., description="The recommended listing price formatted strictly as a string decimal, e.g., '149.99'.")
    stock: str = Field(..., description="The predicted volume of available items as a string integer, e.g., '5'.")