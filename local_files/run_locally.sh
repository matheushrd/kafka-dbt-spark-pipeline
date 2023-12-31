#!/bin/bash

# check_java() {
#     if command -v java >/dev/null 2>&1; then
#         echo "Java is already installed."
#     else
#         echo "Java is not installed. Installing..."
#         sudo apt update
#         sudo apt install -y openjdk-11-jre
#         if [ $? -eq 0 ]; then
#             echo "Java installed successfully."
#         else
#             echo "Failed to install Java. Please check for errors."
#             exit 1
#         fi
#     fi
# }

# check_java

# CONFLUENT_HUB_URL="https://client.hub.confluent.io/confluent-hub-client-latest.tar.gz"
# INSTALL_DIR="/usr/"
# FINAL_DIR="/usr/confluent-hub"

# # Check if Confluent CLI is installed
# if command -v confluent >/dev/null 2>&1; then
#     echo "Confluent CLI is already installed."
#     confluent version
# else
#     echo "Confluent CLI is not installed. Installing..."

#     # Create a temporary directory
#     TMP_DIR="/tmp/confluent-hub"
#     mkdir -p "$TMP_DIR"
#     sudo chmod 1777 /tmp

#     # Download and unzip Confluent Hub CLI
#     TMP_TAR="$TMP_DIR/confluent-hub-client-latest.tar.gz"
#     curl -L "$CONFLUENT_HUB_URL" -o "$TMP_TAR"
#     tar -xz -C "$TMP_DIR" -f "$TMP_TAR"

#     echo "Moving to bin..."
#     # Create the destination directory if it doesn't exist
#     mkdir -p "$FINAL_DIR"

#     # Use rsync to merge contents of the temporary directory with the final directory
#     rsync -a "$TMP_DIR/" "$FINAL_DIR/"

#     # Cleanup
#     rm -rf "$TMP_DIR"
#     echo "Adding to path..."

#     # Create a custom script in /etc/profile.d/ to add to the PATH
#     CONFLUENT_HUB_SH="/etc/profile.d/confluent-hub.sh"
#     echo "export PATH=\$PATH:$FINAL_DIR/bin" | tee "$CONFLUENT_HUB_SH"

#     # Reload the environment to apply the changes
#     source "$CONFLUENT_HUB_SH"

#     # Check installation
#     if command -v confluent-hub >/dev/null 2>&1; then
#         echo "Confluent CLI installed successfully."
#         confluent-hub version
#     else
#         echo "Failed to install Confluent CLI. Please check for errors."
#     fi
# fi

# echo $PWD
# sudo apt install unzip
# mkdir confluent-plugins && cd confluent-plugins
# wget https://api.hub.confluent.io/api/plugins/confluentinc/kafka-connect-s3/versions/10.5.0/archive
# unzip archive
# # cd .. && mkdir -p plugins/kafka-connect-s3
# # mv confluent-plugins/confluentinc-kafka-connect-s3-10.5.0/lib/* plugins/kafka-connect-s3/

# # mkdir .aws && cd .aws
# # vi credentials


#docker build -t local_spark:3.3.0 . && 

docker compose down && docker compose up -d

sleep 10

# Debezium Connectors API URL
#!/bin/bash

# docker pull bitnami/spark:latest

# git clone https://github.com/bitnami/containers.git
# cd bitnami/APP/VERSION/OPERATING-SYSTEM
# docker build -t bitnami/APP:latest .



DEBEZIUM_API_URL="http://localhost:8083/connectors"
DEBEZIUM_CONNECTOR_JSON="debezium-config.json"

# Load the NEW_CONNECTOR value from the JSON file
NEW_CONNECTOR=$(grep -o '"name": *"[^"]*"' debezium-config.json | cut -d'"' -f4)

echo "New_connector: $NEW_CONNECTOR"
# Function to check if a connector is present

post_connector() {
  curl -X POST -H "Content-Type: application/json" --data @"$DEBEZIUM_CONNECTOR_JSON" "$DEBEZIUM_API_URL"
}


check_connector() {
  connector_list=$(curl -s -X GET "$DEBEZIUM_API_URL")

  # Extract the names of connectors using 
  echo "connector_list: $connector_list"
  # Check if the connector name exists in the list
  if [[ "$connector_list" =~ "$NEW_CONNECTOR" ]]; then
    echo "Connector $NEW_CONNECTOR already exists."
  else
    echo "Connector $NEW_CONNECTOR does not exist. Creating $NEW_CONNECTOR"
    post_connector
  fi
}

# Call the function to check the connector
check_connector

# docker compose exec -it --user root spark-master /bin/bash
# sleep 3
# cd ../../.. 
# chmod 777 -R data 
# exit
