#version 330 core

layout(location = 0) in vec3 in_position;
layout(location = 1) in vec2 uv;

uniform sampler2DArray texture_array_id_1;

out vec4 color;
void main(){
    vec3 texture_color = texture(texture_array_id_1, vec3(uv, 0)).rgb;
    color = vec4(texture_color, 1.0);
    gl_Position = vec4(in_position, 1.0);
}