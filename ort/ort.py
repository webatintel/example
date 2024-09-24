import onnxruntime as ort
ort_sess = ort.InferenceSession('../../../webatintel/onnx-models/candy-8.onnx')
inputs = ort_sess.get_inputs()
for input in inputs:
  print(input)

#outputs = ort_sess.run(None, {'input': x.numpy()})
