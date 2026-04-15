# Estrategia del sistema de diseño: The Clinical Precision Framework

## 1. Visión general y estrella creativa: "The Digital Surgeon"
Este sistema de diseño se aleja de la estética de "startup amigable" de burbujas redondeadas y colores primarios planos. Nuestra estrella creativa es **The Digital Surgeon**: un lenguaje visual que se siente tan preciso, esterilizado y tecnológico como un quirófano moderno. 

Para romper con el aspecto de "plantilla", empleamos **Asimetría intencional**. En lugar de rejillas centradas y equilibradas, usamos barras laterales con peso visual y capas superpuestas con aspecto de "rayos X". Al combinar el rigor técnico de `Inter` con la sensación editorial de alto nivel de `Manrope`, establecemos una jerarquía que resulta a la vez autoritaria y vanguardista. Rechazamos la web "encajonada"; abrazamos una interfaz que se siente como una pantalla frontal fluida (HUD).

---

## 2. Colores: profundidad tonal y la regla "sin líneas"
La paleta se basa en `Clinical Blue` y `Tech Cyan`, pero su sofisticación proviene de cómo superponemos estos tonos.

### La regla "sin líneas"
**Instrucción explícita:** No uses bordes `1px solid` para definir secciones. Los bordes tradicionales crean ruido visual y se sienten anticuados. En su lugar, los límites deben definirse mediante:
- **Cambios tonales:** Colocar un componente `surface-container-low` sobre un fondo `surface`.
- **Espacio negativo:** Usar los tokens de espaciado `12` (3rem) o `16` (4rem) para crear límites mentales.

### Jerarquía de superficies y anidamiento
Trata la UI como una serie de capas físicas: láminas apiladas de vidrio esmerilado de grado médico.
- **Base:** `surface` (#f8f9fa)
- **Bloques principales de layout:** `surface-container-low` (#f3f4f5)
- **Tarjetas interactivas:** `surface-container-lowest` (#ffffff) para una sensación de elevación.
- **Superposiciones/Modales:** `surface-bright` con 80% de opacidad y un `backdrop-blur` de `20px`.

### La regla "vidrio y gradiente"
Para indicar "escaneo con IA", usa gradientes de `Tech Cyan`. Un gradiente lineal de `secondary` (#006877) a `secondary-container` (#75e7fe) en un ángulo de 45 grados debe reservarse para elementos de IA de alta intención, como barras de progreso de escaneo o resaltados de diagnóstico. Esto aporta "alma visual" que los colores HEX planos no pueden ofrecer.

---

## 3. Tipografía: la escala editorial
Usamos un sistema de doble tipografía para equilibrar los datos clínicos con una autoridad de marca de alto nivel.

*   **Display y titulares (Manrope):** Esta es nuestra "voz editorial". `display-lg` (3.5rem) debe usarse con moderación para mensajes heroicos, creando un contraste intenso frente a la densidad de datos de una app dental.
*   **Interfaz y datos (Inter):** Todos los elementos funcionales (etiquetas, cuerpo, títulos) usan `Inter`. Esta tipografía está pensada para ofrecer legibilidad en tamaños pequeños, algo crucial para leer historiales dentales y puntuaciones de confianza de IA.
*   **Contraste intencional:** Combina un `headline-sm` (Manrope, 1.5rem) con un `label-sm` (Inter, 0.6875rem) en mayúsculas y con un espaciado entre letras de `0.05em` para crear una estética de "manual técnico".

---

## 4. Elevación y profundidad: superposición tonal
No usamos sombras para representar "importancia"; las usamos para representar "flotación".

*   **El principio de superposición:** La profundidad se consigue apilando. Una tarjeta `surface-container-lowest` apoyada sobre un fondo `surface-container-high` proporciona una elevación natural y suave.
*   **Sombras ambientales:** Para módulos flotantes de IA, usa una sombra personalizada: `0 20px 40px rgba(0, 86, 179, 0.06)`. Observa el uso del color `primary` en la sombra: esto imita la refracción de la luz a través de vidrio médico teñido de azul en lugar de una sombra gris muerta.
*   **El recurso de "borde fantasma":** Si un contenedor necesita un borde duro (por ejemplo, una tabla de datos de alta densidad), usa un `Ghost Border`. Se trata del token `outline-variant` al **15% de opacidad**. Debe sentirse, no verse.
*   **Glassmorphism:** Los paneles de información de IA deben usar `backdrop-filter: blur(12px)` sobre un `surface-container-lowest` semitransparente. Esto garantiza que el usuario nunca pierda el contexto del escaneo dental bajo los datos.

---

## 5. Componentes: primitivas de precisión

### Botones: el "comando táctil"
- **Primario:** Fondo `primary` (#003f87), texto `on-primary`. Usa `rounded-md` (0.375rem). El estado hover no es un cambio de color, sino una ligera expansión de la sombra ambiental azul.
- **Secundario (acción de IA):** Fondo `secondary-container`, texto `on-secondary-container`. Úsalo para "Run AI Analysis" para diferenciarlo de "Save/Submit".

### Campos de entrada: la "entrada técnica"
- **Estilo:** Sin borde inferior ni caja completa. Usa un fondo sutil `surface-container-high` con `rounded-sm`. Al recibir foco, transiciona el fondo a `surface-container-lowest` y añade una barra de acento izquierda de `2px` en `secondary`.

### Tarjetas y listas: el "flujo fluido"
- **Regla:** **Prohibidas estrictamente las líneas divisorias horizontales.** 
- Separa los registros de pacientes o los datos dentales usando `spacing-4` (1rem) y cambios sutiles alternos de fondo (rayado cebra usando `surface` y `surface-container-low`). Esto mantiene la interfaz "respirable".

### Chips de escaneo de IA
- **Interactivos:** Usa `rounded-full` con un resplandor `secondary` (Tech Cyan). Cuando un escaneo de IA esté "Active", el chip debe pulsar con un desenfoque de `4px` del color `secondary`.

---

## 6. Lo que sí y lo que no

### Haz:
- **Usa ritmo vertical:** Mantente estrictamente en los tokens de espaciado `4` (1rem) y `8` (2rem) para todos los márgenes.
- **Abraza el espacio en blanco:** Deja respirar al "Clinical Blue". Una app dental de alta densidad necesita "silencio visual" para evitar la fatiga del usuario.
- **Movimiento sutil:** Los elementos de IA deben fundirse con una transición `ease-out` de `200ms`; no deben simplemente "aparecer de golpe".

### No hagas:
- **No uses negro al 100%:** Usa `on-surface` (#191c1d) para el texto. El negro puro es demasiado duro para un contexto médico.
- **No uses sombras "por defecto":** Evita la `shadow-lg` estándar de Tailwind. Usa nuestra especificación de sombra ambiental para conseguir una sensación premium y personalizada.
- **No redondees en exceso:** Nunca uses `rounded-xl` ni `full` para los contenedores principales. Tiene un aspecto demasiado "consumer-tech". Quédate con `md` (0.375rem) para una apariencia profesional y bien diseñada.
- **No añadas líneas divisorias innecesarias:** Si sientes la necesidad de añadir una línea, añade `16px` de espacio en su lugar. 
