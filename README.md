# Project RapportSystem Backend Setup Guide

## Introduction

Welcome to the comprehensive guide for setting up the backend of our group project within the framework of Fagskolen i Viken's Programming with Professional Leadership course. This guide is tailored to facilitate the setup of a robust reporting system designed for a business context. The backend solution comprises a Flask API with security measures such as bcrypt and various essential components.

 * The documentation for the entire API is generated using Doxygen. For detailed setup instructions and steps, refer to the full guide at:
 * https://bjorgeh.github.io/rapportsystem-backend/doc_files/index.html

## Project Context

This guide is part of a group project at Fagskolen i Viken, focusing on Programming with Professional Leadership. The objective is to develop a reporting system for a business context, with the backend solution facilitated through this Flask API.

## Flask API Overview

Our backend solution centers around a Flask API, a micro web framework for Python, providing a lightweight yet powerful foundation for building web applications.

## SQL Server
We utilize MariaDB as our SQL server to store and manage data efficiently.

## Security Measures

Security is a paramount concern, and our implementation includes the use of bcrypt for securely managing passwords and ensuring data integrity.

## Getting Started

This section will guide you through the initial steps required to kickstart the setup process for our robust backend solution.

### Requirements

Before you begin, make sure you have:

1. **Basic Linux Command Knowledge:**
   - Familiarity with fundamental Linux commands is highly recommended to navigate and operate within the Debian/Ubuntu VM environment.

2. **Understanding of MariaDB and Database Management:**
   - A foundational understanding of MariaDB and database management concepts is essential for configuring and interacting with the database component of our backend solution.

Stay tuned for the upcoming sections, where we'll guide you through each step, ensuring a smooth and successful setup of the Debian/Ubuntu VM, MariaDB, Git repository, and Swagger UI for API interaction within our Flask-based backend solution.

## Google Account Setup

### Google Account

1. Navigate to [Gmail](https://gmail.com/) with your preferred browser.
2. Create a new Gmail/Google account with your information.
3. Log into the new account.

### Cloud Platform Account

1. **Google Cloud Platform Account:**
   - Sign up for a Google Cloud Platform account if you don't already have one: [GCP Signup](https://cloud.google.com/free).

2. **Project Creation:**
   - Create a new project in the Google Cloud Console.

## Create a VM Instance (Debian/Ubuntu)

1. **Navigate to Compute Engine:**
   - In the GCP Console, go to "Navigation Menu" > "Compute Engine" > "VM instances."

2. **Click "Create Instance":**
   - Click the "Create" button to set up a new VM instance.

3. **Configure Instance Details:**
   - Enter a name for your instance.
   - Choose a region and zone for your VM.
   - Select the machine type (specify vCPUs and memory).

4. **Choose Boot Disk:**
   - Click on "Change" under the Boot disk section.
   - Choose an operating system image (e.g., Debian or Ubuntu).
   - Set the size of the boot disk.

5. **Configure Firewall:**
   - Under the "Firewall" section, allow HTTP/HTTPS and ports for SQL traffic or customize as needed.

6. **Optional: Add Startup Script (Advanced):**
   - Add a startup script to execute commands or install software during boot.

7. **Create the Instance:**
   - Click "Create" to create the VM instance.

## Access the VM

1. **Connect via SSH:**
   - On the "VM instances" page, find your instance and click the "SSH" button next to it.

2. **Update and Upgrade:**
   - Once connected via SSH, run the following commands:
     ```bash
     sudo apt update
     sudo apt upgrade
     ```

3. **Use SSH from the Command Line (Optional):**
   - You can also use an SSH client like PuTTY or the `gcloud` command-line tool to connect.

## Install and Set Up MariaDB

1. **Install MariaDB:**
   ```bash
   sudo apt install mariadb-server
   ```

2. **Start and Enable MariaDB:**
   ```bash
   sudo systemctl start mariadb
   sudo systemctl enable mariadb
   ```

3. **Secure MariaDB Installation:**
   - Run the following command to secure your MariaDB installation. Follow the prompts to set a root password and answer security-related questions.
   ```bash
   sudo mysql_secure_installation
   ```

4. **Log into MariaDB as Root:**
   ```bash
   sudo mysql -u root -p
   ```

5. **Create a New Database and User:**
   - Replace `your_database`, `admin`, and `your_password` with your desired values.
   ```sql
   CREATE DATABASE your_database;
   CREATE USER 'admin'@’%' IDENTIFIED BY 'your_password';
   ```

6. **Grant Privileges to the User:**
   ```sql
   GRANT ALL PRIVILEGES ON your_database.* TO 'admin'@'%';
   GRANT ALL PRIVILEGES ON *.* TO 'admin'@'%' WITH GRANT OPTION;
   FLUSH PRIVILEGES;
   ```

7. **Exit MariaDB:**
   ```sql
   EXIT;
   ```

## Test MariaDB Connection

1. **Log in with the New User:**
   ```bash
   mysql -u admin -p
   ```

2. **Enter the Password When Prompted:**
   - You should now be logged in as the 'admin' user to MariaDB.

## Conclusion

You have successfully installed and set up MariaDB on your Debian/Ubuntu VM on Google Cloud Platform. The MariaDB server is now ready for use with the 'admin' user and the specified password.

Note: Always follow best practices for securing your database, such as using strong passwords.

## Execute SQL Commands to Set Up a Database and Tables

1. **Connect to MariaDB:**
   ```bash
   mysql -u admin -p
   ```

2. **Enter the Password When Prompted:**

3. **Execute SQL Commands:**
   ```sql
   CREATE DATABASE users;

   USE users;

   -- Set up the user_info table
   CREATE TABLE user_info(
       id INT AUTO_INCREMENT PRIMARY KEY,
       email VARCHAR(50) UNIQUE,
       accountType VARCHAR(255),
       databaseName VARCHAR(255),
       userPass VARCHAR(255),
       creator_name VARCHAR(255),
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
   );

   -- Create a new table for JWT tokens
   CREATE TABLE tokens (
       token_id VARCHAR(767) PRIMARY KEY,
       user_id INT,
       expiration DATETIME DEFAULT (CURRENT_TIMESTAMP + INTERVAL 30 MINUTE),
       revoked BOOLEAN DEFAULT FALSE,
       FOREIGN KEY (user_id) REFERENCES user_info(id)
   );

   -- Set up the user_activity table
   CREATE TABLE user_activity(
       id INT AUTO_INCREMENT PRIMARY KEY,
       user_id INT,
       ip_address VARCHAR(50),
       user_agent VARCHAR(255),
       operating_system VARCHAR(255),
       activity_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       FOREIGN KEY (user_id) REFERENCES user_info(id)
   );
   ```

Now, your MariaDB database named 'users' should have three tables: 'user_info', 'tokens', and 'user_activity'. These tables are designed according to the provided SQL code.

## Install

 GIT for the VM Server

1. **Install Git:**
   - If you haven't installed Git yet, you can do so using the following commands:
   ```bash
   sudo apt-get update
   sudo apt-get install git
   ```

2. **Clone the Repository:**
   ```bash
   mkdir rapportsystem-backend
   cd rapportsystem-backend
   git clone https://github.com/Bjorgeh/rapportsystem-backend.git
   ```

3. **Navigate to the SQLconnections Directory:**
   ```bash
   cd rapportsystem-backend/SQLconnections
   ```

4. **Create `secret.py` File:**
   ```bash
   touch secret.py
   ```

5. **Edit `secret.py` File:**
   - Use your preferred text editor to edit the `secret.py` file. For example:
   ```bash
   nano secret.py
   ```

   Add the following content to `secret.py`:
   ```python
   # Sets app config
   host_IP = 'YOUR SQL SERVER IP'
   host_user = 'YOUR ADMIN USER'
   host_password = 'YOUR ADMIN PASSWORD'
   host_database = None
   host_userdatabase = "users"
   host_users_table = "user_info"
   host_session_table = "tokens"

   # This is used in API.py to apply config
   def setConfig(app):
       app.config['SECRET_KEY'] = 'TESTKEY'
       app.config['JWT_SECRET_KEY'] = 'SUPER_SECRET_KEY'
       return 1
   ```

6. **Save and Exit:**
   - In Nano, press `Ctrl + X` to exit, press `Y` to confirm changes, and press `Enter`.

## Conclusion

You have now cloned the repository, created the `secret.py` file, and added the required content. This file will be utilized for database connections and configuration in your application. Adjust the file as needed for your specific setup.

## Install Python, Frameworks, and Requirements

In your Linux VM terminal, install the following:

```bash
sudo apt-get update
sudo apt-get install python3.12
sudo apt-get -y install python3-pip
```

Now that you have Python and PIP installed, proceed to install the required Python packages:

```bash
pip install mysql-connector-python Flask flask-restx flask-session bcrypt httpagentparser flask-cors flask-jwt-extended
```

If the VM won't let the install complete, try adding `--break-system-packages` at the end of the one-liner like this:

```bash
pip install mysql-connector-python Flask flask-restx flask-session bcrypt httpagentparser flask-cors flask-jwt-extended --break-system-packages
```

## Setup the Screen Plugin for Linux

If you want to run the `API.py` file using `screen` on your Linux distribution, follow these steps:

1. **Install `screen` (if not already installed):**
   - Use the package manager for your Linux distribution to install `screen`. For Ubuntu/Debian, you can use:
   ```bash
   sudo apt-get update
   sudo apt-get install screen
   ```

2. **Start a New `screen` Session:**
   ```bash
   screen
   ```

3. **Run `API.py` in the `screen` Session:**
   - Navigate to the directory where `API.py` is located (in your case, it should be in `rapportsystem-backend`). Then, run:
   ```bash
   sudo python3 API.py
   ```

4. **Detach from the `screen` Session:**
   - To detach from the `screen` session and leave the process running in the background, press `Ctrl + A`, followed by `Ctrl + D`.

5. **Reattach to the `screen` Session (if needed):**
   - If you need to reattach to the `screen` session later, use:
   ```bash
   screen -r
   ```

## Conclusion

Now, your `API.py` is running in the background within a `screen` session. This helps keep the application running even after you close the terminal or log out.

Make sure to monitor the application's logs or screen session for any output or errors. Adjust the process as needed based on your specific requirements and monitoring preferences.

## Interacting with Swagger UI for Your API

1. **Access Swagger UI:**
   - Ensure your API is running. If not, follow the steps in the previous guide.
   - Open a web browser and navigate to the Swagger UI endpoint. Typically, it's at `http://your_server_ip:port/api`.

2. **Explore Endpoints:**
   - Swagger UI presents a user-friendly interface showcasing available API endpoints.
   - Explore endpoints, parameters, request bodies, and expected responses.

3. **Test API Requests:**
   - Use Swagger UI to test API requests directly from the interface.
   - Input parameters, adjust request bodies, and execute requests to see live responses.

4. **Understand Responses:**
   - Review detailed information about each API operation, including response codes and data formats.

5. **Interactive Documentation:**
   - Swagger UI serves as interactive documentation, making it easy for users to understand and interact with your API.

## Conclusion

You've successfully set up your API and Swagger UI. Users can now explore, test, and understand your API's functionalities using the Swagger user interface.

Note: Ensure that your Swagger UI endpoint matches your API setup and update any placeholder values accordingly. If you encounter issues, check the API logs and Swagger UI documentation for troubleshooting.

## Using the API in browser:
   
   - Run API.py
   - http://127.0.0.1:5001/api/
   - Create user
    ![image](https://github.com/Bjorgeh/rapportsystem-backend/assets/122554284/7158ae72-527f-4981-ac10-bdaf2e0d83aa)

   - Login
   ![image](https://github.com/Bjorgeh/rapportsystem-backend/assets/122554284/13f1385e-fbd2-41f5-a038-73eedbf5d14a)

   - Add your bearer Token from the login response:
   ![image](https://github.com/Bjorgeh/rapportsystem-backend/assets/122554284/8f211927-f7ec-4217-9f10-8b59aef3a929)

   - Auth:
   ![image](https://github.com/Bjorgeh/rapportsystem-backend/assets/122554284/afff75f4-7a1f-4fa8-924d-e3018260bf6f)
   ![image](https://github.com/Bjorgeh/rapportsystem-backend/assets/122554284/b83ac38b-ffad-49cc-9791-37938edde0e4)

   - You now have access to the functionality of the usertype of your account.
   
