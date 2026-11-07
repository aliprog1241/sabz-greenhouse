export type Category = { id: number; name: string; slug: string; parent: number | null };
export type MediaImage = { id: number; image: string; alt_text: string; sort_order: number };
export type Product = {
  id: number; name: string; slug: string; brand: string; unit: string; category: Category;
  is_featured: boolean; primary_image?: MediaImage | null; sku?: string; description?: string;
  specifications?: Record<string, string | number>; images?: MediaImage[];
};
export type Service = { id: number; title: string; slug: string; summary: string; description: string; is_featured: boolean; sort_order: number };
export type Project = { id: number; title: string; slug: string; location: string; completed_on: string | null; challenge: string; actions: string; results: string; is_featured: boolean; is_demo: boolean; images: MediaImage[] };
export type Certificate = { id: number; title: string; issuer: string; issued_on: string | null; description: string; image: string | null; is_demo: boolean };
export type Paginated<T> = { count: number; next: string | null; previous: string | null; results: T[] };
export type SubmissionResponse = { success: boolean; tracking_code: string; status: string };
