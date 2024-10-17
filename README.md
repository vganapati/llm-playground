# Large Language Model (LLM) playground

Playground of Python scripts for using LLMs and LLM agents for scientific discovery.

## Install Instructions

### Get the repository

Clone the repository:

```
export WORKING_DIR={your-working-directory}
cd $WORKING_DIR
git clone https://github.com/vganapati/llm-playground.git
cd llm-playground
```

### Secrets

Add `.env.development.local` to your `.gitignore`.

Create a file `.env.development.local` at the base (root) of this repo
that contains secrets that should NEVER be checked into GitHub:

```
vi .env.development.local
export API_KEY={your-openai-api-key}
# more keys...
```

Make sure `.env.development.local` is in you `.gitignore`!

### Conda environment

Create conda environment and install dependencies (Mac directions):
```
conda create --name llm_env python=3.12
conda activate llm_env
python -m pip install -r requirements.txt
brew install libomp
```

Can deactivate the conda environment:
```
conda deactivate
```

## Startup

After installation, you can startup in a new terminal:
```
source .env.development.local
conda activate llm_env
```
