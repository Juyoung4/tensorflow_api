# Kubeflow 기반 Tensorflow 심층 신경망 경량화의 실험적 분석

 [![Platform](https://img.shields.io/badge/Platform-Kubeflow-blue?logo=Kubeflow)](https://www.kubeflow.org/) [![ML](https://img.shields.io/badge/ML-tensorflow-orange?logo=tensorflow)](https://www.tensorflow.org/?hl=ko) [![Container](https://img.shields.io/badge/language-Docker-red?logo=docker)](https://www.docker.com/) [![language](https://img.shields.io/badge/language-Python-green?logo=python)](https://www.python.org/) 

## 💡 요약
우리는 엣지 컴퓨팅을 위해 필요한 머신러닝 경량화 모델을 생성하는 방법을 연구하였다. Tensorflow API의 Optimization Toolkit을 이용하여 Weight pruning, Quantization등의 경량화 기술을 12가지 방법으로 조합해 모델 경량화 실험을 진행하고 분석한다. 이러한 모델 경량화 실험은 머신러닝 실험의 전 과정을 관리해주는 Kubeflow 플랫폼에서 진행되었으며 Kubeflow Pipelines를 이용해 12개의 실험을 하나의 ML Pipeline으로 구축하였다.

## 사용 기술 및 플랫폼 소개
### 1. Tensorflow Model Optimization Toolkit

### 2. Kubeflow
 ![kubeflow](./image/kubeflow.png)
## ⚙ 실험 내용
### [1. Lightweight Deep Learning](https://github.com/Juyoung4/tensorflow_api/tree/master/Lightweight%20Deep%20Learning)

### [2. Kubeflow Setting](https://github.com/Juyoung4/tensorflow_api/tree/master/Setting)

###  [3. Kubeflow Katib](https://github.com/Juyoung4/tensorflow_api/tree/master/Katib)

###  [4. Kubeflow Fairing]()

###  [5. Kubeflow Pipelines](https://github.com/Juyoung4/tensorflow_api/tree/master/Lightweight%20Deep%20Learning)

###  [6. Coral Board](https://github.com/Juyoung4/tensorflow_api/tree/master/Coral_board)
