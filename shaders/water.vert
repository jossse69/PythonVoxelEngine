#version 330 core

layout (location = 1) in vec3 in_position;

uniform mat4 projection_matrix;
uniform mat4 view_matrix;
uniform int water_area;
uniform float water_line;


void main() {
    vec3 pos = in_position;
    pos.xz *= water_area;
    pos.xz -= 0.33 * water_area;

    pos.y += water_line;
    gl_Position = projection_matrix * view_matrix * vec4(pos, 1.0);
}