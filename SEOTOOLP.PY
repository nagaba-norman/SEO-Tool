import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('stopwords')
nltk.download('punkt')

def get_page_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching page content: {e}")
        return None

def extract_keywords(content, num_keywords=10):
    if not content:
        return []

    soup = BeautifulSoup(content, 'html.parser')

    # Extract text content from HTML
    text_content = soup.get_text(separator=' ')

    # Tokenize the text
    words = word_tokenize(text_content)

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    filtered_words = [word.lower() for word in words if word.isalnum() and word.lower() not in stop_words]

    # Count word frequencies
    word_counter = Counter(filtered_words)

    # Get the top N keywords
    top_keywords = word_counter.most_common(num_keywords)

    return top_keywords

def keyword_research_tool(url):
    content = get_page_content(url)

    if content:
        keywords = extract_keywords(content)
        result_text = f"Top Keywords for {url}:\n"
        for keyword, count in keywords:
            result_text += f"{keyword}: {count}\n"
        return result_text
    else:
        return "Keyword research failed."

def analyze_keywords():
    url = url_entry_keywords.get()

    try:
        result = keyword_research_tool(url)
        result_label_keywords.config(text=result)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Request Error: {e}")

def generate_deep_link(app_id, page_id):
    base_url = "myawesomeapp://"
    deep_link = f"{base_url}app/{app_id}/page/{page_id}"
    return deep_link

def create_deep_link():
    app_id = app_id_entry.get()
    page_id = page_id_entry.get()

    if not app_id or not page_id:
        messagebox.showerror("Error", "Please enter both App ID and Page ID.")
        return

    deep_link = generate_deep_link(app_id, page_id)
    result_label_deep_link.config(text=f"Deep Link: {deep_link}")

def analyze_performance(visitor_count, bounce_rate, conversion_rate, result_label):
    try:
        # Calculate engagement metrics
        engaged_visitors = visitor_count * (1 - bounce_rate)
        conversions = engaged_visitors * conversion_rate

        result_text = f"Performance Analytics:\n"
        result_text += f"Total Visitors: {visitor_count}\n"
        result_text += f"Engaged Visitors: {int(engaged_visitors)}\n"
        result_text += f"Conversions: {int(conversions)}"

        result_label.config(text=result_text)

    except Exception as e:
        result_label.config(text=f"Error: {e}")

# ...

def get_page_speed(api_key, url, result_label):
    try:
        base_url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
        params = {
            "url": url,
            "key": api_key,
        }

        response = requests.get(base_url, params=params)
        data = response.json()

        if "error" in data:
            result_label.config(text=f"Error: {data['error']['message']}")
        else:
            result_text = f"URL: {url}\nPageSpeed Insights:\n"
            result_text += f"  Score: {data['lighthouseResult']['categories']['performance']['score']}\n"
            result_text += "  Metrics:\n"
            for metric, value in data['lighthouseResult']['audits']['metrics']['details']['items'][0].items():
                result_text += f"    {metric}: {value}\n"

            result_label.config(text=result_text)

    except requests.exceptions.RequestException as e:
        result_label.config(text=f"Error: {e}")

# ... (other functions)

def analyze_pagespeed():
    url = url_entry_pagespeed.get()
    api_key = "AIzaSyC8o2Csh05cxEwqqqZm3_YEg2dHl6yT-D8"  # Replace with your actual Google API key

    if not api_key:
        messagebox.showerror("Error", "Please provide a valid API key.")
        return

    try:
        get_page_speed(api_key, url, result_label_pagespeed)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Request Error: {e}")

# ... (rest of your code)


def get_website_info(url, result_label):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses

        soup = BeautifulSoup(response.text, 'html.parser')
        # Extract meta tags
        meta_tags = soup.find_all('meta')
        meta_info = {tag.get('name', tag.get('property', tag.get('http-equiv'))): tag.get('content', '') for tag in meta_tags}

        # Display results on GUI
        title_result = f"Title: {soup.title.string}"
        url_result = f"URL: {url}"
        meta_tags_result = "Meta Tags:"
        
        for name, content in meta_info.items():
            meta_tags_result += f"\n  {name}: {content}"

        result_label.config(text=f"{title_result}\n{url_result}\n{meta_tags_result}")

    except requests.exceptions.RequestException as e:
        result_label.config(text=f"Error: {e}")

def analyze_website():
    url = url_entry_website.get()

    try:
        get_website_info(url, result_label_website)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Request Error: {e}")

# GUI setup
root = tk.Tk()
root.title("SEO Tools")

# Notebook for Tabs
notebook = ttk.Notebook(root)

# Tab 1: Keyword Research Tool
keyword_research_tab = ttk.Frame(notebook)
notebook.add(keyword_research_tab, text="Keyword Research Tool")

# URL Entry
url_label_keywords = ttk.Label(keyword_research_tab, text="Enter URL:")
url_label_keywords.grid(row=0, column=0, padx=10, pady=10, sticky="w")

url_entry_keywords = ttk.Entry(keyword_research_tab, width=30)
url_entry_keywords.grid(row=0, column=1, padx=10, pady=10)

# Analyze Button
analyze_button_keywords = ttk.Button(keyword_research_tab, text="Analyze Keywords", command=analyze_keywords)
analyze_button_keywords.grid(row=1, column=0, columnspan=2, pady=10)

# Results Display
result_label_keywords = ttk.Label(keyword_research_tab, text="")
result_label_keywords.grid(row=2, column=0, columnspan=2, pady=10)

# Tab 2: Deep Link Generator
deep_link_tab = ttk.Frame(notebook)
notebook.add(deep_link_tab, text="Deep Link Generator")

# App ID Entry
app_id_label = ttk.Label(deep_link_tab, text="Enter App ID:")
app_id_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

app_id_entry = ttk.Entry(deep_link_tab, width=30)
app_id_entry.grid(row=0, column=1, padx=10, pady=10)

# Page ID Entry
page_id_label = ttk.Label(deep_link_tab, text="Enter Page ID:")
page_id_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

page_id_entry = ttk.Entry(deep_link_tab, width=30)
page_id_entry.grid(row=1, column=1, padx=10, pady=10)

# Generate Deep Link Button
generate_button = ttk.Button(deep_link_tab, text="Generate Deep Link", command=create_deep_link)
generate_button.grid(row=2, column=0, columnspan=2, pady=10)

# Results Display
result_label_deep_link = ttk.Label(deep_link_tab, text="")
result_label_deep_link.grid(row=3, column=0, columnspan=2, pady=10)

# Tab 3: Performance Analytics Tool
performance_analytics_tab = ttk.Frame(notebook)
notebook.add(performance_analytics_tab, text="Performance Analytics Tool")

# Visitor Count Entry
visitor_label = ttk.Label(performance_analytics_tab, text="Enter Visitor Count:")
visitor_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

visitor_entry = ttk.Entry(performance_analytics_tab, width=15)
visitor_entry.grid(row=0, column=1, padx=10, pady=10)

# Bounce Rate Entry
bounce_label = ttk.Label(performance_analytics_tab, text="Enter Bounce Rate (as a decimal):")
bounce_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

bounce_entry = ttk.Entry(performance_analytics_tab, width=15)
bounce_entry.grid(row=1, column=1, padx=10, pady=10)

# Conversion Rate Entry
conversion_label = ttk.Label(performance_analytics_tab, text="Enter Conversion Rate (as a decimal):")
conversion_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

conversion_entry = ttk.Entry(performance_analytics_tab, width=15)
conversion_entry.grid(row=2, column=1, padx=10, pady=10)

# Analyze Button for Performance Analytics
analyze_button_performance = ttk.Button(performance_analytics_tab, text="Analyze Performance", command=lambda: analyze_performance(
    int(visitor_entry.get()),
    float(bounce_entry.get()),
    float(conversion_entry.get()),
    result_label_performance
))
analyze_button_performance.grid(row=3, column=0, columnspan=2, pady=10)

# Results Display for Performance Analytics
result_label_performance = ttk.Label(performance_analytics_tab, text="")
result_label_performance.grid(row=4, column=0, columnspan=2, pady=10)

# Tab 4: PageSpeed Tool
page_speed_tab = ttk.Frame(notebook)
notebook.add(page_speed_tab, text="PageSpeed Tool")

# URL Entry for PageSpeed Tool
url_label_pagespeed = ttk.Label(page_speed_tab, text="Enter URL:")
url_label_pagespeed.grid(row=0, column=0, padx=10, pady=10, sticky="w")

url_entry_pagespeed = ttk.Entry(page_speed_tab, width=30)
url_entry_pagespeed.grid(row=0, column=1, padx=10, pady=10)

# Analyze Button for PageSpeed Tool
analyze_button_pagespeed = ttk.Button(page_speed_tab, text="Run Analysis", command=analyze_pagespeed)
analyze_button_pagespeed.grid(row=1, column=0, columnspan=2, pady=10)

# Results Display for PageSpeed Tool
result_label_pagespeed = ttk.Label(page_speed_tab, text="")
result_label_pagespeed.grid(row=2, column=0, columnspan=2, pady=10)

# Tab 5: Website Info Tool
website_info_tab = ttk.Frame(notebook)
notebook.add(website_info_tab, text="Website Info Tool")

# URL Entry for Website Info Tool
url_label_website = ttk.Label(website_info_tab, text="Enter URL:")
url_label_website.grid(row=0, column=0, padx=10, pady=10, sticky="w")

url_entry_website = ttk.Entry(website_info_tab, width=30)
url_entry_website.grid(row=0, column=1, padx=10, pady=10)

# Analyze Button for Website Info Tool
analyze_button_website = ttk.Button(website_info_tab, text="Run Analysis", command=analyze_website)
analyze_button_website.grid(row=1, column=0, columnspan=2, pady=10)

# Results Display for Website Info Tool
result_label_website = ttk.Label(website_info_tab, text="")
result_label_website.grid(row=2, column=0, columnspan=2, pady=10)

# Pack the notebook
notebook.pack(expand=True, fill="both")

# Start the GUI
root.mainloop()
