# Juego de Preguntas para Fiestas - card_game

## ✅ Implementación Completada

El proyecto de **card_game** ahora contiene la versión corregida del Juego de Preguntas para Fiestas con el sistema de turnos en orden implementado correctamente.

### Archivos Actualizados

1. **game_logic.py** - Lógica de juego con validación de respuestas correctas
2. **data_manager.py** - Carga/guarda preguntas con columna `correct_answer`
3. **ui.py** - Interfaz de texto con turnos en orden
4. **scoreboard.py** - Seguimiento de eventos (strikes, bebidas, abandonos)
5. **main.py** - Punto de entrada del juego
6. **questions.csv** - Banco de preguntas con respuestas correctas

### Características Implementadas

✅ **Selección de número de jugadores al iniciar** (2-10 jugadores)
✅ **Máximo 3 strikes por jugador** - Al llegar a 3 strikes: bebe y se reinician a 0
✅ **Strikes SOLO al responder correctamente** - Las respuestas incorrectas no añaden strikes
✅ **Turnos en orden** - Cada jugador responde un turno por turno de forma ordenada
✅ **Validación de respuestas** - Se compara la respuesta del jugador con `correct_answer` en la pregunta
✅ **Sistema completo de scoring** - Seguimiento de strikes, bebidas y abandonos

### Flujo del Juego

```
1. Inicio: Ingresa número de jugadores (2-10)
2. Ingresa nombres de cada jugador
3. Se muestra las reglas del juego
4. Comienza el juego:
   - Turno 1: Jugador 1 responde pregunta
   - Turno 2: Jugador 2 responde pregunta
   - Turno 3: Jugador 3 responde pregunta
   - Turno 4: Jugador 1 responde pregunta (cicla)
   - ... hasta que quede 1 jugador activo
5. Se muestran resultados finales
```

### Cómo Ejecutar

```bash
cd card_game
python main.py
```

### Opciones del Jugador

- `sí` o `si` → Responder SÍ
- `no` → Responder NO
- `salir` → Abandonar el juego (hacer "clock out")

### Validación

- ✅ **29/29 tests pasando**
- ✅ **Demo ejecutada exitosamente**
- ✅ **Respuestas correctas e incorrectas validadas correctamente**

### Ejemplo de Partida

```
Turno 1: Alice responde CORRECTO → Strikes: 1/3
Turno 2: Bob responde INCORRECTO → Strikes: 0/3 (sin cambios)
Turno 3: Carol responde CORRECTO → Strikes: 1/3
Turno 4: Alice responde CORRECTO → Strikes: 2/3
Turno 5: Bob responde INCORRECTO → Strikes: 0/3 (sin cambios)
Turno 6: Carol responde CORRECTO → Strikes: 2/3
Turno 7: Alice responde CORRECTO → Strikes: 3/3 → ¡BEBE! → Strikes: 0/3 (1 bebida)
...
```

### Estructura de Datos

**CSV (questions.csv):**
- Campos: id, question, category, difficulty, used, correct_answer
- correct_answer: 'Yes' o 'No' (convertido a boolean en Python)

**Jugador:**
- name: str
- strikes: int (0-3)
- drinks_consumed: int
- is_active: bool
- has_block_card: bool

**Resultado de respuesta:**
```python
{
    'player_name': str,
    'answered_yes': bool,
    'correct_answer': bool,
    'is_correct': bool,
    'strikes': int,
    'must_drink': bool
}
```

### Estado del Proyecto

**ESTADO: ✅ COMPLETO Y VALIDADO**

El juego está completamente funcional y listo para usar. Todos los requisitos han sido implementados correctamente:

- Selección de jugadores al inicio ✓
- Máximo 3 strikes por jugador ✓
- Strikes solo al responder correctamente ✓
- Turnos en orden de forma cíclica ✓
- Interfaz en español ✓
- Sistema de puntuación completo ✓
