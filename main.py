from mutual import get_mutual_connections
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QSpacerItem, QSizePolicy, QTextEdit
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import json
import time
from PyQt5.QtCore import QCoreApplication

def get_credentials(key):
    with open("credentials.json", 'r') as json_file:
        data = json.load(json_file)
        return find_key_value(data, key)

def find_key_value(data, key):
    if isinstance(data, dict):
        for k, v in data.items():
            if k == key:
                return v
            elif isinstance(v, (dict, list)):
                result = find_key_value(v, key)
                if result is not None:
                    return result
    elif isinstance(data, list):
        for item in data:
            result = find_key_value(item, key)
            if result is not None:
                return result

    return None


# Create a new instance of the Chrome driver


def show_mutual_connections():
    username = username_input.text()
    password = password_input.text()
    targets = target_input.toPlainText().split("\n")

    table_widget.setRowCount(0)  # Clear table

    driver = webdriver.Chrome()

    # Navigate to the LinkedIn login page
    driver.get("https://www.linkedin.com/login")
    wait = WebDriverWait(driver, 10)
    wait.until(EC.visibility_of_element_located((By.ID, "username")))

    # Enter the username and password into the input fields and press Enter
    username_element  = driver.find_element(By.ID, "username")
    password_element  = driver.find_element(By.ID, "password")
    
    username_element.send_keys(username)
    password_element.send_keys(password)
    password_element.send_keys(Keys.ENTER)

    wait.until(EC.url_changes("https://www.linkedin.com/login"))

    connections_data = {}

    for target_url in targets:
        connections = get_mutual_connections(wait, driver, target_url)


        connections_data[target_url] = connections

        row = table_widget.rowCount()
        table_widget.insertRow(row)

        # Add target URL
        item = QTableWidgetItem(target_url)
        item.setFlags(item.flags() & ~Qt.ItemIsEditable)
        table_widget.setItem(row, 0, item)

        row += 1
        for name, url in connections.items():
            table_widget.insertRow(row)
            table_widget.setItem(row, 1, QTableWidgetItem(name))
            table_widget.setItem(row, 2, QTableWidgetItem(url))
            row += 1
            QCoreApplication.processEvents()

    table_widget.resizeColumnsToContents()

    # with open('connections_data.json', 'w') as outfile:
    #     json.dump(connections_data, outfile, indent=4)
    
    driver.quit()

app = QApplication(sys.argv)
app.setWindowIcon(QIcon("linkedin_icon.png"))
app.setStyleSheet("""
    QWidget {
        background-color: #F1F2F5;
        color: black;
    }
    QLabel {
        font-size: 14px;
        color: black;
        font-weight: bold;
    }
    QLineEdit, QTableWidget {
        font-size: 14px;
        padding: 5px;
        background-color: white;
        border: 1px solid #CED0D4;
        border-radius: 3px;
        color: black;
    }
    QPushButton {
        font-size: 14px;
        font-weight: bold;
        padding: 8px 16px;
        background-color: #0077B5;
        color: white;
        border: none;
        border-radius: 3px;
    }
    QPushButton:hover {
        background-color: #006097;
    }
""")

window = QWidget()
window.setWindowTitle("LinkedIn Mutual Connections")
window.setFixedSize(800, 600)
layout = QVBoxLayout()

header = QLabel("LinkedIn Mutual Connections")
header.setFont(QFont("Arial", 24, QFont.Bold))
header.setAlignment(Qt.AlignCenter)
layout.addWidget(header)

form_layout = QVBoxLayout()

username_label = QLabel("Username:")
form_layout.addWidget(username_label)
username_input = QLineEdit()
form_layout.addWidget(username_input)

password_label = QLabel("Password:")
form_layout.addWidget(password_label)
password_input = QLineEdit()
password_input.setEchoMode(QLineEdit.Password)
form_layout.addWidget(password_input)

target_label = QLabel("Target Profile URLs (one per line):")
form_layout.addWidget(target_label)
target_input = QTextEdit()
form_layout.addWidget(target_input)

button_layout = QHBoxLayout()
# button_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
# button_layout.addItem(button_spacer)
submit_button = QPushButton("Get Mutual Connections")
submit_button.clicked.connect(show_mutual_connections)
button_layout.addWidget(submit_button)

form_layout.addLayout(button_layout)

layout.addLayout(form_layout)

table_widget = QTableWidget()
table_widget.setColumnCount(3)
table_widget.setHorizontalHeaderLabels(["Target URL", "Profile Name", "Profile Link"])
table_widget.horizontalHeader().setStretchLastSection(True)
table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
layout.addWidget(table_widget)

username_input.setText(get_credentials("email"))
password_input.setText(get_credentials("password"))


window.setLayout(layout)
window.show()
sys.exit(app.exec_())

