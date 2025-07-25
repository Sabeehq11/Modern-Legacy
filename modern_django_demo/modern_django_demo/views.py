from django.http import HttpResponse

def home(request):
    html = """
    <html>
    <head>
        <title>Django Demo</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                background-color: #f5f5f5;
            }
            h1 { color: #092e20; }
            .info { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            .legacy { background: #fee; padding: 15px; border-radius: 5px; margin: 20px 0; }
            .modern { background: #efe; padding: 15px; border-radius: 5px; margin: 20px 0; }
            code { background: #f0f0f0; padding: 2px 5px; border-radius: 3px; }
        </style>
    </head>
    <body>
        <h1>🎉 Django is Running!</h1>
        <div class="info">
            <h2>Welcome to Modern Django</h2>
            <p>This is a <strong>Django 4.2</strong> application running on <strong>Python 3.10</strong>.</p>
            
            <div class="modern">
                <h3>✅ Modern Django Features:</h3>
                <ul>
                    <li>Simple <code>path()</code> URL routing</li>
                    <li>Python 3.10+ with type hints</li>
                    <li>Async view support</li>
                    <li>Modern security defaults</li>
                </ul>
            </div>
            
            <div class="legacy">
                <h3>📚 Legacy edX Codebase:</h3>
                <ul>
                    <li>Located in <code>legacy-edx/</code></li>
                    <li>Django 1.8.15 (from 2016)</li>
                    <li>~985,000 lines of code</li>
                    <li>49 Django apps in LMS alone</li>
                    <li>Great for studying technical debt!</li>
                </ul>
            </div>
            
            <h3>Next Steps:</h3>
            <ul>
                <li>Visit <a href="/admin/">Django Admin</a> (create superuser first)</li>
                <li>Explore the legacy edX codebase</li>
                <li>Compare old vs new Django patterns</li>
            </ul>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html) 