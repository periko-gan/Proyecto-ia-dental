/**
 * Mapeo de nombres de problemas dentales al español
 * Basado en los problemas detectados por la IA
 */

export const problemTranslations = {
  cavity: 'Caries',
  caries: 'Caries',
  decay: 'Caries dental',

  filling: 'Empaste',
  restoration: 'Restauración defectuosa',
  crown: 'Corona',

  implant: 'Implante',

  plaque: 'Placa bacteriana',
  placa: 'Placa bacteriana',
  tartar: 'Sarro',
  calculus: 'Cálculo dental',

  periodontitis: 'Periodontitis',
  gingivitis: 'Gingivitis',
  inflammation: 'Inflamación',
  inflamation: 'Inflamación',

  endodontic: 'Problema endodóntico',
  pulp: 'Afección pulpar',
  abscess: 'Absceso',

  bone_loss: 'Pérdida ósea',
  resorption: 'Resorción',

  fracture: 'Fractura',
  broken: 'Diente fracturado',

  malocclusion: 'Maloclusión',
  misalignment: 'Desalineación',

  normal: 'Saludable',
  healthy: 'Saludable',
  impacted: 'Diente impactado',
};

export const problemColors = {
  cavity: '#EF4444',
  caries: '#EF4444',
  decay: '#DC2626',

  filling: '#F59E0B',
  restoration: '#F59E0B',
  crown: '#F59E0B',

  implant: '#8B5CF6',

  plaque: '#F97316',
  placa: '#F97316',
  tartar: '#EA580C',
  calculus: '#EA580C',

  periodontitis: '#EC4899',
  gingivitis: '#EC4899',
  inflammation: '#F43F5E',
  inflamation: '#F43F5E',

  endodontic: '#06B6D4',
  pulp: '#06B6D4',
  abscess: '#0369A1',

  bone_loss: '#A78BFA',
  resorption: '#A78BFA',

  fracture: '#6B21A8',
  broken: '#6B21A8',

  malocclusion: '#06B6D4',
  misalignment: '#06B6D4',

  normal: '#10B981',
  healthy: '#10B981',
  impacted: '#8B5CF6',
};

function removeDiacritics(value) {
  return value.normalize('NFD').replace(/[\u0300-\u036f]/g, '');
}

function normalizeProblemKey(value) {
  if (!value) return '';

  return removeDiacritics(String(value)
    .toLowerCase()
    .trim()
    .replace(/\([^)]*\)/g, '')
    .replace(/[0-9]+%?/g, '')
    .replace(/[^a-z\s_-]/g, ' ')
    .replace(/[\s-]+/g, '_')
    .replace(/_+/g, '_')
    .replace(/^_+|_+$/g, ''));
}

function resolveProblemName(problemInput) {
  if (!problemInput) return '';

  if (typeof problemInput === 'object') {
    return problemInput.label || problemInput.className || problemInput.name || '';
  }

  return String(problemInput);
}

function findTranslationByContains(normalizedKey) {
  if (!normalizedKey) return '';

  const entries = Object.entries(problemTranslations);
  const exact = entries.find(([key]) => key === normalizedKey);
  if (exact) return exact[1];

  const partial = entries.find(([key]) => normalizedKey.includes(key) || key.includes(normalizedKey));
  return partial ? partial[1] : '';
}

/**
 * Obtiene la traducción de un nombre de problema
 * Si no existe, devuelve el nombre original
 */
export function translateProblem(problemInput) {
  const rawName = resolveProblemName(problemInput);
  if (!rawName) return 'Hallazgo detectado';

  const normalized = normalizeProblemKey(rawName);
  const translated = findTranslationByContains(normalized);

  return translated || rawName;
}

/**
 * Obtiene el nivel de severidad basado en el nombre del problema
 */
export function getProblemSeverity(problemInput) {
  const rawName = resolveProblemName(problemInput);
  const normalized = normalizeProblemKey(rawName);

  if (normalized.includes('critical') || normalized.includes('crítico')) return 'critical';
  if (normalized.includes('caries') || normalized.includes('abscess') || normalized.includes('fracture') || normalized.includes('decay')) return 'critical';
  if (normalized.includes('plaque') || normalized.includes('tartar') || normalized.includes('inflamation') || normalized.includes('inflammation') || normalized.includes('gingivitis')) return 'warning';
  if (normalized.includes('normal') || normalized.includes('healthy')) return 'success';

  return 'warning';
}

/**
 * Mapea severidad a colores y badges
 */
export const severityConfig = {
  critical: {
    color: 'error',
    label: 'CRÍTICO',
    className: 'border-error ring-error/20',
  },
  warning: {
    color: 'warning',
    label: 'SEGUIMIENTO',
    className: 'border-warning ring-warning/20',
  },
  success: {
    color: 'success',
    label: 'ÓPTIMO',
    className: 'border-success/50 ring-success/20',
  },
};

export function getProblemColor(problemInput) {
  const rawName = resolveProblemName(problemInput);
  const normalized = normalizeProblemKey(rawName);

  const entries = Object.entries(problemColors);
  const exact = entries.find(([key]) => key === normalized);
  if (exact) return exact[1];

  const partial = entries.find(([key]) => normalized.includes(key));
  if (partial) return partial[1];

  return '#6B7280';
}
