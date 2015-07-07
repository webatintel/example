#version 330
in vec4 vPosition;
uniform mat2x3 world23;
uniform mat2x4 world24;
uniform mat3x2 world32;
uniform mat3x4 world34;
uniform mat4x2 world42;
uniform mat4x3 world43;
uniform mat4 world4;
void main()
{
  gl_Position = vec4(vPosition.xyz, world23[0].x + world24[0].x + world32[0].x + world34[0].x + world42[0].x + world43[0].x) * world4;
}
