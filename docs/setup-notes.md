# WSL Managment

## Delete wsl image

> wsl --unregister Ubuntu

## Install wsl image

> wsl --install -d Ubuntu

## Restart wsl image

> wsl -t Ubuntu

## Update to version 2

> wsl --set-version Ubuntu 2

## Reference

- https://learn.microsoft.com/en-us/windows/wsl/install

# Conda Setup

## Installation

> wget https://repo.anaconda.com/miniconda/Miniconda3-py37_23.1.0-1-Linux-x86_64.sh
> bash Miniconda3-py37_23.1.0-1-Linux-x86_64.sh

**NOTE:** To avoid strange errors it is best to restart wsl after installing Conda

## Create / remove environment

> conda create -n <name> python=3.7
> conda remove -n <name> --all

## List and install revisions

> conda list --revisions
> conda install --rev REVNUM

## List environments

> conda info --envs

## Activate environment

> conda activate <name>

## If you'd prefer that conda's base environment not be activated on startup

> conda config --set auto_activate_base false

## Reference

- https://conda.io/projects/conda/en/latest/user-guide/getting-started.html

# Python

# Recent Commands

> conda remove -n donut_v1 --all
> conda create -n donut_v1 python=3.7

- http://172.19.76.86:7860/

Copy of Final Finetune donut (for your own dataset)
- https://www.freecodecamp.org/news/how-to-fine-tune-the-donut-model/
- https://colab.research.google.com/drive/17J2NMdqdrpKx9taYiRXjqNSmyLJ3wQ8r#scrollTo=zJRT9ZWrevV3
- https://drive.google.com/drive/folders/1-JmqlyE4J59Y65N1d2tkj_PW3ldVr2vA

# Issue References

- https://github.com/gradio-app/gradio/issues/4591

```
curl 'http://172.19.76.86:7860/run/predict' \
  --data-raw '{"data":["data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEEAAAA2CAIAAAAXsmNrAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAABRSURBVGhD7c8BDQAwEAOh+Tfd2eCTwwFv93UwdDB0MHQwdDB0MHQwdDB0MHQwdDB0MHQwdDB0MHQwdDB0MHQwdDB0MHQwdDB0MHQwdDDcP2wfWfb7N58EmyQAAAAASUVORK5CYII="],"event_data":null,"fn_index":0,"session_hash":"vb55vuo8ya"}'
  
  {"detail":[{"type":"model_attributes_type","loc":["body"],"msg":"Input should be a valid dictionary or object to extract fields from","input":"{\"data\":[\"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEEAAAA2CAIAAAAXsmNrAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAABRSURBVGhD7c8BDQAwEAOh+Tfd2eCTwwFv93UwdDB0MHQwdDB0MHQwdDB0MHQwdDB0MHQwdDB0MHQwdDB0MHQwdDB0MHQwdDB0MHQwdDDcP2wfWfb7N58EmyQAAAAASUVORK5CYII=\"],\"event_data\":null,\"fn_index\":0,\"session_hash\":\"vb55vuo8ya\"}","url":"https://errors.pydantic.dev/2.5/v/model_attributes_type"}]}
```

> curl -s -X POST -H 'Content-type: application/json' 'https://b0ad88bdd3c77fdbfb.gradio.live/run/predict'   --data-raw '{"data":["Save the World"]}'

{"data":["Save the Databricks"],"is_generating":false,"duration":0.00038123130798339844,"average_duration":0.0005707007188063401}

# Training

- https://github.com/clovaai/donut
- https://www.freecodecamp.org/news/how-to-fine-tune-the-donut-model/
- https://github.com/katanaml/sparrow

> python train.py --config config/train_cord.yaml \
                --pretrained_model_name_or_path "naver-clova-ix/donut-base" \
                --dataset_name_or_paths '["naver-clova-ix/cord-v2"]' \
                --exp_version "test_experiment"   

> python train.py --config config/train_example.yaml \
                --pretrained_model_name_or_path "naver-clova-ix/donut-base" \
                --exp_version "test_experiment"   
				
# Unused
- https://www.youtube.com/watch?v=qKFk2kwyp4o&ab_channel=AndrejBaranovskij
- Models stored on Model Hub? https://huggingface.co/docs/hub/models-the-hub

- https://www.philschmid.de/fine-tuning-donut
- https://pypi.org/project/synthdog/

"Yup thanks that worked, just that for task_prompt I had to use s_synthdog as the prompt which was hard to find in docs. It was once I saw other task_prompts that it clicked to me to use synthdog as it was the Pre-Training database."
- https://www.reddit.com/r/MachineLearning/comments/151u6pk/d_donut_base_model_usage/?rdt=35410

Interesting training question
- https://stackoverflow.com/questions/75248458/pre-training-donut-document-understanding-transformer

GPU Options 2023
- https://www.youtube.com/watch?v=OnuIjDRvZ_0

Other: 
- https://ocrmypdf.readthedocs.io/en/latest/
- https://github.com/microsoft/vscode-jupyter/wiki/Jupyter-Kernels-and-the-Jupyter-Extension#python-extension-and-ipykernel
- https://code.visualstudio.com/blogs/2019/09/03/wsl2
- https://code.visualstudio.com/docs/datascience/jupyter-notebooks
- https://visualstudio.microsoft.com/vs/features/notebooks-at-microsoft/ (formerly Azure Notebooks)
- https://code.visualstudio.com/docs/datascience/notebooks-web
- https://colab.research.google.com/

Q: What can I use instead of Google Colab?

A: There are several alternatives to Google Colab, such as Noteable, Azure Notebooks, Databricks, Amazon SageMaker, Deepnote, IBM Watson Studio, and Paperspace Gradient.
	- https://noteable.io/blog/google-colab-alternatives/#:~:text=What%20can%20I%20use%20instead,Watson%20Studio%2C%20and%20Paperspace%20Gradient.

colab-connect
- https://github.com/amitness/colab-connect
- Mine: https://colab.research.google.com/drive/1waI37Bx8DMg-vPq58agJQEyehGqMWmjQ#scrollTo=BNj85daEi-mR
- VS Code Extension: "Remote - Tunnels"
- Remote Connect to Tunnel > GitHub > 465bbcb10a37 (https://code.visualstudio.com/docs/remote/vscode-server)
- /content/drive/MyDrive/Colab Notebooks

git lfs
- curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash
- sudo apt-get install git-lfs
- git lfs install
- https://github.com/git-lfs/git-lfs/issues/2898

Hugging Face
- Downloading Models
  - https://huggingface.co/docs/hub/models-downloading
  - git@hf.co:naver-clova-ix/donut-base-finetuned-cord-v2
  - https://hf.co/naver-clova-ix/donut-base-finetuned-cord-v2

