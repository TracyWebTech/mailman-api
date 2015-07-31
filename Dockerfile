
FROM ubuntu:14.04

MAINTAINER devops@tracy.com.br

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update

RUN apt-get install -y mailman

RUN /usr/lib/mailman/bin/newlist public public@example.com 12345

RUN /usr/lib/mailman/bin/newlist private private@example.com 12345

RUN echo "m.Lock(); m.description = 'Public List'; m.Save()" | /usr/lib/mailman/bin/withlist public

RUN echo "m.Lock(); m.description = 'Private List'; m.archive_private = 1; m.Save()" | /usr/lib/mailman/bin/withlist private
