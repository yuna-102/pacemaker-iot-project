FROM tensorflow/tensorflow:2.6.0-gpu
RUN apt-key del 7fa2af80 && apt-key adv --fetch-keys http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/3bf863cc.pub
RUN apt-get update
RUN apt-get install -y zsh tmux wget git libsndfile1
RUN pip install ipython && \
    pip install TensorFlowTTS  && \
    pip install git+https://github.com/repodiac/german_transliterate.git#egg=german_transliterate && \
    pip install streamlit==1.10.0 streamlit_option_menu==0.3.2 Soundfile==0.10.3.post1 tensorflow==2.6.0 keras==2.6 pandas pymodi
RUN mkdir /workspace
WORKDIR /workspace
