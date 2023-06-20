# -!- coding: utf-8 -!-
import argparse


def get_prompt():
    std_generation_cnndm_prompt = open("./prompts/std_generation_cnndm.txt").read()
    std_generation_xsum_prompt = open("./prompts/std_generation_xsum.txt").read()
    cot_generation_cnndm_prompt = open("./prompts/cot_generation_cnndm.txt").read()
    cot_generation_xsum_prompt = open("./prompts/cot_generation_xsum.txt").read()
    cot_extraction_prompt = ""
    for line in open("./prompts/cot_element_extraction.txt"):
        cot_extraction_prompt += line

    prompt = {"std_generation_cnndm_prompt": std_generation_cnndm_prompt,
              "std_generation_xsum_prompt": std_generation_xsum_prompt,
              "cot_generation_cnndm_prompt": cot_generation_cnndm_prompt,
              "cot_generation_xsum_prompt": cot_generation_xsum_prompt,
              "cot_extraction_prompt": cot_extraction_prompt}

    return prompt


def parse_arguments():
    parser = argparse.ArgumentParser(description="SumCoT")
    parser.add_argument("--cot_true", type=bool, default="False",
                        help="standard or cot-based generation")
    parser.add_argument("--model", type=str, default="gpt3-xl",
                        choices=["gpt3", "gpt3-medium", "gpt3-large", "gpt3-xl"],
                        help="model used for decoding")
    parser.add_argument("--dataset", type=str, default="cnndm",
                        choices=["cnndm", "xsum"], help="dataset source")
    parser.add_argument("--start_id", type=int, default="0")
    parser.add_argument("--end_id", type=int, default="0")
    args = parser.parse_args()

    prompt = get_prompt()
    args.cot = prompt["cot_extraction_prompt"]

    if args.dataset == "cnndm":
        args.std_prompt = prompt["std_generation_cnndm_prompt"]
        args.cot_prompt = prompt["cot_generation_cnndm_prompt"]
    elif args.dataset == "xsum":
        args.std_prompt = prompt["std_generation_xsum_prompt"]
        args.cot_prompt = prompt["cot_generation_xsum_prompt"]
    else:
        raise "Invalid Dataset!"

    return args
