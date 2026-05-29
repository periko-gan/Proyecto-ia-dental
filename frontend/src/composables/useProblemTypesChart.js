import {computed} from 'vue'
import {useMyAnalyses} from '@/composables/useMyAnalyses'
import {useDiagnosticAnalysis} from '@/composables/useDiagnosticAnalysis'

export function useProblemTypesChart() {
    // Usar el límite máximo para traer todos los análisis
    const {analyses} = useMyAnalyses(200)
    const {currentAnalysis} = useDiagnosticAnalysis()

    // Obtener análisis únicos y completados
    const completedAnalyses = computed(() => {
        const unique = new Map()

        for (const analysis of analyses.value) {
            if (analysis?.analysisId && analysis?.status === 'COMPLETED') {
                unique.set(analysis.analysisId, analysis)
            }
        }

        if (currentAnalysis.value?.analysisId && currentAnalysis.value?.status === 'COMPLETED') {
            unique.set(currentAnalysis.value.analysisId, currentAnalysis.value)
        }

        return [...unique.values()]
    })

    // Obtener todas las detecciones
    const allDetections = computed(() => {
        return completedAnalyses.value.flatMap((analysis) => analysis?.detections ?? [])
    })

    // Contar cada tipo de problema basado en el className
    const problemCounts = computed(() => {
        const counts = {
            caries: 0,
            empaste: 0,
            implante: 0,
            impactado: 0,
        }

        for (const detection of allDetections.value) {
            // Usar className que es el campo correcto
            const className = (detection?.className ?? '').toLowerCase()

            if (className.includes('cavity')) {
                counts.caries += 1
            } else if (className.includes('filling') || className.includes('empaste')) {
                counts.empaste += 1
            } else if (className.includes('implant') || className.includes('implante')) {
                counts.implante += 1
            } else if (className.includes('impacted') || className.includes('impactado')) {
                counts.impactado += 1
            }
        }

        return counts
    })

    // Calcular total
    const totalProblems = computed(() => {
        return Object.values(problemCounts.value).reduce((sum, count) => sum + count, 0)
    })

    // Calcular porcentajes
    const problemPercentages = computed(() => {
        if (totalProblems.value === 0) {
            return {
                caries: 0,
                empaste: 0,
                implante: 0,
                impactado: 0,
            }
        }

        return {
            caries: Math.round((problemCounts.value.caries / totalProblems.value) * 100),
            empaste: Math.round((problemCounts.value.empaste / totalProblems.value) * 100),
            implante: Math.round((problemCounts.value.implante / totalProblems.value) * 100),
            impactado: Math.round((problemCounts.value.impactado / totalProblems.value) * 100),
        }
    })

    return {
        problemCounts,
        problemPercentages,
        totalProblems,
        completedAnalyses,
        allDetections,
    }
}
