# Django OWASP Top 10 Demo Application

This is a small Django web application based on the Django tutorial polls app.  
It has been modified to demonstrate 5 different security vulnerabilities from the **OWASP Top 10 (2021)** list, as well as their fixes.  

Each vulnerability is implemented in the code with a **commented-out fix** directly below the vulnerable code.  
Screenshots demonstrating the flaws **before and after the fix** are stored in the `screenshots/` folder.  

---

## Vulnerabilities Demonstrated

1. **SQL Injection (Injection / A03:2021)** 
   - https://github.com/taneljuu/django-owasp-project/blob/9ee64d41ebff253b04e92770c6af259c0b2077c2/polls/views.py#L56 
   - The search function uses raw SQL with string interpolation, allowing attackers to change the query logic.  
   - **Fix:** Use the Django ORM or parameterized SQL queries so user input is always treated as data, never as part of the SQL statement.

2. **CSRF vulnerability** 
   - https://github.com/taneljuu/django-owasp-project/blob/9ee64d41ebff253b04e92770c6af259c0b2077c2/polls/views.py#L31  
   - `@csrf_exempt` removes CSRF protection from the voting view and the form is missing `{% csrf_token %}`, enabling forged POST requests from attacker-controlled pages.  
   - **Fix:** Remove `@csrf_exempt`, add `{% csrf_token %}` to the form and/or use `@csrf_protect` (or rely on Django’s default CSRF middleware).

3. **Broken Access Control (A01:2021)** 
   - https://github.com/taneljuu/django-owasp-project/blob/9ee64d41ebff253b04e92770c6af259c0b2077c2/polls/views.py#L76   
   - The `/polls/reset_votes/` endpoint can be accessed by anyone, allowing unauthorized users to reset all votes.  
   - **Fix:** Add proper access control (e.g. require login and admin/staff role using `@login_required` and `@user_passes_test(lambda u: u.is_staff)`) or another secure authorization mechanism.

4. **Security Misconfiguration (A05:2021)**  
   - https://github.com/taneljuu/django-owasp-project/blob/9ee64d41ebff253b04e92770c6af259c0b2077c2/mysite/settings.py#L26  
   - `DEBUG = True` in `settings.py` and an empty `ALLOWED_HOSTS` reveal detailed internal information on errors and allow requests from any host in development. An attacker can use this information to facilitate other attacks.  
   - **Fix:** Set `DEBUG = False` in production and populate `ALLOWED_HOSTS` with the real domain names your app should respond to (e.g. `['example.com', 'www.example.com']`).

5. **Cross-Site Scripting (XSS) (Injection / A03:2021)**  
   - https://github.com/taneljuu/django-owasp-project/blob/fd15d473483740d986ba76ab118bddd16baa7d43/polls/views.py#L84  
   - The `add_comment` view stores `request.POST["text"]` directly without validation or sanitization. Malicious input such as `<script>alert('XSS')</script>` can be saved and later executed in other users' browsers.  
   - **Fix:** Sanitize user input (e.g. `bleach.clean()`), and/or ensure templates escape output (avoid `|safe`); prefer escaping in templates and sanitize when allowing a subset of HTML.


---

## Installation

The application is implemented with **Python** and **Django**.  

- If you have completed the previous parts of the course, all dependencies are already installed.  
- Otherwise, follow the installation guide here:  
  [https://cybersecuritybase.mooc.fi/installation-guide](https://cybersecuritybase.mooc.fi/installation-guide)

---

