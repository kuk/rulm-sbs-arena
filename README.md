Dev env

```bash
python -m venv ~/.venvs/rulm-sbs-tasks
source ~/.venvs/rulm-sbs-tasks/bin/activate

pip install tqdm pandas pyarrow openai

pip install ipywidgets ipykernel
python -m ipykernel install --user --name rulm-sbs-tasks
```

Download Arena
```bash
mkdir -p data/arena
curl -L https://huggingface.co/datasets/lmsys/chatbot_arena_conversations/resolve/main/data/train-00000-of-00001-cced8514c7ed782a.parquet > data/arena/train-00000-of-00001-cced8514c7ed782a.parquet
```
