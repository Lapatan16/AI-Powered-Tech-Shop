export interface SubCategoryModel {
  id: number;
  name: string;
}

export interface CategoryTreeModel {
  id: number;
  name: string;
  sub_categories: SubCategoryModel[];
}