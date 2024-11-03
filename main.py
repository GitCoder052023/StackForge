import os
import questionary
import subprocess
import time
from rich.console import Console
from rich.panel import Panel

console = Console()

def run_command(command, cwd=None):
    try:
        subprocess.run(command, cwd=cwd, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]Error executing command:[/bold red] {command}\n{e}")

def purge_scripts_section(text):
    start_index = text.find('"scripts": {')
    if start_index == -1:
        return text
    
    end_index = text.find('},', start_index) + 2
    updated_text = text[:start_index] + text[end_index:].strip()
    return updated_text

def create_express_app():
    # Get project configuration from user
    project_name = questionary.text("Enter the name of your project:").ask()
    
    # Ask for output directory
    use_custom_path = questionary.confirm("Do you want to specify a custom output directory?").ask()
    
    if use_custom_path:
        output_dir = questionary.text(
            "Enter the absolute path where you want to create the project:",
            default=os.getcwd()
        ).ask()
    else:
        output_dir = os.getcwd()
    
    # Ask for directory structure preference
    use_src_dir = questionary.confirm(
        "Do you want to use a 'src' directory for your code? (recommended for better organization)",
        default=True
    ).ask()

    # Create project directory
    project_dir = os.path.join(output_dir, project_name)
    os.makedirs(project_dir, exist_ok=True)

    # Initialize npm and install dependencies
    console.print(Panel("Initializing npm project...", expand=False))
    run_command("npm init -y", cwd=project_dir)
    
    console.print(Panel("Installing express...", expand=False))
    run_command("npm i express", cwd=project_dir)

    console.print(Panel("Installing dotenv...", expand=False))
    run_command("npm i dotenv", cwd=project_dir)

    console.print(Panel("Installing tailwindcss...", expand=False))
    run_command("npm install -D tailwindcss", cwd=project_dir)

    console.print(Panel("Initializing tailwindcss...", expand=False))
    run_command("npx tailwindcss init", cwd=project_dir)

    # Determine base directory for code
    if use_src_dir:
        base_dir = os.path.join(project_dir, 'src')
    else:
        base_dir = project_dir

    # Create directory structure
    os.makedirs(base_dir, exist_ok=True)
    static_dir = os.path.join(base_dir, 'static')
    os.makedirs(static_dir, exist_ok=True)
    os.makedirs(os.path.join(static_dir, 'Assets'), exist_ok=True)
    os.makedirs(os.path.join(static_dir, 'CSS'), exist_ok=True)
    os.makedirs(os.path.join(static_dir, 'JS'), exist_ok=True)
    os.makedirs(os.path.join(static_dir, 'JSON'), exist_ok=True)
    templates_dir = os.path.join(base_dir, 'templates')
    os.makedirs(templates_dir, exist_ok=True)

    # Update tailwind.config.js based on directory structure
    tailwind_config_content = f"""
export default {{
  content: [
    '{os.path.join('./' if not use_src_dir else './src/', 'templates/**/*.html')}',
  ],
  theme: {{
    extend: {{}},
  }},
  plugins: [],
}}
    """
    tailwind_config_path = os.path.join(project_dir, 'tailwind.config.js')
    with open(tailwind_config_path, 'w', encoding='utf-8') as config_file:
        config_file.write(tailwind_config_content)

    # Create index.html file with the provided HTML content
    index_html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>StackForge Setup</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <link rel="stylesheet" href="/static/CSS/output.css">
    <link rel="stylesheet" href="/static/CSS/index.css">
</head>
<body class="flex flex-col min-h-screen">
    <header class="px-4 lg:px-6 h-16 flex items-center fade-in">
        <a class="flex items-center justify-center text-2xl hover-btn" href="#">
            <i class="fas fa-bolt text-yellow-500 bounce"></i>
            <span class="sr-only">StackForge</span>
        </a>
        <nav class="ml-auto flex gap-6">
            <a class="text-sm font-medium hover:underline underline-offset-4 hover-btn" href="#">Features</a>
            <a class="text-sm font-medium hover:underline underline-offset-4 hover-btn" href="#">Documentation</a>
            <a class="text-sm font-medium hover:underline underline-offset-4 hover-btn" href="#">GitHub</a>
        </nav>
    </header>
    <main class="flex-1 fade-up">
        <section class="w-full py-16 md:py-32 lg:py-48 fade-up">
            <div class="container mx-auto px-4 md:px-6">
                <div class="flex flex-col items-center space-y-6 text-center">
                    <h1 class="text-4xl font-bold tracking-tighter sm:text-5xl md:text-6xl lg:text-7xl fade-up">
                        Welcome to StackForge Setup
                    </h1>
                    <p class="mx-auto max-w-[700px] text-gray-600 md:text-lg lg:text-xl fade-up">
                        The open-source, beginner-friendly npm package to kickstart your web development projects.
                    </p>
                    <div class="space-x-4">
                        <button class="inline-flex h-10 items-center justify-center rounded-md bg-gray-900 px-5 py-3 text-base font-medium text-white shadow transition hover-btn">
                            Get Started
                            <i class="fas fa-arrow-right ml-2"></i>
                        </button>
                        <a class="inline-flex h-10 items-center justify-center rounded-md border border-gray-300 bg-white px-5 py-3 text-base font-medium text-gray-700 shadow-sm hover-btn" href="#">
                            Learn more
                        </a>
                    </div>
                </div>
            </div>
        </section>
        <section class="w-full py-16 md:py-32 bg-gray-100 fade-up">
            <div class="container mx-auto px-4 md:px-6">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-10 lg:gap-16 items-start">
                    <div class="grid gap-10 lg:gap-16">
                        <div class="flex flex-col items-center space-y-6 text-center fade-up">
                            <i class="fas fa-code text-4xl text-blue-600 bounce"></i>
                            <h2 class="text-2xl font-bold">Open Source</h2>
                            <p class="text-gray-600">
                                Fully open-source and community-driven. Contribute, customize, and make it your own.
                            </p>
                        </div>
                        <div class="flex flex-col items-center space-y-6 text-center fade-up">
                            <i class="fas fa-bolt text-4xl text-yellow-500 bounce"></i>
                            <h2 class="text-2xl font-bold">Beginner Friendly</h2>
                            <p class="text-gray-600">
                                Designed with beginners in mind. Easy to understand and quick to set up.
                            </p>
                        </div>
                    </div>
                    <div class="grid gap-10 lg:gap-16">
                        <div class="flex flex-col items-center space-y-6 text-center fade-up">
                            <i class="fab fa-github text-4xl text-black bounce"></i>
                            <h2 class="text-2xl font-bold">Community Support</h2>
                            <p class="text-gray-600">
                                Join a vibrant community of developers. Get help, share ideas, and grow together.
                            </p>
                        </div>
                        <div class="flex flex-col items-center space-y-6 text-center fade-up">
                            <i class="fas fa-box-open text-4xl text-green-600 bounce"></i>
                            <h2 class="text-2xl font-bold">npm Package</h2>
                            <p class="text-gray-600">
                                Easily integrate into your projects with a simple npm install command.
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        <section class="w-full py-16 md:py-32 fade-up">
            <div class="container mx-auto px-4 md:px-6">
                <div class="flex flex-col items-center justify-center space-y-6 text-center">
                    <h2 class="text-4xl font-bold sm:text-5xl md:text-6xl fade-up">Start Your Project Today</h2>
                    <p class="max-w-[900px] text-gray-600 text-lg md:text-xl fade-up">
                        StackForge Setup provides everything you need to build modern web applications. Get started in seconds with a simple npm install and focus on what matters most - your code.
                    </p>
                    <div class="w-full max-w-sm space-y-4 fade-up">
                        <div class="relative">
                            <div class="absolute inset-0 flex items-center">
                                <span class="w-full border-t"></span>
                            </div>
                            <div class="relative flex justify-center text-xs uppercase bg-white px-2">
                                Install with npm
                            </div>
                        </div>
                        <div class="flex items-center justify-between rounded-md border px-5 py-3 text-sm font-medium code-box transition-colors">
                            <code>npm install stackforge-setup</code>
                            <button class="h-8 w-8 rounded-full bg-gray-900 text-white hover-btn">
                                <i class="fas fa-arrow-right"></i>
                            </button>
                        </div>
                    </div>
                    <button class="inline-flex h-10 items-center justify-center rounded-md bg-gray-900 px-5 py-3 text-base font-medium text-white shadow transition hover-btn">
                        Get StackForge Setup
                    </button>
                </div>
            </div>
        </section>
    </main>
    <footer class="flex flex-col gap-2 sm:flex-row py-6 w-full items-center px-4 md:px-6 border-t fade-up">
        <p class="text-xs text-gray-500">© 2024 StackForge. All rights reserved.</p>
        <nav class="sm:ml-auto flex gap-4 sm:gap-6">
            <a class="text-xs hover:underline underline-offset-4 hover-btn" href="#">Terms of Service</a>
            <a class="text-xs hover:underline underline-offset-4 hover-btn" href="#">Privacy</a>
        </nav>
    </footer>
    <script src="/static/JS/index.js"></script>
</body>
</html>"""
    with open(os.path.join(templates_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(index_html_content)

 # Create app.js with updated paths
    app_js_content = f"""
const express = require("express");
const path = require("path");
const dotenv = require("dotenv");
const app = express();

dotenv.config({{ path: path.resolve(__dirname, "{'..' if use_src_dir else '.'}", ".env") }});

// Set up the port
const port = process.env.PORT || 3000;

// Setup middlewares
app.use(express.json());
app.use("/static", express.static(path.join(__dirname, "static")));

// Setup Routes
app.get('/', (req, res) => {{
   res.sendFile("templates/index.html", {{ root: path.join(__dirname, "./") }});
}});

app.listen(port, () => {{
  console.log(`Server running at http://localhost:${{port}}`);
}});
    """
    with open(os.path.join(base_dir, 'app.js'), 'w', encoding='utf-8') as f:
        f.write(app_js_content)

    # Create main.css in CSS
    main_css_content = """
@tailwind base;
@tailwind components;
@tailwind utilities;
    """
    css_path = os.path.join(static_dir, 'CSS', 'main.css')
    with open(css_path, 'w', encoding='utf-8') as f:
        f.write(main_css_content)

    # Create index.css in CSS
    index_css_content = """
.hover-btn { transition: transform 0.3s ease, box-shadow 0.3s ease; }

.hover-btn:hover { transform: translateY(-4px); box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1); }


.fade-in { opacity: 0; animation: fadeIn 1s forwards; }

@keyframes fadeIn { to { opacity: 1; } }


.bounce { animation: bounce 1.5s infinite; }

@keyframes bounce { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-10px); } }


.fade-up { opacity: 0; transform: translateY(20px); animation: fadeUp 0.8s ease-out forwards; }

@keyframes fadeUp { to { opacity: 1; transform: translateY(0); } }


.code-box:hover { background-color: #f9fafb; border-color: #e5e7eb; }
"""
    index_css_path = os.path.join(static_dir, 'CSS', 'index.css')
    with open(index_css_path, 'w', encoding='utf-8') as f:
        f.write(index_css_content)

    # Create index.js in JS
    index_js_content = """
    // Wait for the DOM to be fully loaded
document.addEventListener("DOMContentLoaded", () => {
  // Select all elements with the 'fade-up' and 'fade-in' classes
  const fadeUpElements = document.querySelectorAll(".fade-up");
  const fadeInElements = document.querySelectorAll(".fade-in");

  // Intersection Observer for fade-up animations
  const observerOptions = {
    root: null,
    rootMargin: "0px",
    threshold: 0.1,
  };

  const handleFadeUp = (entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add("visible");
        observer.unobserve(entry.target);
      }
    });
  };

  const fadeUpObserver = new IntersectionObserver(handleFadeUp, observerOptions);

  fadeUpElements.forEach(element => {
    element.classList.remove("visible");
    fadeUpObserver.observe(element);
  });

  // Intersection Observer for fade-in animations
  const handleFadeIn = (entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add("visible");
        observer.unobserve(entry.target);
      }
    });
  };

  const fadeInObserver = new IntersectionObserver(handleFadeIn, observerOptions);

  fadeInElements.forEach(element => {
    element.classList.remove("visible");
    fadeInObserver.observe(element);
  });

  // Copy npm install command to clipboard
  const copyButton = document.querySelector(".code-box button");
  copyButton.addEventListener("click", () => {
    const codeText = document.querySelector(".code-box code").innerText;
    navigator.clipboard.writeText(codeText)
      .then(() => {
        alert("Command copied to clipboard!");
      })
      .catch(err => {
        console.error("Failed to copy command:", err);
      });
  });
});

    """
    index_js_path = os.path.join(static_dir, 'JS', 'index.js')
    with open(index_js_path, 'w', encoding='utf-8') as f:
        f.write(index_js_content)



    # Update package.json with correct paths
    package_json_path = os.path.join(project_dir, 'package.json')
    with open(package_json_path, 'r', encoding='utf-8') as file:
        package_json = file.read()

    updated_package_json = purge_scripts_section(package_json)
    app_path = f"./src/app.js" if use_src_dir else "./app.js"
    css_input_path = f"./src/static/CSS/main.css" if use_src_dir else "./static/CSS/main.css"
    css_output_path = f"./src/static/CSS/output.css" if use_src_dir else "./static/CSS/output.css"
    
    updated_package_json = updated_package_json.replace(
        '"main": "index.js",',
        f'"main": "{app_path}",\n  "scripts": {{\n    "build:css": "tailwindcss -i {css_input_path} -o {css_output_path} --watch",\n    "dev": "nodemon {app_path}",\n    "start": "node {app_path}"\n  }},'
    )

    with open(package_json_path, 'w', encoding='utf-8') as file:
        file.write(updated_package_json)

    # Create environment files
    with open(os.path.join(project_dir, '.env'), 'w', encoding='utf-8') as f:
        f.write("PORT=3000")

    with open(os.path.join(project_dir, '.env.example'), 'w', encoding='utf-8') as f:
        f.write("PORT=3000")

    # Create .gitignore
    gitignore_content = """
node_modules/
.env
"""
    with open(os.path.join(project_dir, '.gitignore'), 'w', encoding='utf-8') as f:
        f.write(gitignore_content)

    # Ask about MIT license
    add_license = questionary.confirm("Do you want to add an MIT license to your project?", default=True).ask()
    
    if add_license:
        license_content = f"""MIT License

Copyright (c) {time.strftime("%Y")} {project_name}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""

        with open(os.path.join(project_dir, 'LICENSE.md'), 'w', encoding='utf-8') as f:
            f.write(license_content)


    # Create README.md
    readme_content = f"""# {project_name}

A modern web application built with Express.js and TailwindCSS, scaffolded using [**StackForge**](https://github.com/yourusername/stackforge).

## Quick Start

1. **Install Dependencies**
   ```bash
   npm install
   ```

2. **Start Development**

   In one terminal, start the Express server:
   ```bash
   npm run dev
   ```

   In another terminal, start Tailwind CSS build process:
   ```bash
   npm run build:css
   ```

   Your app will be running at `http://localhost:3000`

## Project Structure

```
{project_name}/
├── src/                 # Source files
│   ├── static/         # Static assets
│   │   ├── Assets/    # Images, fonts, etc.
│   │   ├── CSS/      # CSS files (including Tailwind)
│   │   ├── JS/       # JavaScript files
│   │   └── JSON/     # JSON data files
│   ├── templates/     # HTML templates
│   └── app.js        # Main application file
├── .env               # Environment variables
└── package.json      # Project configuration
```

## Available Scripts

- `npm run dev` - Start development server with hot-reload
- `npm run build:css` - Build and watch Tailwind CSS
- `npm start` - Start production server

## Configuration

1. **Environment Variables**
   - Copy `.env.example` to `.env`
   - Modify variables as needed:
     ```env
     PORT=3000
     ```

2. **Tailwind CSS**
   - Configuration file: `tailwind.config.js`
   - Main CSS file: `src/static/CSS/main.css`

## Development

1. **Adding Routes**
   - Add new routes in `src/app.js`:
     ```javascript
     app.get('/new-route', (req, res) => {{
       res.send('New Route');
     }});
     ```

2. **Static Files**
   - Place in appropriate directory under `src/static/`
   - Access via `/static/` URL path

3. **Templates**
   - Add new HTML files in `src/templates/`

## Learn More

- [Express.js Documentation](https://expressjs.com/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Node.js Documentation](https://nodejs.org/docs)
"""
    with open(os.path.join(project_dir, 'README.md'), 'w', encoding='utf-8') as f:
        f.write(readme_content)

    # Run Tailwind build command
    console.print(Panel("Running Tailwind CSS build...", expand=False))
    time.sleep(1)
    run_command(f"npx tailwindcss -i {css_input_path} -o {css_output_path}", cwd=project_dir)

    console.print(f"[bold green]Project '{project_name}' setup completed![/bold green]")
    console.print(f"[bold blue]Project created at: {project_dir}[/bold blue]")
    
    # Ask if user wants to start the development server
    if questionary.confirm("Do you want to start the development server?", default=True).ask():
        console.print("[bold yellow]Starting the development server...[/bold yellow]")
        run_command("npm run dev", cwd=project_dir)

if __name__ == "__main__":
    create_express_app()