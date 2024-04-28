
import argparse
import torch


class Llm(object):
    def __init__(self):
        parser = argparse.ArgumentParser(description='LLM')
        parser.add_argument(
            '--model-name', dest='model_name', help='model name')
        parser.add_argument(
            '--model-path', dest='model_path', help='model path')
        parser.add_argument('--prompt', dest='prompt',
                            help='prompt', default='What is AI?')
        parser.add_argument('--device', dest='device',
                            help='device', default='cuda')

        parser.epilog = '''
    examples:
    {0} {1} --model llama3
    '''.format('python', parser.prog)

        parser.formatter_class = argparse.RawTextHelpFormatter
        args = parser.parse_args()

        if args.model_name == 'llama2':
            model_path = 'modelscope/Llama-2-7b-ms'
        elif args.model_name == 'llama3':  # OK
            model_path = 'LLM-Research/Meta-Llama-3-8B-Instruct'
        elif args.model_name == 'phi2':  # OK
            model_path = 'microsoft/phi-2'
        elif args.model_name == 'phi3':  # pip uninstall -y transformers && pip install git+https://github.com/huggingface/transformers
            model_path = 'microsoft/Phi-3-mini-4k-instruct'

        self.args = args
        self.model_path = model_path

    def run(self):
        model_name = self.args.model_name
        if model_name.startswith('llama'):
            from modelscope import AutoModelForCausalLM, AutoTokenizer, pipeline
        else:
            from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

        model = AutoModelForCausalLM.from_pretrained(
            self.model_path,
            device_map='auto',
            torch_dtype='auto',
            trust_remote_code=True,
        )
        tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        messages = [
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': self.args.prompt}
        ]

        text = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        model_inputs = tokenizer(
            [text], return_tensors='pt').to(self.args.device)
        generated_ids = model.generate(
            model_inputs.input_ids,
            max_new_tokens=512
        )
        generated_ids = [
            output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]
        output = tokenizer.batch_decode(
            generated_ids, skip_special_tokens=True)[0]
        print(output)


if __name__ == '__main__':
    llm = Llm()
    llm.run()
