# En OpenGL, los shaders se escriben en lenguaje GLSL
# Graphics Library Shader Language


# ----------------------- Skybox Shaders -----------------------#
skybox_vertex = '''
#version 450 core

layout (location = 0) in vec3 position;

uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

out vec3 texCoords;

void main()
{
	texCoords = position;
	gl_Position = projectionMatrix * viewMatrix * vec4(position, 1.0);
}
'''

skybox_fragment = '''
#version 450 core

uniform samplerCube skybox;
in vec3 texCoords;

out vec4 fragmentColor;

void main()
{
	fragmentColor = texture(skybox, texCoords);
}
'''

# ----------------------- Vertex Shaders -----------------------#

# Shader de vertices estandar
vertex_shader = '''
#version 450 core

layout (location = 0) in vec3 position; // Posicion del vertice
layout (location = 1) in vec2 texCoords; // Coordenadas de textura
layout (location = 2) in vec3 normals; // Normales del vertice

// Matrices uniformes para transformaciones
uniform mat4 modelMatrix; // Matriz del modelo
uniform mat4 viewMatrix; // Matriz de vista
uniform mat4 projectionMatrix; // Matriz de proyeccion

// Variables de salida para el fragment shader
out vec2 uvs;
out vec3 fragPosition; // Posicion del fragmento
out vec3 fragNormal; // Normal del fragmento

void main()
{
    vec4 worldPosition = modelMatrix * vec4(position, 1.0);
    fragPosition = vec3(worldPosition);
    vec3 worldNormal = mat3(modelMatrix) * normals; // Normal en espacio mundial
    fragNormal = mat3(viewMatrix) * worldNormal; // Transformar normal al espacio de la vista

    gl_Position = projectionMatrix * viewMatrix * worldPosition;
    uvs = texCoords;
}
'''

# Shader de vertices con efecto de pixelado (estilo Minecraft)
minecraft_vertex = '''
#version 450 core

layout (location = 0) in vec3 position; // Posicion del vertice
layout (location = 1) in vec2 texCoords; // Coordenadas de textura
layout (location = 2) in vec3 normals; // Normales del vertice

// Matrices uniformes para transformaciones
uniform mat4 modelMatrix; // Matriz del modelo
uniform mat4 viewMatrix; // Matriz de vista
uniform mat4 projectionMatrix; // Matriz de proyeccion

// Variable controladora de pixelado
uniform float pixelSize; // tamano del pixel

// Variables de salida para el fragment shader
out vec2 uvs;
out vec3 fragPosition; // Posicion del fragmento
out vec3 fragNormal; // Normal del fragmento

// Funcion para pixelar valores
vec3 pixelate(vec3 value, float gridSize) {
    return floor(value / gridSize) * gridSize;
}

void main()
{
    // Aplicacion del efecto de pixelado
    vec3 pixelatedPosition = pixelate(position, pixelSize);

    // Transformacion del vertice al espacio del mundo con pixelado
    vec4 worldPosition = modelMatrix * vec4(pixelatedPosition, 1.0);
    fragPosition = vec3(worldPosition);

    // Transformacion de las normales
    vec3 worldNormal = mat3(modelMatrix) * normals; // Normal en espacio mundial
    fragNormal = mat3(viewMatrix) * worldNormal; // Transformar normal al espacio de la vista

    // Calculo de la posicion en pantalla
    gl_Position = projectionMatrix * viewMatrix * worldPosition;
    // Paso de las coordenadas de textura
    uvs = texCoords;
}

'''


# ----------------------- Fragment Shaders -----------------------#

# Shader de fragmentos estandar
fragment_shader = '''
#version 450 core

layout (binding = 0) uniform sampler2D tex; // Textura

in vec2 uvs; // Coordenadas de textura

out vec4 fragmentColor; // Color del fragmento

void main()
{
	// Asignar el color del fragmento basado en la textura
	fragmentColor = texture(tex, uvs);
}
'''


# Shader de fragmentos con efecto de brillo
glow_shader = '''
#version 450 core

layout (binding = 0) uniform sampler2D tex; // Textura
in vec2 uvs; // Coordenadas de textura
in vec3 fragPosition; // Posicion del fragmento
in vec3 fragNormal; // Normal del fragmento
uniform vec3 camPosition; // Posicion de la camara

out vec4 fragmentColor; // Color del fragmento

void main()
{
    vec4 textureColor = texture(tex, uvs); // Color de la textura
    vec3 normal = normalize(fragNormal); // Normal normalizada

    // Calculo del brillo basado en la normal y la direccion desde el fragmento a la camara
    vec3 toCameraDir = normalize(camPosition - fragPosition);
    float glowAmount = 1.0 - dot(normal, toCameraDir);
    glowAmount = clamp(glowAmount, 0.0, 1.0); // Asegurarse de que esta en el rango [0, 1]

    vec3 glowColor = vec3(1, 1, 0); // Color del brillo
    // Modificar el brillo basado en glowAmount
    vec3 modifiedGlow = glowColor * glowAmount;

    // Mezclar el color de la textura con el brillo modificado
    vec3 color = vec3(textureColor) + modifiedGlow;
    color = clamp(color, 0.0, 1.0); // Asegurar que el color este dentro de los limites

    fragmentColor = vec4(color, 1.0); // Asignar el color del fragmento (sin cambiar la transparencia)
}

'''

# Shader de fragmentos con efecto psicodelico
psycho_shader = '''
#version 450 core

layout (binding = 0) uniform sampler2D tex; // Textura

in vec2 uvs; // Coordenadas de textura
in vec3 fragPosition; // Posicion del fragmento
in vec3 fragNormal; // Normal del fragmento

uniform vec3 camPosition; // Posicion de la camara
uniform float time; // Tiempo

out vec4 fragmentColor; // Color del fragmento

#define TWO_PI 6.28318530718 // Definicion de 2*PI

void main()
{
	vec4 textureColor = texture(tex, uvs); // Color de la textura
    vec3 normal = normalize(fragNormal); // Normal normalizada

    // Calculo del brillo basado en la normal y la direccion desde el fragmento a la camara
    vec3 toCameraDir = normalize(camPosition - fragPosition);
    float glowAmount = 1.0 - dot(normal, toCameraDir);
    glowAmount = clamp(glowAmount, 0.0, 1.0); // Asegurarse de que esta en el rango [0, 1]

	// Calculo de los valores de brillo para efecto psicodelico
	float diagonalValue = length(fragPosition.xy - vec2(0.5)) + time / 2;
	float rGlow = abs(sin(diagonalValue * TWO_PI));
	float gGlow = abs(sin((diagonalValue + 1.0 / 3.0) * TWO_PI));
	float bGlow = abs(sin((diagonalValue + 2.0 / 3.0) * TWO_PI));
	vec3 newColorEffect = vec3(rGlow, gGlow, bGlow);

	// Mezclar el efecto de color con el color de la textura
	vec3 color = mix(vec3(textureColor), newColorEffect, glowAmount);
	color = clamp(color, 0.0, 1.0); // Asegurar que el color este dentro de los limites

	fragmentColor = vec4(color, 1.0); // Asignar el color del fragmento
}


'''


# Shader de fragmentos con efecto de holograma
hologram_shader = '''
#version 450 core

layout (binding = 0) uniform sampler2D tex; // Textura
in vec2 uvs; // Coordenadas de textura
in vec3 fragPosition; // Posicion del fragmento
in vec3 fragNormal; // Normal del fragmento

uniform vec3 camPosition; // Posicion de la camara
uniform mat4 camMatrix; // Matriz de la camara

out vec4 fragmentColor; // Color del fragmento

void main()
{
	vec4 textureColor = texture(tex, uvs); // Color de la textura
    vec3 normal = normalize(fragNormal); // Normal normalizada

    // Calculo del brillo basado en la normal y la direccion desde el fragmento a la camara
    vec3 toCameraDir = normalize(camPosition - fragPosition);
    float glowAmount = 1.0 - dot(normal, toCameraDir);
    if (glowAmount < 0) glowAmount = 0.0;

	// Definir el color del holograma (cian)
	vec3 hologramColor = vec3(0, 1, 1);

	// Crear un patron de lineas para el efecto de holograma
	float linePattern = sin(uvs.x * 100.0) * sin(uvs.y * 100.0);
	linePattern = clamp(linePattern, 0.0, 1.0);

	// Mezclar el color del holograma con el patron de lineas
	vec3 color = mix(hologramColor, hologramColor * linePattern, 0.5);
	// Aplicar el brillo al color
	color *= glowAmount;
	color = clamp(color, 0.0, 1.0); // Asegurar que el color este dentro de los limites

	// Definir la transparencia basada en el brillo
	float alpha = glowAmount;

	// Asignar el color del fragmento incluyendo la transparencia
	fragmentColor = vec4(color, alpha);
}
'''
