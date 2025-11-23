import es from './es.json';
import en from './en.json';

const LOCALES: Record<string, any> = { es, en };

export type Translator = (key: string) => string;

export const getTranslator = (lang: string | null): Translator => {
  const locale = LOCALES[lang || 'es'] || es;

  return (key: string) => {
    const keys = key.split('.');
    let current = locale;
    for (const k of keys) {
      if (current[k] === undefined) return key;
      current = current[k];
    }
    return current as string;
  };
};
