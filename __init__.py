from .nodes.Bori_JsonSetGetCleaner import *

NODE_CLASS_MAPPINGS = {
    # Add mappings here
    "Bori Json Set Get Cleaner": Bori_JsonSetGetCleaner,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Bori Json Set Get Cleaner": "Bori Json Set Get Cleaner", 
}

print ("\033[38;5;123m")
print ("Bori Json Set Get Cleaner")
print ("\033[38;5;183m")
print ("Loaded")
print ("\033[0m")

WEB_DIRECTORY = "./web"
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]