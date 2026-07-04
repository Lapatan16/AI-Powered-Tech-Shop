export interface JwtPayloadModel {
  sub: string;
  id: number;
  exp?: number;
}

export interface AuthResponseModel {
  access_token: string;
  token_type: string;
}

export interface ApiFieldError {
  field: string;
  message: string;
}