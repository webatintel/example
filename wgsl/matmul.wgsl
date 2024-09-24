
@group(0) @binding(0) var<storage, read> a : array<vec4 < f32 >>;
@group(0) @binding(1) var<storage, read> b : array<vec4 < f32>>;
@group(0) @binding(2) var<storage, read_write> result : array<vec4 < f32 >>;

fn mm_readA(batch : i32, row : i32, colIn : i32, batchIndices : u32) -> vec4 < f32 > {
  var value = vec4 < f32 > (0.0);
  let col = colIn * 4;
  if (row <uniforms.dim_a_outer && col < uniforms.dim_inner)
  {
    var aIndices : vec3 < u32>;
    aIndices[0] = batchIndices;
    aIndices[1] = u32(row);
    aIndices[2] = u32(colIn);
    value = get_aByIndices(aIndices);
  }
  return value;
}

fn mm_readB(batch : i32, row : i32, colIn : i32, batchIndices : u32) -> vec4 < f32 > {
  var value = vec4 < f32 > (0.0);
  let col = colIn * 4;
  if(row <uniforms.dim_inner && col < uniforms.dim_b_outer)
  {
    var bIndices : vec2 < u32>;
    bIndices[0] = u32(row);
    bIndices[1] = u32(colIn);
    value = get_bByIndices(bIndices);
  }
  return value;
}

fn mm_write(batch : i32, row : i32, colIn : i32, valueIn : vec4 < f32 >)
{
  let col = colIn * 4;
  if (row < uniforms.dim_a_outer && col < uniforms.dim_b_outer)
  {
    var value = valueIn;
    let coords = vec3 < i32 > (batch, row, colIn);
    set_resultByIndices(vec3 < u32 > (coords), value);
  }
}

var<workgroup> mm_Asub : array<array<vec4 < f32>, 8>, 32>;
var<workgroup> mm_Bsub : array<array<vec4 < f32>, 8>, 32>;

const rowPerThread = 4;
const colPerThread = 4;
const innerElementSize = 4;
const tileInner = 32;

@compute @workgroup_size(8, 8, 1)
fn main(@builtin(local_invocation_id) localId : vec3 < u32>,
@builtin(global_invocation_id) globalId : vec3 < u32>,
@builtin(workgroup_id) workgroupId : vec3 < u32>)
{
  let localRow = i32(localId.y);
  let tileRow = localRow * rowPerThread;
  let tileCol = i32(localId.x);

  let globalRow = i32(globalId.y) * rowPerThread;
  let globalCol = i32(globalId.x);
  let batch = i32(globalId.z);
  let batchIndices = u32(batch);
  let globalRowStart = i32(workgroupId.y) * 32;

  let num_tiles = (uniforms.dim_inner - 1) / tileInner + 1;
  var kStart = 0;

  var acc : array<vec4 < f32>, rowPerThread>;

  //Loop over shared dimension.
  let tileRowB = localRow * 4;
  for (var t = 0; t < num_tiles; t = t + 1)
  {
    //Load one tile of A into local memory.
    for (var innerRow = 0; innerRow < rowPerThread; innerRow = innerRow + 1)
    {
      let inputRow = tileRow + innerRow;
      let inputCol = tileCol;

      mm_Asub[inputRow][inputCol] = mm_readA(batch, globalRow + innerRow, kStart / innerElementSize + inputCol, batchIndices);
    }

    //Load one tile of B into local memory.
    for (var innerRow = 0; innerRow < 4; innerRow = innerRow + 1)
    {
      let inputRow = tileRowB + innerRow;
      let inputCol = tileCol;
      mm_Bsub[inputRow][inputCol] = mm_readB(batch, kStart + inputRow, globalCol, batchIndices);
    }
    kStart = kStart + tileInner;
    workgroupBarrier();

    //Compute acc values for a single thread.
    for (var k = 0; k < tileInner / innerElementSize; k = k + 1)
    {
      let BCached0 = mm_Bsub[k * innerElementSize][tileCol];
      let BCached1 = mm_Bsub[k * innerElementSize + 1][tileCol];
      let BCached2 = mm_Bsub[k * innerElementSize + 2][tileCol];
      let BCached3 = mm_Bsub[k * innerElementSize + 3][tileCol];

      for (var i = 0; i < rowPerThread; i = i + 1)
      {
        let ACached = mm_Asub[tileRow + i][k];
        acc[i] = BCached0 * ACached.x + acc[i];
        acc[i] = BCached1 * ACached.y + acc[i];
        acc[i] = BCached2 * ACached.z + acc[i];
        acc[i] = BCached3 * ACached.w + acc[i];
      }
    }

    workgroupBarrier();
  }

  for (var innerRow = 0; innerRow < rowPerThread; innerRow = innerRow + 1)
  {
    mm_write(batch, globalRow + innerRow, globalCol, acc[innerRow]);
  }
}
