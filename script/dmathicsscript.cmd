# Simple Powershell command file to run mathicsscript
# FIXME: add features of bash script
docker run -it --name dmathics-cli --rm --tty --interactive --network=host mathicsorg/mathics:latest --mode cli
