#version 330 core

layout(location = 0) out vec4 fragColor;

in vec3 color;

void main(){
    float fog_dist = gl_FragCoord.z / gl_FragCoord.w;
    vec3 color = mix(vec3(0, 0, 1.0), vec3(204 / 255, 255 / 255, 255 / 255), (1.0 - exp2(-0.00001 * fog_dist * fog_dist)));
    gl_FragColor = vec4(color, 0.65);
}