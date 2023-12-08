# jams-pub

1. Setup SSH Key
    > chmod 700 ~/.ssh/id_rsa

2. git clone git@github.com:clarkde5/jams-pub.git ~/src/jams-pub

3. git clone git@github.com:clarkde5/jams.git ~/src/jams

4. Install and setup miniconda
    > wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && sudo bash Miniconda3-latest-Linux-x86_64.sh -bfp /usr/local
  
    > source activate
  
    > conda init
  
    > conda env create --prefix ~/src/jams-pub/env --file ~/src/jams-pub/conda/environment.yml
  
    > conda activate /home/dclark/src/jams-pub/env

5. Install dependencies for docTR
    > sudo apt-get install -y libgl1-mesa-glx libpangocairo-1.0-0

6. Install and setup vscode
    > code ~/src/jams-pub/vscode/jams-pub.code-workspace

    > code --install-extension ms-python.python

Review [setup-notes](docs/setup-notes.md)