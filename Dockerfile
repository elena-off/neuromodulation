ARG BASE_IMAGE=sinzlab/pytorch:v3.8-torch1.7.0-cuda11.0-dj0.12.7

# Perform multistage build to pull private repo without leaving behind
# private information (e.g. SSH key, Git token)
FROM ${BASE_IMAGE} as base

WORKDIR /src
# clone projects from public/private github repos
#RUN git clone https://github.com/sinzlab/neuralpredictors &&\
RUN   git clone https://github.com/sinzlab/nnfabrik

FROM ${BASE_IMAGE}
COPY --from=base /src /src

RUN python3.8 -m pip install --upgrade pip
RUN python3.8 -m pip --no-cache-dir install hub
RUN pip install git+https://github.com/sacadena/ptrnets.git@6f459a130ff2fb1a73f29d933e6bea5b435341e7
RUN pip install git+https://github.com/dicarlolab/CORnet
RUN python3.8 -m pip install einops

#RUN cd /src/neuralpredictors && python3.8 -m pip install --no-use-pep517 -e .
#RUN cd /src/nnfabrik && python3.8 -m pip install --no-use-pep517 -e .

ADD . /project
RUN python3.8 -m pip install --no-use-pep517 -e /project/mei
RUN python3.8 -m pip install --no-use-pep517 -e /project/nnvision
RUN python3.8 -m pip install --no-use-pep517 -e /project/nnfabrik #added this rather than line 19
RUN python3.8 -m pip install --no-use-pep517 -e /project/neuralpredictors
RUN python3.8 -m pip install --no-use-pep517 -e /project/neuromodulation
WORKDIR /project

