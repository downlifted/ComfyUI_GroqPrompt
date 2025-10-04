from .nodes import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']

print("\n### ComfyUI GroqPrompt: Advanced GROQ Nodes for ComfyUI ###")
print("### Loaded nodes:")
for node_name in NODE_CLASS_MAPPINGS.keys():
    print(f"### - {node_name}")
print("###")

# Web directory for frontend files
WEB_DIRECTORY = "./web"
