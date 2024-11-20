import argparse
import os
from commons import benchmarks
import datetime
import json

MODEL = "HuggingFaceTB/SmolLM2-1.7B"
SUBTASKS = ["college_biology", "high_school_biology"]

def evaluate_mmlu(args):
    """
    Evaluate the model on the MMLU benchmark.
    """

    # Instantiate dataset
    dataset = benchmarks.BenchmarkDataset(name="cais/mmlu", subtasks=SUBTASKS,
                                          sample_size=args.sample_size, seed=args.seed,
                                          device=args.device)
    dataset.load_model(
            hf_path=MODEL,
            rag=args.rag,
            rag_path=args.kb_path)
    
    # run evaluation
    acc, subset = dataset.evaluate()
    print("Accuracy: ", acc)
    print("Subset: ", subset)

    # save results and score as JSON object
    today = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
    with open(f"{args.log_path}/{today}-mmlu_results.json", "w") as f:
        json.dump({"accuracy": acc, "subset": subset}, f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample_size", type=int, default=100)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--rag", type=bool, default=True)
    parser.add_argument("--kb_path", type=str, default="./rag/knowledgebase")
    parser.add_argument("--result_path", type=str, default="./results")
    parser.add_argument("--device", type=str, default="mps")
    args = parser.parse_args()

    assert os.path.exists(args.kb_path), "Knowledgebase path does not exist."
    if args.rag:
        print("Using RAG pipeline.")

    os.makedirs(args.result_path, exist_ok=True)
    evaluate_mmlu(args)
