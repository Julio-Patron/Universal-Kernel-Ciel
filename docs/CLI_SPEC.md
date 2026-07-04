# Ciel Kernel CLI Specification V0

La CLI debe ser delgada. La inteligencia no vive en los comandos, sino en los contratos y el orquestador.

## Comandos mínimos:

### `ciel analyze`
Ejecuta el análisis completo del repositorio.
```bash
ciel analyze ./repo
```

### `ciel purpose`
Devuelve el `PurposeObject` resolviendo una petición ambigua.
```bash
ciel purpose "Analiza este repo y dime qué hacer primero"
```

### `ciel sources`
Muestra el `Source Role Assignment` para el repositorio.
```bash
ciel sources ./repo
```

### `ciel gap`
Ejecuta solo la detección de brecha entre intención y realidad.
```bash
ciel gap ./repo
```

### `ciel report`
Exporta el reporte del análisis.
```bash
ciel report ./repo --format json
```
o
```bash
ciel report ./repo --format markdown
```
