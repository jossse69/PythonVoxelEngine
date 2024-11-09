#version 330 core

layout(location = 0) in uint packed_data;

int x, y, z;
int ao_id;
int flip_id;

uniform mat4 projection_matrix;
uniform mat4 view_matrix;
uniform mat4 model_matrix;

out vec3 voxel_color;
out vec2 uv;
out float shading;
flat out int voxel_id;
flat out int face_id;

const float[4] ao_values = float[4](0.1, 0.3, 0.55, 0.85);

const float[6] face_shading = float[6](
    1.0, 0.5,
    0.5, 0.8,
    0.5, 0.8
);

const vec2[4] uv_cords = vec2[4](
    vec2(0.0, 0.0),
    vec2(0.0, 1.0),
    vec2(1.0, 0.0),
    vec2(1.0, 1.0)
);

const int[24] uv_indices = int[24](
    1, 0, 2, 1, 2, 3,
    3, 0, 2, 3, 1, 0,
    3, 1, 0, 3, 0, 2,
    1, 2, 3, 1, 0, 2
);

vec3 hash31(float p) {
    vec3 p3 = fract(vec3(p) * vec3(.1031, .1030, .0973));
    p3 += dot(p3, p3.yzx + 19.19);
    return fract((p3.xxy + p3.yxx) * p3.zyx); 
}

void unpack(uint packed_data) {
    // a, b, c, d, e, f, g = x, y, z, voxel_id, face_id, ao_id, flip_id
    uint b_bit = 6u, c_bit = 6u, d_bit = 8u, e_bit = 3u, f_bit = 2u, g_bit = 1u;
    uint b_mask = 63u, c_mask = 63u, d_mask = 255u, e_mask = 7u, f_mask = 3u, g_mask = 1u;
    //
    uint fg_bit = f_bit + g_bit;
    uint efg_bit = e_bit + fg_bit;
    uint defg_bit = d_bit + efg_bit;
    uint cdefg_bit = c_bit + defg_bit;
    uint bcdefg_bit = b_bit + cdefg_bit;
    // unpacking vertex data
    x = int(packed_data >> bcdefg_bit);
    y = int((packed_data >> cdefg_bit) & b_mask);
    z = int((packed_data >> defg_bit) & c_mask);
    //
    voxel_id = int((packed_data >> efg_bit) & d_mask);
    face_id = int((packed_data >> fg_bit) & e_mask);
    ao_id = int((packed_data >> g_bit) & f_mask);
    flip_id = int(packed_data & g_mask);
}

void main() {
    unpack(packed_data);

    vec3 in_position = vec3(x, y, z);
    int uv_index = gl_VertexID % 6 + ((face_id & 1) + flip_id * 2) * 6;

    uv = uv_cords[uv_indices[uv_index]];
    voxel_color = hash31(voxel_id);
    shading = face_shading[face_id] * ao_values[ao_id];
    gl_Position = projection_matrix * view_matrix * model_matrix * vec4(in_position, 1.0);
}