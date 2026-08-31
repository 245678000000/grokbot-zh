import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const root = join(dirname(fileURLToPath(import.meta.url)), '../../data/localized');

function load<T = any>(name: string): T {
  return JSON.parse(readFileSync(join(root, name), 'utf8'));
}

export const pluginsFile = load('plugins.json');
export const templatesFile = load('templates.json');
export const useCasesFile = load('use-cases.json');
export const collectionsFile = load('collections.json');
export const categoriesFile = load('categories.json');
export const integrationsFile = load('integrations.json');
export const newsFile = load('news.json');
export const stats = load('stats.json');

export const plugins = pluginsFile.items as any[];
export const featuredPlugins = (pluginsFile.featured || plugins.filter((p: any) => p.featured)) as any[];
export const templates = templatesFile.items as any[];
export const freshDrops = (templatesFile.fresh || templates.slice(0, 12)) as any[];
export const useCases = useCasesFile.items as any[];
export const collections = collectionsFile.items as any[];
export const categories = categoriesFile.items as any[];
export const integrations = integrationsFile.items as any[];
export const news = newsFile.items as any[];

export function pluginBySlug(slug: string) {
  return plugins.find((p: any) => p.slug === slug);
}
export function templateBySlug(slug: string) {
  return templates.find((t: any) => t.slug === slug);
}
export function useCaseBySlug(slug: string) {
  return useCases.find((u: any) => u.slug === slug);
}
export function collectionBySlug(slug: string) {
  return collections.find((c: any) => c.slug === slug);
}
export function categoryBySlug(slug: string) {
  return categories.find((c: any) => c.slug === slug);
}
export function integrationBySlug(slug: string) {
  return integrations.find((c: any) => c.slug === slug);
}

export function byCategory(slug: string) {
  return {
    plugins: plugins.filter((p: any) => p.category === slug || (p.categories || []).includes(slug)),
    useCases: useCases.filter((u: any) => u.category === slug || (u.categories || []).includes(slug)),
    templates: templates.filter(
      (t: any) => t.primary_category === slug || (t.tags || []).includes(slug),
    ),
  };
}

export function byIntegration(slug: string) {
  const has = (arr: any[]) =>
    (arr || []).some((i: any) => (typeof i === 'string' ? i === slug : i.slug === slug));
  return {
    plugins: plugins.filter((p: any) => has(p.integrations)),
    useCases: useCases.filter((u: any) => has(u.integrations)),
    templates: templates.filter((t: any) => has(t.integrations)),
  };
}

export const SITE = {
  name: 'Grok Bot 中文目录',
  tagline: '你的 Grok Bot 本可以做的一切',
  description:
    '即用的 Grok Bot 提示词、插件与合集。独立社区中文目录，内容译自 grokbot.dev，不隶属于 xAI。',
};
