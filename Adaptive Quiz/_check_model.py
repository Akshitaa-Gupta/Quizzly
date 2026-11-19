import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from gemini_service import get_model_name

print("RESOLVED_MODEL_REPR=" + repr(get_model_name()))
print("RESOLVED_MODEL=" + get_model_name())
