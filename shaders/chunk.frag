#version 330 core

layout(location = 0) out vec4 fragColor;

const vec3 gamma = vec3(2.2);
const vec3 inv_gamma = vec3(1.0 / gamma);

uniform sampler2DArray texture_array_id_0;

in vec3 voxel_color;
in vec2 uv;
in float shading;

flat in int face_id;
flat in int voxel_id;

void main(){
    vec2 face_uv = uv;
    face_uv.x = uv.x / 3.0 - min(face_id, 2) / 3.0;
    vec3 texture_color = texture(texture_array_id_0, vec3(face_uv, voxel_id)).rgb;
    float alpha = texture(texture_array_id_0, vec3(face_uv, voxel_id)).a;

    texture_color = pow(texture_color, gamma);

    //texture_color.rgb *= voxel_color;
    texture_color *= shading;

    
    float fog_dist = gl_FragCoord.z / gl_FragCoord.w;
    texture_color = mix(texture_color, vec3(204 / 255, 255 / 255, 255 / 255), (1.0 - exp2(-0.00001 * fog_dist * fog_dist)));

    texture_color = pow(texture_color, inv_gamma);
	fragColor = vec4(texture_color, alpha);
}