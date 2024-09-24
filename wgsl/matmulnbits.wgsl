enable f16;

struct Uniforms { output_size : u32, K : u32, N : u32, accuracy_level : u32, bits : u32, block_size : u32, a_shape : vec3 < u32>, a_strides : vec3 < u32>, b_shape : vec3 < u32>, b_strides : vec3 < u32>, scales_shape : u32, scales_strides : u32, output_shape : vec3 < u32>, output_strides : vec3 < u32> };
  @group(0) @binding(4) var<uniform> uniforms : Uniforms;
  fn i2o_a(indices : vec3 < u32>) -> u32 {
    return uniforms.a_strides[2] * (indices[2]) + uniforms.a_strides[1] * (indices[1]) + uniforms.a_strides[0] * (indices[0]);
  }

  fn get_aByIndices(indices : vec3 < u32>) -> vec4 < f16> {
    return a[i2o_a(indices)];
  }

  fn i2o_b(indices : vec3 < u32>) -> u32 {
    return uniforms.b_strides[2] * (indices[2]) + uniforms.b_strides[1] * (indices[1]) + uniforms.b_strides[0] * (indices[0]);
  }

  fn get_bByIndices(indices : vec3 < u32>) -> vec4 < u32> {
    return b[i2o_b(indices)];
  }


  fn o2i_output(offset : u32) -> vec3 < u32> {
    var indices : vec3 < u32>;
    var current = offset;

    let dim0 = current / uniforms.output_strides[0];
    let rest0 = current % uniforms.output_strides[0];
    indices[0] = dim0;
    current = rest0;

    let dim1 = current / uniforms.output_strides[1];
    let rest1 = current % uniforms.output_strides[1];
    indices[1] = dim1;
    current = rest1;
    indices[2] = current;
    return indices;
  }

  fn i2o_output(indices : vec3 < u32>) -> u32 {
    return uniforms.output_strides[2] * (indices[2]) + uniforms.output_strides[1] * (indices[1]) + uniforms.output_strides[0] * (indices[0]);
  }

  fn set_outputByIndices(indices : vec3 < u32>, value : vec4 < f16>)
  {
    output[i2o_output(indices)]=value;
  }


  fn dequantize(quantized : mat2x4 < f16>, zero_point : f16, scale : f16) -> mat2x4 < f16> {
    var zero_points : mat2x4 < f16> = mat2x4 < f16 > (zero_point, zero_point, zero_point, zero_point, zero_point, zero_point, zero_point, zero_point);
    return (quantized - zero_points) * scale;
  }

  fn ortUnpack8x4snorm(value : u32) -> mat2x4 < f16> {
    var quantized : mat2x4 < f16>;
    var offset : u32 = 0;
    let count : u32 = 4;
    for (var i : u32 = 0; i < 8u; i++)
    {
      var result = f16(extractBits(value, offset, count));
      quantized[i / 4][i % 4] = result;
      offset += count;
    }
    return quantized;
  }
  @group(0) @binding(0) var<storage, read> a : array<vec4 < f16>>;
  @group(0) @binding(1) var<storage, read> b : array<vec4 < u32>>;
  @group(0) @binding(2) var<storage, read> scales : array<f16>;
  @group(0) @binding(3) var<storage, read_write> output : array<vec4 < f16>>;
  @compute @workgroup_size(64, 1, 1)
  fn main(@builtin(global_invocation_id) global_id : vec3 < u32>,
  @builtin(workgroup_id) workgroup_id : vec3 < u32>,
  @builtin(local_invocation_id) local_id : vec3 < u32>)
  {
    let global_idx = global_id.x; let local_idx = local_id.x;

    if (global_idx >= uniforms.output_size)
    { return; }
      var output_values : array<vec4 < f16>, 4>;
      var output_indices = o2i_output(global_idx);
      var n = output_indices[2];
      var m = output_indices[1];
      var a_indices : vec3 < u32> = output_indices;
          //Two zero points are packed into one byte because uniforms.bits <= 4.
          //zero_point_offset is either 0 or 4. It is bit offset within one byte.
          //TODO support zero_point_offset for bits > 4

      var scale_index = n * 256;
      var b_indices : vec3 < u32>;
      for (var c : u32 = 0; c < 4; c++)
      {
        b_indices[0]=n * 4 + c; ;
        var block_offset : u32 = 0;
        for (var block : u32 = 0; block < 64; block++)
        {
              //The scale and zero points are computed per block.
          let scale = scales[scale_index];
              //The default zero point is 8 for unsigned 4-bit quantization.
          let zero_point = f16(8);
          b_indices[1]=block; ;
          var word_offset : u32 = block_offset;
          for (var word : u32 = 0; word < 4; word += 4)
          {
            b_indices[2]=word; ;
            let b_data = get_bByIndices(b_indices);
            for (var i : u32 = 0; i < 4; i++)
            {
              let b_value = b_data[word + i];
              let b_quantized_values : mat2x4 < f16> = ortUnpack8x4snorm(b_value);
              let b_dequantized_values = dequantize(b_quantized_values, zero_point, scale);
                  //Number of B elements per 32-bit word is 32/bits = 32/4 = 8
              var offset : u32 = word_offset;
              for (var j : u32 = 0; j < 8 / 4; j++)
              {
                a_indices[2]=offset / 4; ;
                for (var k : u32 = 0; k < 4u; k++)
                {
                  a_indices[1]=m * 4 + k; ;
                  let a_data = get_aByIndices(a_indices);
                  output_values[k][c] += dot(a_data, b_dequantized_values[j]);
                }
                offset += 4;
              }
              word_offset += 8;
            }
          }
          scale_index++;

          block_offset += uniforms.block_size;
        }
            //Drop the trailing 4 bits if the zero_poit_offset is not a byte boundary to align with the next byte.

      }
      for (var k : u32 = 0u; k < 4u; k++)
      {
        output_indices[1]=4 * m + k; ;
        set_outputByIndices(output_indices, output_values[k]);
      }
    }
