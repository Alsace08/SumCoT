# -!- coding: utf-8 -!-
import json
import os
from api_request import Decoder
from arguments import parse_arguments


def get_llm_summary(args, decoder):
    in_file = os.path.join("./data", args.dataset+"_element_aware.json")
    with open(in_file, "r", encoding="utf-8") as f:
        if "cnndm" in in_file:
            data = json.load(f)["cnndm"]
            data_output = {"cnndm": []}
        elif "xsum" in in_file:
            data = json.load(f)["xsum"]
            data_output = {"xsum": []}
        else:
            raise "Invalid Dataset!"

    for i in range(args.start_id, args.end_id + 1):
        src = data[i]["src"]
        ori_sum = data[i]["original_summary"]
        new_sum = data[i]["element-aware_summary"]

        x = "Article: " + src + "\n" + args.std_prompt
        pred_std = decoder.decode(x, model=args.model, max_length=2048)

        x = "Article: " + src + "\n" + args.cot
        ele = decoder.decode(x, model=args.model, max_length=2048)
        x = x + ele + "\n" + args.cot_prompt
        pred_cot = decoder.decode(x, model=args.model, max_length=2048)

        if "cnndm" in in_file:
            data_output["cnndm"].append({"id": i,
                                         "src": src,
                                         "original_summary": ori_sum,
                                         "element-aware_summary": new_sum,
                                         "gpt3_summary": pred_std,
                                         "gpt3_cot_summary": pred_cot})
        elif "xsum" in in_file:
            data_output["xsum"].append({"id": i,
                                        "src": src,
                                        "original_summary": ori_sum,
                                        "element-aware_summary": new_sum,
                                        "gpt3_summary": pred_std,
                                        "gpt3_cot_summary": pred_cot})

    data_output = json.dumps(data_output, indent=2)
    if "cnndm" in in_file:
        with open("cnndm_output.json", "w", newline='\n') as g:
            g.write(data_output)
    if "xsum" in in_file:
        with open("xsum_output.json", "w", newline='\n') as g:
            g.write(data_output)


if __name__ == '__main__':
    args = parse_arguments()
    decoder = Decoder(api_key="xxx")

    get_llm_summary(args, decoder)

