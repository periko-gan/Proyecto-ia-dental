/**
 * Mapeo de nombres de problemas dentales al español
 * Basado en los problemas detectados por la IA
 */

export const problemTranslations = {
    cavity: 'Caries',
    filling: 'Empaste',
    implant: 'Implante',
    impacted: 'Diente impactado',
}

export const problemColors = {
    cavity: '#EF4444',
    // caries: '#EF4444',

    filling: '#F59E0B',
    // empaste: '#F59E0B',

    implant: '#12457EFF',
    // implante: '#8B5CF6',

    impacted: '#8B5CF6',
    // impactado: '#8B5CF6',
}

function removeDiacritics(value) {
    // Elimina acentos para comparaciones más tolerantes.
    return value.normalize('NFD').replace(/[\u0300-\u036f]/g, '')
}

function normalizeProblemKey(value) {
    if (!value) return ''

    // Normaliza a snake_case para facilitar el matching.
    return removeDiacritics(
        String(value)
            .toLowerCase()
            .trim()
            .replace(/\([^)]*\)/g, '')
            .replace(/[0-9]+%?/g, '')
            .replace(/[^a-z\s_-]/g, ' ')
            .replace(/[\s-]+/g, '_')
            .replace(/_+/g, '_')
            .replace(/^_+|_+$/g, ''),
    )
}

function resolveProblemName(problemInput) {
    if (!problemInput) return ''

    // Soporta objetos de detección y strings simples.
    if (typeof problemInput === 'object') {
        return problemInput.label || problemInput.className || problemInput.name || ''
    }

    return String(problemInput)
}

function findTranslationByContains(normalizedKey) {
    if (!normalizedKey) return ''

    // Primero intenta matching exacto.
    const entries = Object.entries(problemTranslations)
    const exact = entries.find(([key]) => key === normalizedKey)
    if (exact) return exact[1]

    // Luego intenta matching parcial para variaciones menores.
    const partial = entries.find(
        ([key]) => normalizedKey.includes(key) || key.includes(normalizedKey),
    )
    return partial ? partial[1] : ''
}

/**
 * Obtiene la traducción de un nombre de problema
 * Si no existe, devuelve el nombre original
 */
export function translateProblem(problemInput) {
    const rawName = resolveProblemName(problemInput)
    if (!rawName) return 'Hallazgo detectado'

    const normalized = normalizeProblemKey(rawName)
    const translated = findTranslationByContains(normalized)

    return translated || rawName
}

/**
 * Obtiene el nivel de severidad basado en el nombre del problema
 */
export function getProblemSeverity(problemInput) {
    const rawName = resolveProblemName(problemInput)
    const normalized = normalizeProblemKey(rawName)

    if (normalized.includes('critical') || normalized.includes('crítico')) return 'critical'
    if (
        normalized.includes('caries') ||
        normalized.includes('abscess') ||
        normalized.includes('fracture') ||
        normalized.includes('decay')
    )
        return 'critical'
    if (
        normalized.includes('plaque') ||
        normalized.includes('tartar') ||
        normalized.includes('inflamation') ||
        normalized.includes('inflammation') ||
        normalized.includes('gingivitis')
    )
        return 'warning'
    if (normalized.includes('normal') || normalized.includes('healthy')) return 'success'

    return 'warning'
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
}

// Mapear problemas específicos a un color/tema (clase DaisyUI)
export const problemColorMap = {
    cavity: 'error',
    caries: 'error',
    decay: 'error',
    filling: 'primary',
    implant: 'success',
    plaque: 'warning',
    tartar: 'warning',
    calculus: 'warning',
    abscess: 'error',
    fracture: 'error',
    crown: 'primary',
    restoration: 'primary',
    periodontitis: 'warning',
    gingivitis: 'warning',
    normal: 'success',
    healthy: 'success',
}

export function getProblemColor(problemInput) {
    const raw = resolveProblemName(problemInput)
    const normalized = normalizeProblemKey(raw)
    return problemColorMap[normalized] || 'warning'
}

export function getProblemBorderClass(problemInput) {
    const color = getProblemColor(problemInput)
    return `border-${color} ring-${color}/20`
}

export function getProblemBadgeClass(problemInput) {
    const color = getProblemColor(problemInput)
    return `badge-${color}`
}

export function getProblemHexColor(problemInput) {
    const rawName = resolveProblemName(problemInput)
    const normalized = normalizeProblemKey(rawName)

    const entries = Object.entries(problemColors)
    const exact = entries.find(([key]) => key === normalized)
    if (exact) return exact[1]

    const partial = entries.find(([key]) => normalized.includes(key))
    if (partial) return partial[1]

    return '#6B7280'
}
