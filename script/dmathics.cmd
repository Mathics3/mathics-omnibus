# Simple Powershell command file to run mathics
# FIXME: add features of bash script
docker run --name dmathics-cli --rm --tty --interactive --network=host mathicsorg/mathics:latest --mode mathics
