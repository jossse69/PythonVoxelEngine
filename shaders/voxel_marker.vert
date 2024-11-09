#version 330 core

layout (location = 0) in vec2 texture_id_0;
layout (location = 1) in vec3 in_position;

uniform mat4 projection_matrix;
uniform mat4 view_matrix;
uniform mat4 model_matrix;
uniform uint mode_id;

const vec3 marker_colors[2] = vec3[2](vec3(1, 0, 0), vec3(0, 0, 1));

out vec3 marker_color;
out vec2 uv;


void main() {
    uv = texture_id_0;
    marker_color = marker_colors[mode_id];
    gl_Position =  projection_matrix * view_matrix * model_matrix * vec4((in_position - 0.5) * 1.01 + 0.5, 1.0);
}