FROM mariadb:latest
ENV TZ="America/Mexico_City"
RUN date
EXPOSE 3306