import type { Paginated } from "@/types/api";

export const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api/v1";

export async function apiGet<T>(path: string): Promise<T | null> {
  try {
    const response = await fetch(`${API_BASE}${path}`, { cache: "no-store" });
    if (!response.ok) return null;
    return (await response.json()) as T;
  } catch {
    return null;
  }
}

export function resultsOf<T>(data: Paginated<T> | T[] | null): T[] {
  if (!data) return [];
  return Array.isArray(data) ? data : data.results;
}
