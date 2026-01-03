# 🔗 Pro URL Shortener
A lightweight tool to transform long, messy URLs into short, shareable links. This project focuses on backend logic and string mapping.

## ✨ Features
- **Instant Shortening:** Generates a unique short key for any long URL.
- **Redirection:** Seamlessly redirects users from short links to original destinations.
- **In-Memory Storage:** Efficiently manages URL mappings using Python data structures.

## 🔧 Core Logic
- Uses a unique hashing/random string generator for keys.
- Implements error handling for non-existent short links.

## 🚀 Installation
1. Clone the repo.
2. Run `uvicorn main:app --reload`.
3. Use the POST endpoint to shorten your first URL!
