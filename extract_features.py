import re
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
import whois as pythonwhois
from datetime import datetime


def extract_features(url):
    # Initialize all features to zero
    length_url = 0
    length_hostname = 0
    nb_dots = 0
    nb_hyphens = 0
    nb_at = 0
    nb_qm = 0
    nb_and = 0
    nb_eq = 0
    nb_underscore = 0
    nb_tilde = 0
    nb_percent = 0
    nb_slash = 0
    nb_semicolon = 0
    nb_dollar = 0
    nb_www = 0
    nb_com = 0
    nb_dslash = 0
    http_in_path = 0
    https_token = 0
    domain_age = 0

    parsed_url = urlparse(url)
    length_hostname = len(parsed_url.hostname)

    # Extract domain from URL
    domain = re.findall(r"://([^/]+)/?", url)[0]

    # Extract path from URL
    path = re.findall(r"://[^/]+(/[^?#]*)", url)
    if len(path) > 0:
        path = path[0]
    else:
        path = "/"

    # Extract query string from URL
    query_string = re.findall(r"\?([^#]*)", url)
    if len(query_string) > 0:
        query_string = query_string[0]
    else:
        query_string = ""

    # Extract features
    length_url = len(url)
    nb_dots = domain.count(".")
    nb_hyphens = domain.count("-")
    nb_at = url.count("@")
    nb_qm = url.count("?")
    nb_and = url.count("&")
    nb_eq = url.count("=")
    nb_underscore = url.count("_")
    nb_tilde = url.count("~")
    nb_percent = url.count("%")
    nb_slash = url.count("/")
    nb_semicolon = url.count(";")
    nb_dollar = url.count("$")
    nb_www = 1 if re.match(r"^www\.", domain) else 0
    nb_com = 1 if domain.endswith(".com") else 0
    nb_dslash = url.count('//')
    http_in_path = 1 if "http" in path else 0
    https_token = 1 if "https" in query_string else 0

    # domain age
    try:
        # Extract the domain from the URL
        domain = url.split("//")[-1].split("/")[0]

        # Perform a WHOIS lookup
        domain_info = pythonwhois.whois(domain)

        # Extract the creation date from the WHOIS data
        creation_date = domain_info.creation_date

        # Calculate the domain age (in days)
        if isinstance(creation_date, list):
            creation_date = creation_date[0]  # Use the first creation date if it's a list
        today = datetime.now()
        domain_age = (today - creation_date).days

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    # Put all features in a list
    features = [
        length_url, length_hostname, nb_dots, nb_hyphens, nb_at, nb_qm, nb_and, nb_eq,
        nb_underscore, nb_tilde, nb_percent, nb_slash, nb_semicolon, nb_dollar, nb_www, nb_com, nb_dslash, http_in_path,
        https_token, domain_age
    ]

    return features