FROM mysql:latest

ENV MYSQL_DATABASE=ecommerce
ENV MYSQL_ALLOW_EMPTY_PASSWORD=yes

# Copy the SQL files
COPY ./sample_ecommerce_ddl.sql /docker-entrypoint-initdb.d/

# Change ownership and permissions for the SQL file
RUN chown mysql:mysql /docker-entrypoint-initdb.d/sample_ecommerce_ddl.sql
RUN chmod 644 /docker-entrypoint-initdb.d/sample_ecommerce_ddl.sql

# Change permissions for the directory
RUN chmod 755 /docker-entrypoint-initdb.d