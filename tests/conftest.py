# Asegura que la raíz del repositorio esté en
# sys.path durante la recolección de pytest porque cuando los probé dio este error
#=============================== ERRORS ================================
#_______________ ERROR collecting tests/test_and_gate.py _______________
#ImportError while importing test module '/mnt/c/Users/mjuli/Documentos/GitHub/AC_comp_logicos/tests/test_and_gate.py'.
#Hint: make sure your test modules/packages have valid Python names.    
#Traceback:
#/usr/lib/python3.12/importlib/__init__.py:90: in import_module
#    return _bootstrap._gcd_import(name[level:], package, level)        
#tests/test_and_gate.py:1: in <module>
#    from gates import AND
#E   ModuleNotFoundError: No module named 'gates'
#En todos

#Se me quiere ir la luz pero ya dan todos verde osea que funciona todo 
# ..................   (Punticos verdes) [100%]18 passed in 0.40s
import sys
from pathlib import Path

repo_root = Path(__file__).resolve().parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))
