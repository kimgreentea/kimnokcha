import js
import sys
import io
from pyodide.ffi import create_proxy

def make_web_input(output_div, current_stdout):
    def web_input(prompt_msg=""):
        res = js.prompt(str(prompt_msg))
        if res is None:
            res = ""
        current_stdout.write(f"{prompt_msg}{res}\n")
        output_div.innerText = current_stdout.getvalue()
        return res
    return web_input

def create_runner(row):
    code_textarea = row.querySelector('.code-input')
    output_div = row.querySelector('.output')
    
    def run_python_code(event):
        code = code_textarea.value
        new_stdout = io.StringIO()
        
        global_env = {
            '__name__': '__main__',
            'input': make_web_input(output_div, new_stdout)
        }
        
        old_stdout = sys.stdout
        sys.stdout = new_stdout
        
        try:
            exec(code, global_env)
            result = new_stdout.getvalue()
        except Exception as e:
            result = str(e)
        finally:
            sys.stdout = old_stdout
            
        output_div.innerText = result

    return run_python_code

def setup_all():
    rows = js.document.querySelectorAll('.compiler-row')
    for i in range(rows.length):
        row = rows.item(i)
        btn = row.querySelector('.run-btn')
        runner = create_runner(row)
        btn.addEventListener("click", create_proxy(runner))
        row.querySelector('.output').innerText = "준비 완료!"

setup_all()
