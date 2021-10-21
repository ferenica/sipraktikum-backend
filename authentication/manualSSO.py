import re
import base64
import requests


class SSOClass:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.resultText = ""

    def login(self):
        # First, ask the session
        sso_result = requests.get(url="https://sso.ui.ac.id/cas/login", headers={
            "Connection": "close",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.9",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document", }).text
        # List of regex

        session_regex = re.compile(base64.b64decode("anNlc3Npb25pZFw9W0EtWjAtOV0r".encode("utf-8")).decode("utf-8"))
        lt_regex = re.compile(base64.b64decode("dmFsdWVcPSJMVFtcLTAtOWEtekEtWl0r".encode("utf-8")).decode("utf-8"))
        # Parse the values
        start, end = re.search(session_regex, sso_result).span()
        session_value = sso_result[start + 11:end]
        start, end = re.search(lt_regex, sso_result).span()
        lt_value = sso_result[start + 7:end]
        # Create the POST data
        login_data = {
            "username": self.username,
            "password": self.password,
            "lt": lt_value,
            "execution": "e1s1",
            "_eventId": "submit"
        }
        # Second, include the session
        self.resultText = requests.post(url="https://sso.ui.ac.id/cas/login;jsessionid=" + session_value, headers={
            "Connection": "close",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
            "Origin": "https://sso.ui.ac.id",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.9",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
            "Referer": "https://sso.ui.ac.id/cas/login"}, data=login_data, cookies={"JSESSIONID": session_value}).text

    def checkLogin(self):
        return "Log In Successful" in self.resultText
