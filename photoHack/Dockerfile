FROM django

COPY ./ ./
COPY requirements.txt ./

RUN apt-get update

RUN apt-get install apt-file -yqq

RUN apt-file update

RUN apt-get install vim -yqq

RUN apt-get install sudo && adduser user && echo "user ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/user && chmod 0440 /etc/sudoers.d/user

CMD /bin/bash

RUN sudo apt-get install python-pip -yqq
RUN pip install --upgrade pip
RUN sudo apt-get install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0 -yqq
RUN sudo apt-get install python-pyaudio -yqq
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]